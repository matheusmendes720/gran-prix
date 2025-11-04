# CI Pipeline Plan for Timeout Isolation Suite

## Objetivo
Garantir que a bateria de testes `tests_api_isolation/timeout` execute automaticamente a cada alteração relevante, produzindo artefatos de diagnóstico (pytest, k6, locust e HAR) e sinalizando falhas de timeout antes que mudanças cheguem à produção.

## Escopo dos jobs
- **pytest** (obrigatório): roda sempre, mesmo quando k6/locust estiverem ausentes.
- **k6 smoke** (opcional, mas recomendado): executa somente se o binário estiver disponível no runner.
- **locust smoke headless** (opcional): valida concorrência mínima em 1 minuto.
- **Uploads de artefatos**: `tests_api_isolation/timeout/reports/raw/` e `tests_api_isolation/timeout/reports/summary/`.

## Pré-requisitos do runner
- Python 3.10+ com `pip`.
- Node/npm para instalar `k6` via pacote ZIP ou binário portátil.
- PowerShell (Windows) ou Bash (Linux) para scripts auxiliares (`create_venv.*`).
- Variáveis de ambiente seguras (se execução live for habilitada):
  - `RUN_LIVE=1`
  - `OPENWEATHER_API_KEY=<secret>`

## Fluxo sugerido (GitHub Actions)
```yaml
name: timeout-isolation-suite

on:
  push:
    paths:
      - 'tests_api_isolation/timeout/**'
      - 'backend/config/external_apis_config.py'
      - 'src/pipeline/brazilian_apis.py'
  pull_request:
    paths:
      - 'tests_api_isolation/timeout/**'

jobs:
  timeout-suite:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install --upgrade pip
          pip install -r tests_api_isolation/timeout/setup/requirements.txt
      - name: Install k6 (portable)
        run: |
          curl -L https://github.com/grafana/k6/releases/download/v0.49.0/k6-v0.49.0-linux-amd64.tar.gz -o k6.tar.gz
          tar -xzf k6.tar.gz
          echo "$(pwd)/k6-v0.49.0-linux-amd64" >> $GITHUB_PATH
      - name: Execute suite orchestrator
        env:
          RUN_LIVE: ${{ secrets.RUN_LIVE }}
          OPENWEATHER_API_KEY: ${{ secrets.OPENWEATHER_API_KEY }}
        run: |
          source .venv/bin/activate
          python tests_api_isolation/timeout/tools/run_suite.py --ci-mode
      - name: Publish artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: timeout-suite-reports
          path: |
            tests_api_isolation/timeout/reports/raw/**
            tests_api_isolation/timeout/reports/summary/**
```

## Critérios de falha
- Qualquer falha no `pytest` ou `run_suite` retorna código ≠ 0.
- Falta de binários k6/locust não deve falhar o job: o `--ci-mode` registra status `skipped`, mas mantém saída do comando.
- Caso `RUN_LIVE=1` e faltarem secrets, o job deve acusar falha explícita (idealmente via validação inicial no pipeline).

## Monitoramento do pipeline
- Habilitar branch protection para exigir aprovação do job antes do merge.
- Configurar alertas (Slack/Teams) quando o pipeline falhar.
- Armazenar artefatos por pelo menos 7 dias para auditoria de regressões.

## Próximas ações
1. Criar secrets `RUN_LIVE` e `OPENWEATHER_API_KEY` no repositório, se necessário.
2. Ajustar comandos de instalação para runners Windows se a infraestrutura utilizar Self-Hosted.
3. Validar execução manual em branch feature antes de habilitar proteção obrigatória.
