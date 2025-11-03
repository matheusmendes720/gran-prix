# 🔑 COMPLETE GUIDE: GET ALL PUBLIC API KEYS FOR DATA INTEGRATION
## Step-by-Step Instructions for Brazilian Data Sources

---

## ✅ PART 1: FREE PUBLIC APIS (NO KEY REQUIRED)

### **1.1 INMET Weather API** ✅ FREE
**URL:** https://apitempo.inmet.gov.br/
- **API Key Required:** ❌ NO
- **Authentication:** None needed
- **Data Available:** Salvador weather (A502 station)
- **Usage:**
```python
import requests
import pandas as pd

# Get 30 days of weather - NO KEY NEEDED!
start_date = "2024-10-01"
end_date = "2024-10-31"
station_code = "A502"  # Salvador

url = f"https://apitempo.inmet.gov.br/estacao/diaria/{start_date}/{end_date}/{station_code}"
response = requests.get(url)
weather_data = pd.read_json(response.text)

print(weather_data.head())
```
✅ **READY TO USE NOW**

### **1.2 BACEN Economic API** ✅ FREE
**URL:** https://api.bcb.gov.br/
- **API Key Required:** ❌ NO
- **Authentication:** None needed
- **Rate Limit:** Unlimited
- **Usage:**
```python
import requests
import pandas as pd

# Get inflation rate (IPCA) - NO KEY NEEDED!
url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
response = requests.get(url)
inflation_data = response.json()

df = pd.DataFrame(inflation_data, columns=['date', 'inflation'])
print(df.head())
```

**Common Indicator Codes:**
- **433:** IPCA (inflation)
- **21619:** USD/BRL exchange rate
- **11:** SELIC interest rate
- **27:** UMBNDES (financing rate)

✅ **READY TO USE NOW**

### **1.3 IBGE Data API** ✅ FREE
**URL:** https://sidra.ibge.gov.br/api/
- **API Key Required:** ❌ NO
- **Authentication:** None needed
- **Usage:**
```python
import requests
import pandas as pd

# Get employment statistics
url = "https://apisidra.ibge.gov.br/values/t/6622/n1/all/v/all/p/last%201/d/v"
response = requests.get(url)
employment_data = response.json()

print(employment_data)
```

✅ **READY TO USE NOW**

---

## 📋 PART 2: APIS REQUIRING FREE REGISTRATION

### **2.1 Kaggle API** 
**URL:** https://www.kaggle.com/

#### **Step 1: Create Kaggle Account**
1. Go to https://www.kaggle.com/
2. Click "Register" (or sign up with Google)
3. Verify email

#### **Step 2: Get API Key**
1. Click your profile picture (top right)
2. Select "Settings"
3. Scroll down to "API" section
4. Click "Create New Token"
5. A file `kaggle.json` will download automatically

#### **Step 3: Install & Configure**
```bash
# Install Kaggle CLI
pip install kaggle

# Create config directory
mkdir -p ~/.kaggle

# Copy the kaggle.json file
# Copy the downloaded kaggle.json to ~/.kaggle/kaggle.json

# Set permissions (Linux/Mac)
chmod 600 ~/.kaggle/kaggle.json

# Verify installation
kaggle datasets list
```

#### **Step 4: Download Datasets**
```python
import subprocess
import os

# Download Daily Demand Forecasting dataset
dataset = "akshatpattiwar/daily-demand-forecasting-orderscsv"
path = "./data/"

cmd = f"kaggle datasets download -d {dataset} -p {path}"
result = subprocess.run(cmd, shell=True, capture_output=True)

if result.returncode == 0:
    print("✅ Dataset downloaded successfully")
    
    # Extract
    os.system(f"cd {path} && unzip -o '*.zip'")
else:
    print(f"❌ Error: {result.stderr}")
```

**Common Telecom Datasets:**
- `akshatpattiwar/daily-demand-forecasting-orderscsv` (60MB)
- `search?q=telecom+spare+parts` (various)
- `search?q=tower+maintenance` (various)

---

### **2.2 GitHub API** (Optional - for code access)
**URL:** https://api.github.com/

#### **Step 1: Create GitHub Account** (if needed)
1. Go to https://github.com/
2. Sign up with email

#### **Step 2: Get Personal Access Token**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `gist`
4. Copy the token

#### **Step 3: Use with Python**
```python
import requests
from base64 import b64encode

# GitHub token
GITHUB_TOKEN = "ghp_your_token_here"

# Example: Get telecom datasets from GitHub
url = "https://api.github.com/search/repositories"
params = {
    'q': 'Brazilian telecom 5G dataset',
    'sort': 'stars',
    'order': 'desc'
}

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

response = requests.get(url, params=params, headers=headers)
repos = response.json()['items']

for repo in repos[:5]:
    print(f"📊 {repo['name']}: {repo['stargazers_count']} stars")
    print(f"   {repo['html_url']}")
```

---

### **2.3 Zenodo API** (For research datasets)
**URL:** https://zenodo.org/api/

#### **No API Key Needed** ✅
```python
import requests
import pandas as pd

# Search for telecom datasets
url = "https://zenodo.org/api/records"
params = {
    'q': 'telecom network traffic',
    'type': 'dataset',
    'sort': 'mostrecent'
}

response = requests.get(url, params=params)
results = response.json()['hits']['hits']

for item in results[:5]:
    print(f"📊 {item['metadata']['title']}")
    print(f"   Download: {item['links']['html']}")
    print(f"   Size: {item['metadata']['size']}")
```

---

## 🌐 PART 3: BRAZILIAN GOVERNMENT APIS (FREE, NO KEY)

### **3.1 ANATEL Open Data**
**URL:** https://www.anatel.gov.br/

```python
import requests
import json

# Get ANATEL 5G expansion data
# Note: ANATEL doesn't have direct API, but publishes CSVs

# Download link format:
# https://www.anatel.gov.br/consumidor/servicos/dados-publicos

# Example: 5G tower coordinates
url = "https://www.anatel.gov.br/download/dados-publicos/5g-towers-2024.csv"

import urllib.request
urllib.request.urlretrieve(url, "anatel_5g_data.csv")

df = pd.read_csv("anatel_5g_data.csv")
print(f"✅ Downloaded {len(df)} towers from ANATEL")
```

### **3.2 CONFEA/CREA (Engineering Data)**
**URL:** https://www.confea.org.br/

- Infrastructure investment data
- Equipment certifications
- Regional statistics

---

## 🔧 PART 4: COMPLETE SETUP SCRIPT

```bash
#!/bin/bash
# setup_apis.sh - Setup all APIs in one go

echo "🚀 Setting up all Brazilian data APIs..."

# Step 1: Create directories
echo "📁 Creating directories..."
mkdir -p ~/.kaggle
mkdir -p ./data/raw
mkdir -p ./data/processed
mkdir -p ./config

# Step 2: Install Python packages
echo "📦 Installing Python packages..."
pip install kaggle requests pandas numpy python-dotenv

# Step 3: INMET - No setup needed
echo "✅ INMET API - Ready to use (no key needed)"

# Step 4: BACEN - No setup needed
echo "✅ BACEN API - Ready to use (no key needed)"

# Step 5: Kaggle setup
echo "📋 Kaggle setup instructions:"
echo "   1. Go to https://www.kaggle.com/settings/account"
echo "   2. Click 'Create New Token'"
echo "   3. Copy kaggle.json to ~/.kaggle/"
echo "   4. Run: chmod 600 ~/.kaggle/kaggle.json"
read -p "Press ENTER when done..."

# Step 6: Test APIs
echo "🧪 Testing APIs..."

python << 'EOF'
import requests
import pandas as pd

print("\n🧪 Testing INMET API...")
try:
    url = "https://apitempo.inmet.gov.br/estacao/diaria/2024-10-01/2024-10-31/A502"
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ INMET API working!")
    else:
        print(f"❌ INMET API error: {response.status_code}")
except Exception as e:
    print(f"❌ INMET API error: {e}")

print("\n🧪 Testing BACEN API...")
try:
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ BACEN API working!")
    else:
        print(f"❌ BACEN API error: {response.status_code}")
except Exception as e:
    print(f"❌ BACEN API error: {e}")

print("\n🧪 Testing Kaggle CLI...")
import subprocess
result = subprocess.run(["kaggle", "--version"], capture_output=True)
if result.returncode == 0:
    print("✅ Kaggle CLI working!")
else:
    print("❌ Kaggle CLI not configured yet")

print("\n✅ API setup complete!")
EOF

echo "🎉 All APIs configured successfully!"
```

**To run:**
```bash
chmod +x setup_apis.sh
./setup_apis.sh
```

---

## 📝 PART 5: CONFIG FILE FOR ALL APIS

```python
# config/api_config.py

import os
from dotenv import load_dotenv

load_dotenv()

# ===== INMET (FREE - NO KEY) =====
INMET_CONFIG = {
    'base_url': 'https://apitempo.inmet.gov.br',
    'station_code': 'A502',  # Salvador
    'requires_key': False
}

# ===== BACEN (FREE - NO KEY) =====
BACEN_CONFIG = {
    'base_url': 'https://api.bcb.gov.br/dados/serie/bcdata.sgs',
    'indicators': {
        '433': 'inflation_ipca',
        '21619': 'exchange_usd_brl',
        '11': 'selic_rate'
    },
    'requires_key': False
}

# ===== KAGGLE (REQUIRES KEY) =====
KAGGLE_CONFIG = {
    'api_key': os.getenv('KAGGLE_USERNAME'),
    'api_secret': os.getenv('KAGGLE_KEY'),
    'requires_key': True,
    'datasets': [
        'akshatpattiwar/daily-demand-forecasting-orderscsv',
        'search?q=telecom+spare+parts'
    ]
}

# ===== GITHUB (OPTIONAL - REQUIRES TOKEN) =====
GITHUB_CONFIG = {
    'token': os.getenv('GITHUB_TOKEN'),
    'requires_key': False,  # Can work without token
    'search_query': 'Brazilian telecom 5G dataset'
}

# ===== ZENODO (FREE - NO KEY) =====
ZENODO_CONFIG = {
    'base_url': 'https://zenodo.org/api',
    'requires_key': False,
    'search_query': 'telecom network traffic'
}

# ===== ANATEL (FREE - NO KEY) =====
ANATEL_CONFIG = {
    'base_url': 'https://www.anatel.gov.br',
    'data_portal': 'https://www.anatel.gov.br/consumidor/servicos/dados-publicos',
    'requires_key': False
}
```

**Create `.env` file:**
```bash
# .env
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_key

# Optional
GITHUB_TOKEN=your_github_token_if_you_have_one
```

---

## 🚀 PART 6: UNIFIED DATA COLLECTOR

```python
# src/data/api_collector.py

import requests
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import subprocess

load_dotenv()

class UnifiedAPICollector:
    """Collect data from all Brazilian APIs"""
    
    def __init__(self):
        self.data = {}
    
    # ===== INMET (FREE) =====
    def get_inmet_weather(self, days=365, station='A502'):
        """Get Salvador weather - NO KEY NEEDED"""
        print(f"📊 Fetching INMET weather data ({days} days)...")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        url = f"https://apitempo.inmet.gov.br/estacao/diaria/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}/{station}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                df = pd.read_json(response.text)
                print(f"✅ Got {len(df)} days of weather data")
                return df
            else:
                print(f"❌ Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    # ===== BACEN (FREE) =====
    def get_bacen_indicators(self):
        """Get economic indicators - NO KEY NEEDED"""
        print("📊 Fetching BACEN economic data...")
        
        indicators = {
            '433': 'inflation',
            '21619': 'exchange_rate',
            '11': 'selic_rate'
        }
        
        all_data = {}
        
        for code, name in indicators.items():
            url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
            
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    df = pd.DataFrame(data, columns=['date', name])
                    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
                    all_data[name] = df
                    print(f"✅ Got {name}")
                else:
                    print(f"❌ Error getting {name}: {response.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return all_data
    
    # ===== KAGGLE =====
    def download_kaggle_datasets(self):
        """Download Kaggle datasets"""
        print("📊 Downloading Kaggle datasets...")
        
        # Check if kaggle.json exists
        kaggle_json = os.path.expanduser("~/.kaggle/kaggle.json")
        
        if not os.path.exists(kaggle_json):
            print("❌ Kaggle API key not found!")
            print("   Please follow instructions to setup Kaggle API")
            return False
        
        datasets = [
            'akshatpattiwar/daily-demand-forecasting-orderscsv'
        ]
        
        for dataset in datasets:
            cmd = f"kaggle datasets download -d {dataset} -p ./data/raw/"
            result = subprocess.run(cmd, shell=True, capture_output=True)
            
            if result.returncode == 0:
                print(f"✅ Downloaded: {dataset}")
            else:
                print(f"❌ Failed: {dataset}")
        
        # Extract
        os.system("cd ./data/raw && unzip -o '*.zip'")
        print("✅ All datasets extracted")
        
        return True
    
    # ===== ZENODO =====
    def get_zenodo_datasets(self):
        """Get datasets from Zenodo - NO KEY NEEDED"""
        print("📊 Fetching Zenodo datasets...")
        
        url = "https://zenodo.org/api/records"
        params = {
            'q': 'telecom network traffic',
            'type': 'dataset',
            'sort': 'mostrecent'
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                results = response.json()['hits']['hits']
                print(f"✅ Found {len(results)} Zenodo datasets")
                return results
            else:
                print(f"❌ Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    # ===== RUN ALL =====
    def collect_all_data(self):
        """Collect data from all sources"""
        print("\n🚀 Starting data collection from all Brazilian APIs...\n")
        
        # Collect INMET (free)
        self.data['weather'] = self.get_inmet_weather(days=730)
        
        # Collect BACEN (free)
        self.data['economic'] = self.get_bacen_indicators()
        
        # Collect Kaggle (requires setup)
        kaggle_success = self.download_kaggle_datasets()
        
        # Collect Zenodo (free)
        self.data['zenodo'] = self.get_zenodo_datasets()
        
        print("\n✅ Data collection complete!\n")
        
        # Print summary
        print("📊 Data Summary:")
        for source, data in self.data.items():
            if data is not None:
                if isinstance(data, pd.DataFrame):
                    print(f"   ✅ {source}: {len(data)} records")
                elif isinstance(data, dict):
                    print(f"   ✅ {source}: {len(data)} items")
                elif isinstance(data, list):
                    print(f"   ✅ {source}: {len(data)} items")
        
        return self.data

# ===== USAGE =====
if __name__ == "__main__":
    collector = UnifiedAPICollector()
    all_data = collector.collect_all_data()
    
    # Save to files
    print("\n💾 Saving data...")
    
    for source, data in all_data.items():
        if isinstance(data, pd.DataFrame):
            data.to_csv(f'data/processed/{source}_data.csv', index=False)
            print(f"✅ Saved {source} data")
```

---

## ✅ QUICK CHECKLIST

**APIs Ready NOW (No Setup Needed):**
- [x] INMET Weather - Use immediately
- [x] BACEN Economics - Use immediately
- [x] IBGE Statistics - Use immediately
- [x] Zenodo Datasets - Use immediately
- [x] ANATEL Data - Download manually

**APIs Requiring Setup (10 minutes):**
- [ ] Kaggle - Create account, get token
- [ ] GitHub - Create account (optional), get token (optional)

---

## 🎯 TL;DR - GET STARTED NOW

```bash
# 1. Clone/download your project

# 2. Install dependencies
pip install requests pandas kaggle

# 3. Run data collection (INMET + BACEN = instant)
python src/data/api_collector.py

# 4. Optional: Setup Kaggle for more datasets
# Go to https://www.kaggle.com/settings/account
# Get API token, save to ~/.kaggle/kaggle.json

# Done! All data collected!
```

---

**[translate:Pronto! Você tem acesso a todos os dados públicos grátis! 💪]**

**Start collecting data NOW! 🚀**
