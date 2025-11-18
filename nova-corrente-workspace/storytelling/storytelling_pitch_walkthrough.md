# Nova Corrente Storytelling – Pitch Walkthrough

## Objetivo do Demo
- Mostrar como o app traduz dados descritivos, preditivos e prescritivos em ações
- Comprovar impacto operacional (rupturas evitadas, giro otimizado, risco controlado)
- Sustentar narrativa comercial para o pitch deck

## Roteiro de Apresentação
1. **Tela de Abertura (60s)**
   - KPI cards carregados por `get_kpi_snapshot`: séries cobertas, % com forecast, séries críticas
   - Destaque: ROI projetado (192%+), payback <5 meses (texto auxiliar)
2. **Painel de Demanda & Forecast (3 min)**
   - Mapa de calor por `familia` com filtros (dados de `storytelling_timeseries.parquet`)
   - Drill-down para série `ABRASIVOS` exibindo:
     - Linha histórica (actual_qty) + faixa de previsão (forecast_qty / intervalos)
     - Contribuição ARIMA x XGBoost (colunas dedicadas)
3. **Alerta Prescritivo (2 min)**
   - Lista de `critical` via `get_alerts_by_status`
   - Explicar cálculo ROP/SS e prazo de ruptura
   - Ação sugerida: geração de pedido automático ou ajuste de lead time
4. **Contexto Externo (2 min)**
   - Cartões climáticos/macroeconômicos originados do Gold (temperatura, IPCA, câmbio)
   - Narrativa: como sinal externo ajusta previsão (multiplicadores de contexto)
5. **Encerramento (1 min)**
   - Recapitular reduções de ruptura / estoque morto
   - Mostrar backlog de features (tempo real, mobile, simulações próximas)

## Componentes-Chave do Dashboard
- **SummaryHero**: consome `storytelling_summary.json`
- **FamilyForecastExplorer**: deriva de `get_family_timeseries(familia)`
- **AlertCommandCenter**: lista priorizada com badges de severidade
- **ContextInsightsStrip**: chama dados do Gold (`FactDemand`) para clima/macro

## Mensagens para Pitch Deck
- “Plataforma pronta para plugar em APIs / ERP” – base nos loaders Python recém-criados
- “Insights prescritivos acionáveis” – demonstrar conversão de alerta em ordem
- “Roadmap validado” – alinhar com `improvements-summary.json` (fase 1 concluída)

## Preparação Técnica
- Executar `python -m scripts.storytelling.build_storytelling_assets ...` antes da demo
- Validar `storytelling_loader.get_kpi_snapshot()` e `get_alerts_by_status()` em notebook
- Pré-carregar gráficos no notebook `quick-executive-dashboard.ipynb` (cache Polaris)

## Follow-up Pós-Demo
- Exportar dashboards em vídeo/gif para o deck
- Montar anexo técnico com APIs previstas (websocket, endpoints REST)
- Registrar feedbacks para roadmap da fase 2 (UX & mobile)

