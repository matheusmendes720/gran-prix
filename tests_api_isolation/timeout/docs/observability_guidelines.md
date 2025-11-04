# Observability Guidelines — Timeout Isolation Program

## Objetivo
Incorporar métricas da suíte `tests_api_isolation/timeout` em observabilidade contínua, permitindo detectar regressões de latência, erros de timeout e impactos de rate limiting em produção.

## Métricas essenciais
- **Latência (p50/p95/p99)** por endpoint e valor de timeout testado.
- **Taxa de sucesso** (2xx/total) em testes de concorrência e replays de produção.
- **Retry Attempts**: contagem média de tentativas antes do sucesso.
- **Rate Limit Events**: número de respostas 429/Retry-After por janela.
- **Timeout Failures**: quantidade de exceções `requests.exceptions.Timeout` por job.

## Fontes de dados
1. `reports/raw/run_suite_summary_<timestamp>.json` — consolida resultado de pytest/k6/locust.
2. `k6_summary.json` — exportar no futuro via `handleSummary`; contém percentis de latência e taxas de erro.
3. `locust_stats.csv` — estatísticas de requisições concorrentes.
4. HAR e `request_traces.jsonl` — inputs para análises detalhadas (podem ser ingeridos em Elastic/Datadog).
5. Logs de produção (Prometheus/Grafana, ELK, CloudWatch) — devem ser correlacionados com os parâmetros de timeout recomendados.

## Pipeline sugerido (Prometheus + Grafana)
1. Converter `run_suite_summary` em métricas do tipo `gauge` via script cron ou job adicional.
2. Enviar para Prometheus Pushgateway com labels:
   - `endpoint="BACEN"`, `timeout="5"`, `tool="pytest"`, etc.
3. Criar dashboards em Grafana:
   - Painel 1: Latência x timeout (linha)
   - Painel 2: Taxa de sucesso vs concorrência
   - Painel 3: Eventos 429/Retry-After ao longo do tempo
4. Configurar alertas (Grafana Alerting):
   - `success_rate < 0.9 por 5 min`
   - `latency_p95 > recommended_timeout * 0.8`
   - `timeouts_total > 10 por job`

## Integração com CI/CD
- Adicionar etapa pós-execução no pipeline (ver `ci_pipeline_plan.md`) para publicar métricas no Pushgateway.
- Utilizar o artefato `run_suite_summary` como fonte primária, evitando parsing duplicado de logs.

## Automação opcional
- Criar script `tools/reporting/push_metrics.py` que:
  1. Lê `run_suite_summary_*.json` mais recente.
  2. Extrai métricas-chave.
  3. Envia via HTTP POST para Pushgateway ou API de monitoramento.
- Agendar execução via cron/Scheduler após cada merge.

## Governança
- Revisar dashboards mensalmente com SRE e dev.
- Atualizar valores de timeout recomendados em `final_recommendation.md` quando métricas reais indicarem necessidade.
- Registrar toda alteração significativa no changelog seguindo o template Contexto/Evidências/Recomendações.

## Próximos passos
1. Definir destino das métricas (Prometheus, Datadog ou equivalente).
2. Implementar script de exportação a partir do `run_suite_summary`.
3. Construir dashboards e alertas iniciais, validando com execuções live.
