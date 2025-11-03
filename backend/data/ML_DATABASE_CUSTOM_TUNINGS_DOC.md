# 🎯 NOVA CORRENTE ML DATABASE - CUSTOM TUNINGS DOCUMENTATION

## Complete Guide to All Custom Tunings for ML Processing

**Version:** 1.0  
**Date:** November 2025  
**Database:** `Nova_Corrente_ML_Ready_DB.sql`

---

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Brazilian-Specific Customizations](#brazilian-customizations)
3. [Nova Corrente B2B Customizations](#nova-corrente-customizations)
4. [ML Feature Categories (73 Features)](#ml-features)
5. [Stored Procedures](#stored-procedures)
6. [Views for ML Processing](#views)
7. [Usage Examples](#usage-examples)

---

## 🎯 OVERVIEW

This database schema includes **ALL custom tunings** required for Nova Corrente's ML-based demand forecasting system, specifically designed for:

- **Brazilian B2B Telecom Market** (18,000+ towers)
- **Top 5 Material Families** (MATERIAL ELETRICO, FERRO E AÇO, EPI, MATERIAL CIVIL, FERRAMENTAS E EQUIPAMENTOS)
- **Salvador/BA Operations** (Climate, regional factors)
- **Brazilian Holidays & Calendar**
- **Economic Indicators** (BACEN)
- **5G Expansion Tracking** (ANATEL)

---

## 🇧🇷 BRAZILIAN-SPECIFIC CUSTOMIZATIONS

### 1. CalendarioBrasil Table

**Purpose:** Brazilian holidays and calendar features

**Custom Features:**
- `is_feriado`: Brazilian national/regional/municipal holidays
- `is_carnaval`: Carnival period (February/March)
- `is_natal`: Christmas/New Year period (December/January)
- `is_verao`: Summer season (Dec-Feb) impact
- `is_chuva_sazonal`: Rainy season (May-Aug) for Salvador
- `impact_demanda`: Demand multiplier based on period

**Usage:**
```sql
-- Get all Brazilian holidays for a month
SELECT * FROM CalendarioBrasil 
WHERE data_referencia BETWEEN '2025-01-01' AND '2025-01-31' 
AND is_feriado = TRUE;

-- Calculate demand impact for carnival period
SELECT AVG(impact_demanda) 
FROM CalendarioBrasil 
WHERE is_carnaval = TRUE;
```

**Data Source:** Brazilian national calendar, regional holidays

---

### 2. ClimaSalvador Table

**Purpose:** INMET climate data for Salvador/BA

**Custom Features:**
- `temperatura_media`: Average temperature (°C)
- `precipitacao_mm`: Precipitation (mm)
- `umidade_percentual`: Humidity (%)
- `is_extreme_heat`: Temperature > 35°C
- `is_heavy_rain`: Precipitation > 50mm
- `corrosion_risk`: Corrosion risk calculation (0-1)
- `field_work_disruption`: Field work disruption risk (0-1)

**Calculated Features:**
```sql
-- Corrosion risk: High humidity + rain + temperature
corrosion_risk = (umidade_percentual / 100) * (precipitacao_mm / 100) * (temperatura_media / 40)

-- Field work disruption: Heavy rain or extreme conditions
field_work_disruption = CASE 
    WHEN is_heavy_rain THEN 0.8
    WHEN is_extreme_heat THEN 0.6
    WHEN velocidade_vento_kmh > 60 THEN 0.7
    ELSE 0.1
END
```

**Data Source:** INMET (Instituto Nacional de Meteorologia) - Salvador/BA station

---

### 3. IndicadoresEconomicos Table

**Purpose:** BACEN economic indicators

**Custom Features:**
- `taxa_inflacao`: Monthly inflation (IPCA)
- `taxa_cambio_brl_usd`: BRL/USD exchange rate
- `pib_crescimento`: GDP growth (%)
- `taxa_selic`: SELIC interest rate
- `is_high_inflation`: Inflation > 6% annual
- `is_currency_devaluation`: Currency devaluation > 5%

**Usage:**
```sql
-- Get economic features for a date range
SELECT data_referencia, taxa_inflacao, taxa_cambio_brl_usd, is_high_inflation
FROM IndicadoresEconomicos
WHERE data_referencia BETWEEN '2024-01-01' AND '2025-01-01';
```

**Data Source:** BACEN (Banco Central do Brasil)

---

### 4. Expansao5G Table

**Purpose:** 5G expansion indicators (ANATEL)

**Custom Features:**
- `cobertura_5g_percentual`: 5G coverage % in Brazil
- `investimento_5g_brl_billions`: 5G investment in billions BRL
- `torres_5g_ativas`: Active 5G towers count
- `municipios_5g`: Municipalities with 5G
- `is_5g_milestone`: Important 5G expansion milestones
- `taxa_expansao_5g`: 5G expansion rate (%)

**Impact on Demand:**
```sql
-- 5G expansion impacts material demand
-- Higher 5G coverage = More tower maintenance = More material demand
SELECT 
    data_referencia,
    cobertura_5g_percentual,
    CASE 
        WHEN cobertura_5g_percentual > 40 THEN 'HIGH_DEMAND'
        WHEN cobertura_5g_percentual > 20 THEN 'MEDIUM_DEMAND'
        ELSE 'LOW_DEMAND'
    END as demand_category
FROM Expansao5G;
```

**Data Source:** ANATEL (Agência Nacional de Telecomunicações)

---

## 🏢 NOVA CORRENTE B2B CUSTOMIZATIONS

### 5. Tier Levels (Criticidade)

**Purpose:** Material criticality classification (Tier 1/2/3)

**Custom Fields:**
- `Material.tier_nivel`: Material tier (TIER_1, TIER_2, TIER_3)
- `Familia.categoria_criticidade`: Family tier classification
- `Material.sla_penalty_brl`: SLA penalty in BRL per downtime hour
- `Material.disponibilidade_target`: Availability target (%)

**Tier Definitions:**
```
TIER_1 (Critical): 20% of materials
- 99.5% SLA target
- High SLA penalty (>R$ 10,000/hour)
- 18,000+ towers impact
- Emergency reorder triggers

TIER_2 (Important): 50% of materials
- 99% SLA target
- Medium SLA penalty (R$ 5,000-10,000/hour)
- Regional impact

TIER_3 (Standard): 30% of materials
- 98% SLA target
- Low SLA penalty (<R$ 5,000/hour)
- Local impact
```

**Usage:**
```sql
-- Get all Tier 1 critical materials
SELECT material_id, nome_material, sla_penalty_brl, disponibilidade_target
FROM Material
WHERE tier_nivel = 'TIER_1'
ORDER BY sla_penalty_brl DESC;
```

---

### 6. Top 5 Families Configuration

**Purpose:** Pre-configured for Nova Corrente's top 5 material families

**Top 5 Families:**
1. **MATERIAL ELETRICO** (32.3% of movements)
2. **FERRO E AÇO** (19.0%)
3. **EPI** (19.1%)
4. **MATERIAL CIVIL** (16.5%)
5. **FERRAMENTAS E EQUIPAMENTOS** (13.0%)

**View:** `vw_top5_familias_nova_corrente`

```sql
-- Get statistics for top 5 families
SELECT * FROM vw_top5_familias_nova_corrente;
```

---

### 7. Lead Time Customizations

**Purpose:** Nova Corrente-specific lead time tracking

**Custom Fields:**
- `Fornecedor.lead_time_medio`: Average lead time per supplier
- `Fornecedor.lead_time_std`: Lead time variability
- `Fornecedor_Material.lead_time_padrao`: Material-specific lead time
- `Material.lead_time_medio`: Material average lead time

**Lead Time Categories:**
```sql
-- Fast: <7 days (50% of orders)
-- Normal: 7-14 days (25%)
-- Slow: 14-30 days (15%)
-- Very Slow: >30 days (10%)
```

**Stored Procedure:** Calculated from `MovimentacaoEstoque` dates

---

### 8. Site/Tower Tracking

**Purpose:** Track materials by site/tower (18,000+ towers)

**Custom Fields:**
- `MovimentacaoEstoque.site_id`: Site/tower identifier
- Aggregations by site in hierarchical features

**Usage:**
```sql
-- Get movements by site
SELECT site_id, COUNT(*) as movimentacoes, SUM(quantidade_movimentada) as total
FROM MovimentacaoEstoque
WHERE site_id IS NOT NULL
GROUP BY site_id
ORDER BY movimentacoes DESC;
```

---

## 🔬 ML FEATURE CATEGORIES (73 FEATURES)

### Feature Storage: `MaterialFeatures` Table

All 73 features are stored in `MaterialFeatures` with categories:

### 1. TEMPORAL Features (15 features)

**Basic:**
- `year`, `month`, `day`, `weekday`, `quarter`, `day_of_year`

**Cyclical (sin/cos):**
- `month_sin`, `month_cos`
- `day_of_year_sin`, `day_of_year_cos`
- `quarter_sin`, `quarter_cos` (optional)

**Boolean:**
- `is_weekend`, `is_holiday` (from CalendarioBrasil)

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = 'TEMPORAL'
AND material_id = 123;
```

---

### 2. CLIMATE Features (12 features)

**From ClimaSalvador:**
- `temperature_avg_c`
- `precipitation_mm`
- `humidity_percent`
- `wind_speed_kmh`

**Calculated:**
- `extreme_heat`
- `cold_weather`
- `heavy_rain`
- `no_rain`
- `is_intense_rain`
- `is_high_humidity`
- `corrosion_risk`
- `field_work_disruption`

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = 'CLIMATE'
AND DATE(data_coleta) = CURDATE();
```

---

### 3. ECONOMIC Features (6 features)

**From IndicadoresEconomicos:**
- `inflation_rate`
- `exchange_rate_brl_usd`
- `gdp_growth_rate`
- `selic_rate`

**Calculated:**
- `high_inflation`
- `currency_devaluation`

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = 'ECONOMIC'
AND DATE(data_coleta) BETWEEN '2024-01-01' AND '2025-01-01';
```

---

### 4. 5G Features (5 features)

**From Expansao5G:**
- `5g_coverage_pct`
- `5g_investment_brl_billions`
- `is_5g_milestone`
- `is_5g_active`
- `5g_expansion_rate`

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = '5G'
AND DATE(data_coleta) = CURDATE();
```

---

### 5. LEAD_TIME Features (8 features)

**Calculated:**
- `lead_time_days` (from Nova Corrente data)
- `base_lead_time_days`
- `total_lead_time_days`
- `customs_delay_days`
- `strike_risk`
- `is_critical_lead_time`
- `lead_time_category`
- `supplier_lead_time_mean`, `supplier_lead_time_std`

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = 'LEAD_TIME'
ORDER BY material_id, feature_name;
```

---

### 6. SLA Features (4 features)

**B2B-Specific:**
- `sla_penalty_brl`
- `availability_target`
- `downtime_hours_monthly`
- `sla_violation_risk`

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = 'SLA'
AND material_id IN (SELECT material_id FROM Material WHERE tier_nivel = 'TIER_1');
```

---

### 7. HIERARCHICAL Features (10 features)

**By Family:**
- `family_demand_ma_7`, `family_demand_ma_30`
- `family_demand_std_7`, `family_demand_std_30`
- `family_frequency`

**By Site:**
- `site_demand_ma_7`, `site_demand_ma_30`
- `site_frequency`

**By Supplier:**
- `supplier_frequency`
- `supplier_lead_time_mean`, `supplier_lead_time_std`

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = 'HIERARCHICAL'
ORDER BY feature_name;
```

---

### 8. CATEGORICAL Features (5 features)

**Encoded:**
- `familia`, `familia_encoded`
- `deposito`, `site_id`
- `fornecedor`

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = 'CATEGORICAL';
```

---

### 9. BUSINESS Features (8 features)

**Nova Corrente-Specific:**
- `item_id`, `material`, `produto_servico`
- `quantidade`, `unidade_medida`
- `solicitacao`, `data_requisitada`, `data_solicitado`, `data_compra`

**Usage:**
```sql
SELECT material_id, feature_name, feature_value
FROM MaterialFeatures
WHERE feature_category = 'BUSINESS'
ORDER BY material_id;
```

---

## 🛠️ STORED PROCEDURES

### 1. `sp_calcular_historico_diario`

**Purpose:** Calculate daily aggregations with Brazilian calendar features

**Parameters:**
- `p_data_referencia`: Date to calculate
- `p_material_id`: Material ID (NULL for all)

**Features Calculated:**
- Quantities (initial, final, entrada, saida)
- Statistics (mean, max, min, std dev)
- Brazilian calendar (weekend, holiday)

**Usage:**
```sql
-- Calculate for all materials for yesterday
CALL sp_calcular_historico_diario(DATE_SUB(CURDATE(), INTERVAL 1 DAY), NULL);

-- Calculate for specific material
CALL sp_calcular_historico_diario('2025-01-15', 123);
```

---

### 2. `sp_extrair_features_material_completo`

**Purpose:** Extract all 73 ML features for a material

**Parameters:**
- `p_material_id`: Material ID
- `p_data_referencia`: Reference date

**Features Extracted:**
- Statistical features
- Hierarchical features
- Temporal features
- All 73 features stored in `MaterialFeatures`

**Usage:**
```sql
-- Extract features for material 123
CALL sp_extrair_features_material_completo(123, CURDATE());

-- Extract for all materials
CALL sp_extrair_features_material_completo(NULL, CURDATE());
```

---

### 3. `sp_extrair_features_externas_brasil`

**Purpose:** Extract Brazilian external features (climate, economic, 5G)

**Parameters:**
- `p_data_referencia`: Reference date

**Features Extracted:**
- Climate features from `ClimaSalvador`
- Economic features from `IndicadoresEconomicos`
- 5G features from `Expansao5G`

**Usage:**
```sql
-- Extract external features for today
CALL sp_extrair_features_externas_brasil(CURDATE());

-- Extract for a date range (call in loop)
CALL sp_extrair_features_externas_brasil('2025-01-15');
```

---

## 📊 VIEWS FOR ML PROCESSING

### 1. `vw_material_ml_features`

**Purpose:** Comprehensive material view with all ML features

**Columns:**
- Material basic info
- ML-enhanced columns (reorder_point, safety_stock, ABC, tier)
- Family information
- Movement statistics
- Time in system

**Usage:**
```sql
SELECT * FROM vw_material_ml_features
WHERE tier_nivel = 'TIER_1'
ORDER BY score_importancia DESC;
```

---

### 2. `vw_material_time_series_brasil`

**Purpose:** Time series view with all Brazilian custom features

**Columns:**
- Daily aggregations
- Brazilian calendar features
- Salvador climate features
- Economic indicators
- 5G expansion features

**Usage:**
```sql
SELECT * FROM vw_material_time_series_brasil
WHERE material_id = 123
AND data_referencia BETWEEN '2024-01-01' AND '2025-01-01'
ORDER BY data_referencia;
```

**Perfect for:** Time series forecasting models (LSTM, Prophet, ARIMA)

---

### 3. `vw_top5_familias_nova_corrente`

**Purpose:** Statistics for Nova Corrente's top 5 families

**Usage:**
```sql
SELECT * FROM vw_top5_familias_nova_corrente;
```

---

### 4. `vw_predictions_summary`

**Purpose:** ML predictions with tracking metrics

**Usage:**
```sql
SELECT * FROM vw_predictions_summary
WHERE data_referencia >= CURDATE()
ORDER BY data_predicao DESC;
```

---

## 💡 USAGE EXAMPLES

### Example 1: Daily Feature Engineering Pipeline

```sql
-- Step 1: Calculate daily aggregations
CALL sp_calcular_historico_diario(CURDATE(), NULL);

-- Step 2: Extract Brazilian external features
CALL sp_extrair_features_externas_brasil(CURDATE());

-- Step 3: Extract material features for all materials
-- (This would be done in a loop for all materials)
CALL sp_extrair_features_material_completo(123, CURDATE());
```

---

### Example 2: Get ML-Ready Dataset for Training

```sql
-- Get time series data for LSTM training
SELECT 
    material_id,
    data_referencia,
    entrada_total as target,
    temperatura_media,
    precipitacao_mm,
    is_feriado,
    is_weekend,
    cobertura_5g_percentual,
    taxa_inflacao,
    taxa_cambio_brl_usd
FROM vw_material_time_series_brasil
WHERE material_id IN (
    SELECT material_id FROM Material 
    WHERE familia_id IN (
        SELECT familia_id FROM Familia 
        WHERE nome_familia IN (
            'MATERIAL ELETRICO',
            'FERRO E AÇO',
            'EPI',
            'MATERIAL CIVIL',
            'FERRAMENTAS E EQUIPAMENTOS'
        )
    )
)
AND data_referencia >= '2024-01-01'
ORDER BY material_id, data_referencia;
```

---

### Example 3: Get Material Features for Prediction

```sql
-- Get all 73 features for a material
SELECT 
    feature_name,
    feature_value,
    feature_category
FROM MaterialFeatures
WHERE material_id = 123
AND DATE(data_coleta) = CURDATE()
ORDER BY feature_category, feature_name;
```

---

### Example 4: Monitor Predictions vs Actual

```sql
-- Get prediction accuracy
SELECT 
    m.nome_material,
    pred.tipo_predicao,
    pred.valor_predito,
    track.valor_real,
    track.erro_percentual as mape,
    track.mae,
    track.rmse
FROM MLPredictions pred
JOIN Material m ON pred.material_id = m.material_id
JOIN MLPredictionTracking track ON pred.prediction_id = track.prediction_id
WHERE pred.data_referencia >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
ORDER BY track.erro_percentual DESC;
```

---

## 📝 NOTES

### Data Population Order

1. **Base Tables:** Usuario, Familia, Fornecedor, Material
2. **Reference Tables:** CalendarioBrasil, ClimaSalvador, IndicadoresEconomicos, Expansao5G
3. **Movements:** MovimentacaoEstoque
4. **Aggregations:** Run `sp_calcular_historico_diario` for date range
5. **Features:** Run `sp_extrair_features_externas_brasil` and `sp_extrair_features_material_completo`

### Performance Optimization

- All tables have appropriate indexes
- Daily aggregations are pre-calculated
- Features are stored for fast retrieval
- Views are optimized for ML queries

### Maintenance

- Run daily aggregation procedures daily
- Update external features (climate, economic, 5G) daily
- Refresh material features weekly or on-demand
- Monitor prediction tracking for model retraining

---

## ✅ CUSTOM TUNINGS SUMMARY

| Category | Custom Tuning | Table/Field | Purpose |
|----------|---------------|--------------|---------|
| **Brazilian** | Holidays Calendar | `CalendarioBrasil` | Brazilian holidays impact on demand |
| **Brazilian** | Salvador Climate | `ClimaSalvador` | INMET climate data for Salvador/BA |
| **Brazilian** | Economic Indicators | `IndicadoresEconomicos` | BACEN economic data |
| **Brazilian** | 5G Expansion | `Expansao5G` | ANATEL 5G expansion tracking |
| **Nova Corrente** | Tier Levels | `Material.tier_nivel` | TIER_1/2/3 criticality |
| **Nova Corrente** | Top 5 Families | `Familia`, View | Pre-configured top families |
| **Nova Corrente** | Lead Time | `Fornecedor`, `Fornecedor_Material` | Supplier/material lead times |
| **Nova Corrente** | Site/Tower Tracking | `MovimentacaoEstoque.site_id` | 18,000+ towers tracking |
| **Nova Corrente** | SLA Features | `Material.sla_penalty_brl` | B2B SLA penalties |
| **ML** | 73 Features | `MaterialFeatures` | All ML features organized |

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Status:** ✅ **COMPLETE** - All Custom Tunings Documented

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

