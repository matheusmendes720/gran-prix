"""Feature taxonomy aligning with strategic documents."""

FEATURE_GROUPS = {
    "Temporal": [
        "day_of_week",
        "week_of_year",
        "month",
        "year",
        "lag_1",
        "lag_7",
        "lag_28",
        "rolling_mean_7",
        "rolling_std_7",
    ],
    "Climate": [
        "temp_min_c",
        "temp_max_c",
        "precipitation_mm",
        "wind_speed_kmh",
        "humidity_pct",
    ],
    "Economic": [
        "ptax_value",
        "selic_value",
    ],
    "5G": [
        "coverage_sites",
        "deployment_phase",
    ],
    "Lead Time": [
        "lead_time_days",
        "lead_time_volatility",
    ],
    "SLA": [
        "sla_tier",
        "response_hours",
        "open_incidents_7d",
    ],
    "Hierarchical": [
        "item_category",
        "region",
        "supplier_id",
    ],
    "Categorical": [
        "item_id",
        "site_id",
    ],
    "Business": [
        "project_phase",
        "budget_segment",
    ],
}

