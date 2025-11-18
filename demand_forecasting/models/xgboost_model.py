from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import numpy as np
import pandas as pd
import xgboost as xgb


@dataclass
class XGBoostConfig:
    max_depth: int = 6
    learning_rate: float = 0.05
    n_estimators: int = 500
    subsample: float = 0.8
    colsample_bytree: float = 0.8
    objective: str = "reg:squarederror"


class XGBoostForecaster:
    def __init__(self, config: XGBoostConfig | None = None) -> None:
        self.config = config or XGBoostConfig()
        self.model = xgb.XGBRegressor(
            tree_method="gpu_hist",
            predictor="gpu_predictor",
            **self.config.__dict__,
        )

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

    def feature_importance(self) -> Dict[str, float]:
        booster = self.model.get_booster()
        scores = booster.get_score(importance_type="gain")
        return scores

