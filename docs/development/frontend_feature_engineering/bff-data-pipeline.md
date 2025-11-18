# BFF Data Pipeline

## Visão Geral
- **Meta:** Substituir dados mockados por respostas do FastAPI BFF alimentado pelos artefatos `nova-corrente-workspace`.
- **Principais arquivos backend:**
  - `backend/bff/main.py` — endpoints `/bff/dashboard/summary`, `/bff/alerts`, `/bff/forecasts`, `/bff/features/climate`.
  - `backend/bff/service.py` — transformações (geo, clima, recomendações).
  - `backend/bff/schemas.py` — contratos Pydantic.
  - `nova-corrente-workspace/workspace/data-sources/storytelling_loader.py` — cargas parquet/JSON.

## Frontend Impactado
- Hooks: `frontend/src/hooks/use-api.ts` (`useDashboardSummary`, `useAlerts`, `useBffForecasts`, `useClimateFeatures`).
- Cliente: `frontend/src/lib/api-client.ts` (funções `getBff*`).
- Componentes: Dashboard, GeoHeatmap, Climate page, PrescriptiveRecommendations.

## Problemas
- **Disponibilidade do BFF:** backend precisa ser iniciado manualmente, sem fallback automático.
- **Schemas divergentes:** campos como `stock_status`/`status` e `items`/`data` geraram erros até ajustes manuais.
- **Infra local:** necessidade de rodar scripts Python para gerar artefatos antes dos testes.

## Rollback / Mitigação
1. Desabilitar chamadas BFF na camada de hooks, retornando dados mock padrão:
   ```ts
   export function useDashboardSummary() {
     return { data: MOCK_SUMMARY, error: undefined };
   }
   ```
2. `git checkout <commit-base> -- backend/bff frontend/src/hooks/use-api.ts frontend/src/lib/api-client.ts`.
3. Remover variáveis `NEXT_PUBLIC_BFF_URL` e dependências dos componentes (substituir por mocks originais).

## Recomendações
- Criar flag de feature (`NEXT_PUBLIC_ENABLE_BFF`) para controlar uso em produção vs. demo.
- Montar pipeline de validação dos artefatos parquet para garantir compatibilidade antes de subir BFF.
