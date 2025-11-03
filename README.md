# 🎯 Nova Corrente - Demand Forecasting & Analytics System

## 🏆 **PRODUCTION READY FOR GRAND PRIX 2025**

A comprehensive demand forecasting and analytics platform for Nova Corrente, a telecom company in Salvador, Brazil.

---

## ✨ **KEY FEATURES**

### 📊 **Real-Time Analytics Dashboard**
- Interactive Brazil map (27 states)
- 5-tab analytics interface
- K-means clustering analysis
- LLM-powered prescriptive recommendations
- Mathematical formula calculators

### 🤖 **Advanced ML/AI**
- Ensemble forecasting (ARIMA + Prophet + LSTM)
- Equipment failure prediction
- Tower performance clustering
- Regional demand forecasting
- Cost optimization recommendations

### 📈 **Business Intelligence**
- Real-time KPIs (Stockout Rate, MAPE, Savings)
- Supplier performance tracking
- SLA penalty monitoring
- Regional inventory optimization
- Project status tracking

---

## 🚀 **QUICK START**

### Prerequisites
- Python 3.8+
- Node.js 18+
- Pandas, NumPy, scikit-learn

### Installation

**1. Clone Repository**
```bash
git clone <repository-url>
cd gran_prix
```

**2. Install Backend Dependencies**
```bash
pip install flask flask-cors pandas numpy scikit-learn
```

**3. Install Frontend Dependencies**
```bash
cd frontend
npm install
```

### Run Dashboard

**Terminal 1 - Backend API:**
```bash
python api_standalone.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open Browser:**
```
http://localhost:3000/main
```

---

## 📁 **PROJECT STRUCTURE**

```
gran_prix/
├── api_standalone.py          # Flask API with clustering & prescriptive endpoints
├── data/
│   ├── processed/
│   │   └── unified_dataset_with_factors.csv  # ⭐ Main dataset (27.25 MB, 118K rows)
│   ├── raw/                    # 📥 33 datasets with complete documentation
│   │   ├── [33 dataset folders]/
│   │   │   └── [DATASET_ID]_[SOURCE]_[CONTEXT]_technical_docs.md  # Technical documentation
│   │   ├── DATASETS_INDEX.md   # 📚 Complete index by category
│   │   └── DATASETS_EXECUTIVE_SUMMARY.md  # 📊 Executive summary
│   ├── training/               # 🎓 Training splits ready for ML
│   │   ├── unknown_train.csv   # ⭐ Main training (93,881 rows)
│   │   ├── unknown_test.csv    # Test split (23,471 rows)
│   │   └── metadata.json       # Training metadata
│   └── PROJECT_DATA_OVERVIEW.md  # 📊 Complete data overview
├── docs/
│   ├── proj/strategy/          # Strategic documentation
│   └── guides/                 # User guides
├── frontend/
│   ├── src/
│   │   ├── app/main/page.tsx              # Main dashboard
│   │   ├── components/
│   │   │   ├── Analytics.tsx              # 5-tab analytics interface
│   │   │   ├── ClusteringDashboard.tsx    # K-means clustering visualization
│   │   │   ├── PrescriptiveRecommendations.tsx  # AI recommendations
│   │   │   ├── FormulaExplainer.tsx       # Mathematical formulas
│   │   │   ├── ModelPerformanceDashboard.tsx    # ML model comparison
│   │   │   ├── InteractiveMap.tsx         # Brazil map
│   │   │   └── ...
│   │   └── lib/api.ts                     # API client
│   └── package.json
└── docs/
    └── BENCHMARK_REGISTRY.md              # Changelog & improvements
```

---

## 🔌 **API ENDPOINTS**

### Analytics
- `GET /api/kpis` - Real-time KPIs
- `GET /api/alerts` - Inventory alerts
- `GET /api/forecast/30days` - 30-day forecast

### Clustering
- `GET /api/clustering/equipment-failure` - Equipment failure clusters
- `GET /api/clustering/tower-performance` - Tower performance clusters

### Prescriptive
- `GET /api/prescriptive/recommendations` - LLM recommendations

### Geographic
- `GET /api/geographic/data` - Brazil regional data

### Models
- `GET /api/models/performance` - ML model comparison

---

## 📊 **DATASETS DOCUMENTATION**

### Complete Dataset Collection

**33 datasets** with full technical documentation:

| Document | Purpose | Location |
|----------|---------|----------|
| **DATASETS_INDEX.md** | 📚 Complete index by category | `data/raw/DATASETS_INDEX.md` |
| **DATASETS_EXECUTIVE_SUMMARY.md** | 📊 Executive summary & status | `data/raw/DATASETS_EXECUTIVE_SUMMARY.md` |
| **PROJECT_DATA_OVERVIEW.md** | 📈 Complete data overview | `data/PROJECT_DATA_OVERVIEW.md` |
| **DATASETS_COMPLETE_DOCUMENTATION_SUMMARY.md** | 📋 Complete documentation summary | `docs/DATASETS_COMPLETE_DOCUMENTATION_SUMMARY.md` |

**Dataset Categories:**
- ⭐ **Essential Datasets** (8) - Primary ML training
- 🇧🇷 **Brazilian Datasets** (8) - Brazilian market context
- 📡 **Anatel Datasets** (6) - Regulatory data
- 📦 **Kaggle Datasets** (7) - Public competition data
- 🔗 **GitHub Datasets** (2) - Open source data
- 📊 **Reference Datasets** (5) - Context only

**Key Datasets:**
- ✅ **Zenodo Milan Telecom** (116K rows) - ONLY public telecom + weather dataset
- ✅ **Brazilian Operators Structured** (B2B contracts) - Stable demand
- ✅ **Brazilian Demand Factors** (2,190 rows) - Integrated external factors
- ✅ **Kaggle Equipment Failure** (10K rows) - Predictive maintenance
- ✅ **GitHub Network Fault** (7.4K rows) - Telecom faults

**All datasets include:**
- ✅ Complete technical documentation (`*_technical_docs.md`)
- ✅ Source references & academic papers
- ✅ Data structure & schema details
- ✅ Use cases for Nova Corrente
- ✅ ML algorithm recommendations

**Quick Search:** All technical docs follow pattern:
```
[DATASET_ID]_[SOURCE]_[CONTEXT]_technical_docs.md
```

### Main Training Dataset

- **File:** `data/processed/unified_dataset_with_factors.csv`
- **Size:** 27.25 MB
- **Records:** 118,082 rows
- **Features:** 31 columns
- **Date Range:** 2013-11-01 to 2025-01-31 (11+ years)
- **Status:** ✅ Ready for ML training

**Training Splits:**
- `data/training/unknown_train.csv` - 93,881 rows (80% split)
- `data/training/unknown_test.csv` - 23,471 rows (20% split)

---

## 🎨 **ANALYTICS TABS**

### 1. Geographic
- Interactive Brazil map
- State-level inventory & supplier analytics
- Maintenance history visualization
- Project status tracking

### 2. Formulas
- LaTeX mathematical formulas
- Interactive PP & SS calculators
- MAPE, RMSE, MAE explanations

### 3. Clustering
- Equipment failure risk analysis
- Tower performance categorization
- K-means visualization
- Cluster statistics

### 4. Models
- ARIMA vs Prophet vs LSTM vs Ensemble
- Loss curves & feature importance
- Residual analysis
- Model comparison charts

### 5. Prescriptive
- LLM-powered recommendations
- Priority-based actions
- Impact & savings estimates
- Regional mapping

---

## 🛠️ **TECHNICAL STACK**

### Backend
- Flask API
- Pandas (data processing)
- NumPy (calculations)
- scikit-learn (K-means clustering)
- Python 3.8+

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- Recharts (visualizations)
- react-katex (LaTeX)
- D3.js (maps)

### ML/AI
- ARIMA (statistical)
- Prophet (Facebook forecasting)
- LSTM (deep learning)
- Ensemble models
- K-means clustering

---

## 📈 **PERFORMANCE METRICS**

### API Performance
- Health Check: <10ms
- Clustering: <500ms
- Prescriptive: <100ms
- Caching: 30-second TTL

### Code Quality
- ✅ Zero TypeScript errors
- ✅ Zero linting issues
- ✅ 100% type safety
- ✅ Production-grade quality

### Clustering Accuracy
- Equipment Failure: 3 risk clusters
- Tower Performance: 4 tiers
- Real-time processing

---

## 🎯 **BUSINESS VALUE**

### Insights
- **Predictive Maintenance:** Identify high-risk equipment
- **Tower Optimization:** 4-tier performance classification
- **Cost Reduction:** Prescriptive recommendations
- **Regional Analysis:** 27-state Brazil coverage
- **Mathematical Accuracy:** LaTeX formula explanations

### ROI
- Equipment Failure: 35% high-risk vs 2% low-risk
- Tower Performance: 4-tier classification
- Recommendations: 5 actionable items
- Clustering: Real-time 10k+ record analysis

---

## 📚 **DOCUMENTATION**

- `docs/BENCHMARK_REGISTRY.md` - Changelog & improvements
- `DASHBOARD_COMPLETE.md` - Complete feature overview
- `docs/MATH_COMPLETE_MASTER_REFERENCE.md` - Mathematical formulas

---

## 🤝 **CONTRIBUTING**

This project is for the Grand Prix 2025 demoday.

---

## 📄 **LICENSE**

[Specify License]

---

## 👥 **AUTHORS**

Nova Corrente Team  
Gran Prix 2025 - SENAI

---

## 🙏 **ACKNOWLEDGMENTS**

- Kaggle for open datasets
- GitHub open-source communities
- PrevIA_telecom frontend components

---

**Status: ✅ PRODUCTION READY**  
**Last Updated: November 1, 2025**  
**Version: 1.0.0**

---

*Built with ❤️ for Nova Corrente Telecom*
