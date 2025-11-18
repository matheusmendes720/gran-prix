# Climate Storytelling

## Objetivo
Habilitar aba "Climate" com dados dinâmicos de clima/risco de corrosão para reforçar narrativa de operações resilientes.

## Implementação
- **Backend:** `backend/bff/service.py` (`load_climate_features`) e `/bff/features/climate` (filtros `start_date`, `end_date`, `limit`).
- **Frontend:**
  - `frontend/src/hooks/use-api.ts` — hook `useClimateFeatures` com SWR e retry.
  - `frontend/src/app/features/climate/page.tsx` — cards de resumo + insights + `ClimateTimeSeriesChart`.
  - `frontend/src/components/charts/ClimateTimeSeriesChart.tsx` — componente visual desacoplado de fetch.

## Situação Atual
- Página carrega mas depende do BFF estar ativo; sem fallback, retorna erro de rede.
- Chart usa dados reais quando endpoint responde, porém falta fallback narrativo para demos offline.
- Storytelling docs: `docs/development/STORYTELLING_SCENARIO_GUIDE.md` cobre narrativa, mas precisa atualização para clima.

## Rollback Strategy
1. Restaurar arquivos para versão mockada (pré-BFF) usando commit base.
2. Manter componente `ClimateTimeSeriesChart` mas abastecer com dataset estático em `page.tsx`.
3. Desligar rota `/features/climate` no menu até revalidação.

## Próximas Ações
- Adicionar `climateSnapshot.json` em `frontend/public/demo-data` e fallback automático.
- Atualizar documentação com métricas esperadas (temperatura, precipitação) para comparar com dados reais.
