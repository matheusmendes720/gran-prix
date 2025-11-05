# 🔄 Complete ETL Pipeline Architecture
## Nova Corrente - Bronze/Silver/Gold Data Layers

**Pipeline Version:** 2.0  
**Architecture:** Medallion (Bronze → Silver → Gold → Platinum)  
**Update Frequency:** Real-time to Daily

---

## 🏗️ Pipeline Overview

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888'
}}}%%

flowchart TB
    subgraph Sources["📥 DATA SOURCES"]
        S1[dadosSuprimentos.xlsx<br/>Manual Upload]
        S2[BACEN API<br/>Economic]
        S3[INMET API<br/>Climate]
        S4[ANATEL API<br/>Regulatory]
        S5[ANTT API<br/>Transport]
        S6[ANTAQ API<br/>Ports]
        S7[ANEEL API<br/>Energy]
        S8[25+ More APIs<br/>Brazilian Public]
    end
    
    subgraph Ingestion["🔌 INGESTION LAYER"]
        I1[File Upload Handler<br/>Excel/CSV parser]
        I2[API Collectors<br/>Rate limiting]
        I3[Data Validators<br/>Schema checks]
        I4[Error Handler<br/>Retry logic]
        I5[Event Queue<br/>Kafka/RabbitMQ]
    end
    
    subgraph Bronze["🥉 BRONZE LAYER (Raw)"]
        B1[(Raw File Storage<br/>Parquet/CSV)]
        B2[(API Response Cache<br/>JSON)]
        B3[(Error Log<br/>Failed records)]
        B4[Timestamp: Created]
        B5[No Transformations]
    end
    
    subgraph Silver["🥈 SILVER LAYER (Cleaned)"]
        SV1[Data Cleaning<br/>Null handling]
        SV2[Type Conversion<br/>Standardization]
        SV3[Deduplication<br/>Unique keys]
        SV4[Validation Rules<br/>Business logic]
        SV5[(Cleaned Tables<br/>Fact & Dim)]
        SV6[Quality Metrics<br/>Completeness]
    end
    
    subgraph Gold["🥇 GOLD LAYER (Analytics)"]
        G1[Aggregations<br/>Daily/Weekly/Monthly]
        G2[Business Metrics<br/>KPIs]
        G3[Enrichment Joins<br/>Star schema]
        G4[(Analytics Tables<br/>Denormalized)]
        G5[Performance Views<br/>Pre-computed]
    end
    
    subgraph Platinum["💎 PLATINUM LAYER (ML)"]
        P1[Feature Engineering<br/>90+ features]
        P2[Lag Features<br/>MA, STD]
        P3[Cyclical Encoding<br/>Sin/Cos]
        P4[ABC Classification<br/>Pareto]
        P5[(Feature Store<br/>ML-ready)]
        P6[Train/Val/Test Splits<br/>64/16/20]
    end
    
    subgraph Consumption["📊 CONSUMPTION"]
        C1[ML Models<br/>ARIMA/Prophet/LSTM]
        C2[Dashboards<br/>Next.js Frontend]
        C3[APIs<br/>REST endpoints]
        C4[Reports<br/>PDF/Excel]
        C5[Alerts<br/>Email/Slack]
    end
    
    S1 --> I1
    S2 --> I2
    S3 --> I2
    S4 --> I2
    S5 --> I2
    S6 --> I2
    S7 --> I2
    S8 --> I2
    
    I1 --> I3
    I2 --> I3
    I3 --> I4
    I4 --> I5
    
    I5 --> B1
    I5 --> B2
    I4 -.errors.-> B3
    B1 -.metadata.-> B4
    B2 -.metadata.-> B4
    B1 -.raw.-> B5
    
    B1 --> SV1
    B2 --> SV1
    SV1 --> SV2
    SV2 --> SV3
    SV3 --> SV4
    SV4 --> SV5
    SV5 -.metrics.-> SV6
    
    SV5 --> G1
    SV5 --> G2
    SV5 --> G3
    G1 --> G4
    G2 --> G4
    G3 --> G4
    G4 --> G5
    
    G4 --> P1
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    P5 --> P6
    
    P5 --> C1
    G4 --> C2
    G5 --> C3
    G4 --> C4
    SV6 -.quality issues.-> C5
    
    classDef sourceStyle fill:#4A90E2,stroke:#357ABD,stroke-width:2px,color:#fff
    classDef ingestionStyle fill:#9B59B6,stroke:#7D3C98,stroke-width:2px,color:#fff
    classDef bronzeStyle fill:#CD7F32,stroke:#A86424,stroke-width:2px,color:#fff
    classDef silverStyle fill:#C0C0C0,stroke:#999,stroke-width:2px,color:#000
    classDef goldStyle fill:#FFD700,stroke:#DAA520,stroke-width:3px,color:#000
    classDef platinumStyle fill:#E5E4E2,stroke:#BCC6CC,stroke-width:3px,color:#000
    classDef consumeStyle fill:#2ECC71,stroke:#27AE60,stroke-width:2px,color:#000
    
    class Sources,S1,S2,S3,S4,S5,S6,S7,S8 sourceStyle
    class Ingestion,I1,I2,I3,I4,I5 ingestionStyle
    class Bronze,B1,B2,B3,B4,B5 bronzeStyle
    class Silver,SV1,SV2,SV3,SV4,SV5,SV6 silverStyle
    class Gold,G1,G2,G3,G4,G5 goldStyle
    class Platinum,P1,P2,P3,P4,P5,P6 platinumStyle
    class Consumption,C1,C2,C3,C4,C5 consumeStyle
```

---

## 📋 Layer Specifications

### 🥉 Bronze Layer (Raw Data)

**Purpose:** Store raw, unprocessed data exactly as received

**Characteristics:**
- ✅ Immutable (append-only)
- ✅ Full audit trail
- ✅ Schema on read
- ✅ Compressed storage (Parquet)

**Tables:**

```
bronze/
├── raw_suprimentos/
│   ├── suprimentos_2024_10_09.parquet
│   ├── suprimentos_2024_10_10.parquet
│   └── ...
├── raw_bacen_api/
│   ├── economic_indicators_2024_10.json
│   └── ...
├── raw_inmet_api/
│   ├── climate_data_2024_10.json
│   └── ...
└── raw_anatel_api/
    ├── regulatory_data_2024_10.json
    └── ...
```

**Storage Strategy:**
- Format: Parquet (columnar, compressed)
- Partitioning: Year/Month/Day
- Retention: 2 years
- Compression: Snappy

---

### 🥈 Silver Layer (Cleaned Data)

**Purpose:** Cleaned, validated, deduplicated data ready for business use

**Transformations:**

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888'
}}}%%

flowchart LR
    subgraph Input["📥 Bronze Input"]
        I1[Raw Records<br/>Duplicates, Nulls]
    end
    
    subgraph Clean["🧹 Cleaning"]
        C1[Remove Duplicates<br/>Based on keys]
        C2[Handle Nulls<br/>Impute or Flag]
        C3[Type Conversion<br/>String → Numeric]
        C4[Standardize Format<br/>Dates, Codes]
    end
    
    subgraph Validate["✅ Validation"]
        V1[Schema Check<br/>Column types]
        V2[Range Check<br/>Min/Max values]
        V3[Business Rules<br/>Logical checks]
        V4[Referential Integrity<br/>FK validation]
    end
    
    subgraph Output["📤 Silver Output"]
        O1[Clean Records<br/>Quality flags]
    end
    
    I1 --> C1
    C1 --> C2
    C2 --> C3
    C3 --> C4
    
    C4 --> V1
    V1 --> V2
    V2 --> V3
    V3 --> V4
    
    V4 --> O1
    
    classDef inputStyle fill:#FB8072,stroke:#E06660,stroke-width:2px,color:#000
    classDef cleanStyle fill:#F39C12,stroke:#D68910,stroke-width:2px,color:#000
    classDef validateStyle fill:#3498DB,stroke:#2874A6,stroke-width:2px,color:#fff
    classDef outputStyle fill:#2ECC71,stroke:#27AE60,stroke-width:2px,color:#000
    
    class Input,I1 inputStyle
    class Clean,C1,C2,C3,C4 cleanStyle
    class Validate,V1,V2,V3,V4 validateStyle
    class Output,O1 outputStyle
```

**Quality Checks:**

| Check Type | Rule | Action on Failure |
|------------|------|-------------------|
| **Duplicate** | Unique (date_id, site_id, part_id) | Keep most recent |
| **Null** | quantidade NOT NULL | Reject record |
| **Range** | quantidade > 0 | Reject record |
| **Range** | lead_time_days >= 0 | Flag for review |
| **Range** | temperature BETWEEN -20 AND 50 | Flag outlier |
| **FK** | site_id EXISTS in Dim_Site | Reject record |
| **FK** | part_id EXISTS in Dim_Part | Reject record |
| **Date** | data_solicitado <= CURRENT_DATE | Reject record |

**Tables:**

```
silver/
├── Fact_Demand_Daily_cleaned
├── Dim_Calendar_cleaned
├── Dim_Part_cleaned
├── Dim_Site_cleaned
├── Dim_Supplier_cleaned
├── Fact_Climate_Daily_cleaned
├── Fact_Economic_Daily_cleaned
└── ...
```

---

### 🥇 Gold Layer (Analytics-Ready)

**Purpose:** Business-optimized, aggregated data for analytics and reporting

**Aggregations:**

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888'
}}}%%

graph TB
    subgraph Silver["🥈 Silver Input"]
        S1[Fact_Demand_Daily]
        S2[All Dimensions]
        S3[All External Facts]
    end
    
    subgraph Aggregations["📊 Aggregations"]
        A1[Daily Rollups<br/>By site, part, familia]
        A2[Weekly Rollups<br/>7-day windows]
        A3[Monthly Rollups<br/>Calendar month]
        A4[YTD Metrics<br/>Year to date]
    end
    
    subgraph Enrichment["🔗 Enrichment"]
        E1[Star Schema Joins<br/>All dimensions]
        E2[External Data Joins<br/>Climate, Economic, etc.]
        E3[Calculated Metrics<br/>KPIs, ratios]
        E4[Denormalization<br/>Flatten for speed]
    end
    
    subgraph GoldTables["🥇 Gold Tables"]
        G1[Demand_Analytics_Daily<br/>Denormalized]
        G2[Demand_Summary_Weekly<br/>Pre-aggregated]
        G3[Demand_Summary_Monthly<br/>Pre-aggregated]
        G4[Part_Performance_Metrics<br/>ABC analysis]
        G5[Site_Performance_Metrics<br/>Operational KPIs]
        G6[Supplier_Performance_Metrics<br/>Lead time, reliability]
    end
    
    S1 --> A1
    S1 --> A2
    S1 --> A3
    S1 --> A4
    
    A1 --> E1
    S2 --> E1
    S3 --> E2
    E1 --> E3
    E2 --> E3
    E3 --> E4
    
    E4 --> G1
    A2 --> G2
    A3 --> G3
    E3 --> G4
    E3 --> G5
    E3 --> G6
    
    classDef silverStyle fill:#C0C0C0,stroke:#999,stroke-width:2px,color:#000
    classDef aggStyle fill:#F39C12,stroke:#D68910,stroke-width:2px,color:#000
    classDef enrichStyle fill:#3498DB,stroke:#2874A6,stroke-width:2px,color:#fff
    classDef goldStyle fill:#FFD700,stroke:#DAA520,stroke-width:3px,color:#000
    
    class Silver,S1,S2,S3 silverStyle
    class Aggregations,A1,A2,A3,A4 aggStyle
    class Enrichment,E1,E2,E3,E4 enrichStyle
    class GoldTables,G1,G2,G3,G4,G5,G6 goldStyle
```

**Key Tables:**

**Demand_Analytics_Daily:**
```sql
CREATE TABLE Demand_Analytics_Daily AS
SELECT 
    f.date_id,
    c.full_date,
    c.year, c.month, c.weekday,
    f.site_id,
    s.site_name, s.region_id, r.region_name,
    f.part_id,
    p.material, p.familia, p.abc_class,
    f.quantidade,
    f.lead_time_days,
    
    -- External enrichment
    cl.temperature_avg_c,
    cl.precipitation_mm,
    ec.inflation_rate,
    ec.exchange_rate_brl_usd,
    reg.coverage_5g_pct,
    
    -- Calculated metrics
    f.quantidade * p.avg_unit_cost AS estimated_cost,
    CASE WHEN f.lead_time_days > s.avg_lead_time THEN 1 ELSE 0 END AS is_delayed,
    p.abc_class AS part_priority
    
FROM Fact_Demand_Daily f
INNER JOIN Dim_Calendar c ON f.date_id = c.date_id
INNER JOIN Dim_Part p ON f.part_id = p.part_id
INNER JOIN Dim_Site s ON f.site_id = s.site_id
INNER JOIN Dim_Region r ON s.region_id = r.region_id
LEFT JOIN Fact_Climate_Daily cl ON f.date_id = cl.date_id AND f.site_id = cl.site_id
LEFT JOIN Fact_Economic_Daily ec ON f.date_id = ec.date_id
LEFT JOIN Fact_Regulatory_Daily reg ON f.date_id = reg.date_id AND s.region_id = reg.region_id;
```

---

### 💎 Platinum Layer (ML Feature Store)

**Purpose:** ML-ready features with train/val/test splits

**Feature Engineering Pipeline:**

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888'
}}}%%

flowchart TD
    subgraph Input["🥇 Gold Input"]
        I1[Demand_Analytics_Daily<br/>Enriched data]
    end
    
    subgraph Temporal["⏰ Temporal Features"]
        T1[Cyclical Encoding<br/>month_sin/cos]
        T2[Day of Year<br/>day_sin/cos]
        T3[Holiday Flags<br/>is_holiday, is_weekend]
        T4[Fiscal Period<br/>fiscal_quarter]
    end
    
    subgraph Lag["📉 Lag Features"]
        L1[Moving Averages<br/>7d, 30d, 90d]
        L2[Standard Deviation<br/>7d, 30d]
        L3[Trend<br/>Linear regression]
        L4[Seasonality<br/>YoY comparison]
    end
    
    subgraph Categorical["🏷️ Categorical Encoding"]
        CA1[One-Hot<br/>familia, site_type]
        CA2[Target Encoding<br/>supplier_id]
        CA3[Frequency Encoding<br/>Part frequency]
        CA4[ABC Classification<br/>Ordinal]
    end
    
    subgraph Derived["🔬 Derived Features"]
        D1[Risk Scores<br/>SLA, lead time]
        D2[Ratios<br/>Demand/capacity]
        D3[Interactions<br/>Climate × Region]
        D4[Clusters<br/>K-means groups]
    end
    
    subgraph Output["💎 Feature Store"]
        O1[ML Dataset<br/>90+ features]
        O2[Train Split<br/>64%]
        O3[Validation Split<br/>16%]
        O4[Test Split<br/>20%]
    end
    
    I1 --> Temporal
    I1 --> Lag
    I1 --> Categorical
    I1 --> Derived
    
    Temporal --> O1
    Lag --> O1
    Categorical --> O1
    Derived --> O1
    
    O1 --> O2
    O1 --> O3
    O1 --> O4
    
    classDef inputStyle fill:#FFD700,stroke:#DAA520,stroke-width:2px,color:#000
    classDef temporalStyle fill:#3498DB,stroke:#2874A6,stroke-width:2px,color:#fff
    classDef lagStyle fill:#9B59B6,stroke:#7D3C98,stroke-width:2px,color:#fff
    classDef categoricalStyle fill:#E74C3C,stroke:#C0392B,stroke-width:2px,color:#fff
    classDef derivedStyle fill:#F39C12,stroke:#D68910,stroke-width:2px,color:#000
    classDef outputStyle fill:#E5E4E2,stroke:#BCC6CC,stroke-width:3px,color:#000
    
    class Input,I1 inputStyle
    class Temporal,T1,T2,T3,T4 temporalStyle
    class Lag,L1,L2,L3,L4 lagStyle
    class Categorical,CA1,CA2,CA3,CA4 categoricalStyle
    class Derived,D1,D2,D3,D4 derivedStyle
    class Output,O1,O2,O3,O4 outputStyle
```

**Feature Categories (90+ total):**

| Category | Count | Examples |
|----------|-------|----------|
| **Temporal** | 25 | year, month, day, weekday, is_weekend, is_holiday, month_sin/cos, day_sin/cos |
| **Climate** | 14 | temperature_avg/min/max, precipitation, humidity, wind_speed, corrosion_risk |
| **Economic** | 12 | inflation_rate, exchange_rate, gdp_growth, selic_rate, credit_operations |
| **Regulatory** | 10 | 5g_coverage_pct, spectrum_allocation, active_operators, b2b_contracts |
| **Transport** | 8 | road_freight_volume, transport_cost, highway_congestion, customs_delay |
| **Energy** | 6 | energy_consumption, power_outages, grid_reliability, fuel_price |
| **Employment** | 5 | employment_rate, hiring_count, labor_availability |
| **Lag/MA** | 20 | family_demand_ma_7/30, site_demand_ma_7/30, supplier_lead_time_mean/std |
| **Categorical** | 8 | familia_encoded, abc_class, site_type, criticality |
| **Derived** | 12 | sla_violation_risk, delivery_impact, corrosion_risk, abc_class |

---

## 🔄 Data Flow Schedule

### Batch Processing

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888'
}}}%%

gantt
    title Daily ETL Schedule (UTC-3 Brazil Time)
    dateFormat HH:mm
    axisFormat %H:%M
    
    section Bronze
    API Collection - Economic    :00:00, 30m
    API Collection - Climate      :00:30, 30m
    API Collection - Regulatory   :01:00, 30m
    API Collection - Transport    :01:30, 30m
    File Upload Processing        :02:00, 60m
    
    section Silver
    Data Cleaning                 :03:00, 60m
    Validation & Deduplication    :04:00, 45m
    Quality Checks                :04:45, 30m
    
    section Gold
    Daily Aggregations            :05:15, 45m
    Star Schema Enrichment        :06:00, 60m
    KPI Calculation               :07:00, 30m
    
    section Platinum
    Feature Engineering           :07:30, 90m
    ML Dataset Generation         :09:00, 45m
    Train/Val/Test Splits         :09:45, 30m
```

### Real-time Processing

**Stream Processing (Kafka/RabbitMQ):**

```
Event Stream → Bronze (immediate)
             → Silver (5 min delay)
             → Gold (15 min delay)
             → Platinum (hourly batch)
```

**Update Frequencies:**

| Layer | Update Frequency | Latency |
|-------|------------------|---------|
| **Bronze** | Real-time | <1 minute |
| **Silver** | Every 5 minutes | 5-10 minutes |
| **Gold** | Every 15 minutes | 15-30 minutes |
| **Platinum** | Hourly batch | 1 hour |
| **API Refresh** | Daily 00:00-02:00 | Next day |

---

## 🛠️ Implementation Code

### Bronze Layer - API Collector

```python
# backend/data/collectors/api_collector_base.py

import requests
from datetime import datetime
import json
from pathlib import Path

class APICollectorBase:
    def __init__(self, api_name, base_url, rate_limit_per_min=60):
        self.api_name = api_name
        self.base_url = base_url
        self.rate_limit = rate_limit_per_min
        self.bronze_path = Path(f"data/bronze/{api_name}")
        self.bronze_path.mkdir(parents=True, exist_ok=True)
    
    def collect(self, endpoint, params=None):
        """Collect data from API and save to bronze layer"""
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Save to bronze (raw)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.bronze_path / f"{endpoint}_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    'collected_at': datetime.now().isoformat(),
                    'endpoint': endpoint,
                    'params': params,
                    'data': data
                }, f, indent=2)
            
            return data
            
        except Exception as e:
            self._log_error(endpoint, str(e))
            return None
    
    def _log_error(self, endpoint, error):
        error_log = self.bronze_path / "errors.log"
        with open(error_log, 'a') as f:
            f.write(f"{datetime.now()},{endpoint},{error}\n")
```

### Silver Layer - Data Cleaner

```python
# backend/data/pipelines/silver_cleaner.py

import pandas as pd
import numpy as np

class SilverDataCleaner:
    def __init__(self, table_name):
        self.table_name = table_name
        self.quality_metrics = {}
    
    def clean_demand_data(self, bronze_df):
        """Clean Fact_Demand_Daily from bronze to silver"""
        df = bronze_df.copy()
        
        # 1. Remove duplicates
        initial_rows = len(df)
        df = df.drop_duplicates(subset=['date_id', 'site_id', 'part_id', 'solicitacao'])
        self.quality_metrics['duplicates_removed'] = initial_rows - len(df)
        
        # 2. Handle nulls
        df['quantidade'] = df['quantidade'].fillna(0)
        df['lead_time_days'] = df['lead_time_days'].fillna(df['lead_time_days'].median())
        
        # 3. Type conversion
        df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
        df['date_id'] = pd.to_datetime(df['date_id']).dt.strftime('%Y%m%d').astype(int)
        
        # 4. Range validation
        df = df[df['quantidade'] > 0]
        df = df[df['lead_time_days'] >= 0]
        
        # 5. Add quality flags
        df['data_quality_score'] = 100
        df.loc[df['data_requisitada'].isna(), 'data_quality_score'] -= 20
        df.loc[df['lead_time_days'] > 90, 'data_quality_score'] -= 10
        
        self.quality_metrics['final_rows'] = len(df)
        self.quality_metrics['completeness_pct'] = (df.notna().sum() / df.size * 100).mean()
        
        return df
```

### Gold Layer - Aggregator

```python
# backend/data/pipelines/gold_aggregator.py

import pandas as pd

class GoldAggregator:
    def create_daily_analytics(self, silver_dfs):
        """Create gold layer analytics from silver tables"""
        
        fact = silver_dfs['Fact_Demand_Daily']
        dim_calendar = silver_dfs['Dim_Calendar']
        dim_part = silver_dfs['Dim_Part']
        dim_site = silver_dfs['Dim_Site']
        
        # Star schema join
        analytics = (fact
            .merge(dim_calendar, on='date_id', how='inner')
            .merge(dim_part, on='part_id', how='inner')
            .merge(dim_site, on='site_id', how='inner')
        )
        
        # Add external facts
        if 'Fact_Climate_Daily' in silver_dfs:
            analytics = analytics.merge(
                silver_dfs['Fact_Climate_Daily'],
                on=['date_id', 'site_id'],
                how='left'
            )
        
        if 'Fact_Economic_Daily' in silver_dfs:
            analytics = analytics.merge(
                silver_dfs['Fact_Economic_Daily'],
                on='date_id',
                how='left'
            )
        
        # Calculate KPIs
        analytics['estimated_cost'] = analytics['quantidade'] * analytics['avg_unit_cost']
        analytics['is_high_value'] = analytics['abc_class'] == 'A'
        analytics['is_delayed'] = analytics['lead_time_days'] > analytics['lead_time_days'].median()
        
        return analytics
```

### Platinum Layer - Feature Engineer

```python
# backend/ml/feature_store.py

import pandas as pd
import numpy as np

class FeatureEngineer:
    def engineer_features(self, gold_df):
        """Generate 90+ ML features from gold layer"""
        df = gold_df.copy()
        
        # Temporal features
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        df['day_of_year_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
        df['day_of_year_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
        
        # Lag features
        df['family_demand_ma_7'] = df.groupby('familia')['quantidade'].transform(
            lambda x: x.rolling(7, min_periods=1).mean()
        )
        df['family_demand_ma_30'] = df.groupby('familia')['quantidade'].transform(
            lambda x: x.rolling(30, min_periods=1).mean()
        )
        df['family_demand_std_7'] = df.groupby('familia')['quantidade'].transform(
            lambda x: x.rolling(7, min_periods=1).std()
        )
        
        # Frequency encoding
        df['family_frequency'] = df.groupby('familia')['familia'].transform('count')
        df['site_frequency'] = df.groupby('site_id')['site_id'].transform('count')
        
        # Categorical encoding
        df['familia_encoded'] = df['familia'].astype('category').cat.codes
        df['abc_class_encoded'] = df['abc_class'].map({'A': 3, 'B': 2, 'C': 1})
        
        # Risk scores
        df['sla_violation_risk'] = (
            (df['is_delayed'].astype(int) * 0.4) +
            (df['is_high_value'].astype(int) * 0.3) +
            ((df['lead_time_days'] > 30).astype(int) * 0.3)
        )
        
        return df
    
    def create_train_test_split(self, df, test_size=0.2, val_size=0.16):
        """Create temporal train/val/test splits"""
        df = df.sort_values('full_date')
        
        n = len(df)
        train_end = int(n * (1 - test_size - val_size))
        val_end = int(n * (1 - test_size))
        
        train = df.iloc[:train_end]
        val = df.iloc[train_end:val_end]
        test = df.iloc[val_end:]
        
        return train, val, test
```

---

## ✅ Pipeline Benefits

### Performance
- ✅ Incremental processing (only new data)
- ✅ Partitioned storage (faster queries)
- ✅ Pre-computed aggregations
- ✅ Columnar format (Parquet)

### Quality
- ✅ Automated validation at each layer
- ✅ Quality metrics tracked
- ✅ Error handling & retry logic
- ✅ Full lineage tracking

### Scalability
- ✅ Horizontal scaling (parallel processing)
- ✅ Event-driven architecture
- ✅ Caching layer
- ✅ Rate limiting

### Maintainability
- ✅ Clear layer separation
- ✅ Modular code design
- ✅ Automated testing
- ✅ Monitoring & alerts

---

**Pipeline Status:** 🔧 **DESIGN COMPLETE**  
**Next Step:** Implement bronze layer collectors  
**Estimated Processing Time:** 2-3 hours daily (batch)
