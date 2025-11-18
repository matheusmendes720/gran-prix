# 📊 HISTORICAL TIME SERIES DATA — LONG-TERM ARCHIVES & BULK DOWNLOADS

**Focus:** Maximum historical depth (5-20 years+) for econometric modeling, ARIMAX/SARIMA, Prophet multi-year training, and backtesting

---

## 🏛️ 1. IBGE (Instituto Brasileiro de Geografia e Estatística)

### IPCA (Monthly Inflation) — **30+ Years**
```
FTP Download (Full History):
  └─ ftp://ftp.ibge.gov.br/Indices_de_Precos_ao_Consumidor/IPCA/
  
Direct CSV:
  └─ https://sidra.ibge.gov.br/cgi-bin/tabela?t=1737
  
Series Mapping:
  ├─ Table 1737: IPCA monthly (1980–2025)
  ├─ Table 1705: IPCA-15 (1989–2025)
  ├─ Table 1736: INPC (1979–2025)
  └─ Table 190: IGP-M (1944–2025)
  
Download All (Bash):
  $ wget -r ftp://ftp.ibge.gov.br/Indices_de_Precos_ao_Consumidor/
```

### GDP (PIB) — **1990–2025 Quarterly + Annual**
```
Quarterly Historical:
  └─ https://sidra.ibge.gov.br/acervo#/q/Q12462C
     Format: CSV/Excel | Depth: 1990 Q1 – present
     
Annual Historical:
  └─ https://sidra.ibge.gov.br/acervo#/q/Q5932C
     Format: CSV/Excel | Depth: 1900–2025
     
Growth Rates & Components:
  └─ https://sidra.ibge.gov.br/busca/tabela
     Buscar: "PIB por setor" / "componentes"
     
API (JSON, full historical):
  $ curl "https://apisidra.ibge.gov.br/values/t/5932/n1/v"
```

### Employment & Unemployment — **1990–2025 Monthly**
```
Series PNAD Contínua (2012–present monthly):
  └─ https://sidra.ibge.gov.br/acervo#/q/Q6385C
  
PME (Pesquisa Mensal Emprego) — older series:
  └─ ftp://ftp.ibge.gov.br/Trabalho_e_Rendimento/Pesquisa_Mensal_de_Emprego/
  
Full history (100+ months):
  $ wget -r ftp://ftp.ibge.gov.br/Trabalho_e_Rendimento/
```

### Demographic Data (Population, Birth Rates) — **1900–2025**
```
Intercensal Estimates:
  └─ https://sidra.ibge.gov.br/acervo#/q/Q29168C
  
Census Data (Historical):
  └─ https://www.ibge.gov.br/estatisticas/sociais/populacao/2093-censo-demografico.html
```

### Producer Price Index (IPP) — **2004–2025 Monthly**
```
Wholesale/Producer Index:
  └─ https://sidra.ibge.gov.br/busca/tabela
     Search: "Índice de Preços" + "Produtor"
```

---

## 🏦 2. BACEN (Banco Central do Brasil)

### Exchange Rate (USD/BRL) — **1994–2025 Daily**
```
PTAX Historical (Complete):
  └─ https://www.bcb.gov.br/pom/moc/cotacao
  
Direct Download (Excel):
  └─ https://www4.bcb.gov.br/pom/moc/consultarTabela.asp
     Selecionar: Data inicial 1994-01-01, final 2025-11-08
     Download: Excel .xls (completo 30+ anos)
  
CSV via FTP (Faster):
  └─ ftp://ftp.bcb.gov.br/  (if available)
  
Manual extraction (API pagination):
  $ for year in {1994..2025}; do
      curl "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinal=@dataFinal)?@dataInicial='01-01-$year'&@dataFinal='12-31-$year'&\$format=json" > ptax_$year.json
    done
```

### Selic (Interest Rate) — **1996–2025 Daily**
```
Historical Series (GSC.432):
  └─ https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados
  
Manual Download (Excel):
  └─ https://www.bcb.gov.br/controleinflacao/historicotaxasjuros
  
COPOM Decisions (Historical):
  └─ https://www.bcb.gov.br/controleinflacao/taxaselic
  
Full 30-year series:
  $ curl "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados" | jq . > selic_completo.json
```

### Other Key Series (BACEN API)
```
Series Database (GSC.X format):
  ├─ 432: Selic (Interest Rate)
  ├─ 433: Selic + Meta
  ├─ 1: Over/Selic accumulation
  ├─ 11: Dollar selling (end-of-day)
  ├─ 12: Dollar buying (end-of-day)
  ├─ 433: CDB rates
  └─ (More: https://www.bcb.gov.br/controleinflacao/publicacoes)
  
API Pattern for any series:
  $ curl "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{SERIES_ID}/dados"
```

### Historical Data (OpenDataBCB - Bulk)
```
OpenData Portal:
  └─ https://opendata.bcb.gov.br/
  
Available Datasets:
  ├─ Câmbio (Diário, 1994–present)
  ├─ Selic (Diário, 1996–present)
  ├─ IGP (Mensal, 1944–present)
  ├─ Inflação (IPCA, monthly)
  └─ Crédito (Credit market data)
  
Bulk Download (API):
  $ for series_id in 11 12 432 433; do
      curl "https://api.bcb.gov.br/dados/serie/bcdata.sgs.$series_id/dados" > bcb_$series_id.json
    done
```

---

## 📈 3. INMET (Instituto Nacional de Meteorologia)

### Climate Data (Precipitation, Temperature) — **1961–2025 Daily**
```
BDMEP (Banco de Dados Meteorológicos Para Ensino e Pesquisa):
  └─ https://bdmep.inmet.gov.br/
  
Historical Weather Data Download:
  1. Registrar (gratuito): https://bdmep.inmet.gov.br/cadastro/
  2. Download: https://bdmep.inmet.gov.br/ → Selecionar período + estações
  3. Formatos: CSV, TXT (compatível Excel)
  
Major Weather Stations (Brazil):
  ├─ A001 (Salvador, Bahia) — 40+ years
  ├─ A004 (Rio de Janeiro)
  ├─ A003 (São Paulo)
  ├─ A301 (Brasília)
  └─ (500+ automáticas)
  
FTP Archive (Automated Stations):
  └─ ftp://ftp1.inmet.gov.br/dane_estacoes_auto/
  
Python (BDMEP query):
  $ pip install pynmet  # Unofficial wrapper
```

### Alternative: OpenWeather Historical
```
OpenWeatherMap Bulk Historical:
  └─ https://openweathermap.org/api
  ⚠️ Requires paid subscription for full history
```

---

## 💼 4. RECEITA FEDERAL (Tax & Tariffs)

### ICMS by State — **Historical rates, 1989–2025**
```
CONFAZ (Conselho Nacional de Política Fazendária):
  └─ https://www1.confaz.fazenda.gov.br/confaz/public/cf
  
Legislative history:
  └─ Convênios + Protocolos → PDF archive (2000–present)
  
ICMS Rate Evolution (manual tracking):
  └─ Build versioned ICMS table from CONFAZ PDFs
  
STF Decision (RE 574.706) — 2021 landmark:
  └─ Reduced rates from 25-30% → 17-18% for telecom
```

### Import Duties (II) — **1960–2025 by HS Code**
```
Nomenclatura Comum do MERCOSUL (NCM/HS):
  └─ https://www.gov.br/siscomex/pt-br/
  
Historical tariff schedules:
  └─ MDIC archives (1994 GATT–present)
  └─ Brazilian Tariff Commission (CTB) — Portarias
  
NCM 8517 (Telecom equipment) history:
  └─ Trace changes 2000-2025 via official gazettes
```

### PIS/COFINS — **1991–2025 (Legal Regime History)**
```
IN 1700/2017 (Current regime):
  └─ https://www.receita.gov.br/legislacao/IN1700
  
Previous regimes (1991-2017):
  └─ Receive Federal archives
  
Tax rate evolution:
  ├─ Cumulativo (1991-2003): 3.65%
  ├─ Não-cumulativo (2004-present): 9.25%
  └─ IBS/CBS transition (2026-2033 planned)
```

---

## 🌐 5. COMTRADE (UN — International Trade)

### Brazil Imports/Exports — **1992–2025 Annual/Monthly**
```
UN Comtrade Official:
  └─ https://comtrade.un.org/
  
Bulk Download (All Brazil trade, annual):
  1. Reporter: 76 (Brazil)
  2. HS Codes: 8517, 8525, 8526 (Telecom)
  3. Trade Flow: Import (1), Export (2)
  4. Years: 1992-2025
  5. Format: CSV/JSON
  
API (Free tier, limited):
  $ curl "https://comtrade.un.org/api/get?max=10000&type=C&freq=A&px=HS&ps=2020,2021,2022,2023,2024,2025&r=76&p=0&rg=1&cc=8517&fmt=json"
```

### AliceWeb2 (MDIC) — **1989–2025 Real-time + Historical**
```
MDIC AliceWeb:
  └─ https://aliceweb2.mdic.gov.br/
  
Access:
  1. Login gratuito (requer CNPJ/CPF)
  2. Selecionar: NCM 8517, 8525 (Telecom)
  3. Período: 1989–2025
  4. Download: CSV, Excel, TXT
  
Bulk Export (Selenium/RPA):
  └─ Exportar por ano/produto em batch
  
Contains:
  ├─ Unit values (preços efetivos)
  ├─ Quantities (toneladas, unidades)
  ├─ Countries (origin)
  └─ Monthly granularity (1989–present)
```

---

## 🚢 6. FRETE GLOBAL (Drewry WCI, FBX, BDI)

### Drewry World Container Index (WCI) — **2010–2025 Weekly**
```
Historical Data Download:
  └─ https://www.drewry.co.uk/supply-chain-research/services/indices/world-container-index-(wci)/historical-data
  
Data Points:
  ├─ Shanghai → Rotterdam (primary)
  ├─ Shanghai → Los Angeles
  ├─ Shanghai → Hamburg
  └─ Frequency: Weekly (Friday close)
  
CSV Export:
  $ wget "https://www.drewry.co.uk/supply-chain-research/services/indices/world-container-index-(wci)/historical-data" -O wci_archive.html
  $ python extract_wci_table.py wci_archive.html > wci_historical.csv
```

### Freightos Baltic Index (FBX) — **2016–2025 Daily**
```
Historical Archive:
  └─ https://www.freightos.com/freight-resources/freight-rate-index/historical-data
  
Data:
  ├─ Daily Shanghai → Los Angeles (FBX)
  ├─ China export index
  ├─ Frequency: Daily (M-F)
  └─ 10+ years of records
  
CSV/JSON (Web scraping):
  $ python fetch_freightos_historical.py
```

### Baltic Dry Index (BDI) — **1985–2025 Daily**
```
Baltic Exchange:
  └─ https://www.balticexchange.com/en/data-services.html
  ⚠️ Full historical requires subscription ($1000+/year)
  
Free Tier (30 days rolling):
  └─ Charts at https://www.balticexchange.com/
  
Proxy (Alternative):
  └─ Trading Economics BDI: https://tradingeconomics.com/commodities/baltic
  └─ Yahoo Finance: BDI index (limited history)
  
Data Sources (Academic/Public):
  └─ FRED St.Louis (some BDI data): https://fred.stlouisfed.org/
```

---

## 📊 7. ANATEL (Telecom-Specific)

### 5G Deployment — **2019–2025 Quarterly**
```
Coverage by City (Historical):
  └─ https://informacoes.anatel.gov.br/paineis/acessibilidade
  
Downloadable Statistics:
  └─ https://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/
  
Historical Resolutions:
  └─ https://informacoes.anatel.gov.br/documentos
  
Coverage Timeline:
  ├─ 2019-2021: Initial 5G pilots
  ├─ 2022-2024: Massive expansion
  └─ 2025: Target ~95% coverage
```

### Telecom Infrastructure Investments — **2015–2025 Annual**
```
Capex Data (by Operator):
  └─ https://informacoes.anatel.gov.br/paineis/investimentos
  
Archive (PDF Reports):
  └─ https://www.anatel.gov.br/consumidor/
  
Operator Reports:
  └─ Claro, Vivo, TIM annual filings (B3/CVM)
```

### Mobile Statistics — **2008–2025 Monthly**
```
Service Statistics:
  └─ https://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/
  
Includes:
  ├─ Active lines (prepaid, postpaid)
  ├─ Revenue (ARPU trends)
  ├─ Data traffic
  └─ Churn rates
  
Download bulk:
  $ wget -r ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/
```

---

## 🏪 8. WORLD BANK & IMF (International Benchmarks)

### PPP (Purchasing Power Parity) — **1990–2025 Annual**
```
World Bank PPP Dataset:
  └─ https://data.worldbank.org/indicator/NY.GDP.MKTP.PP.CD
  
Format: CSV/JSON
  $ curl "https://api.worldbank.org/v2/country/BR/indicator/NY.GDP.MKTP.PP.CD?format=json&per_page=60" > brazil_ppp.json
  
Coverage: 1990–2025 annual
```

### GDP (Nominal) — **1960–2025 Annual**
```
World Bank GDP:
  └─ https://data.worldbank.org/indicator/NY.GDP.MKTP.CD
  
IMF GDP Database:
  └─ https://www.imf.org/external/datamapper/api/v1/NGDPD?countries=BR
  
Both have 50-65 year histories
```

### Logistics Performance Index (LPI) — **2007, 2010, 2012, 2014, 2016, 2018, 2023**
```
World Bank LPI:
  └─ https://lpi.worldbank.org/
  
Historical Scores:
  ├─ Overall LPI
  ├─ Customs
  ├─ Infrastructure
  ├─ Timeliness
  └─ (6 dimensions × multiple years)
  
Data: Excel download available per year
```

### CDS (Credit Default Swaps) — **2008–2025 Daily**
```
IMF/World Bank archives:
  └─ Partial historical data
  
Primary sources:
  └─ Bloomberg (subscription)
  └─ Trading Economics (free 30-day window; historical via API key)
  
Academic datasets:
  └─ FRED St. Louis (some CDS Brazil, 2010–present)
  └─ Kaggle (historical CDS datasets)
```

---

## 🏭 9. FGV (Fundação Getulio Vargas) — IGP-M

### IGP-M (General Price Index) — **1944–2025 Monthly**
```
FGV Portal:
  └─ https://portal.fgv.br/noticias/igp-m
  
Series Histórica (Download):
  └─ https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx
  └─ 80+ year historical record
  
Components:
  ├─ IPA (Índice de Preços ao Produtor)
  ├─ IPC (Índice de Preços ao Consumidor)
  ├─ INCC (Índice de Custos da Construção)
  └─ Available: 1944–2025
```

---

## 🌍 10. FRED (St. Louis Federal Reserve) — International Data

### Brazil Economic Indicators — **1960–2025**
```
FRED Series Search:
  └─ https://fred.stlouisfed.org/search?st=brazil
  
Key Series:
  ├─ GDP (nominal, real): NBRGELQ188S
  ├─ GDP per capita: NBRGLQPCPPPUSD
  ├─ Inflation: BRACPIALLMINMEI
  ├─ Unemployment: LRUN64TTBRA156S
  ├─ Interest rates (various)
  └─ More (search "Brazil")
  
Download All (CSV):
  $ for series in NBRGELQ188S BRACPIALLMINMEI LRUN64TTBRA156S; do
      curl "https://fred.stlouisfed.org/data/$series.txt" > $series.txt
    done
```

---

## 🗄️ 11. KAGGLE & GITHUB (Community-Curated Historical Data)

### Pre-processed Time Series Datasets
```
Kaggle Datasets:
  ├─ "Brazil Economic Indicators": https://www.kaggle.com/search?q=brazil+economics
  ├─ "Exchange Rates Historical": https://www.kaggle.com/datasets
  ├─ "Commodity Prices": https://www.kaggle.com/datasets
  ├─ "Climate Data": https://www.kaggle.com/datasets
  └─ Most: Free download (CSV)

GitHub Repositories:
  ├─ "Brazil Economic Time Series": Search github.com
  ├─ "Brazilian Telecom Data": github.com/topics/
  ├─ Often include Python scripts for API parsing
  └─ Example: https://github.com/4lisson/python-sidra (IBGE wrapper)
```

---

## 🔗 12. DIRECT DOWNLOAD — BULK FTP ARCHIVES

### IBGE FTP (Complete Economic Archive)
```
Main FTP:
  └─ ftp://ftp.ibge.gov.br/
  
Key folders:
  ├─ /Indices_de_Precos_ao_Consumidor/ (IPCA, 40+ years)
  ├─ /Indices_de_Precos_ao_Produtor/ (IPP)
  ├─ /Contas_Nacionais/ (GDP, National Accounts)
  ├─ /Trabalho_e_Rendimento/ (Employment, wages)
  └─ /Pesquisa_de_Orcamentos_Familiares/ (HH expenditure)
  
Bulk Download (Linux/Mac):
  $ wget -r ftp://ftp.ibge.gov.br/ -P ./ibge_archive/
  ⚠️ Large! (~50GB for full archive)
```

### ANATEL FTP (Telecom Statistics Complete)
```
Telecom Archive:
  └─ ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/
  
Includes (2008–2025):
  ├─ Monthly/quarterly statistics
  ├─ By operator, region
  ├─ Revenue, churn, ARPU
  └─ Format: XLS, CSV
  
Download:
  $ wget -r ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/ -P ./anatel_archive/
```

### INMET FTP (Climate Data Bulk)
```
Automated Stations:
  └─ ftp://ftp1.inmet.gov.br/dane_estacoes_auto/
  
Format: Daily CSV/TXT (2000–present)
  
Download Salvador Station (1990–2025):
  $ wget -r ftp://ftp1.inmet.gov.br/dane_estacoes_auto/A001/ -P ./clima_salvador/
```

---

## 📥 PYTHON: AUTOMATED HISTORICAL DOWNLOAD

```python
#!/usr/bin/env python3
"""Download all historical time-series data in one go"""

import pandas as pd
import requests
from datetime import datetime
import os

def download_historical_all():
    """Download all major historical datasets"""
    
    output_dir = './historical_data'
    os.makedirs(output_dir, exist_ok=True)
    
    results = {}
    
    # 1. IBGE IPCA (30 years)
    print("1. IPCA (1980–2025)...")
    try:
        url = "https://apisidra.ibge.gov.br/values/t/1737/n1/v"
        df = pd.DataFrame(requests.get(url, timeout=30).json())
        df.to_csv(f"{output_dir}/01_IPCA_1980-2025.csv", index=False)
        results['ipca'] = f"{len(df)} records"
    except Exception as e:
        results['ipca'] = f"ERROR: {e}"
    
    # 2. BACEN Câmbio (30 years)
    print("2. PTAX Câmbio (1994–2025)...")
    try:
        # Manual Excel download recommended
        print("   ⚠️ Use: https://www4.bcb.gov.br/pom/moc/consultarTabela.asp")
        results['ptax'] = "Manual download (Excel preferred)"
    except Exception as e:
        results['ptax'] = f"ERROR: {e}"
    
    # 3. BACEN Selic (30 years)
    print("3. Selic (1996–2025)...")
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"
        df = pd.DataFrame(requests.get(url, timeout=30).json())
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
        df = df.sort_values('data')
        df.to_csv(f"{output_dir}/02_Selic_1996-2025.csv", index=False)
        results['selic'] = f"{len(df)} daily records"
    except Exception as e:
        results['selic'] = f"ERROR: {e}"
    
    # 4. IBGE PIB (35 years annual)
    print("4. PIB Annual (1990–2025)...")
    try:
        url = "https://apisidra.ibge.gov.br/values/t/5932/n1/v"
        df = pd.DataFrame(requests.get(url, timeout=30).json())
        df.to_csv(f"{output_dir}/03_PIB_Annual_1990-2025.csv", index=False)
        results['pib_annual'] = f"{len(df)} years"
    except Exception as e:
        results['pib_annual'] = f"ERROR: {e}"
    
    # 5. IBGE Unemployment (30 years monthly)
    print("5. Unemployment (1990–2025 monthly)...")
    try:
        url = "https://apisidra.ibge.gov.br/values/t/6385/n1/v"
        df = pd.DataFrame(requests.get(url, timeout=30).json())
        df.to_csv(f"{output_dir}/04_Unemployment_1990-2025.csv", index=False)
        results['unemployment'] = f"{len(df)} monthly records"
    except Exception as e:
        results['unemployment'] = f"ERROR: {e}"
    
    # 6. FGV IGP-M (80 years!)
    print("6. IGP-M (1944–2025)...")
    try:
        # Download Excel from FGV directly
        url = "https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx"
        df = pd.read_excel(url)
        df.to_csv(f"{output_dir}/05_IGP-M_1944-2025.csv", index=False)
        results['igp_m'] = f"{len(df)} monthly records"
    except Exception as e:
        results['igp_m'] = f"Manual download: https://portal.fgv.br/noticias/igp-m"
    
    # 7. World Bank Brazil Data (60+ years)
    print("7. World Bank (1960–2025)...")
    try:
        indicators = {
            'GDP_nominal': 'NY.GDP.MKTP.CD',
            'GDP_ppp': 'NY.GDP.MKTP.PP.CD',
            'GDP_per_capita': 'NY.GDP.PCAP.CD'
        }
        for name, code in indicators.items():
            url = f"https://api.worldbank.org/v2/country/BR/indicator/{code}?format=json&per_page=60"
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                if len(data) > 1 and data[1]:
                    df = pd.DataFrame([{
                        'year': int(r['date']),
                        'value': float(r['value'])
                    } for r in data[1] if r['value']])
                    df.to_csv(f"{output_dir}/06_WorldBank_{name}.csv", index=False)
                    results[name] = f"{len(df)} years"
    except Exception as e:
        results['world_bank'] = f"ERROR: {e}"
    
    # 8. FRED Data (50+ years)
    print("8. FRED (1960–2025)...")
    try:
        series_list = ['NBRGELQ188S']  # Brazil GDP
        for series in series_list:
            url = f"https://fred.stlouisfed.org/data/{series}.txt"
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                with open(f"{output_dir}/07_FRED_{series}.txt", 'w') as f:
                    f.write(resp.text)
                results[series] = "Downloaded"
    except Exception as e:
        results['fred'] = f"ERROR: {e}"
    
    # Print summary
    print("\n" + "="*60)
    print("HISTORICAL DATA DOWNLOAD SUMMARY")
    print("="*60)
    for dataset, status in results.items():
        print(f"✓ {dataset:20} → {status}")
    
    print(f"\n✅ Data saved to: {output_dir}/")
    return output_dir

if __name__ == "__main__":
    download_historical_all()
```

---

## 🎯 RECOMMENDED HISTORICAL DATA STACK (For ML Training)

### Minimum (For Quick Start)
```
1. IPCA mensal (IBGE) — 240 months (20 years)
2. Câmbio USD/BRL diário (BACEN) — 7,800 days (21 years)
3. Selic diário (BACEN) — 7,800 days (21 years)
4. PIB trimestral (IBGE) — 140 quarters (35 years)
5. Desemprego mensal (IBGE) — 360 months (30 years)
```

### Recommended (For Robust Models)
```
+ Frete global (Drewry WCI) — 624 weeks (12 years)
+ 5G deployment (ANATEL) — 24+ quarters
+ Import volumes (AliceWeb2) — 360 months (30 years)
+ Climate data (INMET) — 60+ years daily
+ Investimentos telecom (ANATEL) — 20+ years annual
```

### Premium (For Best Results)
```
+ All above +
+ IGP-M completo (FGV) — 80+ years monthly!
+ Comtrade imports (UN) — 33 years annual
+ PPP/CDS (World Bank) — 35 years annual
+ Producer prices (IBGE) — 20+ years
+ Employment components (IBGE) — 30+ years
```

---

## 📋 QUICK LINKS (Historical Data Only)

| Dataset | Historical Coverage | Primary Link | Format |
|---------|---------------------|--------------|--------|
| **IPCA** | 1980–2025 (45 years) | https://sidra.ibge.gov.br/acervo#/q/Q1737C | CSV/API |
| **Câmbio PTAX** | 1994–2025 (31 years) | https://www4.bcb.gov.br/pom/moc/consultarTabela.asp | Excel |
| **Selic** | 1996–2025 (29 years) | https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados | JSON |
| **PIB (Annual)** | 1900–2025 (125 years) | https://sidra.ibge.gov.br/acervo#/q/Q5932C | CSV |
| **IGP-M** | 1944–2025 (81 years) | https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx | Excel |
| **Desemprego** | 1990–2025 (35 years) | https://sidra.ibge.gov.br/acervo#/q/Q6385C | CSV |
| **Clima (INMET)** | 1961–2025 (64 years) | https://bdmep.inmet.gov.br/ | CSV |
| **Comtrade** | 1992–2025 (33 years) | https://comtrade.un.org/ | CSV/API |
| **WCI Frete** | 2010–2025 (15 years) | https://www.drewry.co.uk/.../historical-data | CSV |
| **GDP (World Bank)** | 1960–2025 (65 years) | https://data.worldbank.org/indicator/NY.GDP.MKTP.CD | JSON/CSV |

---

## 💾 STORAGE & BACKUP RECOMMENDATIONS

```bash
# Organize locally (recommended structure)
historical_data/
├── macroeconomic/
│   ├── ipca_1980-2025.csv
│   ├── selic_1996-2025.csv
│   ├── pib_annual_1900-2025.csv
│   ├── pib_quarterly_1990-2025.csv
│   └── igp_m_1944-2025.csv
├── cambial/
│   ├── ptax_1994-2025.csv
│   └── cny_eur_1995-2025.csv
├── employment/
│   ├── unemployment_1990-2025.csv
│   └── wages_1990-2025.csv
├── telecom/
│   ├── 5g_coverage_2019-2025.csv
│   ├── capex_2015-2025.csv
│   ├── imports_nc_8517_1989-2025.csv
│   └── mobile_stats_2008-2025.csv
├── climate/
│   ├── salvador_1961-2025_daily.csv
│   └── precip_temp_1961-2025.csv
├── logistics/
│   ├── wci_drewry_2010-2025_weekly.csv
│   ├── fbx_2016-2025_daily.csv
│   └── lpi_world_bank_2007-2023.csv
└── metadata/
    ├── sources.json          (URLs, update dates)
    ├── data_dictionary.json  (column definitions)
    └── update_log.csv        (when last updated)

# Backup to cloud (e.g., AWS S3)
aws s3 sync ./historical_data/ s3://nova-corrente-backup/historical_data/ --region sa-east-1

# Version control (Git)
git init
git add .
git commit -m "Initial historical data snapshot - Nov 8, 2025"
git remote add origin https://github.com/nova-corrente/historical-data.git
git push
```

---

**🎯 Bottom Line:** Focus on **FTP downloads + official Excel exports** for comprehensive historical series. Avoid real-time APIs when building ML models — historical depth matters more than frequency.

**Última atualização:** 8 de Novembro, 2025
