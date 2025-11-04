# Live Execution Runbook — Timeout Isolation Suite

## Finalidade
Orientar execuções com `RUN_LIVE=1`, garantindo coleta segura de métricas reais (latência, HAR, logs) nos serviços externos: INMET, BACEN, ANATEL, OpenWeather, IBGE e health interno.

## Pré-execução
1. **Provisionar credenciais**
   - `OPENWEATHER_API_KEY`
   - Outras chaves específicas (caso novos endpoints sejam adicionados).
2. **Variáveis de ambiente**
   - `RUN_LIVE=1`
   - `TIMEOUT_OVERRIDES_JSON` (opcional) para testar combinações específicas.
3. **Ferramentas auxiliares**
   - `toxiproxy` (latência/perda simulada) configurada com `setup/mock_servers/toxiproxy.json`.
   - `mitmproxy` com addon `setup/mock_servers/mitmproxy_addons.py` para capturar HAR automaticamente.
4. **Rede**
   - Garantir acesso externo aos endpoints.
   - Configurar proxies corporativos, caso necessário.

## Passo a passo
1. Preparar ambiente
   ```bash
   cd tests_api_isolation/timeout
   python -m venv .venv
   source .venv/bin/activate  # ou .\.venv\Scripts\Activate.ps1
   pip install -r setup/requirements.txt
   cp setup/.env.example .env  # edite as chaves antes de prosseguir
   ```
2. Ativar ferramentas de rede (opcional)
   - Toxiproxy:
     ```bash
     tools/toxiproxy/start_toxiproxy.sh &
     ```
   - Mitmproxy:
     ```bash
     mitmdump -s setup/mock_servers/mitmproxy_addons.py --listen-host 0.0.0.0 --listen-port 8080
     ```
3. Executar suíte
   ```bash
   python tools/run_suite.py --pytest --k6 --locust --mitmproxy=http://127.0.0.1:8080
   ```
   - O script detecta binários ausentes e registra `skipped` ao invés de falhar.
   - Saídas:
     - `reports/raw/pytest_output.txt`
     - `reports/raw/k6_output.txt`
     - `reports/raw/locust_output.txt`
     - `reports/raw/run_suite_summary_<timestamp>.json`
     - HAR em `reports/raw/*.har`
4. Validar resultados
   - Conferir percentis de latência em `k6_summary.json` (quando disponível).
   - Garantir que `locust_stats.csv` contenha taxa de sucesso ≥ 95% nos timeouts >= 5s.
   - Revisar HAR para headers de rate limit e erros HTTP.

## Tratamento de falhas
- **Timeouts frequentes**: elevar `timeout` no `.env` ou revisar a recomendação em `reports/summary/final_recommendation.md`.
- **Erros 429**: validar se `Retry-After` está sendo respeitado; ajustar `rate_limit` nos testes.
- **Falhas de autenticação**: verificar chaves em `.env` e logs do mitmproxy para detectar headers ausentes.

## Pós-execução
1. Desativar toxiproxy/mitmproxy.
2. Versionar novos relatórios em `reports/summary/` e atualizar changelog usando o template (Contexto/Evidências/Recomendações).
3. Registrar métricas relevantes em dashboards ou anexar aos tickets em andamento.

## Checklist rápido
- [ ] `.env` atualizado com credenciais válidas.
- [ ] `RUN_LIVE=1` definido.
- [ ] Toxiproxy/mitmproxy iniciados (se necessários).
- [ ] `python tools/run_suite.py` executado sem falhas críticas.
- [ ] Logs e HAR revisados.
- [ ] Changelog atualizado com métricas reais e referências @arquivo#linhas.
