# Storytelling Frontend Integration Plan

## Fluxo Geral
1. **Backend**: montar FastAPI usando `api-integration/storytelling_api_stub.py`
2. **Frontend**: criar hooks React para cada endpoint
3. **Estado global**: `React Query` ou `zustand` para cache + streaming
4. **Componentização**:
   - `SummaryHero` -> cards KPI
   - `ForecastExplorer` -> heatmap + linha detalhada
   - `AlertCommandCenter` -> tabela/kanban com ações
   - `ContextStrip` -> cartões climáticos/macro (do Gold)

## Sequência de Implementação
1. **API wiring**
   ```bash
   uvicorn storytelling_api:app --reload
   ```
2. **Client hooks**
   ```ts
   import { useQuery } from '@tanstack/react-query';

   export const useStorytellingKpis = () =>
     useQuery(['storytelling','kpis'], () =>
       fetch('/api/storytelling/kpis').then(r => r.json()));
   ```
3. **Dashboard page**
   ```tsx
   const { data: kpis } = useStorytellingKpis();
   const { data: alerts } = useStorytellingAlerts({ status: ['critical'] });
   const { data: timeseries } = useStorytellingTimeseries({ familia: selectedFamily });
   ```
4. **Alert actions**
   - Botão “Gerar pedido” -> chama serviço ERP (mock)
   - Badge cor por `stock_status`
   - Tooltip com `safety_stock` e `days_to_rupture`

## Métricas para Demo
- Taxa de ruptura evitada = proporção de `critical` tratados em D-1
- Cobertura de séries = `series_with_forecast / series_total`
- Lead time médio por família (usar coluna `lead_time_days` do Gold)

## Próximos Passos (pós-demo)
- Portar API para stream real-time (WebSocket)
- Adicionar filtros por região/site
- Integrar forecast confidence em gráfico de barras empilhado

