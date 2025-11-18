"""Execute the forecasting training pipeline on the latest warehouse snapshot."""

import argparse

from demand_forecasting.features import FeatureBuilder
from demand_forecasting.pipelines.training import ForecastingPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run forecasting pipeline")
    parser.add_argument("--horizon", type=int, default=30, help="Forecast horizon in days")
    parser.add_argument("--max-series", type=int, default=10, help="Maximum item/site series to model")
    parser.add_argument(
        "--enable-prophet",
        action="store_true",
        help="Enable Prophet component (requires CmdStan backend configured)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    builder = FeatureBuilder()
    pipeline = ForecastingPipeline(builder, horizon=args.horizon, enable_prophet=args.enable_prophet)
    pipeline.run(max_series=args.max_series)


if __name__ == "__main__":  # pragma: no cover - convenience script
    main()

