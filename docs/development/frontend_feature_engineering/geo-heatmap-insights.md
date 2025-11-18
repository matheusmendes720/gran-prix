# Geo Heatmap Insights

## Objetivo
Mostrar distribuição geográfica de estoques/demanda em mapa interativo (heatmap) para contar histórias regionais.

## Implementação Tentada
- **Back-end:** `load_geo_data` no `backend/bff/service.py` usando `storytelling_timeseries.parquet` e `DimSite.parquet`.
- **Front-end:**
  - Componentes `GeoHeatmap` (não editado nesta sessão, mas dependente de dados BFF).
  - Hooks `useGeoSummary` planejado (não finalizado) para consumir `/bff/geo/summary`.

## Problemas Enfrentados
- Artefatos parquet não continham colunas esperadas (`uf`, `municipio`, `site_name`, `latitude`, `longitude`).
- BFF passou a retornar apenas agregações por região, sem coordenadas suficientes para mapa.
- Sem fallback estático, componente renderiza vazio.

## Rollback Strategy
- Reutilizar dataset mockado anterior (GeoJSON estático) e injetar via props até que dados reais estejam corretos.
- Reverter alterações de `load_geo_data` para versão que lia mocks.
- Desabilitar aba/feature no menu até reconstrução da pipeline.

## Ações Futuras
1. Criar script de verificação que valida colunas necessárias ao iniciar BFF.
2. Incluir dataset `geo_snapshot.json` em `frontend/public` para demos.
3. Documentar requisitos de dados (coordenadas, códigos IBGE) no repositório para o time de dados.
