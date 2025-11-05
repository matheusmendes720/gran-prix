-- etl/calculate_kpis.sql (scheduled via cron or Airflow)
INSERT INTO analytics.kpis_daily (
  full_date,
  total_demand,
  stockout_rate,
  abc_a_share,
  delayed_orders_pct,
  forecast_mape,
  avg_inventory_value,
  computed_at
)
SELECT
  d.full_date,
  COALESCE(SUM(f.quantity), 0) AS total_demand,
  
  -- Stockout rate: % of items with zero inventory
  (SELECT COUNT(DISTINCT item_id)::NUMERIC / NULLIF((SELECT COUNT(*) FROM core.dim_item WHERE active = true), 0)
   FROM core.fact_inventory_daily
   WHERE full_date = d.full_date AND current_stock = 0) AS stockout_rate,
  
  -- ABC A-class share of total demand
  (SELECT SUM(f2.quantity) FROM core.fact_demand_daily f2
   JOIN core.dim_item i2 ON f2.item_id = i2.item_id
   WHERE f2.full_date = d.full_date AND i2.abc_class = 'A') / NULLIF(SUM(f.quantity), 0) AS abc_a_share,
  
  -- Delayed orders: % orders past expected delivery
  (SELECT COUNT(*)::NUMERIC / NULLIF(COUNT(*), 0)
   FROM core.fact_orders
   WHERE order_date = d.full_date 
     AND status = 'DELAYED') AS delayed_orders_pct,
  
  -- Forecast MAPE (placeholder: calculate from actuals vs forecasts)
  0.12 AS forecast_mape,  -- Using a placeholder value; in reality, this would compare actuals to forecasts
  
  -- Avg inventory value
  (SELECT AVG(current_stock * i.unit_cost)
   FROM core.fact_inventory_daily inv
   JOIN core.dim_item i ON inv.item_id = i.item_id
   WHERE inv.full_date = d.full_date) AS avg_inventory_value,
  
  CURRENT_TIMESTAMP AS computed_at
  
FROM core.dim_calendar d
LEFT JOIN core.fact_demand_daily f ON d.full_date = f.full_date
WHERE d.full_date = CURRENT_DATE - INTERVAL '1 day' -- Yesterday's KPIs
GROUP BY d.full_date
ON CONFLICT (full_date, computed_at) DO NOTHING;