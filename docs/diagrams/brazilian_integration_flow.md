# 📊 Brazilian Integration Flow

## 📋 Overview

Brazilian dataset integration pipeline showing download, parsing, enrichment, and integration phases with 22 new features.

**Source File:** `docs\diagrams\brazilian_integration_flow.mmd`

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
    subgraph Download["📥 Download Phase"]
        D1[Download Script<br/>download_brazilian_datasets.py]
        D2[BGSMT Mobility<br/>Zenodo]
        D3[Anatel Municipal<br/>API/JSON]
        D4[IoT Market<br/>Summary JSON]
        D5[Fiber Expansion<br/>Market Data]
        D6[Operator Market<br/>Share Data]
    end
    
    subgraph Parse["⚙️ Parse Phase"]
        P1[Load JSON Files]
        P2[Convert to CSV]
        P3[Validate Schema]
        P4[Extract Features]
    end
    
    subgraph Enrich["🔧 Enrichment Phase"]
        E1[IoT Features<br/>9 features]
        E2[Fiber Features<br/>3 features]
        E3[Operator Features<br/>10 features]
    end
    
    subgraph Integration["📊 Integration Phase"]
        I1[Load Unified Dataset<br/>117,705 rows × 31 cols]
        I2[Merge IoT Data<br/>iot_timeline.csv]
        I3[Merge Fiber Data<br/>fiber_expansion.json]
        I4[Merge Operator Data<br/>operators_market.json]
        I5[Forward Fill<br/>Temporal Alignment]
    end
    
    subgraph Output["✅ Output"]
        O1[Enhanced Dataset<br/>117,705 rows × 56 cols]
        O2[22 Brazilian Features<br/>Added]
        O3[Ready for ML<br/>Training]
    end
    
    %% Data Flow
    D1 --> D2 & D3 & D4 & D5 & D6
    
    D2 -.Failed.-> D2
    D3 --> P1
    D4 --> P1
    D5 --> P1
    D6 --> P1
    
    P1 --> P2 --> P3 --> P4
    
    P4 --> E1 & E2 & E3
    
    E1 --> I2
    E2 --> I3
    E3 --> I4
    
    I1 --> I2 --> I3 --> I4 --> I5
    
    I5 --> O1 --> O2 --> O3
    
    %% State Evolution
    I1 -.31 cols.-> I2
    I2 -.31→40 cols.-> I3
    I3 -.40→43 cols.-> I4
    I4 -.43→53 cols.-> I5
    I5 -.53→56 cols.-> O1
    
    %% Styling
    classDef downloadStyle fill:#4A90E2,stroke:#357ABD,stroke-width:2px,color:#fff
    classDef parseStyle fill:#FFA07A,stroke:#EE9066,stroke-width:2px,color:#000
    classDef enrichStyle fill:#9370DB,stroke:#8A69D8,stroke-width:2px,color:#fff
    classDef integrationStyle fill:#7FBC7F,stroke:#6FA56F,stroke-width:2px,color:#000
    classDef outputStyle fill:#66C2A5,stroke:#52A88A,stroke-width:2px,color:#fff
    classDef errorStyle fill:#FB8072,stroke:#E06660,stroke-width:2px,color:#000
    
    class Download,D1,D2,D3,D4,D5,D6 downloadStyle
    class Parse,P1,P2,P3,P4 parseStyle
    class Enrich,E1,E2,E3 enrichStyle
    class Integration,I1,I2,I3,I4,I5 integrationStyle
    class Output,O1,O2,O3 outputStyle
    class D2 errorStyle
```

## 🔧 Components

1. **📥 Download Phase**
2. **⚙️ Parse Phase**
3. **🔧 Enrichment Phase**
4. **📊 Integration Phase**
5. **✅ Output**

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

