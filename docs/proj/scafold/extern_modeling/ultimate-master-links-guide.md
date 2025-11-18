# 🔥 ULTIMATE MASTER DOWNLOAD GUIDE — ALL BEST LINKS (Priority-Ranked)

**Purpose:** Complete inventory of downloadable data sources for Nova Corrente demand forecasting  
**Last Updated:** November 9, 2025  
**Target:** MAPE <15%, 60% stock-out reduction via multi-layer feature engineering

---

## 🎯 **TIER 1: CRITICAL (Download FIRST - Use Daily/Weekly)**

### **1A. BACEN (Banco Central do Brasil)**

| Data | Best Link | Format | Frequency | Historical Depth | How to Download |
|------|-----------|--------|-----------|------------------|-----------------|
| **Câmbio PTAX (USD/BRL)** | https://www4.bcb.gov.br/pom/moc/consultarTabela.asp | Excel/CSV | Daily | 1994–present (31 years) | Manual Excel download (recommended); API: https://olinda.bcb.gov.br/olinda/servico/PTAX/ |
| **Selic (Interest Rate)** | https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados | JSON/CSV | Daily | 1996–present (29 years) | API direct; Python: `requests.get('https://api.bcb.gov.br/...')` |
| **Open Data Portal** | https://opendata.bcb.gov.br/ | JSON/CSV | Varies | Multiple series 1990+ | API access; batch download option |

**⚡ Quick Start:**
```bash
# Download Selic (Python one-liner)
python -c "import requests, pandas as pd; df=pd.DataFrame(requests.get('https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados').json()); df.to_csv('selic.csv')"

# Download PTAX (manual better, but API available)
curl -X GET "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/..." > ptax.json
```

---

### **1B. IBGE (Instituto Brasileiro de Geografia e Estatística)**

| Data | Best Link | Format | Frequency | Historical Depth | How to Download |
|------|-----------|--------|-----------|------------------|-----------------|
| **IPCA (Inflation)** | https://sidra.ibge.gov.br/acervo#/q/Q1737C | CSV/Excel/API | Monthly | 1980–present (45 years) | Direct CSV or API: `https://apisidra.ibge.gov.br/values/t/1737/n1/v` |
| **PIB (GDP) Quarterly** | https://sidra.ibge.gov.br/acervo#/q/Q12462C | CSV/Excel/API | Quarterly | 1990–present (35 years) | Same API endpoint |
| **PIB Annual** | https://sidra.ibge.gov.br/acervo#/q/Q5932C | CSV/Excel/API | Annual | 1900–present (125 years!) | Bulk download: `ftp://ftp.ibge.gov.br/Contas_Nacionais/` |
| **Desemprego (Unemployment)** | https://sidra.ibge.gov.br/acervo#/q/Q6385C | CSV/Excel/API | Monthly | 1990–present (35 years) | Same as above |
| **All IBGE Data (Bulk FTP)** | ftp://ftp.ibge.gov.br/ | CSV/XLS | Varies | 30-125 years | `wget -r ftp://ftp.ibge.gov.br/` (large download) |

**⚡ Quick Start:**
```bash
# Download IPCA
curl "https://apisidra.ibge.gov.br/values/t/1737/n1/v" | python -m json.tool > ipca.json

# Bulk FTP (all economic data)
wget -r ftp://ftp.ibge.gov.br/Indices_de_Precos_ao_Consumidor/ --limit-rate=100k
```

---

### **1C. INMET (Instituto Nacional de Meteorologia) — Climate**

| Data | Best Link | Format | Frequency | Historical Depth | How to Download |
|------|-----------|--------|-----------|------------------|-----------------|
| **BDMEP (Historical Climate)** | https://bdmep.inmet.gov.br/ | CSV/TXT | Daily | 1961–present (64 years) | Register free → Download by station/period |
| **Automated Stations (FTP)** | ftp://ftp1.inmet.gov.br/dane_estacoes_auto/ | CSV | Daily | 2000–present | `wget -r ftp://ftp1.inmet.gov.br/dane_estacoes_auto/A001/` (Salvador) |

**⚡ Quick Start:**
```bash
# Download Salvador climate (station A001)
wget -r ftp://ftp1.inmet.gov.br/dane_estacoes_auto/A001/ -P ./clima_salvador/
```

---

### **1D. ANATEL (Agência Nacional de Telecomunicações)**

| Data | Best Link | Format | Frequency | Historical Depth | How to Download |
|------|-----------|--------|-----------|------------------|-----------------|
| **5G Coverage** | https://informacoes.anatel.gov.br/paineis/acessibilidade | Dashboard/CSV | Monthly | 2019–present | Export from dashboard or FTP below |
| **Telecom Statistics** | ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/ | XLS/CSV | Monthly | 2008–present (17 years) | `wget -r ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/` |
| **Open Data API** | https://dados.anatel.gov.br/api/3/action/package_search | JSON | Varies | Multiple series | API access for datasets |

**⚡ Quick Start:**
```bash
# Download all Anatel telecom stats (large)
wget -r ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/ -P ./anatel_data/
```

---

## 🎯 **TIER 2: HIGH-VALUE (Download MONTHLY)**

### **2A. Receita Federal (Taxes — ICMS, PIS, COFINS, IPI)**

| Data | Best Link | Format | Frequency | How to Download |
|------|-----------|--------|-----------|-----------------|
| **PIS/COFINS (IN 1700/2017)** | https://www.receita.gov.br/legislacao/ato-normativo/instrucao-normativa/2017/in-1700 | PDF | Legal (annual updates) | Direct PDF download |
| **ICMS Rates (CONFAZ)** | https://www1.confaz.fazenda.gov.br/confaz/public/cf | Web/PDF | Annual | Web portal lookup per state |
| **State ICMS (Bahia)** | https://www.sefaz.ba.gov.br/ | Web/PDF | Quarterly | Portal lookup (18% for telecom) |

**💡 Hardcoded Tables (Update Annually):**
```python
icms_rates_2025 = {
    'BA': 0.18, 'SP': 0.18, 'RJ': 0.20, 'MG': 0.18,
    # ... other states 0.17
}
pis_cofins_combined = 0.0925  # Non-cumulativo
ipi_telecom = 0.05  # Varies, ~5% for telecom
```

---

### **2B. UN Comtrade (Import/Export Telecom Parts)**

| Data | Best Link | Format | Frequency | Historical Depth | How to Download |
|------|-----------|--------|-----------|------------------|-----------------|
| **Comtrade Classic (Free)** | https://comtrade.un.org/ | CSV/JSON | Annual | 1992–present (33 years) | API: https://comtrade.un.org/api/get?... (limited) |
| **Comtrade Plus (Premium)** | https://comtradeplus.un.org/TradeFlow | CSV/API | Monthly | Latest | API key required |
| **AliceWeb2 (MDIC)** | https://aliceweb2.mdic.gov.br/ | CSV/Excel | Real-time | 1989–present (36 years) | Login → Select product (HS 8517) → Download |

**⚡ Quick Start (Comtrade API):**
```bash
# Brazil imports of HS 8517 (Telecom equipment)
curl "https://comtrade.un.org/api/get?max=10000&type=C&freq=A&ps=2020,2021,2022,2023,2024,2025&r=76&p=0&rg=1&cc=8517&fmt=json" > comtrade_br_telecom_imports.json
```

---

### **2C. FGV (Fundação Getulio Vargas) — IGP-M**

| Data | Best Link | Format | Frequency | Historical Depth | How to Download |
|------|-----------|--------|-----------|------------------|-----------------|
| **IGP-M (80+ years!)** | https://portal.fgv.br/noticias/igp-m | Excel | Monthly | 1944–present (81 years) | Direct Excel: https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx |

**⚡ Quick Start:**
```python
import pandas as pd
df_igp_m = pd.read_excel('https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx')
```

---

## 🌐 **TIER 3: GLOBAL CONTEXT (Download QUARTERLY)**

### **3A. World Bank & IMF**

| Data | Best Link | Format | Frequency | Historical Depth | How to Download |
|------|-----------|--------|-----------|------------------|-----------------|
| **World Bank GDP** | https://data.worldbank.org/indicator/NY.GDP.MKTP.CD | CSV/JSON/API | Annual | 1960–present (65 years) | API: `https://api.worldbank.org/v2/country/BR/indicator/...` |
| **World Bank PPP** | https://data.worldbank.org/indicator/NY.GDP.MKTP.PP.CD | CSV/JSON/API | Annual | 1990–present | Same API pattern |
| **IMF Data** | https://www.imf.org/external/datamapper/api/v1/ | JSON | Quarterly | 1980+ | API direct |
| **LPI (Logistics)** | https://lpi.worldbank.org/ | Excel | 2007–2023 (sporadic) | Multi-year snapshots | Download per year from portal |

**⚡ Quick Start:**
```python
import pandas as pd
import requests

# World Bank GDP
url = "https://api.worldbank.org/v2/country/BR/indicator/NY.GDP.MKTP.CD?format=json&per_page=60"
df_gdp = pd.DataFrame(requests.get(url).json()[1])
```

---

### **3B. Frete Global (Shipping Rates)**

| Data | Best Link | Format | Frequency | Historical Depth | How to Download |
|------|-----------|--------|-----------|------------------|-----------------|
| **Drewry WCI** | https://www.drewry.co.uk/.../historical-data | CSV/Web | Weekly | 2010–present (15 years) | Manual download from portal or web scrape |
| **Freightos FBX** | https://www.freightos.com/freight-resources/freight-rate-index/historical-data | CSV/Web | Daily | 2016–present (9 years) | Download historical CSV |
| **FRED (St. Louis Fed)** | https://fred.stlouisfed.org/ | CSV/API | Varies | 1960+ | API: `https://fred.stlouisfed.org/data/{SERIES_ID}.txt` |

**⚡ Quick Start:**
```bash
# FRED Brazil data
curl https://fred.stlouisfed.org/data/NBRGELQ188S.txt > brazil_gdp_fred.txt
```

---

## 📦 **TIER 4: SPECIALIZED (Download AS-NEEDED)**

### **4A. MERCOSUR & Trade**

| Data | Best Link | Format | How to Download |
|------|-----------|--------|---|
| **MERCOSUR Tariffs** | https://www.mercosur.int/ | PDF/Portal | Manual from portal |
| **Drawback Subsidy** | https://www.gov.br/mdic/pt-br/assuntos/comercio-exterior | PDF/Portal | MDIC portal |

### **4B. Port & Logistics**

| Data | Best Link | Format | How to Download |
|------|-----------|--------|---|
| **Port Congestion** | https://spglobal.com/ (S&P Global) | Dashboard | Subscription (or free summaries) |
| **ANTAQ (Ports)** | https://www.antaq.gov.br/portal/ | PDF/CSV | Manual reports/statistics |

### **4C. Energy & Commodities**

| Data | Best Link | Format | How to Download |
|------|-----------|--------|---|
| **ANP (Fuel Prices)** | https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia | CSV/Excel | Download tables (last 5 years) |
| **OECD** | https://stats.oecd.org/ | JSON/API | API access |

---

## 🚀 **AUTOMATED BATCH DOWNLOAD SCRIPT**

Save as `download_all_data.py` and run monthly:

```python
#!/usr/bin/env python3
import pandas as pd
import requests
import os
from datetime import datetime

output_dir = './nova_corrente_data'
os.makedirs(output_dir, exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d')

# 1. BACEN Selic
print("1. Downloading Selic...")
try:
    df = pd.DataFrame(requests.get('https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados').json())
    df.to_csv(f"{output_dir}/01_selic_{timestamp}.csv")
    print("✓ Selic")
except Exception as e:
    print(f"✗ Selic: {e}")

# 2. IBGE IPCA
print("2. Downloading IPCA...")
try:
    df = pd.DataFrame(requests.get('https://apisidra.ibge.gov.br/values/t/1737/n1/v').json())
    df.to_csv(f"{output_dir}/02_ipca_{timestamp}.csv")
    print("✓ IPCA")
except Exception as e:
    print(f"✗ IPCA: {e}")

# 3. IBGE PIB Annual
print("3. Downloading PIB...")
try:
    df = pd.DataFrame(requests.get('https://apisidra.ibge.gov.br/values/t/5932/n1/v').json())
    df.to_csv(f"{output_dir}/03_pib_annual_{timestamp}.csv")
    print("✓ PIB")
except Exception as e:
    print(f"✗ PIB: {e}")

# 4. FGV IGP-M
print("4. Downloading IGP-M...")
try:
    df = pd.read_excel('https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx')
    df.to_csv(f"{output_dir}/04_igp_m_{timestamp}.csv")
    print("✓ IGP-M")
except Exception as e:
    print(f"✗ IGP-M: {e}")

# 5. World Bank GDP
print("5. Downloading World Bank GDP...")
try:
    url = 'https://api.worldbank.org/v2/country/BR/indicator/NY.GDP.MKTP.CD?format=json&per_page=60'
    data = requests.get(url).json()
    if len(data) > 1 and data[1]:
        records = [{
            'year': int(r['date']),
            'gdp': float(r['value'])
        } for r in data[1] if r['value']]
        df = pd.DataFrame(records)
        df.to_csv(f"{output_dir}/05_worldbank_gdp_{timestamp}.csv")
        print("✓ World Bank GDP")
except Exception as e:
    print(f"✗ World Bank GDP: {e}")

# 6. UN Comtrade
print("6. Downloading Comtrade (imports HS 8517)...")
try:
    url = "https://comtrade.un.org/api/get?max=10000&type=C&freq=A&ps=2020,2021,2022,2023,2024,2025&r=76&p=0&rg=1&cc=8517&fmt=json"
    data = requests.get(url, timeout=30).json()
    if 'dataset' in data:
        df = pd.DataFrame(data['dataset'])
        df.to_csv(f"{output_dir}/06_comtrade_imports_8517_{timestamp}.csv")
        print("✓ Comtrade")
except Exception as e:
    print(f"✗ Comtrade: {e}")

print(f"\n✅ Download complete. Data in: {output_dir}/")
```

**Run monthly via cron:**
```bash
0 2 1 * * /usr/bin/python3 /path/to/download_all_data.py
```

---

## 📋 **QUICK REFERENCE — TOP 15 LINKS TO BOOKMARK**

1. **BACEN Câmbio Excel** → https://www4.bcb.gov.br/pom/moc/consultarTabela.asp
2. **BACEN Selic API** → https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados
3. **IBGE IPCA** → https://apisidra.ibge.gov.br/values/t/1737/n1/v
4. **IBGE PIB Annual** → https://apisidra.ibge.gov.br/values/t/5932/n1/v
5. **IBGE Bulk FTP** → ftp://ftp.ibge.gov.br/Indices_de_Precos_ao_Consumidor/
6. **INMET Climate** → https://bdmep.inmet.gov.br/
7. **ANATEL 5G** → https://informacoes.anatel.gov.br/paineis/acessibilidade
8. **ANATEL Stats FTP** → ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/
9. **AliceWeb2 (MDIC)** → https://aliceweb2.mdic.gov.br/
10. **UN Comtrade** → https://comtrade.un.org/
11. **FGV IGP-M Excel** → https://www.fgv.br/ibre/cecon/CMS/files/IGP-M_mensal.xlsx
12. **World Bank Data** → https://data.worldbank.org/country/BR
13. **Drewry WCI** → https://www.drewry.co.uk/
14. **FRED St. Louis** → https://fred.stlouisfed.org/
15. **CONFAZ ICMS** → https://www1.confaz.fazenda.gov.br/confaz/public/cf

---

## ✅ **CHECKLIST — DOWNLOAD PLAN**

- [ ] **Week 1:** Download Tier 1 (BACEN, IBGE, INMET, ANATEL)
- [ ] **Week 2:** Download Tier 2 (Receita Federal, Comtrade, FGV)
- [ ] **Week 3:** Download Tier 3 (World Bank, IMF, Frete Global)
- [ ] **Week 4:** Set up automated batch script (cron job monthly)
- [ ] **Ongoing:** Validate data quality, check for API updates

---

**🎯 Next Action:** Start with **Tier 1** links. Download BACEN Câmbio (Excel), IBGE IPCA/PIB (API), and you're 70% there!
