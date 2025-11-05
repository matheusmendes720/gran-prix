# Setup de Ambiente Isolado para Testes de APIs

Este diretório contém instruções e scripts necessários para executar a bateria de testes focada na variável `timeout`.

## 1. Criar e ativar ambiente virtual

### Windows (PowerShell)
```powershell
powershell -ExecutionPolicy Bypass -File setup/create_venv.ps1
```

### Linux/macOS
```bash
bash setup/create_venv.sh
```

Após a criação, ative o ambiente:
- Windows: `./.venv/Scripts/Activate.ps1`
- Linux/macOS: `source .venv/bin/activate`

## 2. Instalar dependências mínimas

```bash
pip install -r setup/requirements.txt
```

O arquivo inclui `pytest`, `requests`, `httpx`, `pytest-asyncio`, `pytest-xdist`, `pytest-html`, `locust`, `k6` (via instrução manual) e utilitários para Toxiproxy/mitmproxy.

### Dependências opcionais
- `k6`: instale via [https://k6.io/docs/getting-started/installation/](https://k6.io/docs/getting-started/installation/)
- `mitmproxy`: `pip install mitmproxy`
- `toxiproxy`: consulte [https://github.com/Shopify/toxiproxy](https://github.com/Shopify/toxiproxy)

## 3. Variáveis de ambiente

Copie `.env.example` para `.env` e ajuste conforme necessário.

Variáveis principais:
- `RUN_LIVE=1` para habilitar testes de integração real.
- `OPENWEATHER_API_KEY` e `OPENWEATHER_CITY` se quiser testar OpenWeather.
- `BACEN_TIMEOUT_OVERRIDE`, `INMET_TIMEOUT_OVERRIDE`, etc., para testar ajustes específicos.

Carregue-as:
```bash
set -a && source .env && set +a  # Linux/macOS
# Windows PowerShell
Get-Content .env | ForEach-Object {
  if (-not [string]::IsNullOrWhiteSpace($_) -and -not $_.StartsWith('#')) {
    $name, $value = $_.Split('=', 2)
    Set-Item -Path Env:$name -Value $value
  }
}
```

## 4. Executar testes

```bash
cd tests_api_isolation/timeout
pytest -q --maxfail=1 --durations=5
```

Para executar apenas um subconjunto:
```bash
pytest cases/test_bacen_timeout_connectivity.py -k "default_30" -vv
```

### Execução automatizada (pytest + k6 + locust)

```bash
python tools/run_suite.py           # roda pytest e tenta k6/locust se disponíveis
python tools/run_suite.py pytest    # apenas pytest
python tools/run_suite.py k6 locust # apenas ferramentas de carga
```

O script gera resumos estruturados em `reports/raw/run_suite_summary_*.json` e logs individuais (`pytest_output.txt`, `k6_output.txt`, `locust_output.txt`). Quando `k6` ou `locust` não forem encontrados no `PATH`, o utilitário marca o passo como "skipped" sem interromper a execução geral.

## 5. Scripts de carga

- `k6 run tools/k6/bacen_timeout_smoke.js`
- `locust -f tools/locust/locustfile.py --headless -u 20 -r 5 -t 1m`

## 6. Ferramentas de rede

- `tools/toxiproxy/start_toxiproxy.sh` ou `.ps1` para iniciar proxies com latência/perda.
- `setup/mock_servers/mitmproxy_addons.py` para capturar HAR (executar com `mitmproxy -s mitmproxy_addons.py`).

## 7. Relatórios

- Resultados brutos (HAR, logs, traces) são gravados em `reports/raw/`.
- Relatórios resumidos por endpoint ficam em `reports/summary/`.
- `reports/summary/final_recommendation.md` contém a recomendação consolidada.

## 8. Limpeza

Para remover o ambiente:
```bash
rm -rf .venv
```
Ou ajustado para Windows:
```powershell
Remove-Item -Recurse -Force .venv
```
