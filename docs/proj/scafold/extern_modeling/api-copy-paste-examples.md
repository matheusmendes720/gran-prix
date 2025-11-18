# 🚀 COPY-PASTE API CALLS — EXEMPLOS PRONTOS PARA USAR

## 1️⃣ IBGE (PIB, IPCA, Desemprego)

### IPCA Mensal Acumulado (Últimos 24 meses)
```bash
curl -s "https://sidra.ibge.gov.br/api/v1/datatable/1737/data/0?ibge=true&format=json" | jq . | head -50
```

### Python - Baixar IPCA
```python
import pandas as pd
import requests

# Método 1: Via API SIDRA
url = "https://apisidra.ibge.gov.br/values/t/1737/n1/v"
response = requests.get(url)
df_ipca = pd.DataFrame(response.json())
df_ipca.to_csv('ipca.csv')

# Método 2: Direto via OpenData
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"  # Alternativa com lag
```

### PIB Trimestral
```bash
curl "https://apisidra.ibge.gov.br/values/t/12462/n1/v" | python -m json.tool
```

---

## 2️⃣ BACEN (Câmbio, Selic)

### Câmbio PTAX (Últimos 30 dias)
```bash
# Formato OData + JSON
curl "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinal=@dataFinal)?@dataInicial='11-08-2025'&@dataFinal='11-08-2025'&\$top=10000&\$orderby=dataHora%20asc&\$format=json"
```

### Python - Câmbio PTAX Batch
```python
import pandas as pd
import requests
from datetime import datetime, timedelta

start_date = (datetime.now() - timedelta(days=365)).strftime('%m-%d-%Y')
end_date = datetime.now().strftime('%m-%d-%Y')

url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinal=@dataFinal)?@dataInicial='{start_date}'&@dataFinal='{end_date}'&$top=10000&$orderby=dataHora%20asc&$format=json"

response = requests.get(url)
data = response.json()

if 'value' in data:
    df = pd.DataFrame(data['value'])
    df['data'] = pd.to_datetime(df['dataHora'])
    df['taxa_venda'] = pd.to_numeric(df['cotacaoVenda'])
    df['taxa_compra'] = pd.to_numeric(df['cotacaoCompra'])
    df.to_csv('ptax_1ano.csv', index=False)
    print(f"✓ {len(df)} cotações salvas")
```

### Selic Histórica
```bash
# API BCB
curl "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados" | python -m json.tool
```

### Python - Selic Completa
```python
import pandas as pd
import requests

url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
df['valor'] = pd.to_numeric(df['valor'])
df = df.sort_values('data')
df.to_csv('selic_completa.csv', index=False)
print(f"✓ {len(df)} observações Selic salvas")
```

---

## 3️⃣ AliceWeb (MDIC - Importação/Exportação)

### Login + Extração (via Selenium)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# NOTA: AliceWeb não tem API pública. Usar web scraping.
# Alternativa: Comtrade (UN)
```

### Acesso manual AliceWeb2
```
1. Abrir: https://aliceweb2.mdic.gov.br/
2. Selecionar:
   - Períodos: últimos 5 anos
   - NCM/HS: 8517 (Telecom), 8525 (Transmissão)
   - Tipo: Importação
3. Exportar CSV/Excel
```

---

## 4️⃣ UN Comtrade (Importação/Exportação Global)

### API Comtrade Plus (requer chave)
```bash
# Exemplo: Importações BR de telecomunicações
curl "https://comtradeplus.un.org/api/get?reporter=BR&partner=All&product=8517&start=2019&end=2025&trade_flow=Import&format=json&limit=10000"
```

### Comtrade Clássico (Limited)
```bash
# Free API (com limite)
curl "https://comtrade.un.org/api/get?max=10000&type=C&freq=A&px=HS&ps=2019,2020,2021,2022,2023,2024,2025&r=76&p=0&rg=1&cc=8517&fmt=json"

# r=76 (Brasil)
# rg=1 (Importação)
# cc=8517 (HS code)
```

### Python - Download Comtrade
```python
import pandas as pd
import requests

# Funciona sem API key (com limites)
base_url = "https://comtrade.un.org/api/get"

params = {
    'max': 10000,
    'type': 'C',  # Mercadorias
    'freq': 'M',  # Mensal
    'ps': '202410,202409,202408',  # Períodos (ano+mês)
    'r': '76',   # Reporter = Brasil
    'p': '0',    # Todos os parceiros
    'rg': '1',   # Importação
    'cc': '8517',  # HS Code = Telecom
    'fmt': 'json'
}

response = requests.get(base_url, params=params)
data = response.json()

if 'dataset' in data:
    df = pd.DataFrame(data['dataset'])
    df.to_csv('comtrade_imports_br_telecom.csv', index=False)
    print(f"✓ {len(df)} registros importação salvo")
```

---

## 5️⃣ INMET (Clima - Temperatura, Precipitação)

### Portal BDMEP (Download Manual)
```
1. Acesso: https://bdmep.inmet.gov.br/
2. Selecionar:
   - Estação: A001 (Salvador), A050 (São Paulo), etc.
   - Data: período desejado
   - Parâmetros: Tmed, Prec, DirVen
3. Download CSV
```

### Dados Abertos INMET (Automático)
```bash
# FTP com dados de estações automáticas
wget -r ftp://ftp1.inmet.gov.br/dane_estacoes_auto/ -P ./inmet_dados/
```

### Python - Processar INMET CSV
```python
import pandas as pd

# Após download do BDMEP
df = pd.read_csv('inmet_estacao_A001.csv', sep=';')

# Limpeza básica
df['data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
df['temperatura_max'] = pd.to_numeric(df['TMAX'], errors='coerce')
df['temperatura_min'] = pd.to_numeric(df['TMIN'], errors='coerce')
df['temperatura_media'] = pd.to_numeric(df['TMED'], errors='coerce')
df['precipitacao'] = pd.to_numeric(df['PREC'], errors='coerce')

# Agregação semanal
df_semanal = df.set_index('data').resample('W').agg({
    'temperatura_media': 'mean',
    'precipitacao': 'sum'
})
df_semanal.to_csv('clima_semanal.csv')
```

---

## 6️⃣ ANATEL (5G, Investimentos, Resoluções)

### Painéis de Dados Abertos
```
Cobertura 5G:
  https://informacoes.anatel.gov.br/paineis/acessibilidade
  
Investimentos:
  https://informacoes.anatel.gov.br/paineis/investimentos
  
Estatísticas Móvel:
  https://informacoes.anatel.gov.br/paineis/servicomovel
```

### Download FTP (Estatísticas Históricas)
```bash
# Estatísticas completas por período
wget ftp://ftp.anatel.gov.br/telefonia_publica/EstatisticasCompletas/ -r -P ./anatel_dados/
```

### API Dados Abertos ANATEL
```bash
# Listar datasets
curl "https://dados.anatel.gov.br/api/3/action/package_search?rows=100" | python -m json.tool
```

---

## 7️⃣ Frete Global (Drewry WCI, Freightos FBX)

### Web Scraping Drewry WCI
```python
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.drewry.co.uk/supply-chain-research/services/indices/world-container-index-(wci)"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Localizar tabela de dados
tables = soup.find_all('table')
for table in tables:
    df = pd.read_html(str(table))[0]
    if 'Date' in df.columns or 'Shanghai' in df.columns:
        df.to_csv('drewry_wci.csv', index=False)
        print("✓ WCI salvo")
        break
```

### Freightos Historical Data
```bash
# Download direto (arquivo públco)
wget "https://www.freightos.com/freight-resources/freight-rate-index/historical-data" -O freightos_historical.html
```

### Python - Processar FBX
```python
import pandas as pd
import requests

# Se disponível via CSV download
url = "https://www.freightos.com/freight-api/historical/"
# Requer API key comercial
```

---

## 8️⃣ RECEITA FEDERAL (Tributos, ICMS, PIS/COFINS)

### Consultar IN 1700/2017 (PIS/COFINS)
```bash
# Download direto PDF
curl -O "https://www.receita.gov.br/legislacao/ato-normativo/instrucao-normativa/2017/in-1700"
```

### Tabelas CONFAZ (ICMS por Estado)
```bash
# Acesso portal CONFAZ
curl "https://www1.confaz.fazenda.gov.br/confaz/public/cf" | grep -i "ICMS" | head -20
```

### Python - Tabela ICMS Hardcoded (Rápido)
```python
import pandas as pd

icms_rates = {
    'AC': 0.17, 'AL': 0.17, 'AP': 0.17, 'AM': 0.17,
    'BA': 0.18, 'CE': 0.17, 'DF': 0.17, 'ES': 0.17,
    'GO': 0.17, 'MA': 0.17, 'MT': 0.17, 'MS': 0.17,
    'MG': 0.18, 'PA': 0.17, 'PB': 0.17, 'PR': 0.17,
    'PE': 0.17, 'PI': 0.17, 'RJ': 0.20, 'RN': 0.17,
    'RS': 0.17, 'RO': 0.17, 'RR': 0.17, 'SC': 0.17,
    'SP': 0.18, 'SE': 0.17, 'TO': 0.17
}

df_icms = pd.Series(icms_rates).reset_index()
df_icms.columns = ['UF', 'ICMS_Rate']
df_icms.to_csv('icms_rates.csv', index=False)
print("✓ Tabela ICMS salva")
```

---

## 9️⃣ Trading Economics (Indicadores Agregados)

### Acesso Web (Free Tier)
```bash
# Exemplo: Câmbio Brasil (sem API key)
curl -s "https://www.tradingeconomics.com/brazil/currency" | grep -i "USD" | head -10
```

### API TE (Requer chave)
```bash
# Obter chave em: https://tradingeconomics.com/member/api/

API_KEY="sua_chave_aqui"
curl "https://api.tradingeconomics.com/data/indicator/GBPUSD?client=$API_KEY&format=JSON"
```

### Python - TE com Web Scraping
```python
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://tradingeconomics.com/brazil/indicators"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')

# Extrair indicadores
indicators = {}
for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >= 2:
        name = cells[0].text.strip()
        value = cells[1].text.strip()
        indicators[name] = value

df = pd.DataFrame(list(indicators.items()), columns=['Indicator', 'Value'])
df.to_csv('trading_economics_br.csv', index=False)
```

---

## 🔟 IMF (PPP, Risco Soberano)

### PPP Database
```bash
# API IMF DataMapper
curl "https://www.imf.org/external/datamapper/api/v1/PPPSH?countries=BR" | python -m json.tool
```

### Python - PPP
```python
import pandas as pd
import requests

url = "https://www.imf.org/external/datamapper/api/v1/PPPSH?countries=BR&comparisonCountries=US"
response = requests.get(url)
data = response.json()

if 'data' in data:
    df = pd.DataFrame(data['data']).T
    df.to_csv('imf_ppp_br.csv')
    print("✓ PPP IMF salvo")
```

---

## 1️⃣1️⃣ World Bank (LPI, Dados Econômicos)

### API World Bank
```bash
# Indicadores Brasil
curl "https://api.worldbank.org/v2/country/BR/indicator/NY.GDP.MKTP.CD?format=json&per_page=60" | python -m json.tool
```

### Python - World Bank
```python
import pandas as pd
import requests

# GDP Brasil
indicator = "NY.GDP.MKTP.CD"
url = f"https://api.worldbank.org/v2/country/BR/indicator/{indicator}?format=json&per_page=60"

response = requests.get(url)
data = response.json()

if len(data) > 1 and data[1]:
    records = []
    for record in data[1]:
        if record['value'] is not None:
            records.append({
                'year': record['date'],
                'value': float(record['value'])
            })
    
    df = pd.DataFrame(records)
    df.to_csv('world_bank_gdp_br.csv', index=False)
    print(f"✓ {len(df)} anos de GDP Brasil salvo")
```

---

## 🎯 SCRIPT ORQUESTRADOR COMPLETO

```python
#!/usr/bin/env python3
"""Script para baixar TODOS os dados de uma vez"""

import pandas as pd
import requests
import os
from datetime import datetime, timedelta

def download_all_data(output_dir='./dados_novacorrente'):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    results = {}
    
    # 1. IPCA
    print("[1/10] Baixando IPCA...")
    try:
        url = "https://apisidra.ibge.gov.br/values/t/1737/n1/v"
        df = pd.DataFrame(requests.get(url, timeout=10).json())
        df.to_csv(f"{output_dir}/01_IPCA_{timestamp}.csv")
        results['ipca'] = 'OK'
    except Exception as e:
        results['ipca'] = f"ERRO: {e}"
    
    # 2. Câmbio
    print("[2/10] Baixando Câmbio PTAX...")
    try:
        start = (datetime.now() - timedelta(days=365)).strftime('%m-%d-%Y')
        end = datetime.now().strftime('%m-%d-%Y')
        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinal=@dataFinal)?@dataInicial='{start}'&@dataFinal='{end}'&$top=10000&$orderby=dataHora%20asc&$format=json"
        data = requests.get(url, timeout=10).json()
        df = pd.DataFrame(data['value'])
        df.to_csv(f"{output_dir}/02_PTAX_{timestamp}.csv")
        results['ptax'] = 'OK'
    except Exception as e:
        results['ptax'] = f"ERRO: {e}"
    
    # 3. Selic
    print("[3/10] Baixando Selic...")
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"
        df = pd.DataFrame(requests.get(url, timeout=10).json())
        df.to_csv(f"{output_dir}/03_Selic_{timestamp}.csv")
        results['selic'] = 'OK'
    except Exception as e:
        results['selic'] = f"ERRO: {e}"
    
    # 4. PIB
    print("[4/10] Baixando PIB Trimestral...")
    try:
        url = "https://apisidra.ibge.gov.br/values/t/12462/n1/v"
        df = pd.DataFrame(requests.get(url, timeout=10).json())
        df.to_csv(f"{output_dir}/04_PIB_Trimestral_{timestamp}.csv")
        results['pib'] = 'OK'
    except Exception as e:
        results['pib'] = f"ERRO: {e}"
    
    # ... continuar para outros dados ...
    
    # Relatório final
    print("\n" + "="*50)
    print("RESUMO DE DOWNLOADS")
    print("="*50)
    for source, status in results.items():
        print(f"{source:20} → {status}")
    
    # Salvar log
    with open(f"{output_dir}/download_log_{timestamp}.txt", 'w') as f:
        for source, status in results.items():
            f.write(f"{source}: {status}\n")
    
    print(f"\n✅ Dados salvos em: {output_dir}")

if __name__ == "__main__":
    download_all_data()
```

---

## 📌 RESUMO RÁPIDO

| Dado | Comando Rápido |
|------|---|
| IPCA | `curl "https://apisidra.ibge.gov.br/values/t/1737/n1/v"` |
| Câmbio | `curl "https://olinda.bcb.gov.br/olinda/servico/PTAX/"` |
| Selic | `curl "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados"` |
| PIB | `curl "https://apisidra.ibge.gov.br/values/t/12462/n1/v"` |
| Comtrade | `curl "https://comtrade.un.org/api/get?..."` |
| Climate | Acesso via https://bdmep.inmet.gov.br/ (manual) |

---

**Gerado em:** 08 de Novembro, 2025  
**Próxima atualização:** Quando APIs mudarem
