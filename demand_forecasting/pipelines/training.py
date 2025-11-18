from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple, List

import numpy as np
import pandas as pd

from demand_forecasting.evaluation import RollingCrossValidator
from demand_forecasting.features import FeatureBuilder
from demand_forecasting.flows.utils import PROJECT_ROOT, ensure_directory
from demand_forecasting.models.arima_model import ARIMAForecaster
from demand_forecasting.models.prophet_model import ProphetForecaster
from demand_forecasting.models.tft_model import TFTForecaster, TFTConfig
from demand_forecasting.models.xgboost_model import XGBoostForecaster, XGBoostConfig
from demand_forecasting.pp_calculator import PPCalculator


FORECAST_OUTPUT_ROOT = PROJECT_ROOT / "data" / "outputs" / "nova_corrente" / "forecasts"
logger = logging.getLogger(__name__)


@dataclass
class ForecastArtifacts:
    forecasts: Dict[str, pd.DataFrame]
    metrics: Dict[str, object]
    prescriptive: Dict[str, Dict]


class ForecastingPipeline:
    def __init__(
        self,
        feature_builder: FeatureBuilder,
        horizon: int = 30,
        enable_prophet: bool = False,
    ) -> None:
        self.feature_builder = feature_builder
        self.horizon = horizon
        self.output_dir = ensure_directory(FORECAST_OUTPUT_ROOT)
        self.pp_calculator = PPCalculator(service_level=0.95)
        self.tft_config = TFTConfig()
        self.xgb_config = XGBoostConfig()
        self.cross_validator = RollingCrossValidator(horizon=horizon, window=90)
        self.enable_prophet = enable_prophet

    # ------------------------------------------------------------------
    def _format_series(self, group: pd.DataFrame) -> pd.Series:
        return group.set_index("date").sort_index()["qty_consumed"]

    def _prophet_forecast(self, group: pd.DataFrame) -> pd.DataFrame:
        model = ProphetForecaster()
        try:
            model.fit(group, target_col="qty_consumed")
            return model.forecast(periods=self.horizon)
        except ValueError as exc:
            logger.warning(
                "Prophet forecasting failed for item %s site %s: %s",
                group.get("item_id", ["unknown"]).iloc[-1] if "item_id" in group else "unknown",
                group.get("site_id", ["unknown"]).iloc[-1] if "site_id" in group else "unknown",
                exc,
            )
            last_date = pd.to_datetime(group["date"]).max()
            future = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=self.horizon, freq="D")
            baseline = float(group["qty_consumed"].tail(self.horizon).mean())
            fallback = pd.DataFrame(
                {
                    "ds": future,
                    "forecast": baseline,
                    "lower": baseline,
                    "upper": baseline,
                }
            )
            return fallback

    def _arima_forecast(self, series: pd.Series) -> pd.DataFrame:
        model = ARIMAForecaster(seasonal=True, m=7)
        model.fit(series)
        forecast_df = model.forecast(steps=self.horizon)
        start = series.index[-1] + pd.Timedelta(days=1)
        forecast_df.index = pd.date_range(start=start, periods=self.horizon, freq="D")
        forecast_df = forecast_df.rename_axis("ds").reset_index()
        return forecast_df

    def _xgboost_forecast(self, group: pd.DataFrame) -> pd.Series:
        features = group.drop(columns=["qty_consumed"])
        numeric_features = features.select_dtypes(include=[np.number]).copy()
        target = group["qty_consumed"]
        model = XGBoostForecaster(self.xgb_config)
        train_features = numeric_features.iloc[:-self.horizon]
        train_target = target.iloc[:-self.horizon]
        future_features = numeric_features.iloc[-self.horizon:]

        try:
            model.fit(train_features, train_target)
            preds = model.predict(future_features)
            return preds
        except Exception as exc:  # pragma: no cover - defensive against GPU failures
            logger.warning(
                "XGBoost forecasting failed for item %s site %s: %s",
                group.get("item_id", ["unknown"]).iloc[-1] if "item_id" in group else "unknown",
                group.get("site_id", ["unknown"]).iloc[-1] if "site_id" in group else "unknown",
                exc,
            )
            baseline = float(train_target.tail(self.horizon).mean())
            return np.full(self.horizon, baseline)

    def _prescriptive_summary(self, forecast_df: pd.DataFrame, group: pd.DataFrame) -> Dict:
        lead_time = group.get("lead_time_days", pd.Series([14])).iloc[-1]
        current_stock = group.get("current_stock", pd.Series([0.0])).iloc[-1]
        return self.pp_calculator.calculate_reorder_point(
            forecast=forecast_df, lead_time=int(lead_time), current_stock=float(current_stock)
        )

    def _series_key(self, item_id, site_id) -> str:
        raw = f"item{item_id}_site{site_id}"
        safe = re.sub(r"[^0-9A-Za-z_.-]+", "_", str(raw)).strip("_")
        if not safe:
            safe = f"series_{abs(hash(raw))}"
        return safe

    def _persist(self, key: Tuple[int, int], forecast_df: pd.DataFrame, prescriptive: Dict) -> None:
        item_id, site_id = key
        safe_key = self._series_key(item_id, site_id)
        path = self.output_dir / f"{safe_key}.parquet"
        forecast_df.to_parquet(path)
        meta_path = self.output_dir / f"{safe_key}_prescriptive.json"
        meta_path.write_text(json.dumps(prescriptive, indent=2), encoding="utf-8")

    # ------------------------------------------------------------------
    def run(self, max_series: int = 10) -> ForecastArtifacts:
        training_set = self.feature_builder.build_training_set()
        if hasattr(training_set.features, "to_pandas"):
            df = training_set.features.to_pandas()
        else:
            df = training_set.features.copy()

        if hasattr(training_set.target, "to_pandas"):
            target_series = training_set.target.to_pandas()
        else:
            target_series = training_set.target.copy()

        df["qty_consumed"] = target_series

        forecasts: Dict[str, pd.DataFrame] = {}
        metrics: Dict[str, Dict[str, float]] = {}
        prescriptive: Dict[str, Dict] = {}
        rolling_paths: List[str] = []

        grouped = df.groupby(["item_id", "site_id"])
        for idx, ((item_id, site_id), group) in enumerate(grouped):
            if idx >= max_series:
                break

            group = group.sort_values("date")
            key = self._series_key(item_id, site_id)

            series = self._format_series(group)
            prophet_df = None
            if self.enable_prophet:
                try:
                    prophet_df = self._prophet_forecast(group)
                except ValueError:
                    prophet_df = None

            arima_df = self._arima_forecast(series)
            xgb_preds = self._xgboost_forecast(group)

            combined = arima_df.rename(columns={"forecast": "arima_forecast"})
            result = combined[["ds", "arima_forecast"]].copy()
            result["forecast"] = result["arima_forecast"]
            result["lower"] = result["arima_forecast"]
            result["upper"] = result["arima_forecast"]

            if prophet_df is not None and not prophet_df.empty:
                prophet_clean = prophet_df.rename(
                    columns={
                        "forecast": "prophet_forecast",
                        "lower": "prophet_lower",
                        "upper": "prophet_upper",
                    }
                )
                result = result.merge(prophet_clean, on="ds", how="left")
                result["forecast"] = result["prophet_forecast"].fillna(result["forecast"])
                result["lower"] = result["prophet_lower"].fillna(result["lower"])
                result["upper"] = result["prophet_upper"].fillna(result["upper"])

            if len(xgb_preds) == len(result):
                result["xgboost_forecast"] = xgb_preds
            else:
                logger.warning(
                    "XGBoost prediction length mismatch for item %s site %s; filling with NaN",
                    item_id,
                    site_id,
                )
                result["xgboost_forecast"] = np.nan

            forecast_df = result.sort_values("ds")

            forecasts[key] = forecast_df

            # Evaluate using last horizon as validation
            tail = series.tail(self.horizon)
            merged = tail.to_frame("actual").join(forecast_df.set_index("ds")["forecast"], how="inner")
            if not merged.empty:
                mse = ((merged["actual"] - merged["forecast"]) ** 2).mean()
                mae = (merged["actual"] - merged["forecast"]).abs().mean()
                metrics[key] = {"mse": float(mse), "mae": float(mae)}
                rolling_path = self.cross_validator.evaluate(series, forecast_df.set_index("ds")["forecast"], key)
                metrics[key]["rolling_metrics_path"] = str(rolling_path)
                rolling_paths.append(str(rolling_path))

            prescriptive_info = self._prescriptive_summary(forecast_df, group)
            prescriptive[key] = prescriptive_info
            self._persist((item_id, site_id), forecast_df, prescriptive_info)

        metrics_path = self.output_dir / "metrics.json"
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        summary = self._summarize_metrics(metrics)
        summary["rolling_windows"] = rolling_paths
        summary_path = self.output_dir / "metrics_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        summary["metrics_path"] = str(metrics_path)
        summary["summary_path"] = str(summary_path)

        return ForecastArtifacts(forecasts=forecasts, metrics=summary, prescriptive=prescriptive)

    def _summarize_metrics(self, metrics: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        aggregated: Dict[str, List[float]] = {}
        for values in metrics.values():
            for metric_name, metric_value in values.items():
                if "path" in metric_name:
                    continue
                aggregated.setdefault(metric_name, []).append(metric_value)

        return {name: float(np.mean(vals)) for name, vals in aggregated.items() if vals}

