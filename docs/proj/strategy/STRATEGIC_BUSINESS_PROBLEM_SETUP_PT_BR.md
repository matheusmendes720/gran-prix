# 📊 DOCUMENTO ESTRATÉGICO: PROBLEMA DE NEGÓCIO NOVA CORRENTE
## Previsibilidade de Demandas com Inteligência Artificial - Grand Prix SENAI

**Versão:** 1.0  
**Data:** Novembro 2025  
**Empresa:** Nova Corrente Engenharia de Telecomunicações  
**Localização:** Salvador, Bahia, Brasil

---

## 📋 ÍNDICE

1. [Contexto Empresarial e Setorial](#contexto-empresarial)
2. [Definição do Problema de Negócio](#problema-negocio)
3. [Análise B2B vs B2C](#b2b-vs-b2c)
4. [Proposta de Valor Única (UVP)](#proposta-valor)
5. [Objetivos Estratégicos](#objetivos)
6. [Impacto Esperado](#impacto)
7. [Referências e Benchmarking](#referencias)

---

<a name="contexto-empresarial"></a>
## 1. 🏢 CONTEXTO EMPRESARIAL E SETORIAL

### 1.1 Sobre a Nova Corrente

**Nova Corrente** é uma empresa líder brasileira especializada em:
- **Manutenção de estruturas metálicas** para telecomunicações e energia
- **Operação e Manutenção (O&M)** de torres de telecomunicações
- **Soluções de engenharia** e planejamento
- **Inspeções especializadas** (drones, vistorias, análises estruturais)

**Diferenciais competitivos:**
- **+18.000 torres** sob manutenção
- **3 vezes eleita** melhor empresa de O&M preventivas pela maior Sharing mundial
- **Empresa fundada em 2007** com 18 anos de experiência
- **Presença em Salvador:** +100 posições ativas, projeção 150+ até 2026

### 1.2 Contexto do Setor de Telecomunicações no Brasil

**Investimentos em 2024:**
- **R$ 34,6 bilhões** investidos no setor
- **R$ 318 bilhões** em receita bruta
- **Foco principal:** Expansão 5G e banda larga fixa

**Crescimento 5G:**
- **131% crescimento** em cidades com 5G (812 municípios)
- **37.639 antenas** instaladas (dobro do período anterior)
- **52 milhões** de acessos banda larga fixa (+10,1%)

**Mercado Bahia:**
- **222 vagas** disponíveis na região
- **Operadoras principais:** Claro, Vivo, TIM, Oi
- **Tower Companies:** American Tower, SBA Communications, IHS Towers

---

<a name="problema-negocio"></a>
## 2. 🎯 DEFINIÇÃO DO PROBLEMA DE NEGÓCIO

### 2.1 Problema Central

**Situação Atual:**
```
❌ Gestão manual de estoque
❌ Reação a rupturas (não prevenção)
❌ Excesso de estoque em alguns itens
❌ Falta de estoque em outros (rupturas)
❌ Decisões baseadas em intuição, não dados
❌ Alto risco de descumprimento de SLA
```

**Desafios Específicos:**
1. **Rupturas de Estoque:** Peça crítica em falta → Manutenção atrasada → Falha SLA → Multa
2. **Estoque Exagerado:** Capital travado em peças que não movimentam
3. **Lead Times Variáveis:** Fornecedores diferentes têm tempos de entrega distintos
4. **Sazonalidade:** Padrões de consumo variam ao longo do ano
5. **Fatores Externos:** Clima, economia, eventos tecnológicos afetam demanda
6. **Crescimento:** Expansão rápida (+50 posições até 2026) exige planejamento preciso

### 2.2 Descrição Resumida da Demanda

**Objetivo:**  
Desenvolver uma ferramenta que prevê a demanda futura de **insumos/serviços** baseada em dados históricos e tendências sazonais, otimizando a gestão de compras e logística ao antecipar necessidades com base em padrões anteriores.

**Benefícios Esperados:**
- ✅ Redução de sobras e faltas de materiais
- ✅ Planejamento mais preciso
- ✅ Apoio na tomada de decisão de compras
- ✅ Preservação de SLA (99%+ disponibilidade)
- ✅ Otimização do capital de giro

### 2.3 Detalhamento Técnico

**Objetivo Específico:**  
Prever o consumo/demanda de itens (insumos/serviços) para apoiar compras e logística.

**Entradas Sugeridas para Modelos ML:**
- Histórico de consumo semanal/mensal por item
- Datas/feriados
- Tempo médio de entrega (lead time)
- Sazonalidades

**Saídas Mínimas do Sistema:**
1. Projeção para próximos 30 dias por item (tabela e gráfico)
2. Erro médio da previsão em percentual (MAPE)
3. Recomendação (ex: "comprar X unidades em Y dias" considerando SLA/lead time)

**Restrições:**
- Prever para **≥ 5 itens distintos** (escolha da equipe)
- Exibir métrica de erro de previsão

**Incrementos Possíveis:**
- Cenários (otimista/base/pessimista)
- Alertas de ruptura/sobra
- Integração com lead time/SLA
- Interface conversacional para consultas (ex: "qual o consumo previsto do Item A?")

---

<a name="b2b-vs-b2c"></a>
## 3. 💼 ANÁLISE B2B vs B2C

### 3.1 Nova Corrente: Modelo 100% B2B

**Nova Corrente NÃO vende para consumidor final.**

**Cliente Final:**  
Empresas operadoras de telecomunicações e energia que possuem ou compartilham infraestrutura de torres.

### 3.2 Clientes Diretos da Nova Corrente

**Operadoras de Telecomunicações:**
- **Claro/Vivo/TIM** (Brasil telecom)
- **Oi Telecom**
- **Algar Telecom**

**Tower Companies (Sharings):**
- **American Tower Company** (maior sharing mundial)
- **SBA Communications**

**Concessionárias de Energia:**
- Distribuidoras estaduais

### 3.3 Serviços Oferecidos (B2B)

**1. Manutenção Preventiva (O&M):**
- Limpeza e inspeção de torres
- Aperto de parafusos e componentes
- Verificação de integridade estrutural
- Testes de conectividade

**2. Manutenção Corretiva:**
- Reparos emergenciais (24-48h)
- Substituição de componentes defeituosos
- Restauração de serviços críticos

**3. Implantação:**
- Construção de novos sites
- Instalação de equipamentos
- Ampliação de cobertura

**4. Inspeções Especializadas:**
- Vistorias com drones
- Análises estruturais
- Relatórios técnicos detalhados

### 3.4 SLA (Service Level Agreement) - CRÍTICO para B2B

**Características dos SLAs em B2B:**
```
Disponibilidade Mínima:     99%+ (máximo 1 hora downtime/mês)
Tempo de Resposta:          4-8 horas (emergências)
Multa por Descumprimento:   2-10% do valor do contrato
Garantia de Estoque:        Peças críticas sempre disponíveis
```

**Por que SLA é crítico em B2B?**
- Contratos de longo prazo (anos)
- Penalidades financeiras por falhas
- Impacto na reputação da empresa
- Relacionamento comercial em risco
- Perda de receita recorrente

**Cascata de Impacto de Ruptura:**
```
Ruptura de estoque de peça crítica
  ↓
Manutenção atrasada/interrompida
  ↓
Falha no SLA (99%+)
  ↓
Multa (R$ milhões)
  ↓
Perda de cliente B2B
  ↓
Prejuízo alto para Nova Corrente
```

### 3.5 Diferenças B2B vs B2C Relevant ao Problema

| Característica | B2B (Nova Corrente) | B2C (Típico) |
|----------------|---------------------|--------------|
| **Volume** | Alto volume por cliente | Baixo volume por transação |
| **Relacionamento** | Contratos longos, parcerias | Transações pontuais |
| **Penalidades** | Multas SLA, contratuais | Devolução/reembolso |
| **Especificidade** | Peças técnicas específicas | Produtos genéricos |
| **Lead Time** | Aceita prazos maiores | Espera imediata |
| **Variabilidade** | Padrões relativamente estáveis | Volatilidade alta |
| **Previsibilidade** | Mais previsível (contratos) | Menos previsível (tendências) |

**Implicação:**  
Como B2B, a Nova Corrente tem **padrões de demanda relativamente estáveis** baseados em contratos de manutenção, facilitando a previsão por IA comparado a modelos B2C.

---

<a name="proposta-valor"></a>
## 4. 🚀 PROPOSTA DE VALOR ÚNICA (UVP)

### 4.1 Declaração de Valor

**Para:** Nova Corrente (gestores de compras, gerentes de operação)  
**Quem precisa:** Reduzir rupturas de estoque e otimizar capital de giro  
**Nossa solução:** Sistema de IA que prevê demanda diária de materiais  
**Diferente porque:** Usa ML para aprender padrões de consumo histórico + fatores externos  
**Resultado:** -60% rupturas, -20% estoque excessivo, SLA preservado

### 4.2 Componentes da UVP

**1. Previsão Inteligente de Demanda:**
```
IA Analisa:
- Histórico de 2+ anos de consumo
- Sazonalidade (estações, feriados)
- Fatores climáticos (chuva, calor, tempestades)
- Fatores econômicos (câmbio, inflação)
- Fatores tecnológicos (expansão 5G)
- Fatores operacionais (manutenções agendadas)
```

**2. Cálculo Automático de Reorder Point (PP):**
```
Fórmula: PP = (Demanda_Diária × Lead_Time) + Safety_Stock
- Demanda prevista pela IA
- Lead time do fornecedor
- Buffer de segurança estatístico
```

**3. Alertas Proativos:**
```
Quando Estoque ≤ PP:
🔴 ALERTA para equipe de compras
📧 Email automático
📱 SMS para gerente
📊 Log no dashboard
```

**4. Relatórios Semanais Acionáveis:**
```
"Conector Óptico: Faltam 7 dias até ruptura"
"Compre 250 unidades até 05/11/2025"
"Incluir +50 unidades por alerta meteorológico"
```

### 4.3 Diferenciação Competitiva

**vs. Gestão Manual:**
- ✅ Dados, não intuição
- ✅ Proativa (prevenção), não reativa
- ✅ Escalável (18.000 torres → infinitas)
- ✅ Adaptável (aprende com o tempo)

**vs. Sistemas Genéricos:**
- ✅ Específico para telecomunicações
- ✅ Incorpora fatores setoriais (5G, SLA, climáticos)
- ✅ Validado com datasets MIT/telecom
- ✅ ROI em 1-2 meses (benchmarks Walmart, Tesco)

**vs. Consultorias Manuais:**
- ✅ Custo menor
- ✅ Atualização contínua
- ✅ Decisões em tempo real
- ✅ Não depende de especialista disponível

---

<a name="objetivos"></a>
## 5. 🎯 OBJETIVOS ESTRATÉGICOS

### 5.1 Objetivo Principal

**Implementar sistema de previsão de demanda com IA** que reduza rupturas de estoque em 60% e otimize capital de giro em 20%, mantendo SLA de 99%+.

### 5.2 Objetivos Específicos (SMART)

**1. Precisão da Previsão:**
- **Específico:** Alcançar MAPE < 15%
- **Mensurável:** Erro médio percentual (MAPE)
- **Atingível:** Benchmarks apontam 10-15% para telecom
- **Relevante:** Impacta qualidade das decisões
- **Temporal:** 3 meses após implementação

**2. Redução de Rupturas:**
- **Específico:** Reduzir rupturas de estoque em 60%
- **Mensurável:** Nº de rupturas por mês
- **Atingível:** Controle proativo vs. reativo
- **Relevante:** Preserva SLA 99%
- **Temporal:** 6 meses após implementação

**3. Otimização de Capital:**
- **Específico:** Reduzir estoque médio em 20%
- **Mensurável:** Valor financeiro do estoque
- **Atingível:** Reposicionamento baseado em dados
- **Relevante:** Melhora capital de giro
- **Temporal:** 6-12 meses

**4. Cobertura de Itens:**
- **Específico:** Prever ≥ 5 itens críticos
- **Mensurável:** Nº de itens cobertos
- **Atingível:** Pipeline modular escalável
- **Relevante:** Demonstra viabilidade
- **Temporal:** Demoday + 2 semanas

### 5.3 Objetivos de Longo Prazo (Visão)

**Ano 1:**
- 20+ itens previstos
- Integração com ERP
- API disponível para múltiplos departamentos

**Ano 2:**
- Expansão para 50+ itens
- Interface conversacional (ChatGPT-like)
- Previsão multi-local (regiões distintas)

**Ano 3:**
- MVP pronto para comercialização
- Pivote para SaaS (oferta para outras tower companies)
- Novos streams de receita

---

<a name="impacto"></a>
## 6. 💰 IMPACTO ESPERADO

### 6.1 Métricas de Negócio (KPIs)

| Métrica | Baseline | Target | Impacto Financeiro |
|---------|----------|--------|-------------------|
| **Frequência de Rupturas** | Atual | -60% | Menos multas SLA, emergências |
| **Estoque Médio** | Atual | -20% | Menos capital travado |
| **DIO (Days Inventory Outstanding)** | Atual | -15% | Giro mais rápido |
| **Precisão (MAPE)** | N/A | <15% | Confiabilidade |
| **Lead Time Utilization** | Atual | >85% | Eficiência operacional |

### 6.2 ROI Estimado

**Investimento Inicial:**
- Desenvolvimento: R$ 100k-150k
- Infraestrutura: R$ 20k-30k
- Treinamento: R$ 10k-15k
- **Total:** R$ 130k-195k

**Retorno Anual (estimativa conservadora):**
- Redução multas SLA: R$ 100k-200k
- Otimização estoque: R$ 50k-100k
- Redução emergências: R$ 30k-50k
- **Total:** R$ 180k-350k

**Payback:** 6-12 meses  
**ROI Ano 1:** 80-180%

### 6.3 Impactos Indiretos

**Operacionais:**
- Menos "put out fires" (apagar incêndios)
- Equipe de compras mais estratégica
- Menos stress em emergências
- Melhor planejamento de capacidade

**Organizacionais:**
- Cultura data-driven
- Inovação tecnológica
- Atração de talentos (tech)
- Reputação no mercado

**Estratégicos:**
- MVP para expansão
- Base para outros projetos IA
- Diferenciação competitiva
- Preparação para 5G/crescimento

---

<a name="referencias"></a>
## 7. 📚 REFERÊNCIAS E BENCHMARKING

### 7.1 Frameworks e Modelos Aplicados

**SCOR (Supply Chain Operations Reference):**
- Padrão global para análise de supply chain
- Métricas: Planejamento, Sourcing, Fabricação, Entregas, Retornos
- Aplicação: Estruturar análise de processos Nova Corrente

**CPFR (Collaborative Planning, Forecasting, and Replenishment):**
- Planejamento colaborativo com fornecedores
- Aplicação: Integrar fornecedores no sistema

**VMI (Vendor Managed Inventory):**
- Fornecedores gerenciam estoque do cliente
- Aplicação: Possível expansão futura do sistema

### 7.2 Benchmarks de Sucesso

**Walmart (Retail):**
- 20x mais rápido treinamento ML
- Redução de custos de estoque
- Aplicação: Modelos de ML para demanda

**Tesco (Retail):**
- Previsão para milhares de produtos
- Integração IoT + ML
- Aplicação: Escalabilidade do sistema

**AWS Supply Chain:**
- 25 modelos de previsão (ARIMA, LSTM, Prophet)
- Previsões rápidas e precisas
- Aplicação: Arquitetura de modelos

### 7.3 Datasets de Validação

**MIT Spare Parts Telecom:**
- 2.058 sites, 3 anos
- Máxima relevância
- Uso: Validação

**Kaggle Datasets:**
- Daily Demand Forecasting: MVP
- Logistics Warehouse: PP validation
- Retail Inventory: Modelos complexos

### 7.4 Estudos Acadêmicos

**Multi-Channel Data Fusion Network (MCDFN):**
- CNN + LSTM + GRU integrados
- Aplicação: Ensemble avançado

**DeepAR+ (AWS):**
- Redes neurais multivariadas
- Aplicação: Previsão interdependente

---

## 📌 CONCLUSÃO

Este documento estabelece o **problema de negócio** como base para desenvolvimento do sistema de previsibilidade de demandas com IA para Nova Corrente. O foco em **B2B**, **SLA crítico** e **previsão de demanda (não estoque)** diferencia a solução no mercado.

**Próximos Passos:**
1. Validar objetivos com stakeholders
2. Priorizar itens para previsão (≥5)
3. Estruturar data pipeline
4. Iniciar desenvolvimento MVP

---

**Documento Final:** Novembro 2025  
**Autor:** Equipe Grand Prix SENAI  
**Versão:** 1.0  
**Status:** ✅ Aprovado para Desenvolvimento

