# 🗺️ NAVEGAÇÃO COMPLETA DO SISTEMA
## Nova Corrente - Previsibilidade de Demandas com IA

**Versão:** 1.0  
**Data:** Novembro 2025  
**Status:** ✅ Guia de Navegação Completo  
**Para:** Kick-off e Onboarding de Equipe

---

## 📋 VISÃO GERAL

Este documento é seu **mapa de navegação completo** para entender todo o sistema Nova Corrente, desde o grande quadro até os detalhes de implementação. Use-o como seu guia principal para explicar o sistema e navegar pelos documentos técnicos.

---

## 🎯 ÍNDICE RÁPIDO

1. [🎨 O GRANDE QUADRO](#o-grande-quadro) - O que estamos construindo?
2. [🧩 CONCEITOS TÉCNICOS EXPLICADOS](#conceitos-tecnicos) - Entenda os termos difíceis
3. [🏗️ ARQUITETURA DO SISTEMA](#arquitetura) - Como tudo se conecta
4. [🗺️ MAPA DE NAVEGAÇÃO](#mapa-navegacao) - Onde encontrar cada coisa
5. [📚 CAMINHO DE APRENDIZADO](#caminho-aprendizado) - Ordem sugerida de leitura
6. [📖 GLOSSÁRIO](#glossario) - Dicionário de termos técnicos
7. [🔗 REFERÊNCIAS CRUZADAS](#referencias) - Todos os documentos linkados

---

<a name="o-grande-quadro"></a>

## 🎨 O GRANDE QUADRO

### O Que Estamos Construindo?

Imagine que você tem uma **empresa de telecomunicações** (Nova Corrente) que precisa manter **centenas de torres de celular** funcionando. Para isso, precisa de **materiais** (cabos, equipamentos, peças) em vários lugares do Brasil.

**O Problema:**
- Quando um material acaba, a torre para de funcionar ❌
- Se comprar demais, gasta dinheiro desnecessário 💸
- Se comprar de menos, fica sem material e a torre para 🚫

**A Solução que Estamos Construindo:**
Um **sistema de Inteligência Artificial** que **prevê quanto material vai precisar no futuro**, baseado em:
- Histórico de consumo 📊
- Dados externos (clima, economia, novas torres 5G) 🌦️
- Padrões sazonais (época de chuva, festas) 🎉
- Performance de fornecedores 🏭

**Resultado:**
- ✅ Sabe **quando** comprar
- ✅ Sabe **quanto** comprar  
- ✅ **Evita faltas** (mantém torres funcionando)
- ✅ **Economiza dinheiro** (não compra demais)

---

### Os 4 Pilares do Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   1️⃣ COLETA DE DADOS                     │
│   "Pegamos dados de vários lugares e guardamos"          │
│   - Dados da empresa (ERP)                              │
│   - Clima (APIs de tempo)                               │
│   - Economia (APIs do governo)                          │
│   - Novas torres 5G (Anatel)                            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                2️⃣ PROCESSAMENTO DE DADOS                  │
│   "Limpamos, organizamos e transformamos os dados"       │
│   - Remove erros e duplicatas                            │
│   - Calcula métricas importantes                         │
│   - Cria "features" (características) para IA            │
│   - Organiza em camadas (Bronze → Silver → Gold)         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│          3️⃣ INTELIGÊNCIA ARTIFICIAL (ML)                  │
│   "Modelos que aprendem e fazem previsões"               │
│   - Prophet: detecta padrões sazonais                    │
│   - ARIMA: análise estatística avançada                  │
│   - LSTM: rede neural profunda                           │
│   - Ensemble: combina todos para melhor resultado        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                 4️⃣ APLICAÇÃO WEB (App)                     │
│   "Interface bonita para usar o sistema"                 │
│   - Dashboard: gráficos e relatórios                     │
│   - Alertas: avisos quando material está acabando       │
│   - Previsões: visualização das previsões de demanda     │
│   - Controles: gerenciar materiais e fornecedores        │
└─────────────────────────────────────────────────────────┘
```

---

<a name="conceitos-tecnicos"></a>

## 🧩 CONCEITOS TÉCNICOS EXPLICADOS

### 🔹 O Que é Analytics Engineering?

**Em termos simples:**
É a arte de **transformar dados brutos em informações úteis** usando código (não Excel!). 

**Analogia:**
- **Dados brutos** = ingredientes soltos na cozinha 🥕🥔🍅
- **Analytics Engineering** = receita que organiza os ingredientes 📝
- **Resultado final** = prato pronto e organizado 🍲

**No nosso caso:**
Transformamos planilhas do Excel em um **sistema automático** que:
- Pega dados de várias fontes
- Limpa e organiza
- Calcula métricas
- Cria relatórios automáticos
- Serve para a aplicação web

---

### 🔹 Arquitetura Medallion (Bronze/Silver/Gold)

**Analogia com Filtros de Café:**
```
☕ CAFÉ BRUTO (Bronze)
   ↓ Filtro 1
☕ CAFÉ LIMPO (Silver)  
   ↓ Filtro 2
☕ CAFÉ PRONTO (Gold)
```

**Em termos técnicos:**

#### 🥉 Bronze Layer (Camada Bronze) - "Dados Brutos"
- **O que é:** Dados exatamente como chegam das fontes
- **Características:**
  - Nenhuma transformação
  - Podem ter erros, duplicatas
  - Formato original preservado
- **Exemplo:** Planilha Excel exportada do ERP, exatamente como veio

#### 🥈 Silver Layer (Camada Prata) - "Dados Limpos"
- **O que é:** Dados processados e validados
- **Características:**
  - Erros corrigidos
  - Duplicatas removidas
  - Tipos de dados corretos
  - Prontos para análise
- **Exemplo:** Mesma planilha, mas com datas corretas, números sem erros, sem duplicatas

#### 🥇 Gold Layer (Camada Ouro) - "Dados de Negócio"
- **O que é:** Dados modelados para o negócio
- **Características:**
  - Organizados por dimensões (família, fornecedor, local)
  - Métricas pré-calculadas
  - Otimizados para dashboards
  - Prontos para BI e ML
- **Exemplo:** Tabelas organizadas tipo "fato" (vendas) e "dimensões" (produtos, clientes)

---

### 🔹 ETL vs ELT

**ETL (Extract, Transform, Load):**
```
Pegar → Transformar → Guardar
```
- Primeiro transforma, depois guarda
- Usado quando processamento é limitado

**ELT (Extract, Load, Transform):**
```
Pegar → Guardar → Transformar
```
- Guarda primeiro (bruto), depois transforma
- Mais moderno, usado em cloud (Databricks, Snowflake)
- **É o que usamos!** ✅

**Por quê ELT é melhor:**
- Guarda dados originais (pode reprocessar)
- Mais rápido (processa na cloud)
- Mais flexível (pode mudar transformações depois)

---

### 🔹 dbt (data build tool)

**O que é:**
Ferramenta que permite escrever **SQL organizado como código**, com:
- Versionamento (Git)
- Testes automáticos
- Documentação gerada automaticamente
- Reutilização de código

**Analogia:**
Se SQL normal é "escrever à mão", **dbt é usar um "template inteligente"**:
- Você escreve a transformação uma vez
- Pode reutilizar em vários lugares
- Testa se está correto
- Gera documentação sozinho

**Exemplo Simples:**
```sql
-- ANTES (SQL normal, repetitivo)
SELECT 
    DATE_TRUNC('month', data_venda) as mes,
    SUM(valor) as total_vendas
FROM vendas
GROUP BY mes;

-- COM dbt (organizado, reutilizável)
{{ config(materialized='table') }}
SELECT 
    {{ date_trunc('month', 'data_venda') }} as mes,
    {{ sum('valor') }} as total_vendas
FROM {{ ref('vendas') }}
GROUP BY mes
```

---

### 🔹 Airflow (Orquestração)

**O que é:**
Ferramenta que **coordena** todos os processos do sistema.

**Analogia:**
Se o sistema fosse uma **orquestra**, Airflow seria o **maestro**:
- Define **quando** cada processo roda (diário, semanal)
- Define a **ordem** (primeiro pega dados, depois limpa, depois calcula)
- **Monitora** se algo deu erro
- **Reexecuta** automaticamente se falhar

**Exemplo Prático:**
```
Pipeline Diário:
1. 00:00 - Pegar dados do ERP → Bronze
2. 01:00 - Limpar dados → Silver  
3. 02:00 - Calcular features → Gold
4. 03:00 - Treinar modelos ML
5. 04:00 - Gerar previsões
6. 05:00 - Atualizar dashboard
```

---

### 🔹 MLflow (ML Ops)

**O que é:**
Ferramenta para **gerenciar modelos de Machine Learning**.

**Problemas que resolve:**
- **Versionamento:** Quais versões de modelos foram usadas?
- **Reprodutibilidade:** Como replicar um modelo que funcionou bem?
- **Tracking:** Qual modelo teve melhor performance?
- **Serving:** Como colocar modelo em produção?

**Analogia:**
É como um **"GitHub para modelos ML"**:
- Guarda versões de modelos
- Compara performances
- Permite voltar para versão anterior
- Deploy automático

---

### 🔹 Delta Lake

**O que é:**
Formato de armazenamento de dados que permite:
- **ACID transactions:** Garante consistência (como banco de dados)
- **Time travel:** Voltar no tempo e ver dados antigos
- **Schema evolution:** Adicionar colunas sem quebrar código antigo
- **Upserts:** Atualizar registros existentes (não só adicionar)

**Por que é melhor que Parquet simples:**
- Parquet = só adicionar dados (append-only)
- Delta Lake = pode atualizar, deletar, fazer transações

**Analogia:**
- **Parquet** = caderno onde só pode escrever páginas novas
- **Delta Lake** = caderno onde pode:
  - Editar páginas antigas ✏️
  - Deletar páginas ❌
  - Ver histórico de mudanças 📜
  - Garantir que mudanças são consistentes ✅

---

### 🔹 Feature Engineering

**O que é:**
Criar **características** dos dados que ajudam os modelos de IA a aprender melhor.

**Exemplo:**
Dados brutos:
```
Data: 2025-01-15
Quantidade: 100
```

Features criadas:
```
Data: 2025-01-15
Quantidade: 100
Dia_da_semana: 3 (quarta-feira)
Mes: 1 (janeiro)
É_fim_de_semana: 0 (não)
É_feriado: 0 (não)
Média_últimos_30_dias: 95
Tendência: +5%
```

**Por que é importante:**
IA precisa de "pistas" para aprender. Features são essas pistas!

---

### 🔹 Star Schema (Modelagem de Dados)

**O que é:**
Forma de organizar dados em **tabelas de fatos** (acontecimentos) e **tabelas de dimensões** (características).

**Analogia:**
```
FATO (Tabela Central):
"Vendas" - o que aconteceu
- Data da venda
- Produto (ID)
- Cliente (ID)
- Quantidade
- Valor

DIMENSÕES (Tabelas ao Redor):
"Produtos" - características do produto
- Nome
- Categoria
- Preço

"Clientes" - características do cliente
- Nome
- Cidade
- Segmento
```

**Visualização (parece uma estrela):**
```
        Produtos
           ↓
Clientes → VENDAS ← Tempo
           ↓
      Fornecedores
```

**Por que usar:**
- Consultas mais rápidas ⚡
- Fácil de entender 🧠
- Otimizado para BI 📊

---

### 🔹 Data Lakehouse

**O que é:**
Combinação de **Data Lake** (armazenamento barato) + **Data Warehouse** (estrutura organizada).

**Analogia:**
- **Data Lake** = depósito gigante, tudo misturado, barato 💰
- **Data Warehouse** = armazém organizado, caro, rápido 🏭
- **Data Lakehouse** = depósito organizado, barato E rápido! 🏗️

**Características:**
- Armazena dados brutos (como Lake)
- Permite queries rápidas (como Warehouse)
- Suporta ML e Analytics
- Custo baixo (cloud storage)

---

<a name="arquitetura"></a>

## 🏗️ ARQUITETURA DO SISTEMA

### Visão Completa do Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                    🎨 CAMADA DE APRESENTAÇÃO                          │
│  Next.js Frontend │ Metabase │ Dashboards │ Alertas │ Relatórios     │
└─────────────────────────────────────────────────────────────────────┘
                                    ↕ HTTP/REST/WebSocket
┌─────────────────────────────────────────────────────────────────────┐
│                    🔧 CAMADA DE APLICAÇÃO                            │
│  FastAPI Backend │ APIs REST │ WebSocket │ Cache Redis │ ML Serving  │
└─────────────────────────────────────────────────────────────────────┘
                                    ↕
┌─────────────────────────────────────────────────────────────────────┐
│                    🥇 CAMADA GOLD (Analytics)                         │
│  Star Schema │ dbt Models │ Métricas │ Agregações │ Data Products   │
└─────────────────────────────────────────────────────────────────────┘
                                    ↕
┌─────────────────────────────────────────────────────────────────────┐
│                    🥈 CAMADA SILVER (Limpeza)                         │
│  Dados Limpos │ Validações │ Great Expectations │ Schema Enforcement │
└─────────────────────────────────────────────────────────────────────┘
                                    ↕
┌─────────────────────────────────────────────────────────────────────┐
│                    🥉 CAMADA BRONZE (Raw)                             │
│  Dados Brutos │ Delta Lake │ S3 Storage │ Particionamento por Data   │
└─────────────────────────────────────────────────────────────────────┘
                                    ↕
┌─────────────────────────────────────────────────────────────────────┐
│                    📥 CAMADA DE INGESTÃO                              │
│  Airbyte │ Fivetran │ Custom Python │ Kafka Streams │ API Integrations│
└─────────────────────────────────────────────────────────────────────┘
                                    ↕
┌─────────────────────────────────────────────────────────────────────┐
│                    📊 FONTES DE DADOS                                 │
│  ERP │ Weather APIs │ Anatel │ BACEN │ Supplier APIs │ IoT Sensors   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    🤖 CAMADA ML (Paralela)                            │
│  MLflow │ Feature Store │ Model Registry │ Training │ Inference      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    🎼 CAMADA DE ORQUESTRAÇÃO                          │
│  Airflow │ Prefect │ dbt Cloud │ GitHub Actions │ CI/CD Pipelines    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    🛡️ CAMADA DE GOVERNANÇA                            │
│  DataHub │ Great Expectations │ Unity Catalog │ Data Lineage         │
└─────────────────────────────────────────────────────────────────────┘
```

---

### Fluxo de Dados (End-to-End)

```
1. INGESTÃO
   └─> Dados chegam de fontes externas (ERP, APIs)
        ↓
2. BRONZE
   └─> Guardados raw no Delta Lake (S3)
        ↓
3. SILVER
   └─> Limpos e validados com dbt + Great Expectations
        ↓
4. GOLD
   └─> Modelados em Star Schema para analytics
        ↓
5. ML FEATURES
   └─> Features extraídas para treinar modelos
        ↓
6. MODEL TRAINING
   └─> Modelos treinados e versionados no MLflow
        ↓
7. PREDICTIONS
   └─> Previsões geradas e guardadas
        ↓
8. API SERVING
   └─> FastAPI serve dados e previsões
        ↓
9. FRONTEND
   └─> Next.js exibe dashboards e gráficos
```

---

### Como os Componentes Se Conectam

#### 🎯 Cenario 1: Previsão de Demanda Diária

```
Usuário acessa dashboard
    ↓
Next.js Frontend faz request
    ↓
FastAPI busca dados no Gold Layer
    ↓
Se não estiver em cache, busca no Delta Lake
    ↓
FastAPI busca previsões do MLflow
    ↓
Combina dados + previsões
    ↓
Retorna JSON para frontend
    ↓
Frontend exibe gráfico atualizado
```

#### 🎯 Cenario 2: Pipeline Diário Noturno

```
Airflow acorda às 00:00
    ↓
Tarefa 1: Airbyte pega dados do ERP
    ↓
Salva no Bronze Layer (Delta Lake)
    ↓
Tarefa 2: dbt transforma Bronze → Silver
    ↓
Great Expectations valida qualidade
    ↓
Tarefa 3: dbt transforma Silver → Gold
    ↓
Tarefa 4: Extrai features para ML
    ↓
Tarefa 5: Treina modelos (se necessário)
    ↓
Tarefa 6: Gera previsões para próximo mês
    ↓
Salva previsões no Gold Layer
    ↓
Notifica via email/WebSocket se algo falhou
```

---

<a name="mapa-navegacao"></a>

## 🗺️ MAPA DE NAVEGAÇÃO

### Por Tipo de Conteúdo

#### 📚 **Documentos de Visão Geral e Estratégia**

| Documento | Quando Ler | Nível |
|-----------|------------|-------|
| **README_ROADMAPS.md** | Comece aqui! | ⭐ Iniciante |
| **Este documento (NAVEGACAO_COMPLETA_SISTEMA_PT_BR.md)** | Seu guia principal | ⭐ Iniciante |
| **COMPLETE_ROADMAP_SUMMARY_PT_BR.md** | Resumo executivo | ⭐ Iniciante |
| **ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md** | Roadmap completo detalhado | ⭐⭐ Intermediário |

#### 🏗️ **Documentos de Arquitetura**

| Documento | Quando Ler | Nível |
|-----------|------------|-------|
| **TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md** | Arquitetura técnica completa | ⭐⭐⭐ Avançado |
| **DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md** | Como funcionam os pipelines | ⭐⭐ Intermediário |
| **ETL_DESIGN_PATTERNS_PT_BR.md** | Padrões de ETL/ELT | ⭐⭐ Intermediário |
| **FULLSTACK_INTEGRATION_PATTERNS_PT_BR.md** | Integração backend + frontend | ⭐⭐ Intermediário |

#### 📋 **Documentos por Fase**

| Documento | Fase | Quando Ler |
|-----------|------|------------|
| **PHASE_0_FOUNDATION_DETAILED_PT_BR.md** | Fase 0 (2 semanas) | Setup inicial |
| **PHASE_1_DATA_FOUNDATION_DETAILED_PT_BR.md** | Fase 1 (2 semanas) | Silver layer |
| **PHASE_2_ANALYTICS_LAYER_DETAILED_PT_BR.md** | Fase 2 (4 semanas) | Gold layer + BI |

#### 🔧 **Guias Práticos**

| Documento | Quando Ler | Perfil |
|-----------|------------|--------|
| **QUICK_START_GUIDE_PT_BR.md** | Quer começar agora | Todos |
| **IMPLEMENTATION_TEMPLATES_PT_BR.md** | Precisa de código pronto | Devs |
| **TROUBLESHOOTING_GUIDE_PT_BR.md** | Algo não está funcionando | Todos |
| **PRODUCTION_DEPLOYMENT_GUIDE_PT_BR.md** | Deploy em produção | DevOps |

#### 📊 **Documentos de Estado e Próximos Passos**

| Documento | Quando Ler | O Que Contém |
|-----------|------------|--------------|
| **CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md** | Ver progresso atual | Status Fase 1-2 |
| **NEXT_STEPS_OPTIMIZATION_PT_BR.md** | Próximas tarefas | Semanas 3-4 |
| **CURRENT_ARCHITECTURE_TO_ANALYTICS_ROADMAP_PT_BR.md** | Migração atual | Como migrar sistema atual |

#### 📖 **Referências**

| Documento | Quando Ler | O Que Contém |
|-----------|------------|--------------|
| **REFERENCE_TECHNICAL_STACK_PT_BR.md** | Referência rápida | Stack completo |
| **DATA_PIPELINE_IMPLEMENTATION_EXAMPLES_PT_BR.md** | Exemplos de código | Código produção |

---

<a name="caminho-aprendizado"></a>

## 📚 CAMINHO DE APRENDIZADO RECOMENDADO

### 🎯 Para Entender o Sistema Completo (Kick-off)

**Tempo estimado:** 2-3 horas

#### Etapa 1: Visão Geral (30 min)
1. ✅ **Este documento** (NAVEGACAO_COMPLETA_SISTEMA_PT_BR.md)
   - Leia seções: "O Grande Quadro" e "Arquitetura do Sistema"
2. ✅ **README_ROADMAPS.md**
   - Visão geral de todos os documentos

#### Etapa 2: Conceitos Fundamentais (45 min)
3. ✅ **ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md**
   - Seção 1: "Visão Geral de Analytics Engineering"
   - Seção 2: "Arquitetura de Dados Moderna"
   - Seção 3: "Modelagem de Dados"

#### Etapa 3: Como Funciona na Prática (45 min)
4. ✅ **DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md**
   - Seção 1: "Arquitetura de Pipelines"
   - Seção 2: "Pipeline ETL/ELT Completo"

#### Etapa 4: Estado Atual e Próximos Passos (30 min)
5. ✅ **CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md**
   - Veja o que já foi feito
6. ✅ **NEXT_STEPS_OPTIMIZATION_PT_BR.md**
   - Veja o que vem a seguir

---

### 🎯 Para Implementar (Por Perfil)

#### 👨‍💻 Data Engineer

**Foco:** Pipelines de dados e infraestrutura

1. ✅ **QUICK_START_GUIDE_PT_BR.md** - Seção Data Engineer
2. ✅ **PHASE_0_FOUNDATION_DETAILED_PT_BR.md** - Setup inicial
3. ✅ **DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md** - Pipelines completos
4. ✅ **ETL_DESIGN_PATTERNS_PT_BR.md** - Padrões de implementação
5. ✅ **IMPLEMENTATION_TEMPLATES_PT_BR.md** - Templates prontos

#### 👨‍🔬 Data Scientist

**Foco:** Modelos ML e features

1. ✅ **CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md** - Estado atual
2. ✅ **NEXT_STEPS_OPTIMIZATION_PT_BR.md** - Otimização de modelos
3. ✅ **ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md** - Seção ML Ops
4. ✅ **TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md** - Seção ML Layer

#### 👨‍💼 Analyst / BI

**Foco:** Dashboards e analytics

1. ✅ **PHASE_2_ANALYTICS_LAYER_DETAILED_PT_BR.md** - Gold layer
2. ✅ **ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md** - Seção Analytics e BI
3. ✅ **QUICK_START_GUIDE_PT_BR.md** - Seção Analyst

#### 👨‍💻 Fullstack Developer

**Foco:** App web (Frontend + Backend)

1. ✅ **FULLSTACK_INTEGRATION_PATTERNS_PT_BR.md** - Integração completa
2. ✅ **DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md** - Seção Serving
3. ✅ **PRODUCTION_DEPLOYMENT_GUIDE_PT_BR.md** - Deploy

#### 🛠️ DevOps / SRE

**Foco:** Infraestrutura e produção

1. ✅ **PHASE_0_FOUNDATION_DETAILED_PT_BR.md** - Terraform e infra
2. ✅ **PRODUCTION_DEPLOYMENT_GUIDE_PT_BR.md** - Deploy produção
3. ✅ **TROUBLESHOOTING_GUIDE_PT_BR.md** - Problemas comuns
4. ✅ **REFERENCE_TECHNICAL_STACK_PT_BR.md** - Stack técnico

---

### 🎯 Para Profundar (Avançado)

**Tempo estimado:** 8-12 horas

1. ✅ **TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md** - Tudo detalhado
2. ✅ **ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md** - Roadmap completo
3. ✅ **DATA_PIPELINE_IMPLEMENTATION_EXAMPLES_PT_BR.md** - Código produção
4. ✅ **ETL_DESIGN_PATTERNS_PT_BR.md** - Padrões avançados
5. ✅ Todos os guias detalhados por fase

---

<a name="glossario"></a>

## 📖 GLOSSÁRIO DE TERMOS TÉCNICOS

### A

**ACID Transactions**
- **O que é:** Garantia de que operações em dados são consistentes
- **Analogia:** Como transação bancária - ou completa tudo ou não faz nada
- **No nosso sistema:** Delta Lake garante isso

**Airflow**
- **O que é:** Ferramenta de orquestração de pipelines
- **Função:** Coordena quando cada processo roda
- **Analogia:** Maestro de orquestra

**Analytics Engineering**
- **O que é:** Disciplina que transforma dados brutos em insights com código
- **Diferente de:** Data Science (foco em modelos) ou Data Engineering (foco em infra)

**ARIMA**
- **O que é:** Modelo estatístico para previsão de séries temporais
- **Usado em:** Previsão de demanda
- **Força:** Análise estatística profunda

---

### B

**Bronze Layer**
- **O que é:** Camada de dados brutos (raw)
- **Características:** Nenhuma transformação, pode ter erros
- **No nosso sistema:** Primeira camada no Delta Lake

**Business Intelligence (BI)**
- **O que é:** Ferramentas para criar dashboards e relatórios
- **Exemplos:** Metabase, Superset
- **No nosso sistema:** Camada de apresentação

---

### C

**Change Data Capture (CDC)**
- **O que é:** Capturar apenas mudanças nos dados (não tudo novamente)
- **Vantagem:** Mais eficiente, menos processamento
- **No nosso sistema:** Para sincronização incremental

**CI/CD**
- **O que é:** Continuous Integration / Continuous Deployment
- **Função:** Automatizar testes e deploy
- **No nosso sistema:** GitHub Actions + dbt Cloud

---

### D

**dbt (data build tool)**
- **O que é:** Framework para transformar dados com SQL
- **Função:** Organizar transformações como código
- **No nosso sistema:** Transforma Bronze → Silver → Gold

**Data Lake**
- **O que é:** Armazenamento de dados brutos em grande volume
- **Características:** Barato, armazena tudo
- **No nosso sistema:** S3 + Delta Lake

**Data Lakehouse**
- **O que é:** Combinação de Data Lake + Data Warehouse
- **Vantagens:** Barato como Lake, rápido como Warehouse
- **No nosso sistema:** Arquitetura principal

**Data Product**
- **O que é:** Dados tratados como produto de software
- **Características:** Versionado, documentado, testado
- **No nosso sistema:** Gold layer organizado por domínios

**Data Vault 2.0**
- **O que é:** Metodologia de modelagem de dados
- **Características:** Hub, Link, Satellite tables
- **No nosso sistema:** Usado na Silver layer

**Delta Lake**
- **O que é:** Formato de armazenamento de dados open-source
- **Vantagens:** ACID, time travel, upserts
- **No nosso sistema:** Formato principal de armazenamento

**Dimension Table**
- **O que é:** Tabela com características (ex: produtos, clientes)
- **No Star Schema:** Tabelas ao redor da tabela de fatos
- **Exemplo:** Tabela "Produtos" com nome, categoria, preço

---

### E

**ELT (Extract, Load, Transform)**
- **O que é:** Padrão: Pegar → Guardar → Transformar
- **Vantagem:** Guarda dados brutos primeiro
- **No nosso sistema:** Padrão usado

**ETL (Extract, Transform, Load)**
- **O que é:** Padrão: Pegar → Transformar → Guardar
- **Comparação:** Mais antigo que ELT
- **No nosso sistema:** Não usado (preferimos ELT)

**Ensemble Model**
- **O que é:** Combinação de vários modelos ML
- **Vantagem:** Geralmente melhor que modelo único
- **No nosso sistema:** Prophet + ARIMA + LSTM combinados

---

### F

**Fact Table**
- **O que é:** Tabela central com eventos (ex: vendas)
- **No Star Schema:** Tabela no centro
- **Exemplo:** Tabela "Vendas" com data, produto_id, quantidade

**Feature Engineering**
- **O que é:** Criar características dos dados para ML
- **Exemplo:** Transformar data em "dia_da_semana", "é_fim_de_semana"
- **No nosso sistema:** 73 features criadas

**Feature Store**
- **O que é:** Armazenamento centralizado de features para ML
- **Vantagem:** Reutilização, versionamento
- **No nosso sistema:** Feast ou MLflow Feature Store

---

### G

**Gold Layer**
- **O que é:** Camada de dados modelados para negócio
- **Características:** Star Schema, métricas pré-calculadas
- **No nosso sistema:** Terceira camada, pronta para BI

**Great Expectations**
- **O que é:** Framework de qualidade de dados
- **Função:** Validar dados automaticamente
- **No nosso sistema:** Validação Silver → Gold

---

### I

**Idempotent**
- **O que é:** Operação que pode ser executada várias vezes sem mudar resultado
- **Importância:** Segurança em pipelines
- **No nosso sistema:** Todos os pipelines são idempotentes

**Incremental Loading**
- **O que é:** Carregar apenas dados novos (não tudo novamente)
- **Vantagem:** Eficiência
- **No nosso sistema:** Padrão usado

---

### L

**LSTM**
- **O que é:** Long Short-Term Memory - tipo de rede neural
- **Usado em:** Previsão de séries temporais
- **Força:** Detecta padrões complexos em sequências

---

### M

**MAPE (Mean Absolute Percentage Error)**
- **O que é:** Métrica de erro de previsão
- **Fórmula:** Média do erro percentual absoluto
- **Meta no nosso sistema:** < 15%

**Medallion Architecture**
- **O que é:** Arquitetura Bronze → Silver → Gold
- **Origem:** Databricks
- **No nosso sistema:** Arquitetura principal

**MLflow**
- **O que é:** Plataforma para gerenciar ciclo de vida de ML
- **Funções:** Tracking, registry, serving
- **No nosso sistema:** Gerenciamento de modelos

**ML Ops**
- **O que é:** DevOps para Machine Learning
- **Foco:** Automatizar ciclo de vida de ML
- **No nosso sistema:** MLflow + Airflow

---

### P

**Parquet**
- **O que é:** Formato de arquivo colunar otimizado
- **Vantagem:** Compressão, leitura rápida
- **No nosso sistema:** Formato usado no Bronze

**Prophet**
- **O que é:** Modelo de previsão da Facebook
- **Força:** Detecta sazonalidades automaticamente
- **No nosso sistema:** Um dos modelos usados

**Python UDF (User Defined Function)**
- **O que é:** Função customizada em Python
- **Usado em:** Transformações complexas que SQL não faz bem
- **No nosso sistema:** Para cálculos avançados

---

### S

**Schema Evolution**
- **O que é:** Adicionar colunas sem quebrar código antigo
- **Importância:** Flexibilidade
- **No nosso sistema:** Delta Lake permite

**Silver Layer**
- **O que é:** Camada de dados limpos
- **Características:** Validados, tipos corretos
- **No nosso sistema:** Segunda camada

**Slowly Changing Dimensions (SCD)**
- **O que é:** Dimensões que mudam ao longo do tempo
- **Exemplo:** Preço de produto muda
- **No nosso sistema:** SCD Type 2 usado

**Spark**
- **O que é:** Framework de processamento distribuído
- **Função:** Processar grandes volumes de dados
- **No nosso sistema:** Usado no Databricks

**Star Schema**
- **O que é:** Modelagem com tabela de fatos + dimensões
- **Formato:** Parece uma estrela
- **No nosso sistema:** Usado na Gold layer

**Streaming**
- **O que é:** Processamento de dados em tempo real
- **Tecnologia:** Kafka, Flink
- **No nosso sistema:** Para dados em tempo real

---

### T

**Time Travel**
- **O que é:** Ver dados em versões anteriores
- **Vantagem:** Debug, auditoria
- **No nosso sistema:** Delta Lake permite

**Terraform**
- **O que é:** Ferramenta de Infrastructure as Code
- **Função:** Criar infraestrutura automaticamente
- **No nosso sistema:** Setup de cloud (AWS, Databricks)

---

### U

**Unity Catalog**
- **O que é:** Catálogo de dados do Databricks
- **Função:** Governança, lineage, segurança
- **No nosso sistema:** Catálogo principal

**Upsert**
- **O que é:** Update + Insert (atualizar se existe, inserir se não)
- **Vantagem:** Atualizações eficientes
- **No nosso sistema:** Delta Lake permite

---

### V

**Versionamento**
- **O que é:** Controle de versões (como Git)
- **Aplicado em:** Código, dados, modelos ML
- **No nosso sistema:** Git (código), MLflow (modelos), Delta Lake (dados)

---

<a name="referencias"></a>

## 🔗 REFERÊNCIAS CRUZADAS COMPLETAS

### Por Componente do Sistema

#### 📥 **Ingestão de Dados**

**Documentos relacionados:**
- `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Seção "Pipeline ETL/ELT Completo"
- `ETL_DESIGN_PATTERNS_PT_BR.md` → Seção "Incremental Loading" e "Change Data Capture"
- `PHASE_0_FOUNDATION_DETAILED_PT_BR.md` → Setup Airbyte/Fivetran
- `IMPLEMENTATION_TEMPLATES_PT_BR.md` → Templates de ingestão

**Conceitos chave:**
- Bronze Layer (primeira camada)
- Incremental loading
- Change Data Capture (CDC)

---

#### 🥉 **Bronze Layer (Dados Brutos)**

**Documentos relacionados:**
- `ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md` → Seção "Arquitetura Medallion"
- `TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md` → Seção "Storage Layer"
- `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Pipeline Bronze
- `PHASE_0_FOUNDATION_DETAILED_PT_BR.md` → Setup Bronze

**Conceitos chave:**
- Delta Lake no S3
- Particionamento por data
- Schema evolution
- Formato Parquet/Delta

---

#### 🥈 **Silver Layer (Dados Limpos)**

**Documentos relacionados:**
- `PHASE_1_DATA_FOUNDATION_DETAILED_PT_BR.md` → Guia completo Silver
- `ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md` → Seção "Great Expectations"
- `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Transformação Silver
- `ETL_DESIGN_PATTERNS_PT_BR.md` → Padrões de limpeza

**Conceitos chave:**
- dbt transformations
- Great Expectations (validação)
- Schema enforcement
- Data quality gates

---

#### 🥇 **Gold Layer (Analytics)**

**Documentos relacionados:**
- `PHASE_2_ANALYTICS_LAYER_DETAILED_PT_BR.md` → Guia completo Gold
- `ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md` → Seção "Modelagem de Dados"
- `TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md` → Star Schema
- `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Gold layer serving

**Conceitos chave:**
- Star Schema
- dbt models
- Métricas pré-calculadas
- Data Products

---

#### 🤖 **Machine Learning**

**Documentos relacionados:**
- `NEXT_STEPS_OPTIMIZATION_PT_BR.md` → Otimização de modelos
- `ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md` → Seção "ML Ops"
- `CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md` → Features criadas
- `TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md` → ML Layer

**Conceitos chave:**
- Feature Engineering
- Model training (Prophet, ARIMA, LSTM)
- Ensemble models
- MLflow (tracking, registry)

---

#### 🔧 **Backend (FastAPI)**

**Documentos relacionados:**
- `FULLSTACK_INTEGRATION_PATTERNS_PT_BR.md` → Integração backend
- `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Seção "Serving"
- `PRODUCTION_DEPLOYMENT_GUIDE_PT_BR.md` → Deploy backend
- `IMPLEMENTATION_TEMPLATES_PT_BR.md` → Templates API

**Conceitos chave:**
- REST APIs
- WebSocket (real-time)
- Redis Cache
- Message Queue (Kafka/RabbitMQ)

---

#### 🎨 **Frontend (Next.js)**

**Documentos relacionados:**
- `FULLSTACK_INTEGRATION_PATTERNS_PT_BR.md` → Integração frontend
- `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Seção "Application Layer"
- `PRODUCTION_DEPLOYMENT_GUIDE_PT_BR.md` → Deploy frontend
- `QUICK_START_GUIDE_PT_BR.md` → Quick start

**Conceitos chave:**
- React/Next.js
- API integration
- Real-time updates
- Dashboards

---

#### 🎼 **Orquestração (Airflow)**

**Documentos relacionados:**
- `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Monitoramento
- `PHASE_0_FOUNDATION_DETAILED_PT_BR.md` → Setup Airflow
- `ETL_DESIGN_PATTERNS_PT_BR.md` → Padrões de pipeline
- `TROUBLESHOOTING_GUIDE_PT_BR.md` → Problemas Airflow

**Conceitos chave:**
- DAGs (Directed Acyclic Graphs)
- Task scheduling
- Error handling
- Monitoring

---

#### 🛡️ **Governança (DataHub, Great Expectations)**

**Documentos relacionados:**
- `ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md` → Seção "Governança"
- `TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md` → Unity Catalog
- `PHASE_1_DATA_FOUNDATION_DETAILED_PT_BR.md` → Great Expectations

**Conceitos chave:**
- Data Lineage (linhagem de dados)
- Data Catalog
- Data Quality
- Access control

---

#### 📊 **BI Tools (Metabase, Superset)**

**Documentos relacionados:**
- `PHASE_2_ANALYTICS_LAYER_DETAILED_PT_BR.md` → Setup BI tools
- `ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md` → Seção "Analytics e BI"
- `QUICK_START_GUIDE_PT_BR.md` → Quick start Analyst

**Conceitos chave:**
- Self-service analytics
- Dashboards
- dbt Semantic Layer
- Embed analytics

---

### Por Fase de Implementação

#### **Fase 0: Foundation (Semanas 1-2)**

**Documentos principais:**
- `PHASE_0_FOUNDATION_DETAILED_PT_BR.md` ⭐ Guia detalhado
- `QUICK_START_GUIDE_PT_BR.md` → Seção DevOps
- `IMPLEMENTATION_TEMPLATES_PT_BR.md` → Templates Terraform

**Entregas:**
- Terraform setup
- dbt project structure
- Airflow básico
- Bronze layer setup

---

#### **Fase 1: Data Foundation (Semanas 3-4)**

**Documentos principais:**
- `PHASE_1_DATA_FOUNDATION_DETAILED_PT_BR.md` ⭐ Guia detalhado
- `CURRENT_STATE_DATA_PREPROCESSING_PT_BR.md` → Estado atual
- `NEXT_STEPS_OPTIMIZATION_PT_BR.md` → Próximos passos

**Entregas:**
- Silver layer completo
- Great Expectations suite
- Data profiling
- Documentation

---

#### **Fase 2: Analytics Layer (Semanas 5-8)**

**Documentos principais:**
- `PHASE_2_ANALYTICS_LAYER_DETAILED_PT_BR.md` ⭐ Guia detalhado
- `ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md` → Star Schema

**Entregas:**
- Gold layer (Star Schema)
- dbt Metrics
- BI tools setup
- Dashboards básicos

---

### Por Problema ou Objetivo

#### **Quer entender o sistema inteiro?**
1. Este documento (NAVEGACAO_COMPLETA_SISTEMA_PT_BR.md)
2. `ANALYTICS_ENGINEERING_ROADMAP_COMPLETE_PT_BR.md` → Seções 1-3

#### **Quer implementar algo específico?**
1. `QUICK_START_GUIDE_PT_BR.md` → Escolha seu perfil
2. `IMPLEMENTATION_TEMPLATES_PT_BR.md` → Templates prontos
3. Guia detalhado da fase correspondente

#### **Algo não está funcionando?**
1. `TROUBLESHOOTING_GUIDE_PT_BR.md` → Procure seu problema
2. `REFERENCE_TECHNICAL_STACK_PT_BR.md` → Verifique configurações

#### **Precisa fazer deploy?**
1. `PRODUCTION_DEPLOYMENT_GUIDE_PT_BR.md` → Guia completo
2. `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Design produção

#### **Quer entender arquitetura profunda?**
1. `TECHNICAL_ARCHITECTURE_DEEP_DIVE_PT_BR.md` ⭐ Tudo detalhado
2. `DATA_PIPELINES_PRODUCTION_DESIGN_PT_BR.md` → Pipelines
3. `ETL_DESIGN_PATTERNS_PT_BR.md` → Padrões avançados

---

## 🎓 COMO USAR ESTE DOCUMENTO

### Para Kick-off de Equipe

1. **Apresentação (30 min):**
   - Use seção "O Grande Quadro" para explicar o sistema
   - Use diagrama de arquitetura para mostrar como tudo se conecta

2. **Workshop (2 horas):**
   - Cada pessoa segue "Caminho de Aprendizado" por perfil
   - Discussão sobre dúvidas

3. **Referência:**
   - Mantenha este documento aberto durante implementação
   - Use mapa de navegação para encontrar documentos específicos

---

### Para Explicar para Stakeholders

**Use estas seções:**
- "O Grande Quadro" - explicação simples
- "Os 4 Pilares do Sistema" - visão de alto nível
- Diagrama de arquitetura - visual

**Evite:**
- Detalhes técnicos muito profundos
- Glossário completo (use apenas termos relevantes)

---

### Para Estudar Sozinho

**Siga o "Caminho de Aprendizado Recomendado":**
1. Comece com "Para Entender o Sistema Completo"
2. Depois siga por perfil (Data Engineer, Data Scientist, etc.)
3. Use glossário quando encontrar termos desconhecidos

---

## ✅ CHECKLIST DE NAVEGAÇÃO

Use este checklist para garantir que entendeu o sistema:

### Visão Geral
- [ ] Entendi o problema que estamos resolvendo
- [ ] Entendi os 4 pilares do sistema
- [ ] Vi o diagrama de arquitetura completo

### Conceitos Técnicos
- [ ] Entendi o que é Analytics Engineering
- [ ] Entendi Bronze/Silver/Gold layers
- [ ] Entendi ETL vs ELT
- [ ] Entendi o que é dbt
- [ ] Entendi o que é Airflow

### Arquitetura
- [ ] Entendi o fluxo de dados end-to-end
- [ ] Entendi como componentes se conectam
- [ ] Entendi cenários práticos (previsão, pipeline diário)

### Documentação
- [ ] Sei onde encontrar cada tipo de informação
- [ ] Sei qual caminho seguir pelo meu perfil
- [ ] Sei onde procurar quando tiver problemas

### Próximos Passos
- [ ] Sei qual fase estamos (Fase 1-2 completa)
- [ ] Sei o que vem a seguir (Semanas 3-4)
- [ ] Sei qual documento ler primeiro

---

## 🚀 PRÓXIMOS PASSOS

Agora que você entendeu a navegação:

1. **Se está no kick-off:**
   - Apresente o sistema usando "O Grande Quadro"
   - Faça workshop seguindo "Caminho de Aprendizado"

2. **Se vai implementar:**
   - Siga "Caminho de Aprendizado" por seu perfil
   - Use "Mapa de Navegação" para encontrar documentos

3. **Se tem dúvidas:**
   - Consulte "Glossário" para termos
   - Use "Referências Cruzadas" para contexto
   - Veja "TROUBLESHOOTING_GUIDE_PT_BR.md" para problemas

---

**Boa sorte na sua jornada com o sistema Nova Corrente! 🎉**

---

**Documento criado:** Novembro 2025  
**Versão:** 1.0  
**Autor:** Equipe Grand Prix SENAI  
**Status:** ✅ Guia de Navegação Completo

**Este documento é seu mapa para navegar todo o ecossistema de roadmaps e documentação técnica!**

