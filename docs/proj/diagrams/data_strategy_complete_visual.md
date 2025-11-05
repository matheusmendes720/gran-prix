# 🎨 Nova Corrente Data Strategy - Complete Visual Breakdown

**Comprehensive visual documentation of the data modeling strategy and diagnostic analysis**

---

## 📋 Overview

This document provides a complete visual breakdown of:
1. **Problem Diagnosis** - Root cause analysis of 87% MAPE
2. **Star Schema Architecture** - 12-table relational design
3. **Implementation Roadmap** - 4-week timeline to <15% MAPE
4. **Data Enrichment Tiers** - 3-tier priority system
5. **Business Impact Flow** - From diagnosis to results

---

## 🔍 Diagram 1: Problem Diagnosis & Solution Flow

**Purpose:** High-level overview of problem → solution → impact

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888',
    'secondaryColor':'#2d2d2d',
    'tertiaryColor':'#1a1a1a'
}}}%%

flowchart TD
    subgraph Problem["🔍 PROBLEM DIAGNOSIS"]
        P1[Current State:<br/>MAPE 87.27%]
        P2[Target:<br/>MAPE <15%]
        P3[Gap:<br/>72 percentage points]
        
        P1 --> P3
        P2 --> P3
        
        P4[Root Cause Analysis]
        P3 --> P4
        
        P5[96.3% External<br/>Data Missing]
        P6[Only 73 Features<br/>3.7% Coverage]
        P7[Incomplete ML<br/>Training Signals]
        
        P4 --> P5
        P4 --> P6
        P4 --> P7
    end
    
    subgraph CurrentData["📊 CURRENT DATA INVENTORY"]
        CD1[Nova Corrente ERP<br/>4,207 records]
        CD2[dadosSuprimentos.xlsx<br/>3 sheets]
        CD3[ML Dataset<br/>2,539 records]
        CD4[33 External Datasets<br/>75% ready]
        
        CD2 --> CD1
        CD1 --> CD3
        CD4 -.available.-> CD3
    end
    
    subgraph Solution["💡 SOLUTION ARCHITECTURE"]
        S1[Star Schema Design<br/>12 Tables Total]
        
        S2[6 Core Tables]
        S3[6 External Tables]
        
        S1 --> S2
        S1 --> S3
        
        S4[Fact_Demand_Daily]
        S5[Dim_Calendar]
        S6[Dim_Part]
        S7[Dim_Site]
        S8[Dim_Supplier]
        S9[Dim_Maintenance]
        
        S2 --> S4
        S2 --> S5
        S2 --> S6
        S2 --> S7
        S2 --> S8
        S2 --> S9
        
        S10[Fact_Climate]
        S11[Fact_Economic]
        S12[Fact_Regulatory]
        S13[Fact_Fault]
        S14[Fact_SLA]
        S15[Fact_Supply_Chain]
        
        S3 --> S10
        S3 --> S11
        S3 --> S12
        S3 --> S13
        S3 --> S14
        S3 --> S15
    end
    
    subgraph Impact["📈 EXPECTED IMPACT"]
        I1[Week 1:<br/>Climate Data]
        I2[MAPE: 87% → 62-72%<br/>-15 to -25%]
        
        I3[Week 2:<br/>Economic + Regulatory]
        I4[MAPE: 62-72% → 27-42%<br/>-10 to -20%]
        
        I5[Week 3:<br/>Faults + Retrain]
        I6[MAPE: 27-42% → 17-27%<br/>-10 to -15%]
        
        I7[Week 4:<br/>Optimization]
        I8[MAPE: <15%<br/>✅ TARGET ACHIEVED]
        
        I1 --> I2 --> I3 --> I4 --> I5 --> I6 --> I7 --> I8
    end
    
    Problem --> CurrentData
    CurrentData --> Solution
    Solution --> Impact
    
    classDef problemStyle fill:#FB8072,stroke:#E06660,stroke-width:2px,color:#000
    classDef dataStyle fill:#4A90E2,stroke:#357ABD,stroke-width:2px,color:#fff
    classDef solutionStyle fill:#7FBC7F,stroke:#6FA56F,stroke-width:2px,color:#000
    classDef impactStyle fill:#66C2A5,stroke:#52A88A,stroke-width:2px,color:#fff
    
    class Problem,P1,P2,P3,P4,P5,P6,P7 problemStyle
    class CurrentData,CD1,CD2,CD3,CD4 dataStyle
    class Solution,S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15 solutionStyle
    class Impact,I1,I2,I3,I4,I5,I6,I7,I8 impactStyle
```

### Key Insights

- **Root Cause:** 96.3% of external data missing
- **Current Coverage:** Only 3.7% (73 features out of potential 90+)
- **Solution:** Star schema with 12 tables (6 core + 6 external)
- **Timeline:** 4 weeks to achieve <15% MAPE

---

## 🏗️ Diagram 2: Star Schema Architecture

**Purpose:** Detailed view of relational data model and feature engineering

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888',
    'secondaryColor':'#2d2d2d',
    'tertiaryColor':'#1a1a1a'
}}}%%

flowchart TD
    subgraph CoreFact["⭐ CORE FACT TABLE"]
        F[Fact_Demand_Daily<br/>4,207+ records<br/>Grain: site-part-day-order]
        
        FM1[quantidade TARGET]
        FM2[unit_cost]
        FM3[total_cost]
        FM4[lead_time_days]
        
        F --> FM1
        F --> FM2
        F --> FM3
        F --> FM4
    end
    
    subgraph Dimensions["🔷 DIMENSION TABLES"]
        D1[Dim_Calendar<br/>4,400 days<br/>2013-2025]
        D2[Dim_Part<br/>872 parts<br/>ABC classified]
        D3[Dim_Site<br/>191 sites<br/>268 mappings]
        D4[Dim_Supplier<br/>468 suppliers<br/>Lead time stats]
        D5[Dim_Maintenance<br/>2 types<br/>Prev/Corr]
        D6[Dim_Region<br/>Brazilian<br/>IBGE codes]
    end
    
    subgraph ExternalFacts["🌐 EXTERNAL ENRICHMENT TABLES"]
        E1[Fact_Climate_Daily<br/>Zenodo Milan 116K<br/>Weather/Precipitation]
        E2[Fact_Economic_Daily<br/>Demand Factors 2,190<br/>Inflation/FX/GDP]
        E3[Fact_Regulatory_Daily<br/>Operators 290<br/>5G/Spectrum/B2B]
        E4[Fact_Fault_Events<br/>Network Fault 7,389<br/>Predictive signals]
        E5[Fact_SLA_Daily<br/>Derived<br/>Downtime/Penalties]
        E6[Fact_Supply_Chain<br/>Logistics 3,204<br/>Lead time events]
    end
    
    subgraph APIs["🔌 EXTERNAL APIS"]
        A1[INMET API<br/>Climate Brazil]
        A2[BACEN API<br/>Economic Brazil]
        A3[ANATEL API<br/>Regulatory Brazil]
    end
    
    F -.date_id.-> D1
    F -.part_id.-> D2
    F -.site_id.-> D3
    F -.supplier_id.-> D4
    F -.maint_type_id.-> D5
    D3 -.region_id.-> D6
    
    D1 -.join.-> E1
    D3 -.join.-> E1
    D1 -.join.-> E2
    D1 -.join.-> E3
    D3 -.join.-> E3
    D6 -.join.-> E3
    D1 -.join.-> E4
    D3 -.join.-> E4
    D1 -.join.-> E5
    D3 -.join.-> E5
    D1 -.join.-> E6
    D2 -.join.-> E6
    D4 -.join.-> E6
    
    A1 -.feeds.-> E1
    A2 -.feeds.-> E2
    A3 -.feeds.-> E3
    
    subgraph MLFeatures["🤖 ML FEATURE ENGINEERING"]
        ML1[90+ Features<br/>100% Coverage]
        
        MLF1[Temporal: 25<br/>Calendar features]
        MLF2[Climate: 14<br/>Weather signals]
        MLF3[Economic: 6<br/>Market indicators]
        MLF4[Regulatory: 10<br/>5G/Spectrum]
        MLF5[Lag: 16<br/>Moving averages]
        MLF6[Derived: 19<br/>Risk scores]
        
        ML1 --> MLF1
        ML1 --> MLF2
        ML1 --> MLF3
        ML1 --> MLF4
        ML1 --> MLF5
        ML1 --> MLF6
    end
    
    CoreFact --> MLFeatures
    Dimensions --> MLFeatures
    ExternalFacts --> MLFeatures
    
    classDef factStyle fill:#FDB462,stroke:#E89D4F,stroke-width:3px,color:#000
    classDef dimStyle fill:#4A90E2,stroke:#357ABD,stroke-width:2px,color:#fff
    classDef extStyle fill:#7FBC7F,stroke:#6FA56F,stroke-width:2px,color:#000
    classDef apiStyle fill:#B3B3B3,stroke:#999,stroke-width:2px,color:#000
    classDef mlStyle fill:#BC80BD,stroke:#A366A4,stroke-width:2px,color:#fff
    
    class CoreFact,F,FM1,FM2,FM3,FM4 factStyle
    class Dimensions,D1,D2,D3,D4,D5,D6 dimStyle
    class ExternalFacts,E1,E2,E3,E4,E5,E6 extStyle
    class APIs,A1,A2,A3 apiStyle
    class MLFeatures,ML1,MLF1,MLF2,MLF3,MLF4,MLF5,MLF6 mlStyle
```

### Architecture Components

**Core Fact Table:**
- `Fact_Demand_Daily` - Central transaction table with quantidade (target variable)

**Dimension Tables (6):**
- Calendar, Part (ABC), Site, Supplier, Maintenance Type, Region

**External Enrichment Tables (6):**
- Climate, Economic, Regulatory, Fault, SLA, Supply Chain

**Feature Engineering:**
- 90+ features total (vs. current 73)
- 100% coverage (vs. current 3.7%)

---

## 📅 Diagram 3: 4-Week Implementation Roadmap

**Purpose:** Timeline view of progressive MAPE reduction

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888',
    'secondaryColor':'#2d2d2d',
    'tertiaryColor':'#1a1a1a'
}}}%%

timeline
    title 🚀 4-Week Implementation Roadmap to <15% MAPE
    
    section Week 1: Foundation + Climate
        Day 1-2 : Create Dimensions
                : Run 01_create_star_schema_dimensions.py
                : Validate 5 dimension tables
        Day 3-5 : Climate Integration
                : Load Zenodo Milan Telecom (116K)
                : Create Fact_Climate_Daily
                : Fill 96.3% missing data
        Impact  : MAPE 87% → 62-72%
                : -15 to -25% reduction
    
    section Week 2: Economic + Regulatory
        Day 1-2 : Economic Data
                : Load Brazilian Demand Factors (2,190)
                : Setup BACEN API
                : Create Fact_Economic_Daily
        Day 3-5 : Regulatory Data
                : Load Brazilian Operators (290)
                : Parse ANATEL datasets
                : Create Fact_Regulatory_Daily
        Impact  : MAPE 62-72% → 27-42%
                : -35 to -45% cumulative
    
    section Week 3: Faults + Retraining
        Day 1-3 : Fault Events
                : Load GitHub Network Fault (7,389)
                : Train predictive maintenance model
                : Create Fact_Fault_Events
        Day 4-5 : Model Retraining
                : Regenerate ML dataset (100% coverage)
                : Train XGBoost, RF, LSTM
                : Validate improvements
        Impact  : MAPE 27-42% → 17-27%
                : -50 to -60% cumulative
    
    section Week 4: Optimization
        Day 1-3 : Fine-tuning
                : ABC-based model selection
                : Hyperparameter optimization (Optuna)
                : Ensemble optimization
        Day 4-5 : Validation
                : Test set evaluation
                : Performance report
                : Documentation
        Impact  : MAPE <15% ✅
                : -72+ point total reduction
```

### Implementation Phases

**Week 1:** Foundation + Climate Data
- Create all dimension tables
- Integrate Zenodo Milan Telecom weather data
- Expected MAPE: 87% → 62-72%

**Week 2:** Economic + Regulatory Data
- Add Brazilian economic indicators
- Integrate 5G/spectrum regulatory data
- Expected MAPE: 62-72% → 27-42%

**Week 3:** Fault Events + Retraining
- Add predictive maintenance signals
- Retrain all models with complete features
- Expected MAPE: 27-42% → 17-27%

**Week 4:** Optimization & Validation
- ABC-based model selection
- Hyperparameter tuning
- **Target MAPE: <15%** ✅

---

## 🎯 Diagram 4: Data Enrichment Priority Tiers

**Purpose:** Detailed view of 3-tier enrichment strategy with expected impacts

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'primaryBorderColor':'#444',
    'lineColor':'#888',
    'secondaryColor':'#2d2d2d',
    'tertiaryColor':'#1a1a1a'
}}}%%

flowchart TB
    subgraph Current["📊 CURRENT STATE"]
        CS1[Nova Corrente<br/>4,207 records]
        CS2[73 Features<br/>Engineered]
        CS3[3.7% External<br/>Coverage]
        CS4[MAPE: 87.27%<br/>EPI Family]
        
        CS1 --> CS2 --> CS3 --> CS4
    end
    
    subgraph Tier1["🔥 TIER 1: CRITICAL (Week 1-2)"]
        T1H[Expected Impact:<br/>-35 to -60% MAPE]
        
        T1A[Fact_Climate_Daily]
        T1A1[Zenodo Milan<br/>116,257 records]
        T1A2[INMET API<br/>Real-time]
        T1A3[Impact: -15 to -25%]
        
        T1B[Fact_Economic_Daily]
        T1B1[Demand Factors<br/>2,190 records]
        T1B2[BACEN API<br/>Daily updates]
        T1B3[Impact: -10 to -15%]
        
        T1C[Fact_Regulatory_Daily]
        T1C1[Operators<br/>290 B2B contracts]
        T1C2[ANATEL<br/>Spectrum data]
        T1C3[Impact: -10 to -20%]
        
        T1H --> T1A & T1B & T1C
        T1A --> T1A1 & T1A2 --> T1A3
        T1B --> T1B1 & T1B2 --> T1B3
        T1C --> T1C1 & T1C2 --> T1C3
    end
    
    subgraph Tier2["⚡ TIER 2: HIGH (Week 3-4)"]
        T2H[Expected Impact:<br/>-15 to -25% MAPE]
        
        T2A[Fact_Fault_Events]
        T2A1[Network Fault<br/>7,389 records]
        T2A2[Equipment Failure<br/>10,000 records]
        T2A3[Impact: -10 to -15%]
        
        T2B[Fact_Supply_Chain]
        T2B1[Logistics<br/>3,204 records]
        T2B2[Supply Chain<br/>91,000 records]
        T2B3[Impact: -5 to -10%]
        
        T2H --> T2A & T2B
        T2A --> T2A1 & T2A2 --> T2A3
        T2B --> T2B1 & T2B2 --> T2B3
    end
    
    subgraph Tier3["📋 TIER 3: MEDIUM (Week 5-6)"]
        T3H[Expected Impact:<br/>-8 to -18% MAPE]
        
        T3A[ABC Classification]
        T3A1[Pareto Analysis<br/>872 parts]
        T3A2[Model Selection<br/>A/B/C strategies]
        T3A3[Impact: -3 to -8%]
        
        T3B[Fact_SLA_Daily]
        T3B1[Derived from<br/>Operators]
        T3B2[Criticality<br/>Scoring]
        T3B3[Impact: -5 to -10%]
        
        T3H --> T3A & T3B
        T3A --> T3A1 & T3A2 --> T3A3
        T3B --> T3B1 & T3B2 --> T3B3
    end
    
    subgraph Target["🎯 TARGET STATE"]
        TS1[External Coverage:<br/>100%]
        TS2[90+ Features<br/>Complete]
        TS3[MAPE: <15%<br/>✅ ACHIEVED]
        TS4[Forecast Accuracy:<br/>>85%]
        
        TS1 --> TS2 --> TS3 --> TS4
    end
    
    Current --> Tier1
    Tier1 --> Tier2
    Tier2 --> Tier3
    Tier3 --> Target
    
    classDef currentStyle fill:#FB8072,stroke:#E06660,stroke-width:2px,color:#000
    classDef tier1Style fill:#E74C3C,stroke:#C0392B,stroke-width:3px,color:#fff
    classDef tier2Style fill:#F39C12,stroke:#D68910,stroke-width:2px,color:#000
    classDef tier3Style fill:#3498DB,stroke:#2874A6,stroke-width:2px,color:#fff
    classDef targetStyle fill:#2ECC71,stroke:#27AE60,stroke-width:3px,color:#000
    
    class Current,CS1,CS2,CS3,CS4 currentStyle
    class Tier1,T1H,T1A,T1A1,T1A2,T1A3,T1B,T1B1,T1B2,T1B3,T1C,T1C1,T1C2,T1C3 tier1Style
    class Tier2,T2H,T2A,T2A1,T2A2,T2A3,T2B,T2B1,T2B2,T2B3 tier2Style
    class Tier3,T3H,T3A,T3A1,T3A2,T3A3,T3B,T3B1,T3B2,T3B3 tier3Style
    class Target,TS1,TS2,TS3,TS4 targetStyle
```

### Tier Breakdown

**🔥 Tier 1: CRITICAL (Immediate Priority)**
- Climate Data (Zenodo Milan 116K + INMET API)
- Economic Data (Demand Factors 2,190 + BACEN API)
- Regulatory Data (Operators 290 + ANATEL)
- **Expected Impact:** -35 to -60% MAPE
- **Timeline:** Week 1-2

**⚡ Tier 2: HIGH (Secondary Priority)**
- Fault Events (Network Fault 7,389 + Equipment Failure 10K)
- Supply Chain (Logistics 3,204 + Supply Chain 91K)
- **Expected Impact:** -15 to -25% MAPE
- **Timeline:** Week 3-4

**📋 Tier 3: MEDIUM (Optimization)**
- ABC Classification (Pareto analysis of 872 parts)
- SLA Metrics (Derived from operator contracts)
- **Expected Impact:** -8 to -18% MAPE
- **Timeline:** Week 5-6

---

## 📊 Business Impact Summary

### Current vs. Target State

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| **MAPE** | 87.27% | <15% | **-72+ points** |
| **Forecast Accuracy** | 12.73% | >85% | **+72 points** |
| **External Data Coverage** | 3.7% | 100% | **+96.3 points** |
| **Features Engineered** | 73 | 90+ | **+17+ features** |
| **Stockout Rate** | 15-20% | <5% | **-70%** |
| **Excess Inventory Cost** | Baseline | Optimized | **-20-30%** |
| **SLA Compliance** | 60-70% | >95% | **+25-35 points** |

### Expected Cumulative Impact

- **Week 1:** -15 to -25% MAPE (Climate)
- **Week 2:** -35 to -45% cumulative (+ Economic/Regulatory)
- **Week 3:** -50 to -60% cumulative (+ Faults)
- **Week 4:** **-72+ points total** (Optimization) → **<15% MAPE** ✅

---

## 🔧 Implementation Scripts

### Ready to Execute

1. **`scripts/01_create_star_schema_dimensions.py`** ✅
   - Creates 5 dimension tables
   - ABC classification
   - Cyclical features
   - Lead time statistics

2. **`scripts/02_create_fact_demand_daily.py`** (Planned)
   - Load dadosSuprimentos.xlsx
   - Join with dimensions
   - Calculate derived measures

3. **`scripts/03_integrate_climate_data.py`** (Planned)
   - Merge Zenodo Milan Telecom
   - Create Fact_Climate_Daily
   - Generate weather features

4. **`scripts/04_create_ml_master_dataset.py`** (Planned)
   - Join all fact and dimension tables
   - Generate 90+ ML features
   - Create train/val/test splits

---

## 📚 Related Documentation

- **[COMPREHENSIVE_DATA_MODELING_STRATEGY.md](../roadmaps/COMPREHENSIVE_DATA_MODELING_STRATEGY.md)** - Full technical specs
- **[EXECUTIVE_ENRICHMENT_SUMMARY.md](../roadmaps/EXECUTIVE_ENRICHMENT_SUMMARY.md)** - Business justification
- **[QUICK_START_GUIDE.md](../roadmaps/QUICK_START_GUIDE.md)** - Action plan
- **[COMPLETE_CHAT_HISTORY_ANALYSIS.md](../roadmaps/COMPLETE_CHAT_HISTORY_ANALYSIS.md)** - Full context
- **[README_ROADMAPS.md](../roadmaps/README_ROADMAPS.md)** - Documentation index

---

## ✅ Summary

| Aspect | Status |
|--------|--------|
| **Problem Diagnosed** | ✅ 96.3% missing external data |
| **Solution Designed** | ✅ Star schema with 12 tables |
| **Roadmap Created** | ✅ 4-week timeline |
| **Tiers Prioritized** | ✅ 3-tier system |
| **Scripts Ready** | ✅ 1 complete, 3 planned |
| **Expected Result** | ✅ MAPE <15% achievable |

---

**🎨 Visual framework applied from:** `VISUAL_DOCUMENTATION_FRAMEWORK.md`  
**Created:** 2025-11-05  
**Status:** ✅ **COMPLETE - READY FOR TEAM REVIEW**

---

**Nova Corrente Grand Prix SENAI**  
**From 87% MAPE to <15% in 4 Weeks - Visual Strategy** 🚀
