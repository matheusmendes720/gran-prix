# Nova Corrente External Data Download Playbook

## 1. Objetivo Geral

- Garantir que **todas as 37+ variáveis externas** mapeadas nos arquivos `external_src.md`, `outer_factors.md`, `extern_modelling.md` estejam cobertas por um plano de coleta consistente.
- Distinguir claramente **o que pode ser 100% automatizado por código** versus **o que exige interação manual (login, captcha, download único, aceite de termos)**.
- Conectar cada fonte ao **pipeline ML descrito em `docs/reports/NOVA_CORRENTE_ML_PIPELINE_TECH_SPEC.md`**, definindo localização Bronze → Silver → Feature Store.

> **Formato:** cada subseção traz (i) _variáveis-alvo_, (ii) _links primários_, (iii) _rota de automação_, (iv) _passos manuais inevitáveis_, (v) _próximas ações no pipeline_.

---

## 2. Macro & Fiscal (PIB, IPCA, juros, câmbio, tributos)

| Variável | Fonte Principal | Automação por Código | Etapas Manuais | Próximas Ações Pipeline |
| --- | --- | --- | --- | --- |
| PIB trimestral/anual | `https://apisidra.ibge.gov.br/values/t/5932/...` | `scripts/etl/external/ibge_downloader.py --tables pib_quarterly pib_annual` | Nenhuma | Salvar em `data/landing/external_factors-raw/macro/ibge/`; normalizar datetimes |
| IPCA / IPCA-15 | `https://apisidra.ibge.gov.br/values/t/1737/...` | `ibge_downloader.py --tables ipca ipca15` (usa `c315/7169` p/ índice geral) | Nenhuma | Calcular features `ipca_12m`, `ipca_mom`, `ipca15_mom`; armazenar em Silver |
| INPC | `https://apisidra.ibge.gov.br/values/t/1736/...` | `ibge_downloader.py --tables inpc` | Nenhuma | Feature `inpc_mom`; comparar com IPCA |
| Taxa de desocupação PNAD Contínua | `https://apisidra.ibge.gov.br/values/t/6381/...` | `ibge_downloader.py --tables unemployment` | Nenhuma | Feature `unemployment_rate`; acionar heurísticas de demanda sensíveis ao emprego |
| CDS / PPP fallback | `https://api.stlouisfed.org/fred/series/observations?series_id=DDSI06BRA156NWDB` | `scripts/etl/external/fred_downloader.py --series cds ppp` (requer `FRED_API_KEY`) | Configurar API key (`set FRED_API_KEY=...`) | Silver `macro/cds_spread.parquet`, `macro/ppp_conversion_factor.parquet`; features `cds_spread_bps`, `ppp_conversion_factor_yoy` |
| Selic | `https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados` | `scripts/etl/external/bacen_downloader.py --start 2015-01-01` | Nenhuma | Criar tabela `macro_interest_rates` no Lakehouse |
| Câmbio USD/BRL, CNY/BRL, EUR/BRL | `https://olinda.bcb.gov.br/olinda/servico/PTAX/...` | `bacen_downloader.py --currencies USD EUR CNY` | Nenhuma | Feature `usd_brl_volatility_30d` em Feature Store |
| CDS / PPP | TradingEconomics, IMF (`https://api.tradingeconomics.com/series/CDS:BRA...`) | Requer chave TE; implementar `requests` com token em `.env` | Obter key (manual) | Armazenar segredo em Vault; criar job Airflow quinzenal |
| ICMS (BA/estados) | Portais SEFAZ/CONFAZ (PDF) | Crawler `requests + pdfplumber` para resoluções publicadas | Atualizar mapeamento manual quando layout muda | Extrair tabela `icms_effective_rate`, versionar em `data/manual/` |
| IPI / PIS/COFINS / ISS | Receita Federal, legislações | Web scraping + diffs usando `BeautifulSoup` | Conferir atualizações extraordinárias | Registrar em `tax_regimes_delta.parquet` (Bronze) |

**Checklist Automação:**

1. Clonar funções `fetch_json`/`fetch_csv` (vide snippet sugerido pelo assistente).
2. Parametrizar `date_start`, `date_end` via `config/data_sources.yaml`.
3. Scheduler: Airflow DAG `macro_collect_dag` rodando às 05h BRT.

---

## 3. Comércio Exterior & Tarifas (AliceWeb, COMEX, Drawback)

| Variável | Fonte | Automação | Manual | Pipeline |
| --- | --- | --- | --- | --- |
| Importações NCM (telecom) | `https://aliceweb2.mdic.gov.br/` | `requests.Session` replicando POST (precisa autenticação) | Criar/renovar credencial, resolver captcha inicial | Dump mensal (`data/raw/trade/aliceweb/YYYYMM.csv`) |
| UN Comtrade (backup) | `https://comtradeapi.un.org/public/v1/...` | API REST (limit 100 req/h) | Obter token gratuita | Harmonizar HS→NCM, armazenar em Silver |
| MERCOSUR LETEC / Drawback | `https://www.mercosur.int/` (PDF/CSV) | Scraper HTML → PDF parsing | Validar manualmente novas portarias | Criar tabela `mercosur_tariff_events` (event SCD) |
| Portos (Santos) & congestionamentos | Relatórios S&P Global / UNCTAD | Sem API aberta → scraping PDF + `tabula` | Download manual mensal | Feature `port_congestion_score` calculada via notebook |

**Ações:**

- Criar script `scripts/etl/trade/aliceweb_downloader.py` com login + export CSV (utilizar payload registrado via DevTools).
- Armazenar credenciais no Keyring/Secrets Manager.
- Configurar tarefa manual (DataOps) 1x por mês para validar relatórios físicos (portos).

---

## 4. Telecom & Regulatório (ANATEL, 5G, inspeções)

| Variável | Fonte | Automação | Manual | Pipeline |
| --- | --- | --- | --- | --- |
| Cobertura 5G / 4G | `https://informacoes.anatel.gov.br/paineis/` (CSV download) | Selenium Headless para clicar em "Exportar" ou API `paineis/api` | Ajustar filtros manualmente na primeira vez | Bronze `telecom/coverage/`; agregação por UF/município |
| Estatísticas históricas | `ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/` | `wget -r` agendado (script shell) | Monitorar mudanças em estrutura de pasta | Normalizar para Parquet Silver |
| Resoluções / inspeções | Portal legislação ANATEL | `BeautifulSoup` + diffs | Revisão jurídica (manual) | Feed `regulatory_events` consumido pelo modelo |
| Tor Upgrades / licitações | Releases ANATEL / SBA / Teleco | RSS/news scraping | Curadoria manual | Inserir no canal `events_telecom` via Obsidian note ou DB |

**Passos imediatos:**

1. Adicionar job `wget_anatel_stats.bat` (Windows Task Scheduler).
2. Criar script Python `anatel_paineis_export.py` (usa `selenium-wire` para baixar CSV).
3. Versionar resoluções em `docs/data/regulatory/resolution_YYYYMMDD.pdf`.

---

## 5. Clima & Ambiente (INMET, CEMADEN, Open-Meteo)

| Variável | Fonte | Automação | Manual | Pipeline |
| --- | --- | --- | --- | --- |
| Temperatura/chuva Nordeste | INMET BDMEP (`https://bdmep.inmet.gov.br/`) | `requests` com token + CSV | Criar conta gratuita | Bronze `weather/inmet/station_code` |
| Histórico + forecast (multi-cidades) | OpenWeather (Geocoding, One Call, Forecast) | `scripts/etl/external/openweather_ingest.py` (`config/openweather_cities.json`) | Nenhuma (usar `OPENWEATHER_API_KEY`) | Bronze `weather/openweather/<cidade>/YYYYMMDD/*.json`; gerar `rainfall_7d_sum`, `heatwave_flag` |
| Alertas extremos | INMET API tempo real (`http://apiprevmet3.inmet.gov.br/`) | `requests` token | Renovar token anual | Enviar streaming para Kafka (alerta SLA) |
| Dados satélite backup | Open-Meteo (`https://archive-api.open-meteo.com/v1/archive`) | GET com `latitude`, `longitude` | Nenhuma | Feature `rainfall_accumulated_7d` fallback |
| CEMADEN eventos | `https://www.cemaden.gov.br/dados-download/` | Sem API; scraping | Download manual trimestral | Integrar a `events_disasters` |

**Automação:**

- Criar tabela de estações (Salvador, Nordeste) em `config/weather_stations.csv`.
- Função Airflow `download_inmet_station(station_id, start_date, end_date)`.

---

## 6. Logística & Energia (Frete, combustível, portos, energia)

| Variável | Fonte | Automação | Manual | Pipeline |
| --- | --- | --- | --- | --- |
| World Container Index | Drewry | API paga; script se credencial | Solicitar trial/manual CSV | Bronze `logistics/freight/drewry` |
| Freightos FBX | `https://fbx.freightos.com/data/TrendLine` | API key + `requests` | Criar conta | Feature `container_rate_usd_40ft` |
| Baltic Dry Index | TradingEconomics | `requests` com key | Obter key | Bronze `logistics/bdi` |
| Diesel/Gasolina | ANP dataset (`https://dados.gov.br/...`) | `requests` CSV | Nenhuma | Silver `fuel_prices` (rolling mean) |
| Indicadores ANTT (Sascar, RNTRC, OTIF) | <https://dados.antt.gov.br> | `scripts/etl/manual/antt_ingest.py` (normaliza CSV/XLSX manual) | Exportar planilhas mensalmente | Silver `logistics/antt_metrics`, features `antt_*`, `antt_logistics_stress_index`, `diesel_vs_antt_stress` |
| Energia elétrica | IBGE IPCA energia / ANEEL | `apisidra` + scraping bandeira tarifária | Manual download bandeira se ANEEL retirar API | Feature `electricity_cost_ratio` |

---

## 7. Global Benchmarks & Exógenos Avançados

| Variável | Fonte | Automação | Manual | Pipeline |
| --- | --- | --- | --- | --- |
| GDP mundial / PPP | World Bank API | `scripts/etl/external/worldbank_downloader.py` | Nenhuma | Silver `global_benchmarks` |
| GSCPI | Federal Reserve (`https://api.newyorkfed.org/gscpi/v1/data`) | `requests` | Nenhuma | Feature `gscpi_zscore` |
| Semiconductor PPI | BLS (`https://download.bls.gov/...`) | `ftplib` + parse `.series` | Nenhuma | Bronze `semiconductor_ppi` |
| Port congestion score (proxy) | UNCTAD Pdf | `tabula` | Checar layout manual | Feature `port_congestion_score` com rule |

---

## 8. Micro-Operacional (dados internos + calendário)

- **Automação**: Extrair de ERP/CMMS via scripts existentes (`scripts/analysis/run_nova_corrente_exploratory.py`).  
- **Holidays**: API pública `https://date.nager.at/api/v3/PublicHolidays/2025/BR`.  
- **Greves/Eventos**: News API (`https://newsapi.org/`). Necessário API key.  
- **Passos Manual**: Atualizar feriados estaduais/municipais específicos (ex: Salvador 24/06) via planilha `docs/proj/dadosSuprimentos.xlsx`.

---

### 9. Pipeline ML – Próximas Ações Integradas

1. **Definir storage layout**
   - Bronze: `data/raw/<tier>/<source>/<YYYYMMDD>.{json,csv}`
   - Silver: tabelas normalizadas no Lakehouse (Delta/Parquet).
   - Feature Store: nomes padronizados (`usd_brl_volatility_30d`, `port_congestion_score` etc.).
2. **Agendamento**
   - Criar DAGs no Airflow (ex.: `dag_macro_collect`, `dag_trade_collect`, `dag_weather_collect`).
   - Habilitar `airflow/dags/nova_corrente_external_etl.py` para rodar `openweather_ingest.py`, `bacen_downloader.py`, `ibge_downloader.py` e `worldbank_downloader.py`.
   - Jobs manuais (AliceWeb, Drewry) → registrar em `docs/operations/manual_downloads.md`.
3. **Qualidade & Versionamento**
   - Implementar validações (schema drift, valores ausentes).
   - Registrar checksum dos arquivos manuais.
4. **Integração com `batch_downloader.py`**
   - Expandir classes para cada fonte, reutilizando snippet de `fetch_json/fetch_csv`.
   - Inserir logging estruturado + retries (exponential backoff).
5. **Entrega ao pipeline ML**
   - Atualizar `NOVA_CORRENTE_ML_PIPELINE_TECH_SPEC.md` com referências a este playbook.
   - Assegurar ingestão incremental (watermark por data de referência).

---

### 10. Próximos Passos Imediatos (Sequência Sugerida)

1. **Configurar `.env`** com API keys (OpenWeather, TradingEconomics, Freightos, NewsAPI).
2. **Executar scripts automatizados** (`fetch_all.py`, `openweather_ingest.py`, `bacen_downloader.py`, `ibge_downloader.py`, `worldbank_downloader.py`) para gerar primeira versão Bronze.
3. **Agendar downloads FTP (ANATEL, IBGE indices)** via `wget -r` no Task Scheduler.
4. **Validar manualmente** AliceWeb e Drewry, arquivar CSV em `docs/data/manual/2025`.
5. **Documentar exceções** em `docs/operations/manual_downloads.md` (criar se não existir).
6. **Atualizar Feature Store** com novas colunas uma vez que Silver esteja populado.
7. **Criar dashboards de monitoramento** (Grafana/Metabase) para tempo de atualização de cada fonte.
8. **Testar DAG** `nova_corrente_external_etl` com `airflow dags test nova_corrente_external_etl <data>` e depois ativar execução diária.

---

### 11. Referências Hemodinâmicas (links úteis)

- `docs/proj/scafold/extern_modeling/external_src.md` – pesquisa macro completa  
- `docs/proj/scafold/extern_modeling/outer_factors.md` – heurísticas fiscais / tax reform  
- `docs/proj/scafold/extern_modeling/extern_modelling.md` – modelos ML e causal chains  
- `docs/proj/scafold/extern_modeling/links-verificados-expandidos-100-cobertura.md` – status de cada link  
- Scripts utilitários: `scripts/etl/external/*.py`

---

### 12. Proprietários & Rotina

- **Data Engineering**: automações BACEN/IBGE/INMET/ANATEL, manutenção Airflow.
- **Data Ops**: downloads manuais (AliceWeb, Drewry, portos), atualização de credenciais.
- **Analytics/ML**: validação das features derivadas, monitoramento de drift.
- **Compliance**: revisão de legislação (ISS, ICMS, draw-back) trimestral.

> Qualquer nova fonte identificada deve ser adicionada a este arquivo, com status `Automatizável? (Sim/Não)` e data da última atualização.
