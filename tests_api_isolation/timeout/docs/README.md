# Timeout Isolation Documentation Hub

## Objetivo
Centralizar referências e procedimentos relacionados à suíte `tests_api_isolation/timeout`, cobrindo execução local, automação, coleta de métricas e observabilidade.

## Índice de documentos
- `ci_pipeline_plan.md` — plano de pipeline CI/CD com YAML exemplo, critérios de falha e requisitos do runner.
- `live_execution_runbook.md` — passo a passo para execuções com `RUN_LIVE=1`, incluindo coleta de HAR e mitigação de falhas.
- `observability_guidelines.md` — métricas, dashboards e alertas recomendados.
- `../tools/reporting/push_metrics.py` — script para publicar métricas no Prometheus Pushgateway.

## Fluxo recomendado
1. **Provisionar dependências**: instale `k6`, `locust`, `toxiproxy`, `mitmproxy` conforme `setup/README.md`.
2. **Executar suite**: use `python tools/run_suite.py --pytest --k6 --locust` (ver runbook para `RUN_LIVE`).
3. **Atualizar relatórios**: preencha `reports/summary/` com métricas reais usando o template do changelog.
4. **Automatizar**: configure o pipeline descrito em `ci_pipeline_plan.md`.
5. **Monitorar**: publique métricas com `push_metrics.py` e construa dashboards seguindo `observability_guidelines.md`.

## Próximas manutenções
- Versionar novas instruções ou playbooks aqui.
- Atualizar links sempre que novos documentos forem adicionados.
