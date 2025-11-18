"""Run the full Nova Corrente batch cycle Prefect flow."""

from demand_forecasting.orchestration import batch_cycle_flow


if __name__ == "__main__":  # pragma: no cover - convenience script
    batch_cycle_flow()

