# Scenario Simulator Integration

## Objetivo
Levar o simulador interativo de demanda/lead time (DemandChart) para a página legacy, propagando métricas para alertas e recomendações.

## Implementação Atual
- `frontend/src/components/DemandChart.tsx`
  - Refatorado para usar `useBffForecasts` com limite 200 e fallback de snapshot.
  - Estilização ajustada para a paleta deep-blue; exibe aviso âmbar em caso de fallback.
- `frontend/src/components/Dashboard.tsx`
  - Estado `scenarioMetrics` é atualizado via `onScenarioUpdate` e aplicado a alertas/recomendações.
  - Injetado seletor de séries (BFF) com fallback para `FALLBACK_SERIES` quando vazio.
- `frontend/src/components/PrescriptiveRecommendationsEnhanced.tsx`
  - Ainda depende de `/api/v1/recommendations/insights`; ausência de fallback completo.

## Problemas Identificados
- Falha silenciosa do hook `useBffForecasts` quando BFF indisponível (corrigido parcialmente com snapshot, mas ainda loga erro no console).
- Alerts e recomendações podem exibir dados híbridos (mistura de fallback e BFF), dificultando validação.
- Interface do simulador difere levemente do estilo original (sliders com `accent-brand-*`).

## Rollback Strategy
1. Restaurar DemandChart para versão anterior (pré-integração BFF) usando:
   ```bash
   git checkout <commit-base> -- frontend/src/components/DemandChart.tsx
   ```
2. Remover estado `scenarioMetrics` de `Dashboard.tsx` e restaurar arquivo completo do commit base.
3. Revalidar `PrescriptiveRecommendationsEnhanced` contra endpoints legacy.

## Próximos Passos Recomendados
- Criar testes unitários (React Testing Library) para garantir que fallback continue funcionando se mantivermos a nova versão.
- Documentar dados necessários para BFF servir séries consistentes; hoje dependemos de `series_key` harmonizado.
