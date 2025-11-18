"""Prefect flows for Nova Corrente ingestion pipelines."""

from .climate import climate_ingestion_flow
from .economic import economic_ingestion_flow
from .regulatory import regulatory_ingestion_flow

__all__ = [
    "climate_ingestion_flow",
    "economic_ingestion_flow",
    "regulatory_ingestion_flow",
]

