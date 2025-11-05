# 📊 Nova Corrente System Architecture

## 📋 Overview

Complete system architecture showing data flow from sources through preprocessing, models, evaluation, visualization, and deployment.

**Source File:** `docs\diagrams\nova_corrente_system_architecture.mmd`

**Generated:** 2025-11-05 00:36:46

---

## 🎨 Diagram

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
    'primaryColor':'#1e1e1e',
    'primaryTextColor':'#fff',
    'lineColor':'#888'
}}}%%
flowchart TD
    subgraph DataSources["📥 Data Sources"]
        DS1[Raw Datasets<br/>15+ sources]
        DS2[Brazilian Data<br/>IoT, Fiber, Operators]
        DS3[External Factors<br/>Climate, Economic, Regulatory]
    end
    
    subgraph Preprocessing["⚙️ Preprocessing Pipeline"]
        P1[Download<br/>download_datasets.py]
        P2[Preprocess<br/>preprocess_datasets.py]
        P3[Add External Factors<br/>add_external_factors.py]
        P4[Brazilian Integration<br/>preprocess_brazilian_data.py]
        P5[Merge<br/>merge_datasets.py]
    end
    
    subgraph TrainingData["📊 Training Datasets"]
        TD1[unknown_train.csv<br/>93,881 rows × 56 cols]
        TD2[CONN-001_train.csv<br/>584 rows × 56 cols]
        TD3[unified_dataset<br/>117,705 rows × 56 cols]
    end
    
    subgraph Models["🤖 ML Models"]
        M1[Prophet<br/>Seasonality + Trends]
        M2[LSTM<br/>Deep Learning]
        M3[XGBoost<br/>Feature Interactions]
        M4[Ensemble<br/>Meta-Learner]
    end
    
    subgraph Evaluation["📈 Evaluation"]
        E1[RMSE<br/>Root Mean Squared Error]
        E2[MAPE<br/>Mean Absolute % Error]
        E3[R²<br/>Coefficient of Determination]
    end
    
    subgraph Visualization["📊 Visualization Dashboard"]
        V1[Plotly Dash<br/>Interactive Charts]
        V2[D3.js Map<br/>Geographic Analysis]
        V3[Brazilian Metrics<br/>IoT, Fiber, Operators]
    end
    
    subgraph Deployment["🚀 Production"]
        D1[API Endpoint<br/>FastAPI]
        D2[Model Serving<br/>TensorFlow Serving]
        D3[Monitoring<br/>Performance Metrics]
    end
    
    %% Data Flow
    DS1 --> P1
    DS2 --> P4
    DS3 --> P3
    
    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
    
    P5 --> TD1 & TD2 & TD3
    
    TD1 --> M1 & M2 & M3
    TD2 --> M1 & M2 & M3
    
    M1 & M2 & M3 --> M4
    
    M4 --> E1 & E2 & E3
    
    E1 & E2 & E3 --> V1 & V2 & V3
    
    V1 & V2 & V3 --> D1 & D2 & D3
    
    %% Styling
    classDef sourceStyle fill:#4A90E2,stroke:#357ABD,stroke-width:2px,color:#fff
    classDef processStyle fill:#7FBC7F,stroke:#6FA56F,stroke-width:2px,color:#000
    classDef dataStyle fill:#66C2A5,stroke:#52A88A,stroke-width:2px,color:#fff
    classDef modelStyle fill:#FFA07A,stroke:#EE9066,stroke-width:2px,color:#000
    classDef evalStyle fill:#9370DB,stroke:#8A69D8,stroke-width:2px,color:#fff
    classDef vizStyle fill:#FF6B9D,stroke:#EE5A8B,stroke-width:2px,color:#000
    classDef deployStyle fill:#FFD700,stroke:#E6C200,stroke-width:2px,color:#000
    
    class DataSources,DS1,DS2,DS3 sourceStyle
    class Preprocessing,P1,P2,P3,P4,P5 processStyle
    class TrainingData,TD1,TD2,TD3 dataStyle
    class Models,M1,M2,M3,M4 modelStyle
    class Evaluation,E1,E2,E3 evalStyle
    class Visualization,V1,V2,V3 vizStyle
    class Deployment,D1,D2,D3 deployStyle
```

## 🔧 Components

1. **📥 Data Sources**
2. **⚙️ Preprocessing Pipeline**
3. **📊 Training Datasets**
4. **🤖 ML Models**
5. **📈 Evaluation**
6. **📊 Visualization Dashboard**
7. **🚀 Production**

## 📖 Usage

This diagram can be viewed in:

- **GitHub/GitLab**: Automatically rendered when viewing this file
- **VS Code**: Install the 'Markdown Preview Mermaid Support' extension
- **Obsidian**: Native Mermaid support
- **Documentation Sites**: MkDocs, Docusaurus, etc. with Mermaid plugin

---

## 🔗 Related Documents

- [Documentation Index](docs/INDEX_MASTER_NAVIGATION_PT_BR.md)
- [Diagrams Directory](docs/diagrams/)
- [Project Strategy](docs/proj/strategy/)
- [Roadmaps](docs/proj/roadmaps/)

