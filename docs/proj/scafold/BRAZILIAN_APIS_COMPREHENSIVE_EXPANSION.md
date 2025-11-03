# 🇧🇷 BRAZILIAN PUBLIC APIS - COMPREHENSIVE EXPANSION
## Enriching ML Database with 25+ Public Data Sources

**Version:** 2.0  
**Date:** November 2025  
**Purpose:** Expand Nova Corrente ML database with comprehensive Brazilian metrics

---

## 📊 CURRENT APIS (Already Integrated)

### ✅ Currently Working
1. **BACEN** - Economic indicators (inflation, exchange, SELIC) ✅
2. **INMET** - Climate data (Salvador/BA) ✅
3. **ANATEL** - 5G expansion (partial) ✅
4. **IBGE** - Statistics (mentioned) ⚠️
5. **Kaggle** - Training datasets ✅
6. **Zenodo** - Research datasets ✅

---

## 🚀 NEW APIS TO INTEGRATE (20+ Sources)

### **TIER 1: GOVERNMENT ECONOMIC & TRADE DATA**

#### **1. BACEN - Extended Economic Series**
**Current:** Basic (inflation, exchange, SELIC)  
**Expand to:**
- IPCA-15 (mid-month inflation)
- IGP-M (General Price Index)
- PME (Employment Market)
- Credit Operations
- Foreign Exchange Reserves
- Currency Volatility Index
- Economic Activity Index (IBC-Br)

**API Endpoints:**
```python
# Extended BACEN series
BACEN_SERIES = {
    '433': 'IPCA',
    '433': 'IPCA-15', 
    '189': 'IGP-M',
    '24369': 'IBC-Br (Economic Activity)',
    '13621': 'Foreign Reserves (USD)',
    '11': 'SELIC Rate',
    '21619': 'USD/BRL Exchange',
    '11752': 'Credit Operations',
    '24364': 'Currency Volatility Index'
}
```

#### **2. IPEA Data (Instituto de Pesquisa Econômica Aplicada)**
**URL:** http://www.ipeadata.gov.br/api/odata4/  
**Free:** ✅ YES  
**No Key:** ✅ YES  
**Data Available:**
- Regional GDP
- Employment by sector
- Industrial production
- Construction indices
- Regional development indices

**Usage:**
```python
# IPEA API Example
url = "http://www.ipeadata.gov.br/api/odata4/Metadados"
response = requests.get(url)
```

#### **3. COMEX Stat (Foreign Trade Statistics)**
**URL:** https://www.gov.br/produtividade-e-comercio-exterior/pt-br/assuntos/comercio-exterior/estatisticas  
**Data Available:**
- Import/Export volumes
- Import/Export values by product
- Trade balance
- Port activity
- Customs delays

**Relevance:** ⭐⭐⭐⭐⭐ (Material procurement delays, lead time)

---

### **TIER 2: TRANSPORT & INFRASTRUCTURE**

#### **4. ANTT (Agência Nacional de Transportes Terrestres)**
**URL:** https://www.gov.br/antt/pt-br  
**Data Available:**
- Road freight volume
- Transport costs
- Logistics performance
- Highway maintenance schedules

**Relevance:** ⭐⭐⭐⭐⭐ (Impact on lead time, material delivery)

#### **5. ANAC (Agência Nacional de Aviação Civil)**
**URL:** https://www.anac.gov.br/dadosabertos/  
**Data Available:**
- Cargo transport volume
- Airport activity
- Air freight costs
- Flight delays

**Relevance:** ⭐⭐⭐⭐ (Critical material delivery, time-sensitive items)

#### **6. ANTAQ (Agência Nacional de Transportes Aquaviários)**
**URL:** https://www.gov.br/antaq/pt-br  
**Data Available:**
- Port activity
- Shipping volumes
- Container movements
- Port congestion

**Relevance:** ⭐⭐⭐⭐⭐ (Import materials, customs delays)

---

### **TIER 3: ENERGY & UTILITIES**

#### **7. ANEEL (Agência Nacional de Energia Elétrica)**
**URL:** https://www.aneel.gov.br/dados-abertos  
**Data Available:**
- Energy consumption by region
- Power outages
- Grid reliability
- Energy prices

**Relevance:** ⭐⭐⭐⭐ (Tower operations, equipment demand correlation)

#### **8. ANP (Agência Nacional do Petróleo)**
**URL:** https://www.gov.br/anp/pt-br/dados-abertos  
**Data Available:**
- Fuel prices by region
- Gasoline/diesel price trends
- Refinery operations
- Distribution network

**Relevance:** ⭐⭐⭐⭐ (Transport costs, field operations)

---

### **TIER 4: EMPLOYMENT & LABOR**

#### **9. CAGED (Cadastro Geral de Empregados e Desempregados)**
**URL:** https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas/caged  
**Data Available:**
- Employment by sector
- Hiring/firing trends
- Regional employment
- Skill availability

**Relevance:** ⭐⭐⭐⭐ (Labor availability for field operations)

#### **10. IBGE - Extended Series**
**URL:** https://apisidra.ibge.gov.br/  
**Current:** Basic statistics  
**Expand to:**
- PNAD (National Household Survey)
- PIM (Industrial Production)
- PMS (Monthly Service Survey)
- PMC (Monthly Commerce Survey)
- Regional GDP
- Construction indices

**IBGE Series:**
```python
IBGE_SERIES = {
    '3653': 'Industrial Production (PIM)',
    '8887': 'Service Revenue (PMS)',
    '8888': 'Retail Sales (PMC)',
    '5932': 'Employment (PNAD)',
    '5938': 'Unemployment Rate',
    '6612': 'GDP Regional (Bahia)'
}
```

---

### **TIER 5: CONSTRUCTION & INDUSTRIAL**

#### **11. CBIC (Câmara Brasileira da Indústria da Construção)**
**URL:** https://www.cbic.org.br/  
**Data Available:**
- Construction activity indices
- Material demand forecasts
- Regional construction growth
- Infrastructure investment

**Relevance:** ⭐⭐⭐⭐⭐ (Material demand correlation)

#### **12. ABINEE (Associação Brasileira da Indústria Elétrica e Eletrônica)**
**URL:** https://www.abinee.org.br/  
**Data Available:**
- Electrical equipment production
- Component demand
- Import/export of electrical materials

**Relevance:** ⭐⭐⭐⭐⭐ (Nova Corrente material category correlation)

---

### **TIER 6: REGIONAL & MUNICIPAL DATA**

#### **13. SEI-BA (Salvador/BA Government Portal)**
**URL:** https://www.sei.ba.gov.br/  
**Data Available:**
- Municipal economic indices
- Local infrastructure projects
- Regional development programs
- Municipal spending

**Relevance:** ⭐⭐⭐⭐ (Local operations context)

#### **14. FIESP/DIEESE (Industrial Federation)**
**URL:** https://www.fiesp.com.br/  
**Data Available:**
- Regional industrial production
- Manufacturing indices
- Supply chain activity

---

### **TIER 7: FINANCIAL & MARKET DATA**

#### **15. B3 (Brasil, Bolsa, Balcão)**
**URL:** https://www.b3.com.br/  
**Data Available:**
- Commodity futures
- Market volatility
- Sector performance indices

**Relevance:** ⭐⭐⭐ (Material cost forecasting)

#### **16. CMN (Conselho Monetário Nacional)**
**URL:** https://www.bcb.gov.br/estabilidadefinanceira/cmn  
**Data Available:**
- Monetary policy decisions
- Credit availability
- Financial sector stability

---

### **TIER 8: SPECIALIZED INDUSTRY DATA**

#### **17. TELEBRASIL (Telecom Association)**
**URL:** https://www.telebrasil.org.br/  
**Data Available:**
- Telecom sector investments
- Network expansion plans
- Industry trends
- Operator performance

**Relevance:** ⭐⭐⭐⭐⭐ (Nova Corrente industry context)

#### **18. ABRAS (Retail Association)**
**URL:** https://www.abras.com.br/  
**Data Available:**
- Retail sales by sector
- Consumer demand trends
- Inventory levels

---

### **TIER 9: QUALITY & STANDARDS**

#### **19. INMETRO (National Institute of Metrology)**
**URL:** https://www.gov.br/inmetro/pt-br  
**Data Available:**
- Equipment certifications
- Quality standards compliance
- Product recalls

**Relevance:** ⭐⭐⭐ (Material quality, supplier compliance)

---

### **TIER 10: ENVIRONMENTAL & SOCIAL**

#### **20. INPE (National Institute for Space Research)**
**URL:** http://www.inpe.br/  
**Data Available:**
- Satellite imagery
- Deforestation alerts
- Climate change indicators
- Environmental risks

**Relevance:** ⭐⭐⭐⭐ (Regional environmental factors)

#### **21. FGV Data (Fundação Getulio Vargas)**
**URL:** https://portal.fgv.br/en/research/institutes-centers/ibre/data  
**Data Available:**
- Economic confidence indices
- Consumer confidence
- Business confidence
- Regional economic indicators

---

### **TIER 11: LOGISTICS & SUPPLY CHAIN**

#### **22. DNIT (National Department of Infrastructure Transport)**
**URL:** https://www.gov.br/dnit/pt-br  
**Data Available:**
- Highway maintenance schedules
- Road closures
- Infrastructure projects
- Traffic patterns

**Relevance:** ⭐⭐⭐⭐⭐ (Delivery delays, lead time)

#### **23. Portos do Brasil**
**URL:** https://www.gov.br/antaq/pt-br/dados-abertos  
**Data Available:**
- Real-time port activity
- Container waiting times
- Port congestion
- Vessel arrivals/departures

**Relevance:** ⭐⭐⭐⭐⭐ (Import materials, customs delays)

---

### **TIER 12: TECHNOLOGY & INNOVATION**

#### **24. ANATEL - Extended Telecom Data**
**Current:** 5G expansion  
**Expand to:**
- Mobile subscriber growth by region
- Fixed broadband penetration
- Fiber expansion
- Spectrum allocation
- Tower density by region
- Network quality indicators

#### **25. CGI.br (Internet Steering Committee)**
**URL:** https://www.cgi.br/  
**Data Available:**
- Internet penetration by region
- Digital infrastructure
- Connectivity quality

---

## 📊 METRICS MATRIX - WHAT WE GET FROM EACH API

| API Source | Metrics Category | Features Generated | ML Impact |
|------------|-----------------|-------------------|-----------|
| **BACEN Extended** | Economic (8 metrics) | inflation_15, igp_m, ibc_br, reserves_usd, credit_ops | ⭐⭐⭐⭐⭐ |
| **IPEA** | Regional Economy (5 metrics) | regional_gdp, industrial_prod, construction_idx | ⭐⭐⭐⭐⭐ |
| **COMEX** | Trade (4 metrics) | imports_volume, exports_volume, trade_balance, port_activity | ⭐⭐⭐⭐⭐ |
| **ANTT** | Transport (3 metrics) | freight_volume, transport_cost, logistics_perf | ⭐⭐⭐⭐⭐ |
| **ANAC** | Air Transport (2 metrics) | cargo_volume, flight_delays | ⭐⭐⭐⭐ |
| **ANTAQ** | Maritime (3 metrics) | port_activity, shipping_vol, port_congestion | ⭐⭐⭐⭐⭐ |
| **ANEEL** | Energy (3 metrics) | energy_consumption, outages, grid_reliability | ⭐⭐⭐⭐ |
| **ANP** | Fuel (2 metrics) | fuel_price, refinery_ops | ⭐⭐⭐⭐ |
| **CAGED** | Employment (2 metrics) | employment_rate, hiring_trends | ⭐⭐⭐ |
| **IBGE Extended** | Statistics (6 metrics) | pim, pms, pmc, pnad, gdp_regional | ⭐⭐⭐⭐⭐ |
| **CBIC** | Construction (2 metrics) | construction_idx, material_demand | ⭐⭐⭐⭐⭐ |
| **ABINEE** | Electrical (2 metrics) | equipment_prod, component_demand | ⭐⭐⭐⭐⭐ |
| **SEI-BA** | Municipal (2 metrics) | municipal_econ, local_projects | ⭐⭐⭐ |
| **FIESP** | Industrial (2 metrics) | industrial_prod, manufacturing_idx | ⭐⭐⭐⭐ |
| **B3** | Financial (2 metrics) | commodity_futures, volatility | ⭐⭐⭐ |
| **TELEBRASIL** | Telecom (3 metrics) | sector_investment, network_expansion, trends | ⭐⭐⭐⭐⭐ |
| **ABRAS** | Retail (2 metrics) | retail_sales, consumer_demand | ⭐⭐⭐ |
| **INMETRO** | Quality (1 metric) | equipment_certifications | ⭐⭐⭐ |
| **INPE** | Environmental (2 metrics) | climate_indicators, env_risks | ⭐⭐⭐⭐ |
| **FGV** | Confidence (3 metrics) | econ_confidence, consumer_conf, business_conf | ⭐⭐⭐⭐ |
| **DNIT** | Infrastructure (3 metrics) | highway_maintenance, road_closures, traffic | ⭐⭐⭐⭐⭐ |
| **Portos** | Maritime (3 metrics) | port_congestion, container_wait, vessel_arrivals | ⭐⭐⭐⭐⭐ |
| **ANATEL Extended** | Telecom (5 metrics) | subscriber_growth, broadband, fiber, spectrum, tower_density | ⭐⭐⭐⭐⭐ |
| **CGI.br** | Internet (2 metrics) | internet_penetration, connectivity | ⭐⭐⭐⭐ |

**Total New Metrics: 70+**

---

## 🔧 IMPLEMENTATION GUIDE

### Step 1: API Collection Classes

```python
# backend/data/collectors/brazilian_apis_expanded.py

class ExpandedBrazilianAPICollector:
    """
    Comprehensive Brazilian API data collector
    Collects from 25+ public data sources
    """
    
    def __init__(self):
        self.data = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; NovaCorrenteML/1.0)'
        })
    
    # ===== ECONOMIC DATA =====
    def collect_bacen_extended(self):
        """Collect extended BACEN economic series"""
        # Implementation
        pass
    
    def collect_ipea_data(self):
        """Collect IPEA regional economic data"""
        # Implementation
        pass
    
    def collect_comex_data(self):
        """Collect foreign trade statistics"""
        # Implementation
        pass
    
    # ===== TRANSPORT & LOGISTICS =====
    def collect_antt_data(self):
        """Collect ANTT transport data"""
        # Implementation
        pass
    
    def collect_antaq_data(self):
        """Collect port activity data"""
        # Implementation
        pass
    
    # ... (25+ methods total)
    
    def collect_all(self):
        """Collect from all sources"""
        print("🚀 Starting comprehensive Brazilian data collection...")
        
        # Economic (3 sources)
        self.collect_bacen_extended()
        self.collect_ipea_data()
        self.collect_comex_data()
        
        # Transport (3 sources)
        self.collect_antt_data()
        self.collect_anac_data()
        self.collect_antaq_data()
        
        # Energy (2 sources)
        self.collect_aneel_data()
        self.collect_anp_data()
        
        # ... (continue for all sources)
        
        print(f"✅ Collected data from {len(self.data)} sources")
        return self.data
```

### Step 2: Database Schema Updates

See: `backend/data/Nova_Corrente_ML_Ready_DB_Expanded.sql`

New tables:
- `IndicadoresEconomicosExtended`
- `DadosTransporte`
- `DadosPortuarios`
- `DadosEnergia`
- `DadosEmprego`
- `IndicadoresConstrucao`
- `DadosTelecomunicacoesExtended`
- ... (15+ new tables)

### Step 3: Feature Engineering

New feature categories:
- **TRANSPORT** (10 features)
- **TRADE** (8 features)
- **ENERGY** (6 features)
- **EMPLOYMENT** (4 features)
- **CONSTRUCTION** (5 features)
- **INDUSTRIAL** (5 features)
- **LOGISTICS** (8 features)
- **REGIONAL** (6 features)

**Total New Features: 52+**

---

## 📋 QUICK START

```bash
# 1. Install dependencies
pip install requests pandas numpy beautifulsoup4 lxml

# 2. Run expanded collector
python backend/data/collectors/brazilian_apis_expanded.py

# 3. Load into database
python backend/data/loaders/load_expanded_metrics.py

# 4. Generate features
python backend/data/feature_engineering/expand_features.py
```

---

## ✅ INTEGRATION PRIORITY

### **Phase 1: Critical (Week 1)**
- ✅ BACEN Extended
- ✅ COMEX Stat
- ✅ ANTT
- ✅ ANTAQ
- ✅ IBGE Extended

### **Phase 2: High Value (Week 2)**
- ✅ IPEA
- ✅ CBIC
- ✅ ABINEE
- ✅ TELEBRASIL
- ✅ ANATEL Extended

### **Phase 3: Additional (Week 3)**
- ✅ All remaining sources

---

**Total Metrics: 70+**  
**Total Features: 52+**  
**API Sources: 25+**  
**All FREE Public APIs!** ✅

**CENTRALIZED REPORTS & CHANGELOG SYSTEM COMPLETE!**

