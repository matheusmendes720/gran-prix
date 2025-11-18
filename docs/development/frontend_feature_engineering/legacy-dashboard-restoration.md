# Legacy Dashboard Restoration

## Resumo
- **Objetivo:** Tornar a página "deep-blue" (legacy teal) a experiência padrão novamente.
- **Ações executadas:**
  - Redirecionamos `/` para `frontend/src/app/main/page.tsx`.
  - migrou-se o storytelling dashboard para `frontend/src/app/storytelling-dashboard/page.tsx`.
  - Incorporamos o simulador de cenários, alertas enriquecidos e recomendações dentro de `frontend/src/components/Dashboard.tsx`.
- **Estado atual:** UI restabelecida visualmente, porém ainda dependente das novas integrações (DemandChart, dados BFF) que podem falhar.

## Componentes afetados
- `frontend/src/app/page.tsx`
- `frontend/src/app/main/page.tsx`
- `frontend/src/app/storytelling-dashboard/page.tsx`
- `frontend/src/components/Dashboard.tsx`
- `frontend/src/components/KpiCard.tsx`

## Regressões observadas
- Dependência forte do BFF: quando `useBffForecasts` falha, o simulador exibe mensagem de snapshot (resolvido com fallback, mas ainda novo comportamento).
- `PrescriptiveRecommendationsEnhanced` ainda consome API nova e pode retornar vazio devido a erros de schema.

## Ponto de rollback sugerido
- **Commit alvo:** Último commit antes da refatoração que introduziu o storytelling dashboard (ver histórico em `frontend/src/components/Dashboard.tsx`).
- **Comando:**
  ```bash
  git log frontend/src/components/Dashboard.tsx
  git checkout <commit-antigo> -- frontend/src/app/page.tsx frontend/src/components/Dashboard.tsx frontend/src/components/KpiCard.tsx
  ```
- **Risco:** Reverter apenas esses arquivos remove o simulador e demais melhorias; exigir conciliação com docs atuais.

## Recomendações
1. Avaliar se o storytelling deve permanecer segregado em `/storytelling-dashboard`; caso contrário, remover arquivo e restaurar layout antigo integral.
2. Criar branch `rollback/legacy-dashboard` para testar antes de integrar à main.
3. Congelar merge requests relacionados ao BFF até validação de dados.
