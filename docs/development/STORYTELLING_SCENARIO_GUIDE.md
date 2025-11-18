# Storytelling Scenario Widgets Guide

Este guia descreve como operar e estender os widgets de cenário implementados no dashboard Nova Corrente. Serve como documentação viva para designers, engenheiros e equipes de demonstração que precisam compreender o fluxo completo: dados -> simulação -> narrativa.

---

## 1. Componentes Envolvidos
- `frontend/src/components/DemandChart.tsx`
  - Slider de variação de demanda (`[-30%, +50%]`).
  - Slider de delta de lead time (`[-5, +10]` dias).
  - Emite `ScenarioUpdatePayload` via `onScenarioUpdate`.
- `frontend/src/app/page.tsx`
  - Persistência do cenário selecionado (`scenarioMetrics`).
  - Enriquecimento de alertas e recomendações com métricas simuladas.
  - Banners de modo demo/offline.
- `frontend/src/components/PrescriptiveRecommendations.tsx`
  - Destaques para PP ajustado, estoque de segurança, ordens sugeridas.
- `frontend/src/types.ts`
  - Tipos ampliados (`Alert.scenarioMessage`, etc.).
- `frontend/src/lib/analytics.ts`
  - `trackEvent` para telemetria básica.

---

## 2. Fluxo de Dados
1. Usuário ajusta sliders no `DemandChart`.
2. Component calcula:
   - `demandMultiplier`, `leadTimeMultiplier`.
   - `combinedMultiplier`, `scenarioAvgForecast`.
   - Deltas de estoque de segurança (`baseline` vs `adjusted`).
3. `onScenarioUpdate` envia `ScenarioUpdatePayload`.
4. `DashboardPage` replica métricas para:
   - Alertas (mensagens scenario-aware).
   - Painel de recomendações (card dinâmico).
5. Analytics registra interações relevantes (`materials:select`, `scenario:*`, `demo_toggle`).

---

## 3. Narrativa Recomendada
1. **Selecionar material**: clicar na tabela → demanda atual vs forecast.
2. **Simular evento**: aplicar sliders para picos de demanda ou atrasos logísticos.
3. **Interpretar alertas**: verificar badges com PP ajustado e estoque de segurança.
4. **Converter em ação**: painel prescritivo mostra quantidade sugerida e ajuste de buffer.
5. **Pitch**: enfatizar rapidez de diagnóstico e capacidade de planejar rupturas antes de acontecerem.

---

## 4. Extensões Sugeridas
- Integrar cenário com exportações (PDF/CSV/Livreto).
- Permitir salvar presets de cenário (ex: “Promoção + Climático”).
- Conectar narrativa com tabs de features (clima, SLA, lead time).
- Capturar métricas de uso (taxa de interação por slider, tempo para fechar recomendação).

---

## 5. Checklist de Testes
- Ajustar sliders → alertas exibem PP ajustado e badges.
- Mudar para demo mode → banner indica seções snapshot.
- Desconectar da internet → banner de offline e retry automático (SWR).
- Navegar entre materiais → limpa cenário anterior, dispara analytics.
- Playwright (futuro): roteiros para slider + recomposição de alertas.

---

## 6. Referências
- Código relacionado: ver arquivos listados na seção 1.
- Dados: `storytelling_timeseries.parquet`, `storytelling_prescriptions.parquet`.
- API: `/bff/forecasts`, `/bff/alerts`, `/bff/recommendations`.


