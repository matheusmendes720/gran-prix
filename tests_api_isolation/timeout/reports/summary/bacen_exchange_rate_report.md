# BACEN — Exchange Rate (USD/BRL) — Test Report

- **Endpoint**: https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados
- **Período**: 01/01/2024 a 31/12/2024
- **Variável chave**: `timeout`
- **Variações**: 30s (padrão), 10s, 5s, 1s, omisso
- **Concorrência**: 1, 5, 20, 100
- **Retries**: 0, 1, 3
- **Simulações de rede**: latência 500ms, perda de 5%

## Inputs
- Query params: `formato=json`, `dataInicial=01/01/2024`, `dataFinal=31/12/2024`
- Headers: padrão `requests`
- Faults: opcional via Toxiproxy (`latency_500ms`, `packet_loss_5pct`)
- Ambiente: `RUN_LIVE=1`

## Resultados
- **Status codes**:
  - 30s: 200/204 em 100%
  - 10s: 200/204 em 100%
  - 5s: 200/204 em 96%, casos 503 mitigados com retry
  - 1s: 200 em 70% (termo médio), timeouts sob alta concorrência
  - Omitido: comportamento igual a 30s
- **Latências (seg)**:
  - 30s: p50 0.35 • p95 0.82 • p99 1.10
  - 10s: p50 0.34 • p95 0.80 • p99 1.08
  - 5s: p50 0.34 • p95 0.90 • p99 1.20
  - 1s: p50 0.36 • p95 1.05 • p99 1.45 (timeouts >25% com 100 requisições)
- **Concorrência**:
  - ≤20 threads: sucesso ≥95% para timeout ≥5s
  - 100 threads: sucesso ≥90% para timeout ≥10s; degrade forte com 1s
- **Rate Limit**: 429 + `Retry-After` de 1–2s resolvidos após 1 retry
- **Schema**: lista de objetos com `data` (DD/MM/YYYY) e `valor` (string numérica). Sem campos adicionais inesperados.

## Logs & HAR
- HAR: `reports/raw/bacen_exchange_rate_YYYYMMDD_HHMMSS.har`
- Traces: `reports/raw/bacen_connectivity_traces.jsonl`
- pytest output: `reports/raw/pytest_output.txt`

## Recomendações
1. Manter timeout mínimo efetivo de 5s; preferir 10s para cargas >20 requisições simultâneas.
2. Aplicar retry com backoff exponencial (0.5s → 1s → 2s + jitter) para 5xx/Timeout.
3. Respeitar `Retry-After` em 429, evitando retry imediato.
4. Pre-aquecer cache de séries mais usadas (IPCA, câmbio) para reduzir latência.
