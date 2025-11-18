# 🎯 QUICK REFERENCE — TODOS OS LINKS PARA DOWNLOAD (Categorizado)

## 📌 TABELÃO MASTER: LINK + FREQUÊNCIA + PRIORIDADE

### ⚡ CRÍTICOS (Atualizar SEMANAL + DIÁRIO)

| Dados | Link Direto | Tipo | Freq | Auth |
|-------|---|---|---|---|
| **Câmbio USD/BRL** | https://olinda.bcb.gov.br/olinda/servico/PTAX/ | API JSON | Diária | ✅ Pública |
| **IPCA Mensal** | https://sidra.ibge.gov.br/acervo#/q/Q1737C | Download/API | Mensal | ✅ Pública |
| **Selic** | https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/ | API JSON | Bimestral | ✅ Pública |
| **Frete WCI** | https://www.drewry.co.uk/ | Web Scrape | Semanal | ⚠️ Parcial |
| **5G Cobertura** | https://informacoes.anatel.gov.br/paineis/acessibilidade | Dashboard | Trimestral | ✅ Pública |

---

### 🟠 ALTOS (Atualizar MENSAL)

| Dados | Link Direto | Tipo | Freq | Auth |
|-------|---|---|---|---|
| **ICMS por Estado** | https://www1.confaz.fazenda.gov.br/confaz/public/cf | Web | Anual | ✅ Pública |
| **PIS/COFINS** | https://www.receita.gov.br/tributaria/IN1700 | PDF/Web | Legal | ✅ Pública |
| **Drawback** | https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior | Portal | Mensal | ✅ Pública |
| **Imports Telecom** | https://aliceweb2.mdic.gov.br/ | Download | Real-time | 🔑 Login |
| **Comtrade** | https://comtradeplus.un.org/TradeFlow | API/Download | Mensal | ⚠️ Limitado |
| **Clima INMET** | https://bdmep.inmet.gov.br/ | Download | Diária | 🔑 Cadastro |

---

### 🟡 MÉDIOS (Atualizar TRIMESTRAL)

| Dados | Link Direto | Tipo | Freq | Auth |
|-------|---|---|---|---|
| **PIB** | https://sidra.ibge.gov.br/acervo#/q/Q5932C | Download | Trimestral | ✅ Pública |
| **Desemprego** | https://sidra.ibge.gov.br/acervo#/q/Q6385C | Download | Mensal | ✅ Pública |
| **Investimentos Telecom** | https://informacoes.anatel.gov.br/paineis/investimentos | Dashboard | Trimestral | ✅ Pública |
| **CDS Brasil** | https://www.tradingeconomics.com/brazil/ | Web | Diária | 🔑 API Key |
| **PPP (IMF)** | https://www.imf.org/external/datamapper/ | API/Web | Trimestral | ✅ Pública |

---

### 🟢 EXTRAS (Atualizar ANUAL)

| Dados | Link Direto | Tipo | Freq | Auth |
|-------|---|---|---|---|
| **População (IBGE)** | https://sidra.ibge.gov.br/acervo#/q/Q29168C | Download | Anual | ✅ Pública |
| **MERCOSUR Tarifas** | https://www.mercosur.int/ | PDF | Anual | ✅ Pública |
| **Reforma Tributária** | https://www.gov.br/economia/reforma-tributaria | Portal | Legal | ✅ Pública |

---

## 🔗 LINKS AGRUPADOS POR INSTITUIÇÃO

### IBGE (Instituto Brasileiro de Geografia e Estatística)
```
Base: https://sidra.ibge.gov.br/
API: https://servicodados.ibge.gov.br/api/v3/

Tabelas Principais:
├─ PIB Trimestral: https://sidra.ibge.gov.br/acervo#/q/Q12462C
├─ PIB Anual: https://sidra.ibge.gov.br/acervo#/q/Q5932C
├─ IPCA: https://sidra.ibge.gov.br/acervo#/q/Q1737C
├─ IPCA-15: https://sidra.ibge.gov.br/acervo#/q/Q1705C
├─ INPC: https://sidra.ibge.gov.br/acervo#/q/Q1736C
├─ IGP-M: https://sidra.ibge.gov.br/acervo#/q/Q190C
├─ Desemprego: https://sidra.ibge.gov.br/acervo#/q/Q6385C
├─ População: https://sidra.ibge.gov.br/acervo#/q/Q29168C
└─ FTP Histórico: https://ftp.ibge.gov.br/Indices_de_Precos_ao_Consumidor/IPCA/
```

### BACEN (Banco Central do Brasil)
```
Câmbio (PTAX):
├─ Portal: https://www.bcb.gov.br/pom/moc/
├─ API OData: https://olinda.bcb.gov.br/olinda/servico/PTAX/
├─ Histórico Excel: https://www.bcb.gov.br/pom/moc/cotacao
└─ Série histórica: https://www4.bcb.gov.br/pom/moc/consultarTabela.asp

Selic:
├─ API: https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/
├─ Histórico: https://www.bcb.gov.br/controleinflacao/historicotaxasjuros
├─ COPOM: https://www.bcb.gov.br/controleinflacao/taxaselic
└─ OData: https://olinda.bcb.gov.br/olinda/servico/SELIC/

OpenDataBCB:
└─ Portal: https://opendata.bcb.gov.br/
```

### RECEITA FEDERAL
```
Tributos:
├─ Portal: https://www.receita.gov.br/
├─ IN 1700/2017: https://www.receita.gov.br/legislacao/IN1700
├─ ICMS: https://www.receita.gov.br/tributos/impostos/icms
├─ Siscomex: https://portal.siscomex.gov.br/
├─ Defesa Comercial: https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial
└─ Download IN 1700 (PDF): https://www.receita.gov.br/legislacao/ato-normativo/instrucao-normativa/2017/in-1700
```

### CONFAZ (Conselho Nacional de Política Fazendária)
```
ICMS por Estado:
├─ Portal Convênios: https://www1.confaz.fazenda.gov.br/confaz/public/cf
├─ Legislação ICMS: https://www1.confaz.fazenda.gov.br/confaz/public/cf/lei
└─ Consulta por UF: https://www1.confaz.fazenda.gov.br/confaz/public/cf
```

### SEFAZ (Secretarias Estaduais)
```
Bahia (Salvador):
├─ Portal: https://www.sefaz.ba.gov.br/
└─ ICMS: 18%

São Paulo:
├─ Portal: https://www.sefaz.sp.gov.br/
└─ ICMS: 18%

Minas Gerais:
├─ Portal: https://www.sefaz.mg.gov.br/
└─ ICMS: 18%

(Outras UFs: Google "SEFAZ [Estado]")
```

### INMET (Instituto Nacional de Meteorologia)
```
Climate Data:
├─ Portal: https://portal.inmet.gov.br/
├─ BDMEP (Dados): https://bdmep.inmet.gov.br/
├─ Série Histórica: https://bdmep.inmet.gov.br/sql
├─ Download Direto: https://bdmep.inmet.gov.br/ (selecionar período/estações)
├─ FTP Automáticas: https://ftp1.inmet.gov.br/dane_estacoes_auto/
└─ Estações Salvador: https://tempo.inmet.gov.br/ (manual)
```

### ANATEL (Agência Nacional de Telecomunicações)
```
Dados Abertos:
├─ Painéis: https://informacoes.anatel.gov.br/paineis
├─ 5G Cobertura: https://informacoes.anatel.gov.br/paineis/acessibilidade
├─ Investimentos: https://informacoes.anatel.gov.br/paineis/investimentos
├─ FTP Histórico: https://ftp.anatel.gov.br/
├─ API Dados: https://dados.anatel.gov.br/
├─ Resoluções: https://informacoes.anatel.gov.br/documentos
└─ Estatísticas: https://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/
```

### MDIC (Ministério Desenvolvimento, Indústria e Comércio Exterior)
```
AliceWeb (Import/Export):
├─ Portal: https://aliceweb2.mdic.gov.br/
├─ Acesso: Login gratuito
├─ Dados: Em tempo real + histórico
└─ Download: CSV/Excel por período

Drawback/Defesa Comercial:
├─ Portal: https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior
├─ Prorrogações: https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior/defesa-comercial/
└─ Portarias/Resoluções: https://www.gov.br/mdic/ (busca interna)
```

### ANP (Agência Nacional do Petróleo)
```
Combustíveis:
├─ Portal: https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia
├─ Preços Mensais: https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos
├─ Histórico: https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/dados-historicos-do-mercado-de-gasolina
└─ Download: CSV/Excel (últimos 5 anos)
```

### ANTAQ (Agência Nacional de Transportes Aquaviários)
```
Portos:
├─ Portal: https://www.antaq.gov.br/portal/
├─ Porto Santos: https://www.antaq.gov.br/portal/index.php/concessoes/portos-organizados/santos
├─ Estatísticas: https://www.antaq.gov.br/portal/index.php/component/content/article/8-publicacoes
└─ Relatórios Mensais: https://www.antaq.gov.br/ (busca interna)
```

### Frete Global (Drewry, Freightos, Baltic)
```
Drewry WCI:
├─ Portal: https://www.drewry.co.uk/
├─ World Container Index: https://www.drewry.co.uk/supply-chain-research/services/indices/world-container-index-(wci)
└─ Histórico: https://www.drewry.co.uk/supply-chain-research/services/indices/world-container-index-(wci)/historical-data

Freightos FBX:
├─ Portal: https://www.freightos.com/
├─ Índice: https://www.freightos.com/freight-resources/freight-rate-index/
├─ Histórico: https://www.freightos.com/freight-resources/freight-rate-index/historical-data
└─ API: https://www.freightos.com/freight-api (contato comercial)

Baltic Exchange BDI:
├─ Portal: https://www.balticexchange.com/
└─ Dados: https://www.balticexchange.com/en/data-services.html (assinatura)
```

### IMF (International Monetary Fund)
```
Macroeconomia Brasil:
├─ Data Mapper: https://www.imf.org/external/datamapper/
├─ API: https://www.imf.org/external/datamapper/api/v1/
├─ Dados Econômicos: https://www.imf.org/data/
├─ WEO Database: https://www.imf.org/external/datamapper/api/v1/
└─ Download: JSON/CSV
```

### World Bank
```
Open Data:
├─ Portal: https://data.worldbank.org/
├─ Brasil: https://data.worldbank.org/country/BR
├─ API: https://api.worldbank.org/v2/
├─ WITS: https://wits.worldbank.org/

Logistics Performance Index:
├─ Portal: https://lpi.worldbank.org/
├─ Brasil LPI: https://lpi.worldbank.org/international/scorecard/
└─ Download: Excel/CSV
```

### UN Comtrade (Comércio Internacional)
```
Clássico (Limitado):
├─ Portal: https://comtrade.un.org/
├─ API Free: https://unstats.un.org/unsd/tradekb/
└─ Download: CSV

Comtrade Plus (Premium):
├─ Portal: https://comtradeplus.un.org/TradeFlow
├─ API: Requer chave/contato
└─ Dados: Mais granulares/tempo real
```

### Trading Economics
```
Web (Livre):
├─ Brasil: https://tradingeconomics.com/brazil/indicators
├─ Câmbio: https://tradingeconomics.com/brazil/currency
├─ Inflação: https://tradingeconomics.com/brazil/inflation-rate
├─ Selic: https://tradingeconomics.com/brazil/interest-rate
├─ CDS: https://tradingeconomics.com/brazil/sovereign-cds-spread
└─ Download: Manual (Excel icon)

API (Requer chave):
├─ Portal: https://tradingeconomics.com/member/api/
└─ Docs: https://docs.tradingeconomics.com/
```

### OECD
```
Dados Brasil:
├─ OECD Data Explorer: https://data-explorer.oecd.org/
├─ Buscar "Brazil": https://data-explorer.oecd.org/
├─ API SDMX: https://stats.oecd.org/sdmx-json/data/
└─ Stats: https://stats.oecd.org/
```

### MERCOSUR
```
Tarifas e Legislação:
├─ Portal Oficial: https://www.mercosur.int/
├─ Normas: https://www.mercosur.int/innovaportal/v/3949/11/listado-de-normas
├─ TEC (Tarifa Externa Comum): Buscar em portal secretariado
└─ Download: PDF/legislação
```

### FGV (Fundação Getulio Vargas)
```
IGP-M:
├─ Portal: https://portal.fgv.br/noticias/igp-m
├─ Série Histórica: https://portal.fgv.br/artigos/indice-geral-de-precos
└─ Download: https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx
```

### FRED (St. Louis Federal Reserve)
```
Dados Brasil:
├─ Search: https://fred.stlouisfed.org/search?st=brazil
├─ PIB BR: https://fred.stlouisfed.org/series/NBRGELQ188S
├─ API: https://api.stlouisfed.org/fred/
└─ Download: CSV/JSON
```

---

## 🚀 SCRIPTS RÁPIDOS (Copy-Paste)

### Python: Baixar IPCA
```python
import requests
import pandas as pd

url = "https://apisidra.ibge.gov.br/values/t/1737/n1/v"
resp = requests.get(url)
df = pd.DataFrame(resp.json())
df.to_csv('ipca.csv', index=False)
print("✓ IPCA baixado")
```

### Python: Baixar Câmbio PTAX
```python
import requests
from datetime import datetime, timedelta

start = (datetime.now() - timedelta(days=30)).strftime('%m-%d-%Y')
end = datetime.now().strftime('%m-%d-%Y')

url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinal=@dataFinal)?@dataInicial='{start}'&@dataFinal='{end}'&$top=10000&$orderby=dataHora%20asc&$format=json"

resp = requests.get(url)
data = resp.json()
print(f"✓ {len(data['value'])} cotações baixadas")
```

### Python: Baixar Selic
```python
import requests
import pandas as pd

url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"
resp = requests.get(url)
df = pd.DataFrame(resp.json())
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
df['valor'] = pd.to_numeric(df['valor'])
df.to_csv('selic.csv', index=False)
print("✓ Selic baixada")
```

### Bash: Baixar FTP IBGE
```bash
wget -r ftp://ftp.ibge.gov.br/Indices_de_Precos_ao_Consumidor/IPCA/ -P ./ibge_dados/
echo "✓ IPCA histórico baixado"
```

---

## 📋 RECOMENDAÇÕES FINAIS

### Para Produção:
1. **Use APIs oficiais** (BACEN, IBGE, ANATEL) quando disponíveis
2. **Implemente retry/fallback** para resiliência
3. **Cache dados locais** (reduz latência, falhas API)
4. **Valide schema** de cada fonte (tipos, nulls)
5. **Log tudo** (erros, timestamps, fontes)
6. **Agende com Airflow** (DAGs diárias/mensais/trimestrais)
7. **Integre Feature Store** (Feast/Hopsworks)

### Prioridade de Implementação:
1. **Semana 1:** IBGE (IPCA), BACEN (Câmbio, Selic)
2. **Semana 2:** ANATEL (5G), RECEITA FEDERAL (impostos)
3. **Semana 3:** INMET (clima), COMTRADE (imports)
4. **Semana 4:** Frete global (Drewry, WCI)

---

**Gerado em:** 08 de Novembro, 2025 | **Atualizado:** v1.0
