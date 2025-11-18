## Nova Corrente Exploratory Diagnostics

### 1. Data Coverage


- **Fact records**: 4,188 rows across 20 families,
  872 items, and 468 suppliers.
- **Temporal range**: 2024-10-09 → 2025-10-24 (380 days).
- **Daily quantity (sum)** — mean: 952.48, std: 3026.31,
  min: 1.00, 90th percentile: 1633.90.
- **Average lead time (days)** — mean: 11.29,
  median: 7.56, 90th percentile: 23.16.
- **Top families by total quantity**: FERRO E AÇO, MATERIAL ELETRICO, MATERIAL CIVIL, FERRAMENTAS E EQUIPAMENTOS, SUPRIMENTOS ADMINISTRATIVO.


### 2. Data Quality Observations


Top missingness (excluding identifiers):

| column             |   missing_pct |
|:-------------------|--------------:|
| 5g_coverage_pct    |      1        |
| sla_violation_risk |      0.963467 |
| precipitation_mm   |      0.963467 |
| is_intense_rain    |      0.963467 |
| humidity_percent   |      0.963467 |
| temperature_avg_c  |      0.963467 |
| sla_penalty_brl    |      0.963467 |
| is_flood_risk      |      0.963467 |
| is_high_humidity   |      0.963467 |
| is_holiday         |      0.963467 |


### 3. Daily Relationships (Nova Corrente × Demand Factors)


- Daily demand joined with macro factors (GDP, inflation, FX), weather, and risk flags.
- Effective coverage (non-null ratios):

|                       |   coverage |
|:----------------------|-----------:|
| gdp_growth_rate       |        0.1 |
| inflation_rate        |        0.1 |
| exchange_rate_brl_usd |        0.1 |

Daily correlation matrix (excerpt):

|                       |   total_quantity |   avg_lead_time |   families_active |   gdp_growth_rate |   inflation_rate |   exchange_rate_brl_usd |   temperature_avg_c |   precipitation_mm |   demand_multiplier |
|:----------------------|-----------------:|----------------:|------------------:|------------------:|-----------------:|------------------------:|--------------------:|-------------------:|--------------------:|
| total_quantity        |            1     |           0.065 |             0.141 |             0.386 |           -0.421 |                   0.115 |              -0.035 |              0.063 |               0.201 |
| avg_lead_time         |            0.065 |           1     |             0.269 |             0.222 |           -0.614 |                   0.407 |               0.262 |              0.295 |               0.212 |
| families_active       |            0.141 |           0.269 |             1     |            -0.171 |            0.085 |                   0.256 |               0.309 |              0.255 |               0.057 |
| gdp_growth_rate       |            0.386 |           0.222 |            -0.171 |             1     |           -0.708 |                   0.187 |              -0.137 |              0.078 |               0.32  |
| inflation_rate        |           -0.421 |          -0.614 |             0.085 |            -0.708 |            1     |                  -0.194 |               0.12  |             -0.053 |              -0.233 |
| exchange_rate_brl_usd |            0.115 |           0.407 |             0.256 |             0.187 |           -0.194 |                   1     |               0.94  |              0.965 |               0.823 |
| temperature_avg_c     |           -0.035 |           0.262 |             0.309 |            -0.137 |            0.12  |                   0.94  |               1     |              0.951 |               0.727 |
| precipitation_mm      |            0.063 |           0.295 |             0.255 |             0.078 |           -0.053 |                   0.965 |               0.951 |              1     |               0.858 |
| demand_multiplier     |            0.201 |           0.212 |             0.057 |             0.32  |           -0.233 |                   0.823 |               0.727 |              0.858 |               1     |


### 4. Monthly Relationships (Nova Corrente × Operators × IoT × Municipal Accesses)


Monthly feature coverage:

|                            |   coverage |
|:---------------------------|-----------:|
| total_subscribers          |       0.23 |
| total_iot_connections      |       0.23 |
| total_accesses             |       0    |
| household_penetration_mean |       0.23 |

Monthly correlation matrix (excerpt):

|                            |   total_quantity |   mean_daily_quantity |   avg_lead_time |   total_subscribers |   max_market_share |   market_concentration |   total_iot_connections |   total_accesses |   household_penetration_mean |
|:---------------------------|-----------------:|----------------------:|----------------:|--------------------:|-------------------:|-----------------------:|------------------------:|-----------------:|-----------------------------:|
| total_quantity             |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |
| mean_daily_quantity        |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |
| avg_lead_time              |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |
| total_subscribers          |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |
| max_market_share           |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |
| market_concentration       |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |
| total_iot_connections      |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |
| total_accesses             |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |
| household_penetration_mean |              nan |                   nan |             nan |                 nan |                nan |                    nan |                     nan |              nan |                          nan |


### 5. Key Insights & Next Actions

1. Extend external signals: macro factors present full coverage, but weather and regulatory flags remain sparse — prioritise ingestion backfill.
2. Operator metrics show concentration (HHI) trends; consider joining with supplier families to detect operator-driven demand signals.
3. Municipal accesses provide high-growth signals for 2023; parse full Anatel archives to unlock >24 months and reduce under-fitting.
4. Fiber penetration currently uses synthetic growth values; replace with true Anatel data to avoid misleading correlations.
5. Prepare feature store: persist merged daily/monthly tables for downstream prescriptive experiments (Croston/SBA, probabilistic models).
