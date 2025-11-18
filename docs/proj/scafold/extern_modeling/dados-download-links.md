# 🔗 DADOS ECONÔMICOS, FISCAIS E OPERACIONAIS — LINKS DIRETOS PARA DOWNLOAD

## 📊 MACRO-ECONÔMICO E MONETÁRIO

### IBGE (Instituto Brasileiro de Geografia e Estatística)
- **Portal SIDRA (Banco de Dados)**: https://sidra.ibge.gov.br/
  - **PIB Trimestral**: https://sidra.ibge.gov.br/acervo#/q/Q12462C
  - **PIB Anual**: https://sidra.ibge.gov.br/acervo#/q/Q5932C
  - **IPCA Mensal**: https://sidra.ibge.gov.br/acervo#/q/Q1737C (Tabela 1737)
  - **IPCA-15**: https://sidra.ibge.gov.br/acervo#/q/Q1705C (Tabela 1705)
  - **INPC**: https://sidra.ibge.gov.br/acervo#/q/Q1736C (Tabela 1736)
  - **IGP-M (FGV link)**: https://portal.fgv.br/noticias/igp-m
  - **Taxa Desocupação**: https://sidra.ibge.gov.br/acervo#/q/Q6385C
  - **População Estimada**: https://sidra.ibge.gov.br/acervo#/q/Q29168C

- **API REST IBGE (Dados em JSON)**:
  - Base: `https://servicodados.ibge.gov.br/api/v3/`
  - Exemplos completos: https://servicodados.ibge.gov.br/api/docs/

- **Download em CSV/Excel direto**:
  - https://ftp.ibge.gov.br/Indices_de_Precos_ao_Consumidor/IPCA/

### BACEN (Banco Central do Brasil)
- **OpenDataBCB Portal**: https://opendata.bcb.gov.br/
  - **Câmbio PTAX (Diário)**: https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/
  - **Taxa Selic**: https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados
  - **Decisões COPOM**: https://www.bcb.gov.br/controleinflacao/historicotaxasjuros
  - **Série histórica completa Selic**: https://www.bcb.gov.br/controleinflacao/taxaselic

- **API BACEN (JSON)**:
  - Câmbio: `https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinal=@dataFinal)?@dataInicial='MM-DD-YYYY'&@dataFinal='MM-DD-YYYY'&$top=10000&$orderby=dataHora%20asc&$format=json`
  - Selic Histórico: https://www.bcb.gov.br/api/dados/serie/bcdata.sgs.432

- **Download Série Histórica**:
  - https://www.bcb.gov.br/controleinflacao/historicotaxasjuros (Excel/PDF)

### IGP-M (Fundação Getulio Vargas)
- **Portal FGV**: https://portal.fgv.br/noticias/igp-m
- **Série Histórica**: https://portal.fgv.br/artigos/indice-geral-de-precos
- **Download direto**: https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx

---

## 💰 FISCAL E TRIBUTÁRIO

### Receita Federal do Brasil
- **Portal e-CAC**: https://www.receita.gov.br/
  - **Instrução Normativa IN 1700/2017 (PIS/COFINS)**: https://www.receita.gov.br/legislacao/ato-normativo/instrucao-normativa/2017/in-1700
  - **Tabelas ICMS por Estado**: https://www.receita.gov.br/tributos/impostos/icms
  - **Siscomex - Regime de Drawback**: https://portal.siscomex.gov.br/
  - **Defesa Comercial**: https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial

### CONFAZ (Conselho Nacional de Política Fazendária)
- **Convênios e Protocolos ICMS**: https://www1.confaz.fazenda.gov.br/confaz/public/
  - **Consulta por UF**: https://www1.confaz.fazenda.gov.br/confaz/public/cf
  - **Legislação ICMS Completa**: https://www1.confaz.fazenda.gov.br/confaz/public/cf/lei

### SEFAZ (Secretarias Estaduais da Fazenda)
- **Bahia SEFAZ**: https://www.sefaz.ba.gov.br/ (ICMS 18%)
- **São Paulo SEFAZ**: https://www.sefaz.sp.gov.br/ (ICMS 18-20%)
- **Minas Gerais SEFAZ**: https://www.sefaz.mg.gov.br/
- **Consultas alíquotas por produto**: Acesso via sistemas tributários estaduais

### Prefeituras Municipais (ISS)
- **ISS tabelas municipais**: Consultar prefeitura local ou via IBPT (Instituto Brasileiro de Planejamento Tributário)
  - IBPT Portal: https://www.ibpt.org.br/ (requer login para dados completos)

---

## 🌍 CAMBIAL E RISCO SOBERANO

### BACEN (conforme acima)
- **Câmbio Diário**: https://www.bcb.gov.br/pom/moc/
- **Série histórica arquivo**: https://www.bcb.gov.br/pom/moc/cotacao

### Trading Economics (Free + Paid)
- **Brasil Câmbio USD/BRL**: https://tradingeconomics.com/brazil/currency
- **Brasil Inflação/Selic**: https://tradingeconomics.com/brazil/indicators
- **Download direto (limites)**: https://api.tradingeconomics.com/ (requer API key)

### Bloomberg Terminal / Reuters Eikon
- **CDS Brazil**: Requer assinatura (Bloomberg, Reuters)
- **Alternativa Free**: https://www.datagro.com.br/ (alguns dados públicos)

### IMF (International Monetary Fund)
- **PPP Brazil**: https://www.imf.org/external/datamapper/
- **World Economic Outlook DB**: https://www.imf.org/external/datamapper/api/v1/
- **Download direto**: https://www.imf.org/data/

### World Bank Open Data
- **PPP, Dados Brasil**: https://data.worldbank.org/country/BR
- **Logistics Performance Index**: https://lpi.worldbank.org/
- **Download CSV/Excel**: https://data.worldbank.org/

---

## 📱 TELECOM ESPECÍFICO

### ANATEL (Agência Nacional de Telecomunicações)
- **Painéis de Dados Abertos**: https://informacoes.anatel.gov.br/paineis
  - **5G Cobertura por cidade**: https://informacoes.anatel.gov.br/paineis/acessibilidade
  - **Estatísticas mensais**: https://informacoes.anatel.gov.br/paineis/servicomovel
  - **Investimentos operadores**: https://informacoes.anatel.gov.br/paineis/investimentos

- **Base de Dados FTP**: https://ftp.anatel.gov.br/
  - **Resolução 780/2025**: https://informacoes.anatel.gov.br/documentos
  - **Estatísticas históricas**: https://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/

- **API Dados Abertos**: https://dados.anatel.gov.br/
  - **Download em CSV**: https://dados.anatel.gov.br/dataset

- **Teleco (Não-oficial, agregador)**: https://www.teleco.com.br/
  - **Investimentos telecom**: https://www.teleco.com.br/tudosobretelecom.asp
  - **Dados operadores**: https://www.teleco.com.br/operadores.asp

---

## 🌤️ CLIMA E AMBIENTAL

### INMET (Instituto Nacional de Meteorologia)
- **Portal oficial**: https://portal.inmet.gov.br/
- **Dados históricos**: https://tempo.inmet.gov.br/
- **BDMEP (Banco de Dados Meteorológicos)**: https://bdmep.inmet.gov.br/
  - Acesso à API: https://bdmep.inmet.gov.br/sql
  - Download CSV: https://bdmep.inmet.gov.br/ (selecionar estações e período)

- **Dados em formato aberto (FTP)**:
  - https://ftp1.inmet.gov.br/
  - Estações automáticas: https://ftp1.inmet.gov.br/dane_estacoes_auto/

### OpenWeatherMap (Alternativa)
- **API Weather dados históricos**: https://openweathermap.org/api
- **Free tier**: Dados 5 dias em tempo real; histórico requer "Historical Data" (pago)

### NOAA (National Oceanic and Atmospheric Administration, EUA)
- **Global dados climáticos**: https://www.ncei.noaa.gov/cdo-web/
- **Download em CSV**: Seleção por localidade/período

---

## 📦 LOGÍSTICA E FRETE

### Drewry World Container Index
- **Portal**: https://www.drewry.co.uk/
- **WCI Download**: https://www.drewry.co.uk/supply-chain-research/services/indices/world-container-index-(wci)
- **Histórico arquivo**: https://www.drewry.co.uk/supply-chain-research/services/indices/world-container-index-(wci)/historical-data

### Freightos Baltic Index (FBX)
- **Portal**: https://www.freightos.com/
- **Histórico FBX**: https://www.freightos.com/freight-resources/freight-rate-index/historical-data
- **API (requer contato)**: https://www.freightos.com/freight-api

### Baltic Exchange (Dry Index - BDI)
- **Portal**: https://www.balticexchange.com/
- **BDI Data**: https://www.balticexchange.com/en/data-services.html
- **Download histórico**: Alguns dados públicos; série completa requer assinatura

### ANTAQ (Agência Nacional de Transportes Aquaviários, Brasil)
- **Estatísticas Portuárias**: https://www.antaq.gov.br/portal/
  - **Porto de Santos**: https://www.antaq.gov.br/portal/index.php/concessoes/portos-organizados/santos
  - **Download relatórios**: https://www.antaq.gov.br/portal/index.php/component/content/article/8-publicacoes

### ANP (Agência Nacional do Petróleo - Combustíveis)
- **Preços Combustíveis**: https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia
  - **Série histórica Diesel/Gasolina**: https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos
  - **Download tabelas**: https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/dados-historicos-do-mercado-de-gasolina

---

## 🌐 COMÉRCIO INTERNACIONAL

### UN Comtrade (Nações Unidas)
- **Portal Principal**: https://comtrade.un.org/
- **Nova versão**: https://comtradeplus.un.org/TradeFlow
- **API Access**: https://unstats.un.org/unsd/tradekb/Knowledgebase/50070/ComTrade-Free-Data-Tool
- **Download CSV (Brasil imports/exports)**:
  - Selecionar país: BR
  - Produto: Telecomunicações (HS codes: 8517, 8525, 8526, etc.)
  - Período: últimos 5-10 anos

### WITS (World Bank Trade Statistics)
- **Portal**: https://wits.worldbank.org/
- **Brasil dados**: https://wits.worldbank.org/countrystats/BR/tradecomposition
- **Download em Excel**: Seleção de períodos e commodities

### MDIC/SECEX (Ministério Desenvolvimento, Indústria e Comércio Exterior)
- **AliceWeb**: https://aliceweb2.mdic.gov.br/
  - Login necessário (gratuito)
  - Dados de importação/exportação Brasil em tempo real
  - Download em CSV/Excel

- **Defesa Comercial/Drawback**: https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial
  - Portarias, resoluções, dados de investigações

### MERCOSUR Oficial
- **Portal**: https://www.mercosur.int/
  - **Tarifa Externa Comum (TEC)**: https://www.mercosur.int/innovaportal/v/6/1/estrutura-institucional/secretariado
  - **Documentos e legislação**: https://www.mercosur.int/innovaportal/v/3949/11/listado-de-normas

---

## 📈 ÍNDICES ECONÔMICOS AGREGADOS

### Trading Economics
- **Todos indicadores Brasil**: https://tradingeconomics.com/brazil/indicators
  - Câmbio, Inflação, Selic, Desemprego, etc.
  - Download limites (API key: https://tradingeconomics.com/member/api/)

### Haver Analytics
- **Série histórica grande Brasil**: https://www.haveranalytics.com/
- **Requer assinatura**

### FRED (Federal Reserve Economic Data, EUA)
- **Dados Brasil**: https://fred.stlouisfed.org/search?st=brazil
- **PIB Brasil**: https://fred.stlouisfed.org/series/NBRGELQ188S
- **Download direto**: Opção export em cada série

### OECD Stats
- **OECD Data Explorer**: https://data-explorer.oecd.org/
- **Brasil dados econômicos**: Pesquisar "Brazil"
- **Download em CSV/SDMX**: Opção de export

---

## 🔄 FERRAMENTAS DE AUTOMAÇÃO / BATCH DOWNLOAD

### Python Libraries (recomendadas)
```python
# IBGE
pip install ibgedata
pip install sidrapy

# BACEN
pip install pycbr

# Geral
pip install pandas-datareader
pip install yfinance  # para câmbio simplificado
```

### Scripts/Exemplos Diretos
- **IBGE SIDRA Downloader**: https://github.com/4lisson/python-sidra
- **BACEN API wrapper**: https://github.com/gustavo-marques/pycbr
- **Comtrade download script**: https://github.com/uncomtrade/comtradeapi

### Plataformas Low-Code / Integração
- **Zapier / IFTTT**: Automatizar downloads periódicos
- **Apache Airflow**: Orquestração de pipelines (recomendado)
- **AWS Glue / Lambda**: Ingestão batch na cloud
- **Google Sheets + Apps Script**: Para prototipagem rápida

---

## 🎯 RESUMO — CHECKLIST PARA IMPLEMENTAÇÃO IMEDIATA

| Dados | Link Principal | Frequência | Prioridade |
|-------|---|---|---|
| **IPCA/Inflação** | https://sidra.ibge.gov.br/acervo#/q/Q1737C | Mensal | 🔴 Crítica |
| **Câmbio (PTAX)** | https://olinda.bcb.gov.br/olinda/servico/PTAX | Diária | 🔴 Crítica |
| **Selic** | https://api.bcb.gov.br/dados/serie/bcdata.sgs.432 | Bimestral | 🔴 Crítica |
| **5G Cobertura** | https://informacoes.anatel.gov.br/paineis | Trimestral | 🟠 Alta |
| **Frete (WCI)** | https://www.drewry.co.uk/ | Semanal | 🟠 Alta |
| **ICMS/PIS/COFINS** | https://www.receita.gov.br/ | Legal/Anual | 🟠 Alta |
| **Clima (INMET)** | https://bdmep.inmet.gov.br/ | Diária | 🟡 Média |
| **Comtrade (Import)** | https://comtradeplus.un.org/TradeFlow | Mensal | 🟡 Média |
| **Drawback/Defesa** | https://www.gov.br/mdic | Irregular | 🟡 Média |
| **PPP/CDS** | https://www.imf.org/, https://tradingeconomics.com | Trimestral/Diária | 🟢 Baixa |

---

## 📞 SUPORTE TÉCNICO

- **IBGE Help**: https://www.ibge.gov.br/faq/
- **BACEN Suporte**: https://www.bcb.gov.br/en/contact
- **ANATEL Suporte**: https://www.anatel.gov.br/consumidor/
- **GitHub issues** (bibliotecas Python): Ver repositórios acima

---

**Última atualização**: 8 de novembro de 2025  
**Mantido por**: Nova Corrente Supply Chain Intelligence Team
