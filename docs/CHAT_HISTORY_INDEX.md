# Chat History Index — Nova Corrente Frontend/BFF Rollback

## Visão Geral
- **Período:** Sessão atual (Novembro/2025)
- **Objetivo:** Restaurar UI legacy deep-blue, documentar tentativas de modernização, planejar demo hardcoded.
- **Status Atual:** Frontend e backend revertidos ao baseline; documentação consolidada; novo plano demo hardcoded em andamento.

## Linha do Tempo
1. **Kickoff** – pedido de aprofundar UI/UX com storytelling interativo e BFF.
2. **Implementação Storytelling** – criação de hooks BFF, cenário simulador, clima, banners snapshot.
3. **Incidente** – usuário rejeita visual (“deep blue sumiu”); exige rollback imediato.
4. **Operação Resgate** – branch `rollback/legacy-ui-restore`, checkout para commit `9fd5f4d…`, remoção BFF FastAPI.
5. **Documentação** – produção da série `frontend_feature_engineering/` + `safe-restore-roadmap.md`.
6. **Reindexação** – atualização de `INDEX_MASTER_NAVIGATION_PT_BR.md` com referências de pitch/storytelling.
7. **Foco Demo Hardcoded** – decisão atual: construir dashboard 100% mockado para apresentação.

## Decisões-Chave
- ❌ Abandonar temporariamente BFF FastAPI em produção.
- ✅ Restaurar UI teal original com dados mock.
- ✅ Manter melhorias documentadas para reintrodução futura.
- ✅ Priorizar demo storytelling hardcoded para pitch imediato.

## Artefatos Criados/Atualizados
- `docs/development/frontend_feature_engineering/*.md` – relatórios por feature.
- `docs/development/frontend_feature_engineering/safe-restore-roadmap.md` – passo a passo rollback.
- `docs/INDEX_MASTER_NAVIGATION_PT_BR.md` – novos links para pitch (`demo_dashboard_quick_strategy.md`) e resumo executivo (`Solucao-Completa-Resumida-Final.md`).
- `docs/CHAT_HISTORY_INDEX.md` – este índice.

## Próximas Tarefas
1. Popular `frontend/src/data/demoSnapshot.ts` com dados determinísticos.
2. Scaffold layout demo (Hero, Painel Operacional, Alertas, Geo, ROI).
3. Implementar widgets prioritários (KPI strip → Demand Pulse → Scenario → Alerts → Mapa → Waterfall → ROI gauge).
4. Ensaiar narrativa seguindo `demo_dashboard_quick_strategy.md`.

## Ponto de Contato
- Branch de trabalho: `rollback/legacy-ui-restore`.
- Baseline seguro: commit `9fd5f4dc844c805804c47380f8abe8e4b58476a2`.
- Documentação completa: ver `docs/INDEX_MASTER_NAVIGATION_PT_BR.md`.
