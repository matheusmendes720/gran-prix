# 📊 FASE 2: ANALYTICS LAYER - GUIA DETALHADO
## Nova Corrente - Analytics Engineering Roadmap

**Versão:** 1.0  
**Data:** Novembro 2025  
**Duração:** 4 semanas  
**Status:** 📋 Plano de Implementação

---

## 📋 OBJETIVOS DA FASE 2

**Meta Principal:**
Implementar Gold layer (star schema) com modelos de negócio e métricas pré-calculadas, habilitando self-service BI.

**Objetivos Específicos:**
1. Criar star schema completo (dim/fact tables)
2. Implementar métricas de negócio (dbt metrics)
3. Configurar BI tools (Metabase/Superset)
4. Criar dashboards básicos
5. Habilitar self-service analytics

---

## 🎯 ENTREGAS PRINCIPAIS

### 1. Gold Layer - Star Schema

**Objetivo:** Criar modelo dimensional completo

**Estrutura:**
```
dbt/models/marts/
├── dimensions/
│   ├── dim_items.sql
│   ├── dim_towers.sql
│   ├── dim_suppliers.sql
│   ├── dim_time.sql
│   └── dim_regions.sql
├── facts/
│   ├── fact_forecasts.sql
│   ├── fact_inventory.sql
│   ├── fact_demand.sql
│   └── fact_orders.sql
└── metrics/
    └── forecast_metrics.sql
```

**Exemplo: dim_items.sql**

```sql
-- models/marts/dim_items.sql
{{ config(
    materialized='table',
    schema='marts',
    tags=['marts', 'dimensions', 'items'],
    cluster_by=['category'],
    post_hook="ANALYZE TABLE {{ this }} COMPUTE STATISTICS FOR ALL COLUMNS"
) }}

WITH staging AS (
    SELECT * FROM {{ ref('stg_items') }}
),

final AS (
    SELECT
        -- Primary key
        item_id,
        
        -- Attributes
        item_name,
        category,
        family,
        supplier_id,
        
        -- Metrics
        cost,
        avg_lead_time_days,
        min_lead_time_days,
        max_lead_time_days,
        
        -- Classification
        CASE 
            WHEN cost < 100 THEN 'LOW_COST'
            WHEN cost < 1000 THEN 'MEDIUM_COST'
            ELSE 'HIGH_COST'
        END AS cost_tier,
        
        CASE 
            WHEN avg_lead_time_days <= 7 THEN 'FAST'
            WHEN avg_lead_time_days <= 14 THEN 'MEDIUM'
            ELSE 'SLOW'
        END AS lead_time_tier,
        
        -- SCD Type 2 fields
        CURRENT_TIMESTAMP() AS valid_from,
        NULL AS valid_to,
        TRUE AS is_current
        
    FROM staging
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY item_id
        ORDER BY loaded_at DESC
    ) = 1
)

SELECT * FROM final
```

**Exemplo: fact_forecasts.sql**

```sql
-- models/marts/fact_forecasts.sql
{{ config(
    materialized='table',
    schema='marts',
    tags=['marts', 'facts', 'forecasts'],
    cluster_by=['forecast_date'],
    partition_by={'field': 'forecast_date', 'data_type': 'date'},
    post_hook="ANALYZE TABLE {{ this }} COMPUTE STATISTICS FOR ALL COLUMNS"
) }}

WITH staging_forecasts AS (
    SELECT * FROM {{ ref('stg_forecasts') }}
),

dim_items AS (
    SELECT * FROM {{ ref('dim_items') }}
),

dim_towers AS (
    SELECT * FROM {{ ref('dim_towers') }}
),

dim_time AS (
    SELECT * FROM {{ ref('dim_time') }}
),

enriched AS (
    SELECT
        -- Fact key
        f.forecast_id,
        
        -- Foreign keys
        f.item_id,
        i.item_hk,
        t.tower_id,
        f.forecast_date,
        dt.date_key,
        
        -- Measures
        f.forecasted_demand,
        f.actual_demand,
        f.ci_lower,
        f.ci_upper,
        
        -- Calculated measures
        f.forecasted_demand - f.actual_demand AS forecast_error,
        ABS(f.forecasted_demand - f.actual_demand) AS absolute_error,
        CASE 
            WHEN f.actual_demand > 0 
            THEN ABS(f.forecasted_demand - f.actual_demand) / f.actual_demand * 100
            ELSE NULL
        END AS mape,
        
        -- Model info
        f.model_type,
        f.accuracy_level,
        
        -- Dimensions
        i.category,
        i.cost_tier,
        i.lead_time_tier,
        t.region,
        t.sla_tier,
        dt.year,
        dt.quarter,
        dt.month,
        dt.is_holiday,
        
        -- Timestamps
        f.created_at
        
    FROM staging_forecasts f
    INNER JOIN dim_items i ON f.item_id = i.item_id
    LEFT JOIN dim_towers t ON f.tower_id = t.tower_id
    INNER JOIN dim_time dt ON f.forecast_date = dt.date
    WHERE f.forecast_date >= CURRENT_DATE - 365  -- Last year
)

SELECT * FROM enriched
```

**Exemplo: dim_time.sql**

```sql
-- models/marts/dim_time.sql
{{ config(
    materialized='table',
    schema='marts',
    tags=['marts', 'dimensions', 'time']
) }}

WITH date_spine AS (
    SELECT 
        date_day
    FROM {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2026-12-31' as date)"
    ) }}
),

enriched AS (
    SELECT
        date_day AS date,
        
        -- Date key for joins
        CAST(REPLACE(CAST(date_day AS STRING), '-', '') AS INTEGER) AS date_key,
        
        -- Basic date parts
        EXTRACT(YEAR FROM date_day) AS year,
        EXTRACT(QUARTER FROM date_day) AS quarter,
        EXTRACT(MONTH FROM date_day) AS month,
        EXTRACT(WEEK FROM date_day) AS week,
        EXTRACT(DAY FROM date_day) AS day,
        EXTRACT(DAYOFWEEK FROM date_day) AS day_of_week,
        EXTRACT(DAYOFYEAR FROM date_day) AS day_of_year,
        
        -- Labels
        FORMAT_DATE('%B', date_day) AS month_name,
        FORMAT_DATE('%A', date_day) AS day_name,
        
        -- Flags
        EXTRACT(DAYOFWEEK FROM date_day) IN (1, 7) AS is_weekend,
        EXTRACT(DAY FROM date_day) <= 7 AS is_month_start,
        EXTRACT(DAY FROM date_day) >= 25 AS is_month_end,
        
        -- Brazilian holidays (simplified - expand with full list)
        date_day IN (
            DATE('2024-01-01'), -- New Year
            DATE('2024-02-12'), -- Carnival
            DATE('2024-04-21'), -- Tiradentes
            DATE('2024-05-01'), -- Labor Day
            DATE('2024-09-07'), -- Independence
            DATE('2024-10-12'), -- Our Lady Aparecida
            DATE('2024-11-02'), -- All Souls
            DATE('2024-11-15'), -- Republic
            DATE('2024-12-25')  -- Christmas
        ) AS is_holiday,
        
        -- Business logic
        CASE 
            WHEN EXTRACT(QUARTER FROM date_day) = 1 THEN 'Q1'
            WHEN EXTRACT(QUARTER FROM date_day) = 2 THEN 'Q2'
            WHEN EXTRACT(QUARTER FROM date_day) = 3 THEN 'Q3'
            ELSE 'Q4'
        END AS quarter_label
        
    FROM date_spine
)

SELECT * FROM enriched
```

**Checklist:**
- [ ] Todas dimension tables criadas
- [ ] Todas fact tables criadas
- [ ] Relacionamentos validados
- [ ] Partições configuradas
- [ ] Clusters otimizados
- [ ] dbt test passando

---

### 2. dbt Metrics (Semantic Layer)

**Objetivo:** Criar métricas de negócio reutilizáveis

**Exemplo: models/metrics/forecast_metrics.yml**

```yaml
# models/metrics/forecast_metrics.yml
version: 2

metrics:
  - name: forecast_accuracy_mape
    label: "Forecast Accuracy (MAPE)"
    description: "Mean Absolute Percentage Error of forecasts"
    model: ref('fact_forecasts')
    calculation_method: average
    expression: |
      CASE 
        WHEN actual_demand > 0 
        THEN ABS(forecasted_demand - actual_demand) / actual_demand * 100
        ELSE NULL
      END
    timestamp: forecast_date
    time_grains: [day, week, month, quarter, year]
    dimensions:
      - category
      - cost_tier
      - lead_time_tier
      - region
      - model_type
    
  - name: total_forecasted_demand
    label: "Total Forecasted Demand"
    description: "Sum of all forecasted demand values"
    model: ref('fact_forecasts')
    calculation_method: sum
    expression: forecasted_demand
    timestamp: forecast_date
    time_grains: [day, week, month, quarter, year]
    dimensions:
      - category
      - cost_tier
      - region
    
  - name: forecast_error_count
    label: "Forecast Error Count"
    description: "Count of forecasts with MAPE > 15%"
    model: ref('fact_forecasts')
    calculation_method: count
    expression: |
      CASE 
        WHEN mape > 15 THEN 1
        ELSE 0
      END
    timestamp: forecast_date
    time_grains: [day, week, month]
    dimensions:
      - category
      - model_type
```

**Checklist:**
- [ ] Métricas de negócio definidas
- [ ] Time grains configurados
- [ ] Dimensions mapeadas
- [ ] API de métricas testada
- [ ] Documentação das métricas

---

### 3. Setup BI Tools

**3.1 Metabase Setup**

**Configuração:**
```yaml
# docker-compose.metabase.yml
version: '3.8'
services:
  metabase:
    image: metabase/metabase:latest
    container_name: nova-corrente-metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: metabase
      MB_DB_PORT: 5432
      MB_DB_USER: metabase
      MB_DB_PASS: metabase
      MB_DB_HOST: postgres
    depends_on:
      - postgres
    volumes:
      - metabase-data:/metabase-data

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: metabase
      POSTGRES_USER: metabase
      POSTGRES_PASSWORD: metabase
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  metabase-data:
  postgres-data:
```

**Conectar ao Databricks:**
1. Add Database → Databricks
2. Host: `<workspace-url>.cloud.databricks.com`
3. Port: 443
4. HTTP Path: `/sql/1.0/warehouses/<warehouse-id>`
5. Personal Access Token: Databricks token

**Checklist:**
- [ ] Metabase instalado e rodando
- [ ] Conexão com Databricks configurada
- [ ] Usuários criados
- [ ] Permissões configuradas

---

**3.2 Superset Setup**

**Configuração:**
```yaml
# docker-compose.superset.yml
version: '3.8'
services:
  superset:
    image: apache/superset:latest
    container_name: nova-corrente-superset
    ports:
      - "8088:8088"
    environment:
      SUPERSET_CONFIG_PATH: /app/superset_config.py
    volumes:
      - ./superset_config.py:/app/superset_config.py
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: superset
      POSTGRES_USER: superset
      POSTGRES_PASSWORD: superset
```

**Checklist:**
- [ ] Superset instalado
- [ ] Conexão com Databricks configurada
- [ ] Dashboards básicos criados
- [ ] Alerts configurados

---

### 4. Dashboards Básicos

**4.1 Dashboard: Forecast Performance**

**Métricas:**
- MAPE médio por categoria
- Forecast accuracy trend (últimos 30 dias)
- Top 10 items com maior erro
- Model performance comparison

**4.2 Dashboard: Inventory Management**

**Métricas:**
- Current stock levels
- Reorder points vs current stock
- Items em risco (stock <= reorder point)
- Lead time analysis

**4.3 Dashboard: Business KPIs**

**Métricas:**
- Total forecasted demand (next 30 days)
- Forecast accuracy (MAPE)
- Stockout risk
- Cost analysis

**Checklist:**
- [ ] 3+ dashboards criados
- [ ] Métricas principais visualizadas
- [ ] Usuários de negócio podem acessar
- [ ] Alerts configurados

---

### 5. Self-Service Analytics

**Habilitar:**
1. Query builder visual (Metabase)
2. Saved queries reutilizáveis
3. Custom dashboards
4. Export Excel/PDF
5. Scheduled reports

**Checklist:**
- [ ] Usuários treinados
- [ ] Documentação de uso criada
- [ ] Templates de queries disponíveis
- [ ] Suporte disponível

---

## 📊 MÉTRICAS DE SUCESSO FASE 2

**Técnicas:**
- ✅ Gold layer: 100% dos modelos criados
- ✅ Métricas dbt: 10+ métricas definidas
- ✅ BI tools: 2 ferramentas configuradas
- ✅ Dashboards: 3+ dashboards funcionando
- ✅ Self-service: 5+ usuários ativos

**Processo:**
- ✅ Documentação completa
- ✅ Usuários treinados
- ✅ Pipeline de atualização funcionando

---

## 🚀 PRÓXIMOS PASSOS

Após conclusão da Fase 2:
1. Expandir dashboards
2. Preparar para Fase 3 (ML Ops)
3. Integração com sistemas externos

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Guia Detalhado Fase 2

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

