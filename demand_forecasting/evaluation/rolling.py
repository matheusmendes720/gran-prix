from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List

import numpy as np
import pandas as pd

from demand_forecasting.flows.utils import LOG_ROOT, ensure_directory


METRICS_DIR = ensure_directory(LOG_ROOT / "metrics")


def mape(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.mean(np.abs((actual - predicted) / (actual + 1e-8))) * 100)


def smape(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.mean(2.0 * np.abs(predicted - actual) / (np.abs(actual) + np.abs(predicted) + 1e-8)) * 100)


def rmse(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.sqrt(np.mean((predicted - actual) ** 2)))


def mae(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.mean(np.abs(predicted - actual)))


DEFAULT_METRICS: Dict[str, Callable[[np.ndarray, np.ndarray], float]] = {
    "MAPE": mape,
    "sMAPE": smape,
    "RMSE": rmse,
    "MAE": mae,
}


@dataclass
class RollingCrossValidator:
    horizon: int
    window: int
    metrics: Dict[str, Callable[[np.ndarray, np.ndarray], float]] = None
    output_dir: Path = METRICS_DIR

    def __post_init__(self) -> None:
        self.metrics = self.metrics or DEFAULT_METRICS
        ensure_directory(self.output_dir)

    def evaluate(self, series: pd.Series, forecasts: pd.Series, key: str) -> Path:
        if len(series) != len(forecasts):
            raise ValueError("Series and forecasts must have the same length for evaluation")

        records: List[Dict[str, float]] = []
        for start in range(0, len(series) - self.window - self.horizon + 1):
            train_end = start + self.window
            test_end = train_end + self.horizon
            actual = series.iloc[train_end:test_end].to_numpy()
            predicted = forecasts.iloc[train_end:test_end].to_numpy()

            entry = {"key": key, "start": series.index[train_end], "end": series.index[test_end - 1]}
            for name, metric in self.metrics.items():
                entry[name] = metric(actual, predicted)
            records.append(entry)

        df = pd.DataFrame.from_records(records)
        path = self.output_dir / f"rolling_metrics_{key}.parquet"
        df.to_parquet(path)
        return path

