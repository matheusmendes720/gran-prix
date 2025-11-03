# 🗺️ ROADMAP COMPLETO: SISTEMAS PREDITIVOS PARA NOVA CORRENTE
## Arquitetura Visual, Diagramas Mermaid & Expansão Operacional

---

## 📋 ÍNDICE

1. [Visão Geral do Sistema](#visao-geral)
2. [Arquitetura ML/DL Completa](#arquitetura)
3. [Expansão por Área Operacional](#areas-operacionais)
4. [Roadmap de Implementação](#roadmap)
5. [Datasets por Área](#datasets)
6. [Mermaid Diagrams](#diagramas)

---

<a name="visao-geral"></a>
# 1. 🎯 VISÃO GERAL DO SISTEMA

## 1.1 Mapa Mental da Solução Completa

```mermaid
mindmap
  root((Nova Corrente<br/>Sistema Preditivo))
    Áreas Operacionais
      Gestão de Estoque
        Demanda de Materiais
        Reorder Points
        Safety Stock
      Manutenção Preventiva
        Previsão de Falhas
        Agendamento Otimizado
        Disponibilidade de Equipamento
      Logística & Transporte
        Roteirização
        Tempo de Viagem
        Disponibilidade de Equipes
      Planejamento de RH
        Demanda de Técnicos
        Escalas de Férias
        Turnover
      Análise Financeira
        Forecasting de Receita
        Custos Operacionais
        Budget Planning
      Expansão 5G
        Demanda de Novos Sites
        Capacidade de Rede
        Investimentos
    Modelos ML/DL
      Time Series
        ARIMA/SARIMA
        Prophet
        LSTM
      Ensemble
        XGBoost
        Random Forest
        Gradient Boosting
      Híbridos
        ARIMA + LSTM
        Prophet + XGBoost
        Multi-Model Stack
    Fatores Externos
      Climáticos
        Temperatura
        Precipitação
        Umidade
        Tempestades
      Econômicos
        Taxa de Câmbio
        Inflação IPCA
        PIB
        Greves
      Regulatórios
        Anatel Auctions
        Spectrum Allocation
        Políticas 5G
      Tecnológicos
        5G Expansion
        IoT Growth
        Fiber Migration
    Outputs
      Alertas
        Reorder Point
        Falha Equipamento
        SLA Risk
      Relatórios
        Daily Dashboard
        Weekly Reports
        Monthly Analysis
      Recomendações
        Compras
        Manutenções
        Escalas
```

---

## 1.2 Pipeline End-to-End

```mermaid
flowchart TD
    A[📥 Coleta de Dados] --> B[🧹 Pré-Processamento]
    B --> C[🔍 Feature Engineering]
    C --> D{🤖 Seleção de Modelo}
    D -->|Time Series| E[📈 ARIMA/SARIMA]
    D -->|Eventos/Sazonalidade| F[🔮 Prophet]
    D -->|Não-Linear| G[🧠 LSTM/GRU]
    D -->|Features Tabulares| H[🌲 XGBoost]
    E --> I[🔀 Ensemble]
    F --> I
    G --> I
    H --> I
    I --> J[✅ Validação]
    J -->|MAPE < 15%| K[🚀 Deploy]
    J -->|MAPE >= 15%| C
    K --> L[📊 Monitoramento]
    L -->|Drift Detectado| M[🔄 Retrain]
    M --> C
    L -->|Performance OK| N[📢 Alertas & Reports]
    
    style A fill:#e1f5ff
    style K fill:#c3f0ca
    style J fill:#fff4cc
    style N fill:#ffe0f0
```

---

<a name="arquitetura"></a>
# 2. 🏗️ ARQUITETURA ML/DL COMPLETA

## 2.1 Comparação de Modelos

```mermaid
graph TB
    subgraph "🔵 Time Series Clássicos"
        A1[ARIMA] -->|Pros| A2["✅ Simples<br/>✅ Rápido<br/>✅ Interpretável"]
        A1 -->|Cons| A3["❌ Linear<br/>❌ Estacionariedade"]
        A1 -->|Use Case| A4["Baseline<br/>Séries simples"]
        
        B1[SARIMA] -->|Pros| B2["✅ Sazonalidade<br/>✅ Ciclos"]
        B1 -->|Cons| B3["❌ Complexidade<br/>❌ Tuning difícil"]
        B1 -->|Use Case| B4["Consumo semanal<br/>Padrões sazonais"]
    end
    
    subgraph "🟢 ML Avançado"
        C1[Prophet] -->|Pros| C2["✅ Múltiplas sazonalidades<br/>✅ Eventos/Feriados<br/>✅ Missing data"]
        C1 -->|Cons| C3["❌ Outliers sensível<br/>❌ Menos flexível"]
        C1 -->|Use Case| C4["Demanda com eventos<br/>Holidays + 5G auctions"]
        
        D1[XGBoost] -->|Pros| D2["✅ Features externas<br/>✅ Non-linear<br/>✅ Fast"]
        D1 -->|Cons| D3["❌ Não sequencial<br/>❌ Hyperparameters"]
        D1 -->|Use Case| D4["Ensemble<br/>Features climáticas"]
    end
    
    subgraph "🔴 Deep Learning"
        E1[LSTM] -->|Pros| E2["✅ Longo prazo<br/>✅ Non-linear<br/>✅ Flexível"]
        E1 -->|Cons| E3["❌ Dados grandes<br/>❌ Lento<br/>❌ Overfitting"]
        E1 -->|Use Case| E4["Padrões complexos<br/>Multi-variate"]
        
        F1[GRU] -->|Pros| F2["✅ Mais rápido LSTM<br/>✅ Menos params"]
        F1 -->|Cons| F3["❌ Mesmos do LSTM"]
        F1 -->|Use Case| F4["Alternativa LSTM<br/>Menos dados"]
    end
    
    style A1 fill:#cce5ff
    style C1 fill:#d4f1d4
    style E1 fill:#ffd4d4
```

---

## 2.2 Arquitetura LSTM Detalhada

```mermaid
graph LR
    subgraph "LSTM Cell"
        X[Input x_t] --> FG[Forget Gate<br/>σ]
        X --> IG[Input Gate<br/>σ]
        X --> CT[Cell Tilde<br/>tanh]
        X --> OG[Output Gate<br/>σ]
        
        H_prev[h_t-1] --> FG
        H_prev --> IG
        H_prev --> CT
        H_prev --> OG
        
        C_prev[C_t-1] -->|×| FG
        FG --> |f_t ⊙ C_t-1| COMB[+]
        IG --> |×| CT
        CT --> |i_t ⊙ C̃_t| COMB
        COMB --> C_t[C_t<br/>Cell State]
        
        C_t --> |tanh| OG
        OG -->|×| H_t[h_t<br/>Output]
        C_t -.->|Next timestep| C_prev
        H_t -.->|Next timestep| H_prev
    end
    
    style FG fill:#ffe6e6
    style IG fill:#e6f3ff
    style OG fill:#e6ffe6
    style C_t fill:#fff4e6
```

### Equações LSTM

**Forget Gate:**
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

**Input Gate:**
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$
$$\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$$

**Cell State:**
$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

**Output:**
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$
$$h_t = o_t \odot \tanh(C_t)$$

---

## 2.3 Arquitetura Híbrida (ARIMA + LSTM + XGBoost)

```mermaid
flowchart TD
    DATA[📊 Historical Data<br/>2+ anos diários] --> DECOMP{Decomposição}
    
    DECOMP -->|Linear Component| ARIMA[📈 ARIMA Model]
    DECOMP -->|Residuals| LSTM[🧠 LSTM Model]
    DECOMP -->|External Features| XGB[🌲 XGBoost]
    
    ARIMA --> |Ŷ_linear| ENSEMBLE[🔀 Weighted Ensemble]
    LSTM --> |Ŷ_residual| ENSEMBLE
    XGB --> |Ŷ_external| ENSEMBLE
    
    ENSEMBLE --> |w1×Ŷ_linear + w2×Ŷ_residual + w3×Ŷ_external| FINAL[✅ Final Prediction]
    
    FINAL --> EVAL{Validation<br/>MAPE < 15%?}
    EVAL -->|Yes| DEPLOY[🚀 Production]
    EVAL -->|No| TUNE[⚙️ Hyperparameter Tuning]
    TUNE --> ARIMA
    TUNE --> LSTM
    TUNE --> XGB
    
    style ARIMA fill:#cce5ff
    style LSTM fill:#ffd4d4
    style XGB fill:#d4f1d4
    style FINAL fill:#ffe6cc
```

### Fórmula do Ensemble

$$\hat{Y}_{final} = w_1 \hat{Y}_{ARIMA} + w_2 \hat{Y}_{LSTM} + w_3 \hat{Y}_{XGBoost}$$

onde $w_1 + w_2 + w_3 = 1$ e pesos são otimizados por validação cruzada.

**Exemplo de pesos:**
- $w_1 = 0.3$ (ARIMA - componente linear)
- $w_2 = 0.4$ (LSTM - padrões não-lineares)
- $w_3 = 0.3$ (XGBoost - features externas)

---

<a name="areas-operacionais"></a>
# 3. 📦 EXPANSÃO POR ÁREA OPERACIONAL

## 3.1 Gestão de Estoque (Já Desenvolvido)

```mermaid
graph TD
    A[📊 Consumo Histórico] --> B[🤖 Modelo Preditivo]
    B --> C[📈 Demanda Prevista]
    C --> D{Cálculo Reorder Point}
    D --> E[PP = Demanda × Lead Time + SS]
    E --> F{Estoque Atual ≤ PP?}
    F -->|Sim| G[🔴 ALERTA COMPRA]
    F -->|Não| H[✅ Monitorar]
    G --> I[📧 Notificar Procurement]
    I --> J[📋 Gerar Recomendação]
    J --> K["Compre X unidades<br/>em Y dias"]
```

### Métricas de Sucesso

| Métrica | Baseline | Target | Atual |
|---------|----------|--------|-------|
| Ruptura de estoque | 15/mês | <5/mês | - |
| Excesso de estoque | R$ 200k | <R$ 100k | - |
| MAPE previsão | - | <15% | - |
| Lead time utilization | 60% | >85% | - |

---

## 3.2 Manutenção Preventiva (Novo)

```mermaid
flowchart TD
    subgraph "Inputs"
        A1[🔧 Histórico Manutenções]
        A2[📊 Telemetria Equipamentos]
        A3[🌡️ Dados Climáticos]
        A4[📅 Schedule Atual]
    end
    
    A1 --> B[🧠 ML Model]
    A2 --> B
    A3 --> B
    A4 --> B
    
    B --> C{Previsão de Falha}
    C -->|Probabilidade > 80%| D[🔴 ALERTA PREVENTIVO]
    C -->|50-80%| E[🟡 MONITORAR]
    C -->|< 50%| F[✅ OK]
    
    D --> G[📋 Priorizar Manutenção]
    E --> H[🔍 Inspeção Agendada]
    
    G --> I[Otimizar Rota Técnico]
    G --> J[Garantir Disponibilidade Peças]
    G --> K[Alocar Equipe]
    
    style D fill:#ffcccc
    style E fill:#fff4cc
    style F fill:#ccffcc
```

### Features para Modelo de Falha

| Feature | Tipo | Importância |
|---------|------|-------------|
| Dias desde última manutenção | Numérica | Alta |
| Número de falhas prévias | Numérica | Alta |
| Temperatura média últimos 7 dias | Numérica | Média |
| Precipitação acumulada | Numérica | Média |
| Idade do equipamento | Numérica | Alta |
| Tipo de equipamento | Categórica | Alta |
| Região (clima) | Categórica | Média |

### Modelo Recomendado

**Random Forest Classifier** para previsão de falha binária:

$$P(\text{Falha}|X) = \frac{1}{T} \sum_{t=1}^T \mathbb{1}[\text{Árvore}_t(X) = \text{Falha}]$$

onde $T$ = 500 árvores.

---

## 3.3 Logística & Roteirização (Novo)

```mermaid
graph TD
    subgraph "Inputs Diários"
        I1[🏢 Sites com Manutenção]
        I2[👷 Técnicos Disponíveis]
        I3[🚗 Veículos & Localização]
        I4[🛣️ Trânsito Real-time]
        I5[⏰ Janelas de Tempo]
    end
    
    I1 --> OPT[⚙️ Otimizador de Rotas]
    I2 --> OPT
    I3 --> OPT
    I4 --> OPT
    I5 --> OPT
    
    OPT --> ALGO{Algoritmo}
    ALGO -->|< 20 sites| EXACT[Exact Solution<br/>Branch & Bound]
    ALGO -->|20-100 sites| HEUR[Heurísticas<br/>Simulated Annealing]
    ALGO -->|> 100 sites| META[Metaheurísticas<br/>Genetic Algorithm]
    
    EXACT --> OUT[📍 Rotas Otimizadas]
    HEUR --> OUT
    META --> OUT
    
    OUT --> VIS[📱 App para Técnicos]
    OUT --> DASH[📊 Dashboard Central]
    
    style OPT fill:#ffe6cc
    style OUT fill:#ccffcc
```

### Problema de Roteirização (VRP - Vehicle Routing Problem)

**Formulação Matemática:**

**Objetivo:** Minimizar distância total

$$\min \sum_{i=1}^n \sum_{j=1}^n \sum_{k=1}^K c_{ij} x_{ijk}$$

sujeito a:

**Restrições:**

1. Cada site visitado exatamente uma vez:
$$\sum_{j=1}^n \sum_{k=1}^K x_{ijk} = 1, \quad \forall i$$

2. Cada veículo sai do depot:
$$\sum_{j=1}^n x_{0jk} = 1, \quad \forall k$$

3. Conservação de fluxo:
$$\sum_{i=1}^n x_{ijk} - \sum_{i=1}^n x_{jik} = 0, \quad \forall j, k$$

4. Capacidade do veículo:
$$\sum_{i=1}^n d_i \sum_{j=1}^n x_{ijk} \leq Q_k, \quad \forall k$$

onde:
- $x_{ijk}$: binário (1 se arco $i \to j$ usado por veículo $k$)
- $c_{ij}$: custo/distância de $i$ para $j$
- $d_i$: demanda do site $i$ (tempo de manutenção)
- $Q_k$: capacidade (tempo disponível) do veículo $k$

---

## 3.4 Planejamento de RH (Novo)

```mermaid
flowchart TD
    A[📊 Histórico Demanda] --> B[🤖 Previsão Demanda]
    B --> C[Técnicos Necessários]
    
    D[👷 Técnicos Atuais] --> E{Gap Analysis}
    C --> E
    
    E -->|Deficit| F[🔴 ALERTA: Contratar]
    E -->|Surplus| G[🟡 ATENÇÃO: Redistribuir]
    E -->|Balanced| H[✅ OK]
    
    F --> I[📋 Plano de Contratação]
    G --> J[📋 Plano de Redistribuição]
    
    I --> K[Timeline: 30-60 dias]
    J --> L[Timeline: 15-30 dias]
    
    M[📅 Férias Planejadas] --> N{Impacto na Capacidade}
    N -->|> 20% redução| O[🔴 ALERTA Férias]
    N -->|10-20%| P[🟡 Ajustar Escala]
    N -->|< 10%| Q[✅ OK]
    
    O --> R[Bloquear Férias<br/>ou Contratar Temporários]
    
    style F fill:#ffcccc
    style G fill:#fff4cc
    style H fill:#ccffcc
```

### Modelo de Demanda de RH

**Fórmula:**

$$\text{Técnicos Necessários} = \frac{\text{Horas de Manutenção Previstas}}{\text{Horas Disponíveis por Técnico}}$$

$$T_{needed} = \frac{D \times t_{avg}}{H_{avail} \times U}$$

onde:
- $D$: Demanda de manutenções (sites/mês)
- $t_{avg}$: Tempo médio por manutenção (horas)
- $H_{avail}$: Horas disponíveis por técnico/mês (160h)
- $U$: Utilização alvo (80%)

**Exemplo:**
- $D = 500$ sites/mês
- $t_{avg} = 4$ horas
- $H_{avail} = 160$ horas
- $U = 0.8$

$$T_{needed} = \frac{500 \times 4}{160 \times 0.8} = \frac{2000}{128} = 15.6 \approx 16 \text{ técnicos}$$

---

## 3.5 Análise Financeira (Novo)

```mermaid
graph LR
    subgraph "Revenue Forecasting"
        A1[Contratos Atuais] --> B1[💰 Receita Recorrente]
        A2[Pipeline Comercial] --> B2[💼 Receita Futura]
        A3[Churn Rate] --> B3[📉 Receita Perdida]
        
        B1 --> C1[Total Revenue]
        B2 --> C1
        B3 -->|Subtrai| C1
    end
    
    subgraph "Cost Forecasting"
        D1[Custos Operacionais] --> E1[💵 OPEX]
        D2[Investimentos] --> E2[💸 CAPEX]
        D3[Materiais & Logística] --> E3[📦 Supply Chain]
        
        E1 --> F1[Total Cost]
        E2 --> F1
        E3 --> F1
    end
    
    C1 --> G[EBITDA Projetado]
    F1 -->|Subtrai| G
    
    G --> H{Análise de Cenários}
    H -->|Otimista| I1[+15% Growth]
    H -->|Base| I2[Current Trend]
    H -->|Pessimista| I3[-10% Contraction]
    
    style C1 fill:#ccffcc
    style F1 fill:#ffcccc
    style G fill:#ffe6cc
```

### Modelo de Revenue Forecasting

**Receita Mensal:**

$$R_t = R_{recorrente} + R_{novos\_contratos} - R_{churn}$$

**Com crescimento:**

$$R_t = R_0 (1 + g)^t (1 - c)$$

onde:
- $R_0$: Receita inicial
- $g$: Taxa de crescimento mensal
- $c$: Taxa de churn mensal
- $t$: Meses

**Exemplo:**
- $R_0 = $ R$ 5.000.000
- $g = 0.05$ (5% crescimento)
- $c = 0.02$ (2% churn)
- $t = 12$ meses

$$R_{12} = 5.000.000 \times (1.05)^{12} \times (1 - 0.02)^{12}$$
$$R_{12} = 5.000.000 \times 1.796 \times 0.785 = R\$ 7.050.000$$

---

## 3.6 Expansão 5G (Novo)

```mermaid
flowchart TD
    subgraph "Análise de Demanda"
        A1[📶 Cobertura Atual] --> B1[Gap Analysis]
        A2[📊 Densidade Populacional] --> B1
        A3[💼 Demanda Empresarial] --> B1
        A4[🏢 Competição] --> B1
    end
    
    B1 --> C{Sites Prioritários}
    
    C -->|Alta Prioridade| D1[🔴 P1: < 3 meses]
    C -->|Média Prioridade| D2[🟡 P2: 3-6 meses]
    C -->|Baixa Prioridade| D3[🟢 P3: > 6 meses]
    
    D1 --> E[Análise de Viabilidade]
    D2 --> E
    D3 --> E
    
    E --> F{Critérios}
    F -->|Técnico| G1[Capacidade Rede]
    F -->|Financeiro| G2[ROI > 12 meses]
    F -->|Regulatório| G3[Licenças Anatel]
    F -->|Operacional| G4[Disponibilidade RH]
    
    G1 --> H{Aprovado?}
    G2 --> H
    G3 --> H
    G4 --> H
    
    H -->|Sim| I[✅ Projeto Aprovado]
    H -->|Não| J[❌ Rejeitado]
    
    I --> K[🏗️ Cronograma Implantação]
    
    style D1 fill:#ffcccc
    style D2 fill:#fff4cc
    style D3 fill:#ccffcc
```

### Modelo de Priorização de Sites

**Score de Prioridade:**

$$P_{score} = w_1 D + w_2 V + w_3 C - w_4 R$$

onde:
- $D$: Demanda (população + empresas)
- $V$: Viabilidade técnica (0-10)
- $C$: Competição (sites concorrentes)
- $R$: Risco (regulatório + operacional)
- $w_i$: Pesos (somam 1)

**Exemplo:**
- $w_1 = 0.4$, $D = 8$ (alta demanda)
- $w_2 = 0.3$, $V = 7$ (viável)
- $w_3 = 0.2$, $C = 5$ (competição média)
- $w_4 = 0.1$, $R = 3$ (risco baixo)

$$P_{score} = 0.4(8) + 0.3(7) + 0.2(5) - 0.1(3)$$
$$P_{score} = 3.2 + 2.1 + 1.0 - 0.3 = 6.0$$

**Classificação:**
- $P_{score} \geq 7$: Alta prioridade (P1)
- $5 \leq P_{score} < 7$: Média prioridade (P2)
- $P_{score} < 5$: Baixa prioridade (P3)

---

<a name="roadmap"></a>
# 4. 🗓️ ROADMAP DE IMPLEMENTAÇÃO

## 4.1 Timeline Geral (6 Meses)

```mermaid
gantt
    title Implementação Sistema Preditivo Nova Corrente
    dateFormat  YYYY-MM-DD
    
    section Fase 1: Fundação
    Coleta Dados Históricos    :2025-11-01, 30d
    Setup Infraestrutura        :2025-11-15, 30d
    Data Cleaning & EDA         :2025-12-01, 20d
    
    section Fase 2: Estoque (Prioridade)
    Modelo Demanda Materiais    :2025-12-15, 30d
    Reorder Point System        :2026-01-01, 20d
    Dashboard & Alertas         :2026-01-15, 15d
    Pilot Test (5 materiais)    :2026-02-01, 30d
    
    section Fase 3: Manutenção
    Modelo Previsão Falhas      :2026-01-15, 30d
    Integração Telemetria       :2026-02-01, 20d
    Priorização Automática      :2026-02-15, 15d
    
    section Fase 4: Logística
    Algoritmo Roteirização      :2026-02-01, 30d
    Integração Trânsito         :2026-02-15, 20d
    App Técnicos                :2026-03-01, 30d
    
    section Fase 5: RH & Financeiro
    Modelo Demanda RH           :2026-03-01, 20d
    Revenue Forecasting         :2026-03-15, 20d
    Dashboards Executivos       :2026-04-01, 15d
    
    section Fase 6: 5G & Scale
    Modelo Expansão 5G          :2026-04-01, 30d
    Integração ANATEL           :2026-04-15, 20d
    Sistema Completo            :2026-05-01, 30d
```

---

## 4.2 Priorização por ROI

```mermaid
graph TD
    A[Áreas Operacionais] --> B{Análise ROI}
    
    B -->|ROI > 300%| C1[🟢 PRIORIDADE 1]
    B -->|ROI 150-300%| C2[🟡 PRIORIDADE 2]
    B -->|ROI < 150%| C3[🔴 PRIORIDADE 3]
    
    C1 --> D1[✅ Gestão de Estoque<br/>ROI: 400%<br/>Payback: 2 meses]
    C1 --> D2[✅ Manutenção Preventiva<br/>ROI: 350%<br/>Payback: 3 meses]
    
    C2 --> E1[⚡ Logística<br/>ROI: 200%<br/>Payback: 5 meses]
    C2 --> E2[⚡ RH Planning<br/>ROI: 180%<br/>Payback: 6 meses]
    
    C3 --> F1[⏳ Análise Financeira<br/>ROI: 120%<br/>Payback: 10 meses]
    C3 --> F2[⏳ Expansão 5G<br/>ROI: 150%<br/>Payback: 12 meses]
    
    style D1 fill:#ccffcc
    style D2 fill:#ccffcc
    style E1 fill:#fff4cc
    style E2 fill:#fff4cc
    style F1 fill:#ffe6cc
    style F2 fill:#ffe6cc
```

---

<a name="datasets"></a>
# 5. 📊 DATASETS POR ÁREA OPERACIONAL

## 5.1 Matriz de Datasets

```mermaid
graph TD
    subgraph "Fontes de Dados Internas"
        INT1[💾 ERP/WMS<br/>Estoque & Compras]
        INT2[🔧 Sistema Manutenção<br/>Ordens de Serviço]
        INT3[👷 RH System<br/>Escalas & Férias]
        INT4[💰 Financeiro<br/>Receitas & Custos]
        INT5[📊 CRM<br/>Contratos & Clientes]
    end
    
    subgraph "Fontes Externas Públicas"
        EXT1[🌐 ANATEL<br/>Dados Telecom Brasil]
        EXT2[🌍 GSMA<br/>Latin America Trends]
        EXT3[🌡️ INMET<br/>Meteorologia]
        EXT4[💹 BACEN<br/>Indicadores Econômicos]
        EXT5[🗺️ Google Maps<br/>Trânsito & Rotas]
    end
    
    subgraph "Aplicações"
        APP1[📦 Gestão Estoque]
        APP2[🔧 Manutenção]
        APP3[🚗 Logística]
        APP4[👥 RH]
        APP5[💵 Financeiro]
        APP6[📶 Expansão 5G]
    end
    
    INT1 --> APP1
    INT2 --> APP2
    INT3 --> APP4
    INT4 --> APP5
    INT5 --> APP5
    
    EXT1 --> APP6
    EXT2 --> APP6
    EXT3 --> APP2
    EXT4 --> APP5
    EXT5 --> APP3
    
    INT1 --> APP3
    INT2 --> APP3
```

---

## 5.2 Datasets Detalhados por Área

### 📦 Gestão de Estoque

| Dataset | Fonte | Periodicidade | Campos Principais |
|---------|-------|---------------|-------------------|
| Consumo Materiais | ERP Interno | Diário | Data, Item_ID, Qty, Site, Custo |
| Lead Times | Fornecedores | Mensal | Supplier, Item, Days, Std_Dev |
| Preços | Compras | Semanal | Item, Preço, Variação |

### 🔧 Manutenção Preventiva

| Dataset | Fonte | Periodicidade | Campos Principais |
|---------|-------|---------------|-------------------|
| Ordens de Serviço | Sistema Manutenção | Diário | OS_ID, Site, Tipo, Status, Data |
| Telemetria | Equipamentos | Horário | Temp, Umidade, Uptime, Erros |
| Clima | INMET | Diário | Temp_Max/Min, Precip, Umidade |
| Histórico Falhas | Sistema | Diário | Equipamento, Falha, Root_Cause |

### 🚗 Logística & Roteirização

| Dataset | Fonte | Periodicidade | Campos Principais |
|---------|-------|---------------|-------------------|
| Sites Ativos | CRM | Diário | Site_ID, Lat/Long, Tipo |
| Técnicos | RH | Diário | Técnico_ID, Localização, Disponível |
| Trânsito | Google Maps API | Real-time | Origem, Destino, Tempo, Distância |
| Manutenções Agendadas | Sistema | Diário | Site, Data, Prioridade, Duração |

### 👥 Planejamento de RH

| Dataset | Fonte | Periodicidade | Campos Principais |
|---------|-------|---------------|-------------------|
| Demanda Histórica | Manutenção | Mensal | Horas_Trabalhadas, Sites_Atendidos |
| Escalas | RH | Semanal | Técnico, Escala, Disponibilidade |
| Férias | RH | Mensal | Técnico, Data_Início, Data_Fim |
| Turnover | RH | Mensal | Admissões, Demissões, Taxa |

### 💵 Análise Financeira

| Dataset | Fonte | Periodicidade | Campos Principais |
|---------|-------|---------------|-------------------|
| Receitas | Financeiro | Mensal | Cliente, Valor, Tipo_Contrato |
| Custos OPEX | Financeiro | Mensal | Categoria, Valor, Centro_Custo |
| Investimentos CAPEX | Financeiro | Mensal | Projeto, Valor, Status |
| Indicadores Macro | BACEN | Mensal | Taxa_Cambio, IPCA, Selic, PIB |

### 📶 Expansão 5G

| Dataset | Fonte | Periodicidade | Campos Principais |
|---------|-------|---------------|-------------------|
| Cobertura Atual | Interno | Mensal | Site, Tecnologia, Alcance |
| Demanda 5G | ANATEL | Trimestral | Município, Usuários, Crescimento |
| Competição | Mercado | Mensal | Operadora, Sites, Cobertura |
| Licenças | ANATEL | Ad-hoc | Município, Status, Prazo |

---

<a name="diagramas"></a>
# 6. 🎨 DIAGRAMAS MERMAID ADICIONAIS

## 6.1 Fluxo de Dados Completo

```mermaid
graph LR
    subgraph "Sources"
        S1[(ERP<br/>Database)]
        S2[(Manutenção<br/>System)]
        S3[ANATEL<br/>API]
        S4[INMET<br/>API]
        S5[Google<br/>Maps API]
    end
    
    S1 --> ETL[🔄 ETL Pipeline]
    S2 --> ETL
    S3 --> ETL
    S4 --> ETL
    S5 --> ETL
    
    ETL --> DW[(🏛️ Data<br/>Warehouse)]
    
    DW --> ML1[📦 Estoque Model]
    DW --> ML2[🔧 Manutenção Model]
    DW --> ML3[🚗 Logística Model]
    DW --> ML4[👥 RH Model]
    DW --> ML5[💵 Financeiro Model]
    DW --> ML6[📶 5G Model]
    
    ML1 --> API[🔌 API Gateway]
    ML2 --> API
    ML3 --> API
    ML4 --> API
    ML5 --> API
    ML6 --> API
    
    API --> DASH[📊 Dashboard]
    API --> ALERT[🔔 Alert System]
    API --> APP[📱 Mobile App]
    
    style DW fill:#ffe6cc
    style API fill:#e6f3ff
```

---

## 6.2 Arquitetura de Deploy (Cloud)

```mermaid
graph TD
    subgraph "AWS Infrastructure"
        LB[⚖️ Load Balancer] --> EC1[EC2: API Server 1]
        LB --> EC2[EC2: API Server 2]
        
        EC1 --> RDS[(🗄️ RDS<br/>PostgreSQL)]
        EC2 --> RDS
        
        EC1 --> S3[📦 S3<br/>Data Lake]
        EC2 --> S3
        
        SAGE[🧠 SageMaker<br/>ML Training]
        SAGE --> S3
        
        LAMBDA[⚡ Lambda<br/>ETL Functions]
        LAMBDA --> S3
        LAMBDA --> RDS
        
        CW[📈 CloudWatch<br/>Monitoring]
        CW --> EC1
        CW --> EC2
        CW --> SAGE
        
        SNS[📧 SNS<br/>Notifications]
        EC1 --> SNS
        EC2 --> SNS
    end
    
    subgraph "Users"
        U1[👨‍💼 Procurement]
        U2[👷 Técnicos]
        U3[👔 Executivos]
    end
    
    U1 --> LB
    U2 --> LB
    U3 --> LB
    
    style LB fill:#e6f3ff
    style SAGE fill:#ffd4d4
    style SNS fill:#fff4cc
```

---

## 6.3 Matriz de Responsabilidades (RACI)

```mermaid
graph TD
    subgraph "Equipes"
        E1[💻 Data Science]
        E2[⚙️ DevOps/MLOps]
        E3[📊 Analytics]
        E4[👔 Business]
    end
    
    subgraph "Atividades"
        A1[Coleta Dados]
        A2[Feature Engineering]
        A3[Model Training]
        A4[Deploy & Monitor]
        A5[Dashboard Design]
        A6[Business Rules]
    end
    
    E1 -->|R - Responsible| A2
    E1 -->|R| A3
    E1 -->|C - Consulted| A1
    E1 -->|I - Informed| A4
    
    E2 -->|R| A4
    E2 -->|A - Accountable| A1
    E2 -->|C| A3
    
    E3 -->|R| A5
    E3 -->|C| A2
    E3 -->|C| A6
    
    E4 -->|A| A6
    E4 -->|I| A3
    E4 -->|I| A5
    
    style E1 fill:#ffd4d4
    style E2 fill:#d4f1d4
    style E3 fill:#e6f3ff
    style E4 fill:#ffe6cc
```

---

# 🎯 CONCLUSÃO E PRÓXIMOS PASSOS

## Resumo Executivo

Este documento expandiu o projeto original de **Gestão de Estoque** para cobrir **6 áreas operacionais** da Nova Corrente:

1. ✅ **Gestão de Estoque** (desenvolvido)
2. 🔧 **Manutenção Preventiva** (roadmap completo)
3. 🚗 **Logística & Roteirização** (algoritmos definidos)
4. 👥 **Planejamento de RH** (modelos especificados)
5. 💵 **Análise Financeira** (forecasting estruturado)
6. 📶 **Expansão 5G** (priorização quantificada)

## Documentos da Série

1. **PDF Matemática Completa** → Fundamentos teóricos
2. **Este Markdown** → Arquitetura visual e roadmap
3. **Próximo:** Notebooks Jupyter com código Python

## Timeline de Implementação

| Fase | Duração | Entregas |
|------|---------|----------|
| **Fase 1:** Estoque | 3 meses | Sistema completo em produção |
| **Fase 2:** Manutenção | 2 meses | Previsão de falhas ativo |
| **Fase 3:** Logística | 2 meses | Rotas otimizadas |
| **Fase 4-6:** Demais áreas | 3 meses | Sistema integrado |

**Total:** 10 meses para sistema completo.

---

**Documento preparado:** 01 de novembro de 2025  
**Versão:** 1.0 ROADMAP COMPLETO  
**Próximo:** Implementação Python com notebooks práticos
