# Documentação de Uso das APIs Externas no Sistema

Este documento consolida como nosso sistema integra e utiliza fontes externas de dados (APIs e scraping) para clima, indicadores econômicos, 5G/telecom e dados operacionais brasileiros.

Caminhos-chave no repositório:

- **Configuração**: [backend/config/external_apis_config.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/config/external_apis_config.py:0:0-0:0)
- **Serviços**:
  - `backend/services/external_data_service.py`
  - `backend/services/expanded_api_integration.py`
- **Pipelines ETL**:
  - [backend/pipelines/climate_etl.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:0:0-0:0)
  - [backend/pipelines/economic_etl.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/economic_etl.py:0:0-0:0)
  - [backend/pipelines/anatel_5g_etl.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/anatel_5g_etl.py:0:0-0:0)
  - [backend/data/pipelines/etl_orchestrator.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/data/pipelines/etl_orchestrator.py:0:0-0:0) (orquestrador expandido)
- **Fetchers (dados brasileiros com requests/scraping)**: [src/pipeline/brazilian_apis.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:0:0-0:0)
- **Health checks**:
  - FastAPI: `backend/app/api/v1/routes/health.py`
  - Flask API: [backend/api/enhanced_api.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/api/enhanced_api.py:0:0-0:0)
- **Testes de conectividade**:
  - `backend/tests/test_external_services.py`
  - `backend/run_api_tests.py`

## Variáveis de Ambiente e Configuração

Arquivo: [backend/config/external_apis_config.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/config/external_apis_config.py:0:0-0:0)

- **INMET (Clima)**

  - `INMET_CONFIG.base_url`: `https://apitempo.inmet.gov.br/`
  - `INMET_CONFIG.station_code`: ex. `A001` (Salvador/BA)
  - `INMET_API_KEY` (se aplicável, vazio por padrão)
  - `timeout`, `retry_attempts`, `retry_delay`, `cache_duration`
- **BACEN (Econômico)**

  - `BACEN_CONFIG.base_url`: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.`
  - `BACEN_CONFIG.series_codes`: `ipca=433`, `selic=11`, `exchange_rate=1`, `gdp=4380`
  - `BACEN_API_KEY` (não exigido para SGS públicas, reservado)
  - `timeout`, `retry_attempts`, `retry_delay`, `cache_duration`
- **ANATEL (5G/Telecom)**

  - `ANATEL_CONFIG.base_url`: `https://www.gov.br/anatel/`
  - `ANATEL_CONFIG.data_endpoint`: `dadosabertos/`
  - `ANATEL_CONFIG.scraping_enabled`: `True` (fallback)
  - `ANATEL_API_KEY` (reservado)
  - `timeout`, `retry_attempts`, `retry_delay`, `cache_duration`
- **OpenWeatherMap (Clima alternativo)**

  - `OPENWEATHER_CONFIG.base_url`: `https://api.openweathermap.org/data/2.5/`
  - `OPENWEATHER_API_KEY`: obrigatório para uso
  - `city`: `Salvador,BR`
  - `timeout`, `retry_attempts`, `cache_duration`
- **Rate limiting**

  - `RATE_LIMIT_CONFIG`: `requests_per_minute=60`, `requests_per_hour=1000`, `enable_rate_limiting=True`
- **Calendário brasileiro**

  - `BRAZILIAN_CALENDAR_CONFIG`: `holiday_source='internal'`, `regions`, `update_frequency='yearly'`
- **Features externas previstas**

  - `EXTERNAL_FEATURES`: listas de `climate_features`, `economic_features`, `5g_features`

## Como o Sistema Consome Cada Fonte

### 1) INMET (Clima)

- **Implementação atual**:
  - ETL: [backend/pipelines/climate_etl.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:0:0-0:0) com métodos `extract/transform/load/run`.
  - [extract()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:17:4-26:17) é placeholder: faz log e retorna `DataFrame` vazio.
  - [transform()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:28:4-61:17) calcula flags/risco caso existam colunas como `temperatura_media`, `precipitacao_mm`, `umidade_percentual`.
  - [load()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:63:4-79:17) escreve em `ClimaSalvador` via `db_service.insert_dataframe(..., if_exists='replace')`.
- **Fetchers auxiliares**:
  - [src/pipeline/brazilian_apis.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:0:0-0:0) classe [INMETClimateDataFetcher](cci:2://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:162:0-259:12):
    - [fetch_daily_climate_data(start_date, end_date)](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:184:4-241:17): atualmente simula dados estruturados por estação (scraping real pendente). Estrutura com `date`, `temperature`, `precipitation`, `humidity`, e flags como `extreme_heat`.
- **Observação**: o endpoint público `apitempo.inmet.gov.br` está configurado, mas a chamada real está como “a implementar”. Uso de scraping do portal `https://portal.inmet.gov.br` está documentado como futuro.

### 2) BACEN (Indicadores Econômicos)

- **Implementação atual**:
  - ETL: [backend/pipelines/economic_etl.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/economic_etl.py:0:0-0:0) com `extract/transform/load`.
  - [extract()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:17:4-26:17) é placeholder.
  - [transform()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:28:4-61:17) deriva `is_high_inflation`, `volatilidade_cambio`, `is_currency_devaluation` se as colunas existirem.
  - [load()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:63:4-79:17) escreve em `IndicadoresEconomicos`.
- **Fetchers reais**:
  - [src/pipeline/brazilian_apis.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:0:0-0:0) classe [BACENEconomicDataFetcher](cci:2://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:31:0-159:67):
    - [fetch_exchange_rate_usd_brl(start_date, end_date)](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:41:4-109:74):
      - Endpoint: `GET https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?dataInicial=DD/MM/YYYY&dataFinal=DD/MM/YYYY&formato=json`
      - Faz paginação por janelas (até 365 dias), consolida e retorna `date`, `exchange_rate_brl_usd`.
    - [fetch_inflation_ipca(start_date, end_date)](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:111:4-159:67):
      - Endpoint: `GET https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?dataInicial=DD/MM/YYYY&dataFinal=DD/MM/YYYY&formato=json`
      - Retorna `date`, `inflation_rate`.
- **Observação**: chamadas reais a BACEN ocorrem nesses fetchers; a etapa de carga para as tabelas acontece pelos ETLs quando conectados.

### 3) ANATEL (5G / Telecom)

- **Implementação atual**:
  - ETL: [backend/pipelines/anatel_5g_etl.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/anatel_5g_etl.py:0:0-0:0):
    - [extract()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:17:4-26:17) placeholder.
    - [transform()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:28:4-61:17) calcula `is_5g_active`, `taxa_expansao_5g`, `is_5g_milestone` se `cobertura_5g_percentual` existir.
    - [load()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:63:4-79:17) escreve em `Expansao5G`.
- **Fetchers auxiliares**:
  - [src/pipeline/brazilian_apis.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:0:0-0:0) classe [AnatelRegulatoryDataFetcher](cci:2://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:262:0-364:12):
    - [fetch_mobile_subscriber_growth(region)](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:273:4-319:17): simulado; a implementação real prevista via scraping de relatórios Anatel.
    - [fetch_5g_coverage_by_city(city, state)](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:321:4-356:17): simulado; timeline de cobertura 5G.
- **Observação**: `ANATEL_CONFIG` prevê scraping (`scraping_enabled=True`). O portal de dados é `https://dadosabertos.anatel.gov.br`; o site institucional é `https://www.anatel.gov.br` e `https://www.gov.br/anatel/`.

### 4) OpenWeatherMap (Clima alternativo)

- **Implementação atual**:
  - Presentes apenas configuração e testes de conectividade.
  - `backend/run_api_tests.py` testa `GET /weather?appid=...&q=Salvador,BR` quando `OPENWEATHER_API_KEY` está configurada.
  - Não há ETL dedicado consumindo OpenWeather em produção no repositório.

### 5) IBGE (Econômico Regional)

- **Fetchers reais**:
  - [src/pipeline/brazilian_apis.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:0:0-0:0) classe [IBGEEconomicDataFetcher](cci:2://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:367:0-413:21):
    - [fetch_regional_gdp_growth(state_code, year)](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:386:4-413:21):
      - Endpoint: `GET https://servicodados.ibge.gov.br/api/v1/economia/pib/v2/{state_code}/{year}`
      - Retorna JSON com PIB regional.
- **Observação**: Integrado no orquestrador expandido via coletores, mas não conectado a um ETL simples como os três principais.

### 6) Operacional (Feriados e Eventos)

- [src/pipeline/brazilian_apis.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:0:0-0:0) classe [BrazilianOperationalDataFetcher](cci:2://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:416:0-480:20):
  - Usa `holidays` (se disponível) para feriados nacionais; fallback interno se não instalado.
  - [get_carnival_dates(year)](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:456:4-480:20): tabela estática de datas de carnaval.

### 7) Integração Expandida (25+ fontes)

- `backend/services/expanded_api_integration.py`: esqueleto com sessão `requests` + `Retry` para fontes como ANTT/DNIT (transporte).
- [backend/data/pipelines/etl_orchestrator.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/data/pipelines/etl_orchestrator.py:0:0-0:0): orquestra pipeline completo com:
  - Coletores: `backend/data/collectors/brazilian_apis_expanded.py` (não abrimos, mas referenciado).
  - Scrapers: `backend/data/collectors/web_scrapers.py` (referenciado).
  - Loader: `backend/data/loaders/load_expanded_metrics.py` (referenciado).
  - Feature engineering: `backend/data/feature_engineering/expand_features.py` (referenciado).
- Observação: estes módulos referenciados indicam arquitetura pronta para >25 fontes, com etapas de extract/transform/load e features, mas os detalhes estão distribuídos nesses arquivos (fora do escopo aberto aqui).

## Fluxos Internos (APIs HTTP do Sistema)

### FastAPI Health (checagem de clientes externos)

Arquivo: `backend/app/api/v1/routes/health.py`

- `GET /health`
  - Retorna `services.database` e `external_apis` com status de configuração:
    - `inmet`, `bacen`, `anatel`, `openweather` mostram `configured`/`not_configured` conforme variáveis em [external_apis_config.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/config/external_apis_config.py:0:0-0:0).
  - Exemplo:
    ```bash
    curl -s http://localhost:8000/health
    ```

### Flask Enhanced API

Arquivo: [backend/api/enhanced_api.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/api/enhanced_api.py:0:0-0:0)

- `GET /health`:
  - Verifica banco e status geral.
  - ```bash
    curl -s http://localhost:5000/health
    ```
- `POST /api/external-data/refresh`
  - Aciona ETLs `climate_etl`, `economic_etl`, `anatel_5g_etl`.
  - Body:
    ```json
    {
      "data_type": "all | climate | economic | 5g",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD"
    }
    ```
  - Exemplo:
    ```bash
    curl -X POST http://localhost:5000/api/external-data/refresh \
      -H "Content-Type: application/json" \
      -d '{"data_type":"all","start_date":"2025-10-01","end_date":"2025-10-31"}'
    ```
- Outros endpoints desta API são para features, modelos e pipelines completos (não diretamente sobre as APIs externas, mas consumirão dados carregados).

Observação: Este repo contém ambas as stacks (FastAPI e Flask). O ambiente de execução decide qual servir.

## Exemplos de Solicitações Diretas às Fontes Externas

- **BACEN (câmbio USD/BRL)**

  ```bash
  curl "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?dataInicial=01/09/2025&dataFinal=31/10/2025&formato=json"
  ```
- **BACEN (IPCA 12m)**

  ```bash
  curl "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?dataInicial=01/01/2024&dataFinal=31/12/2024&formato=json"
  ```
- **OpenWeatherMap (tempo atual em Salvador)**

  ```bash
  curl "https://api.openweathermap.org/data/2.5/weather?q=Salvador,BR&appid=$OPENWEATHER_API_KEY&units=metric"
  ```
- **ANATEL**

  - Portal institucional: `https://www.gov.br/anatel/`
  - Dados abertos: `https://dadosabertos.anatel.gov.br`
  - Os endpoints utilizados serão definidos quando o scraping estiver implementado; por ora, testes de conectividade verificam o site.

## Tratamento de Erros, Retries e Limites

- Retries:

  - `expanded_api_integration.py` usa `requests.Session` com `urllib3.Retry` (`total=3`, `backoff_factor=1`, `status_forcelist=[429,500,502,503,504]`).
  - Testes `backend/tests/test_external_services.py` possuem lógica de retry manual para INMET, BACEN, ANATEL.
- Timeouts:

  - Definidos em [external_apis_config.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/config/external_apis_config.py:0:0-0:0) por fonte (30–60s) e aplicados nos testes/scripts.
- Rate limiting:

  - `RATE_LIMIT_CONFIG` define limites e habilitação. A aplicação de throttling por requisição em runtime não está explícita no código dos ETLs “simples”; a camada expandida e/ou os coletores devem respeitar estes valores.
- Health checks:

  - FastAPI `GET /health` e Flask `GET /health` indicam status e configuração de clientes.
- Cache:

  - Parâmetros `cache_duration` em config; não há camada de cache implementada visível nos ETLs simples, mas prevista na arquitetura.

## Tabelas de Destino e Features Derivadas

- Clima (INMET)

  - Tabela: `ClimaSalvador`
  - Features (potenciais, se as colunas existirem na entrada):
    - `is_extreme_heat`
    - `is_cold_weather`
    - `is_heavy_rain`
    - `is_intense_rain`
    - `is_no_rain`
    - `is_high_humidity`
    - `corrosion_risk`
    - `field_work_disruption`
- Econômico (BACEN)

  - Tabela: `IndicadoresEconomicos`
  - Features:
    - `is_high_inflation`
    - `volatilidade_cambio`
    - `is_currency_devaluation`
- 5G (ANATEL)

  - Tabela: `Expansao5G`
  - Features:
    - `is_5g_active`
    - `taxa_expansao_5g`
    - `is_5g_milestone`
- Conjunto expandido:

  - `EXTERNAL_FEATURES` em config define listas-alvo para clima, economia, 5G a serem enriquecidas na engenharia de atributos.

## Como Executar Testes de Conectividade

- Script: `backend/run_api_tests.py`
  - Executa checagens para ANATEL e, se configurado, OpenWeather, além de BACEN/INMET.
  - Exemplo:
    ```bash
    python backend/run_api_tests.py
    ```
- Pytests: `backend/tests/test_external_services.py`
  - Marcas: `@pytest.mark.integration`, `@pytest.mark.network`.
  - Exemplo:
    ```bash
    pytest -k external_services -m "integration and network" -q
    ```

## Boas Práticas e Observações de Uso

- Configure `.env`/variáveis de ambiente para chaves:
  - `OPENWEATHER_API_KEY`
  - `INMET_API_KEY`, `BACEN_API_KEY`, `ANATEL_API_KEY` (opcionais/preservados)
- Em produção:
  - Completar implementações [extract()](cci:1://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/backend/pipelines/climate_etl.py:17:4-26:17) para INMET/BACEN/ANATEL ETLs com chamadas reais ou scraping.
  - Conectar os fetchers de [src/pipeline/brazilian_apis.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:0:0-0:0) aos ETLs ou ao orquestrador expandido.
  - Implementar cache/controle de taxa quando necessário.
- Uso local:
  - Para obter dados reais já prontos, utilize os métodos das classes em [src/pipeline/brazilian_apis.py](cci:7://file:///c:/Users/Aluno/CascadeProjects/2048/gran-prix/src/pipeline/brazilian_apis.py:0:0-0:0) (BACEN e IBGE já estão implementados).
  - Para popular as tabelas, acione `POST /api/external-data/refresh` (lembrando que os extract atuais retornam vazio; integre os fetchers antes).

# Resumo

- Documentei as configurações, variáveis de ambiente, endpoints externos e a forma como cada API é usada pelos serviços/ETLs internos.
- Esclareci o status atual: BACEN e IBGE com fetchers reais; INMET/ANATEL com placeholders/simulações; OpenWeather apenas em testes.
- Incluí exemplos de chamadas internas e externas, tratamento de erros/retries, e tabelas/features de destino.
