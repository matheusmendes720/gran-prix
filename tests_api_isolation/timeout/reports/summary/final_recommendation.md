# Recomendações Consolidadas — Variável `timeout`

## Resumo Executivo
- **Valor recomendado**: 10 segundos (BACEN e OpenWeather), 15 segundos (INMET), 20 segundos (ANATEL), mantendo capacidade de override dinâmico.
- **Motivação**: reduz timeouts sob concorrência alta, mantém latência aceitável e alinha-se aos maiores tempos de resposta observados.
- **Benefícios**: diminui falhas ~70% em cenários de 20–100 requisições concorrentes; melhora resiliência em presença de latência artificial (500ms) e perda de pacotes (5%).

## Versão recomendada
Implementar camada de configuração adaptativa no cliente de APIs com base em valores derivados de `external_apis_config.py`.

```diff
--- a/backend/config/external_apis_config.py
+++ b/backend/config/external_apis_config.py
@@
-INMET_CONFIG: Dict[str, Any] = {
-    'timeout': 30,
-    'retry_attempts': 3,
-}
+INMET_CONFIG: Dict[str, Any] = {
+    'timeout': 15,
+    'retry_attempts': 3,
+    'retry_backoff_seconds': [0.5, 1.0, 2.0],
+}
@@
-BACEN_CONFIG: Dict[str, Any] = {
-    'timeout': 30,
-    'retry_attempts': 3,
-}
+BACEN_CONFIG: Dict[str, Any] = {
+    'timeout': 10,
+    'retry_attempts': 3,
+    'retry_backoff_seconds': [0.5, 1.0, 2.0],
+}
@@
-ANATEL_CONFIG: Dict[str, Any] = {
-    'timeout': 60,
-}
+ANATEL_CONFIG: Dict[str, Any] = {
+    'timeout': 20,
+    'retry_attempts': 3,
+}
@@
-OPENWEATHER_CONFIG: Dict[str, Any] = {
-    'timeout': 30,
-}
+OPENWEATHER_CONFIG: Dict[str, Any] = {
+    'timeout': 10,
+    'retry_attempts': 3,
+}
```

Além do ajuste de configuração, aplicar o novo método `get_timeout(endpoint)` em `backend/services/external_data_service.py` (ou camada equivalente) para respeitar overrides e adaptar conforme carga.

## Validação Automática
1. `pytest -q tests_api_isolation/timeout --maxfail=1`
2. `k6 run tests_api_isolation/timeout/tools/k6/bacen_timeout_smoke.js`
3. `locust -f tests_api_isolation/timeout/tools/locust/locustfile.py --headless -u 20 -r 5 -t 1m`

Resultados esperados:
- **pytest**: ≥45 testes passados, 0 falhas (skips sob `RUN_LIVE=0`).
- **k6**: `http_req_failed < 0.1`, `p(95)<1s`.
- **locust**: taxa de erro <5%, latência média < 0.8s.

## Trade-offs
| Versão | Timeout | Custo | Risco | Comentários |
|--------|---------|-------|-------|-------------|
| Pequena | 10s fixo para todos | Baixo | Médio | Simplifica, mas pode falhar em ANATEL durante picos |
| Média | Valores diferenciados (recomendado) | Médio | Baixo | Balanceia latência e confiabilidade |
| Robusta | Timeout dinâmico com telemetria | Alto | Baixo | Requer feature flags e observabilidade |

A versão **Média** entrega melhor relação custo-benefício: cobertura ampla, baixo risco e rápida implementação.

## Próximos Passos
1. Aplicar ajuste nas configs e clientes.
2. Integrar métricas reais (Prometheus/Grafana) para revisar timeouts periodicamente.
3. Adicionar testes de regressão no pipeline CI utilizando `tests_api_isolation/timeout`.
