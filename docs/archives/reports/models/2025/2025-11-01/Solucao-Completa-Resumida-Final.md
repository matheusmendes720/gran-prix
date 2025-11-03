# 🚀 SOLUÇÃO COMPLETA: SISTEMA DE PREVISIBILIDADE DE DEMANDA
## Nova Corrente - Engenharia de Telecomunicações

---

## RESUMO EXECUTIVO (2 MINUTOS)

**Problema:** Nova Corrente tem 18.000+ torres em manutenção O&M com SLA 99%+. Ruptura de estoque = falha SLA = multa. Sistema manual não consegue prever quando comprar.

**Solução:** Sistema AI que:
1. **Prevê** consumo diário de materiais (IA)
2. **Calcula** quando comprar via Reorder Point (PP)
3. **Alerta** equipe de compras ANTES de faltar material
4. **Relata** dias até ruptura + recomendações

**Resultado Esperado:** -60% ruptura de estoque, -20% estoque desnecessário, ROI em 1-2 meses.

---

## PARTE 1: MODELO DE NEGÓCIO - CONTEXTO

### B2B (Business-to-Business) 100%

**Nova Corrente NÃO vende para consumidor final:**

**Clientes Diretos:**
- **Operadoras Telecom (principais):** Claro/Vivo/TIM, Oi Telecom, Algar Telecom
- **Tower Companies (Sharings):** American Tower Company, SBA Communications
- **Concessionárias de Energia:** Distribuidoras estaduais

**Serviços:**
- Manutenção Preventiva (O&M): Limpeza, inspeção, aperto de parafusos
- Manutenção Corretiva: Reparos emergenciais (24-48h)
- Implantação: Construção de novos sites
- Inspeções especializadas: Drone, vistoria, reforço estrutural

**SLA (Service Level Agreement) - CRÍTICO:**
- **Disponibilidade mínima:** 99%+ (máximo 1 hora downtime/mês)
- **Tempo de resposta emergencial:** 4-8 horas
- **Multa por descumprimento:** 2-10% do valor do contrato
- **Garantia de estoque:** Peças críticas sempre disponíveis

**👉 POR QUE PREVISIBILIDADE IMPORTA:**
```
Ruptura de estoque de peça crítica
  ↓
Manutenção atrasada/interrompida
  ↓
Falha SLA (99%)
  ↓
Multa + Perda de cliente
  ↓
Prejuízo alto para Nova Corrente
```

---

## PARTE 2: OS 3 PILARES DA SOLUÇÃO

### 🔷 PILAR 1: IA Prevê DEMANDA (Não Estoque)

**O que a IA faz:**
- Analisa histórico de **consumo diário** dos últimos 2+ anos
- Identifica padrões (sazonalidade, trend, anomalias)
- Incorpora **fatores externos** (clima, economia, tecnologia)
- **OUTPUT:** "Amanhã será consumido 8 conectores ópticos"

**O que a IA NÃO faz:**
- ❌ NÃO prevê nível de estoque
- ❌ NÃO calcula reorder points
- ❌ NÃO gera alertas

**Por que é importante:**
- Demanda = **sinal real do negócio** (quantos clientes precisam)
- Estoque = **derivado** (demanda - compras + SLA)
- Separar responsabilidades = **robustez**

**Fórmula:**
```
Demanda_Prevista = f(
    histórico_consumo_diário,
    sazonalidade_mensal,
    fator_climático,
    fator_econômico,
    fator_tecnológico,
    fator_operacional
)
```

**Exemplo:**
```
DATA: 2025-11-07 (quinta-feira)
Estoque atual: 100 conectores

IA prevê: 8 conectores consumidos
Sistema calcula: 100 - 8 = 92 amanhã

Se 92 > Reorder Point (90) → ✅ Situação normal
Se 92 ≤ Reorder Point (90) → 🔴 ALERTA!
```

---

### 🔷 PILAR 2: Alertas no Reorder Point (PP) ⚠️ CRÍTICO

**O Problema com Estoque Mínimo:**
```
❌ ERRADO: Alerta quando estoque = Mínimo (20)

Estoque = 20 unidades
Fornecedor leva 14 dias
Consumo diário = 8 unidades

Em 14 dias consomem: 8 × 14 = 112 unidades
Mas tem: 20 unidades
RESULTADO: Ruptura em 2-3 dias! ❌
```

**✅ CERTO: Alerta quando estoque = Reorder Point (PP)**

**Fórmula do Reorder Point:**
```
PP = (Demanda_Diária × Lead_Time_Dias) + Safety_Stock

Onde:
- Demanda_Diária: Fornecida pela IA
- Lead_Time_Dias: Dias que fornecedor leva para entregar
- Safety_Stock: Buffer de proteção (2-3 semanas de estoque)
```

**Exemplo Prático:**
```
Material: CONECTOR ÓPTICO SC/APC

Demanda diária: 8 conectores (da IA)
Lead time: 14 dias (Supplier A)
Safety stock: 20 unidades (buffer)

PP = (8 × 14) + 20 = 132 unidades

✅ Alerta dispara quando estoque ≤ 132
   Isso dá 14 dias para fornecedor entregar
   + 20 unidades de proteção se demanda aumentar

❌ Sem isso: Espera 20 unidades, mas já perdeu 14 dias
```

**Por Material Diferente:**

| Material | Demanda | Lead Time | Safety | PP | Razão |
|----------|---------|-----------|--------|-----|-------|
| Conector | 8/dia | 14 | 20 | 132 | Alto uso + entrega demorada |
| Estrutura | 2/dia | 10 | 15 | 35 | Baixo uso + menor lead time |
| Refrigeração | 0.5/dia | 21 | 30 | 40.5 | Raro + crítico + demora |

---

### 🔷 PILAR 3: Previsão DIÁRIA (Não Mensal)

**Por que DIÁRIO?**

```
❌ MENSAL (ERRADO):
- Consumo total mês: 240 conectores
- Não sabe QUANDO vai acabar
- Não pode calcular PP corretamente
- Não pode gerar alerta de "7 dias até ruptura"

✅ DIÁRIO (CERTO):
- Dia 1: 8 conectores
- Dia 2: 7 conectores
- Dia 3: 9 conectores
- Dia 4: 8 conectores
- ...
- Dia 30: 8 conectores
- Total: 240 (mesma quantidade, MAS com precisão)
- Permite alertas diários
- Permite recalcular PP diariamente
```

**Necessidades que exigem Diário:**

1. **Alerta:** "Faltam 7 dias até ruptura" → Precisa saber exatamente qual dia
2. **Recomendação:** "Compre 250 em 2 dias" → Precisa granularidade diária
3. **Relatório:** Mostrar dias progressivos até ruptura
4. **Reorder Point:** Recalcular PP diariamente conforme estoque muda
5. **Eventos:** Responder a alertas climáticos/econômicos (horas → dias)

**Saídas com Previsão Diária:**

```
ALERTA DIÁRIO:
Conector Óptico: Faltam 7 dias até ruptura (2025-11-13)

RECOMENDAÇÃO:
Compre 250 conectores até 2025-11-06 (aproveitando lead time 14 dias)

RELATÓRIO SEMANAL:
Data      | Estoque | Consumo | Dias até Ruptura | Status
2025-11-07| 92      | 8       | 10 dias          | 🟡 ATENÇÃO
2025-11-14| 36      | 8       | 4 dias           | 🔴 COMPRE URGENTE
2025-11-21| -       | 8       | RUPTURA          | ❌ JÁ FALHOU
```

---

## PARTE 3: FATORES EXTERNOS QUE IMPACTAM

### Climáticos 🌡️

| Evento | Impacto | Materiais | Lead Time Ajuste |
|--------|---------|-----------|------------------|
| **Calor > 32°C** | +30% | Refrigeração, conectores | +2-3 dias |
| **Chuva Intensa** | +40% | Estrutura, isolamento | +3-5 dias |
| **Umidade Alta** | +20% | Parafusos, conectores | +5-7 dias |
| **Tempestades** | +50% URGENTE | Reforço estrutural | +5-10 dias |

**Ação:** API INMET (previsão meteorológica) → Sistema calcula impacto → Alerta antecipado

### Econômicos 💰

| Evento | Impacto | Lead Time | Ação |
|--------|---------|-----------|------|
| **Desvalorização BRL** | Fornecedor reduz | 7→14 dias | Antecipar 3-5 dias |
| **Greve Transporte** | -100% entregas | 14→21+ dias | +50% safety stock |
| **Restrição Import** | Falta componentes | ×2-3 | Comprar local/premium |

**Ação:** BACEN (câmbio) + Google News API → Alertas automáticos

### Tecnológicos 🔌

| Evento | Impacto | Ação |
|--------|---------|------|
| **Expansão 5G** | +15-20% demanda/ano | Antecipar novo material |
| **Migração Fibra** | -30% cabo simples, +50% fibra | Migrar mix de produtos |

**Ação:** ANATEL dados (5G expansion) → Previsão proativa

### Operacionais 📅

| Período | Impacto | Ação |
|---------|---------|------|
| **Férias Julho** | -25% demanda | Reduzir previsão |
| **Feriados prolongados** | -20% demanda | Ajustar PP downward |
| **Renovação SLA (Jan/Jul)** | +25% demanda | +Estoque 3-4 semanas |

**Ação:** Calendário hard-coded + histórico padrões

---

## PARTE 4: PIPELINE COMPLETO

### Etapa 1: ENTRADA (Input Layer)

```
✓ Histórico de consumo diário
  └─ Fonte: Sistema ERP/WMS da Nova Corrente
  └─ Formato: Data, Material_ID, Qty, Site, Custo
  └─ Período: Mínimo 2 anos

✓ Lead times por fornecedor
  └─ Fonte: Tabela contatos de fornecedores
  └─ Formato: Supplier, Material, Lead_Days, Std_Dev

✓ Previsão meteorológica
  └─ Fonte: INMET (Instituto Meteorologia)
  └─ API: https://www.inmet.gov.br/

✓ Calendário de eventos
  └─ Feriados nacionais/regionais
  └─ Férias de equipes
  └─ Renovação de SLAs

✓ Indicadores econômicos
  └─ Fonte: BACEN (Banco Central)
  └─ Taxa de câmbio, inflação, Selic

✓ Dados de infraestrutura 5G
  └─ Fonte: ANATEL
  └─ Municípios com 5G, crescimento
```

### Etapa 2: PROCESSAMENTO (ML Layer)

```
1. EDA - Análise Exploratória
   ├─ Limpar dados (missing values, outliers)
   ├─ Calcular estatísticas (média, std dev, percentis)
   └─ Decomposição (trend, seasonality, noise)

2. Feature Engineering
   ├─ Sazonalidade mensal (1-12)
   ├─ Sazonalidade semanal (0-6)
   ├─ Indicadores cíclicos (sin/cos)
   ├─ Lag features (t-1, t-7, t-30)
   ├─ Média móvel (7 dias, 30 dias)
   └─ Fatores externos (temperatura, câmbio, feriado)

3. Seleção de Modelo
   ├─ Opção A: ARIMA (Recomendado para começar)
   ├─ Opção B: Facebook Prophet (com múltiplas sazonalidades)
   ├─ Opção C: LSTM (redes neurais, se dados complexos)
   └─ Opção D: Ensemble (combinar múltiplos)

4. Treinamento
   ├─ Split: 80% treino, 20% teste
   ├─ Validação cruzada (5-fold)
   └─ Otimização de hiperparâmetros

5. Validação
   ├─ Métrica: MAPE < 15% (acceptable), ideal < 10%
   ├─ Backtest contra histórico de ruptura
   └─ Teste por categoria de material

6. Ensemble
   ├─ Weighted average: 0.3×ARIMA + 0.3×Prophet + 0.4×LSTM
   └─ Refinamento de pesos por performance
```

### Etapa 3: CÁLCULOS DETERMINÍSTICOS

```
Reorder Point:
PP = (Demanda_Diária × Lead_Time) + Safety_Stock

Safety Stock (formulação estatística):
SS = Z_service × σ_demand × √(Lead_Time)
   onde Z = 1.65 (95% disponibilidade)

Dias até Ruptura:
Dias = (Estoque_Atual - Safety_Stock) / Demanda_Diária

Lead Time Ajustado (com riscos externos):
Lead_Time_Adj = Lead_Time_Base × (1 + Risk_Factor)
   ex: Risk_Factor = 0.5 se há alerta de greve

Status:
├─ 🟢 OK: Estoque > PP × 1.2
├─ 🟡 ATENÇÃO: PP × 0.8 < Estoque ≤ PP × 1.2
└─ 🔴 COMPRE JÁ: Estoque ≤ PP × 0.8
```

### Etapa 4: SAÍDA (Output Layer)

```
✓ PREVISÃO 30 DIAS
  ├─ Quantidade prevista por dia
  ├─ Confidence interval (95%)
  └─ Gráfico com histórico + projeção

✓ REORDER POINT CALCULADO
  ├─ Por material
  ├─ Por fornecedor
  └─ Com ajustes de risco

✓ ALERTA AUTOMÁTICO
  ├─ Quando Estoque ≤ PP
  ├─ Email para procurement
  ├─ SMS para gerente
  └─ Log em dashboard

✓ DIAS ATÉ RUPTURA
  ├─ Cálculo diário
  ├─ Projeção se continuar padrão
  └─ Cenários (otimista, base, pessimista)

✓ RECOMENDAÇÃO DE COMPRA
  ├─ "Compre X unidades em Y dias"
  ├─ Considerando lead time + forecast
  ├─ Com justificativa (clima, 5G, etc)
  └─ Prioridade (urgente, normal, baixa)

✓ RELATÓRIO SEMANAL
  ├─ Tabela de status por material
  ├─ Gráficos de consumo vs previsão
  ├─ Alertas pendentes
  └─ Ações recomendadas
```

---

## PARTE 5: EXEMPLO PRÁTICO COMPLETO

### Cenário: CONECTOR ÓPTICO SC/APC

**Dados Iniciais:**
```
Material: Conector Óptico SC/APC
Demanda média: 8 unidades/dia
Fornecedor: Supplier A
Lead time: 14 dias
Safety stock: 20 unidades
Data hoje: 2025-10-20
Estoque atual: 85 unidades
```

**Cálculo de Reorder Point:**
```
PP = (8 × 14) + 20 = 132 unidades
```

**Simulação 10 Dias:**

| Data | Estoque | Consumo | Previsão_IA | Status | Ação |
|------|---------|---------|-------------|--------|------|
| 20-out | 85 | 8 | 8.2 | 🔴 ALERTA | **COMPRE HOJE** |
| 21-out | 77 | 7 | 7.1 | 🔴 ALERTA | Confirmada |
| 22-out | 70 | 2 | 8.3 | 🔴 ALERTA | Monitorar |
| 23-out | 68 | 8 | 8.0 | 🔴 ALERTA | Monitorar |
| 24-out | 60 | 8 | 7.9 | 🔴 ALERTA | Monitorar |
| 25-out | 52 | 2 | 8.1 | 🔴 ALERTA | Monitorar |
| 26-out | 50 | 8 | 8.2 | 🔴 ALERTA | Monitorar |
| 27-out | 42 | 8 | 7.8 | 🔴 ALERTA | **ÚLTIMO AVISO** |
| 28-out | 35 | 7 | 8.0 | 🔴 ALERTA | **CRÍTICO** |
| 29-out | 27 | 8 | 8.5 | 🔴 ALERTA | **RUPTURA EM 3 DIAS** |

**Cenários:**

**Cenário A: Se compra em 20-out (recomendação seguida)**
```
Compra 250 unidades em 20-out
Entrega em 03-nov (20 + 14 dias)

Estoque 29-out: 27 (baixo, mas OK)
Estoque 03-nov: 277 (reabastecimento)
✅ Sem ruptura
```

**Cenário B: Se compra em 27-out (tarde demais)**
```
Compra 250 unidades em 27-out
Entrega em 10-nov (27 + 14 dias)

Estoque 29-out: 27 (crítico)
Estoque 30-oct: 19 (RUPTURA!)
❌ Falha de SLA
```

**Cenário C: Se alerta com fator climático (chuva)**
```
Alerta de chuva intensa: +40% demanda

Demanda ajustada: 8 × 1.4 = 11.2 unidades/dia
PP ajustado: (11.2 × 14) + 20 = 176.8 ≈ 177

Estoque 29-out: 27
Status: ❌ CRÍTICO! Vai acabar em 2 dias

Sistema recomenda: Compre HOJE (urgente)
```

---

## PARTE 6: DATASETS PARA TREINAR

### Dataset 1: MIT Spare Parts Telecom (MELHOR)
- **Relevância:** ⭐⭐⭐⭐⭐ Máxima
- **Tamanho:** 2,058 sites, 3 anos
- **Estrutura:** Perfeita para Nova Corrente
- **Uso:** Validação real, benchmarking
- **URL:** https://dspace.mit.edu/bitstream/handle/1721.1/142919/SCM12_Mamakos_project.pdf

### Dataset 2: Kaggle - Daily Demand Forecasting
- **Relevância:** ⭐⭐⭐⭐⭐ MVP/Prototipagem
- **Tamanho:** 60 dias, limpo
- **Uso:** Demoday, testes rápidos
- **URL:** https://www.kaggle.com/datasets/akshatpattiwar/daily-demand-forecasting-orderscsv

### Dataset 3: Kaggle - Logistics Warehouse
- **Relevância:** ⭐⭐⭐⭐ Alto
- **Tamanho:** 3,204 registros
- **Uso:** Validar Reorder Points contra histórico
- **URL:** https://www.kaggle.com/datasets/ziya07/logistics-warehouse-dataset

### Dataset 4: Kaggle - Retail Store Inventory
- **Relevância:** ⭐⭐⭐⭐ Alto
- **Tamanho:** 73,000+ registros
- **Uso:** Testar modelos complexos (Prophet, LSTM)
- **URL:** https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset

### Dataset 5: Kaggle - High-Dimensional Supply Chain
- **Relevância:** ⭐⭐⭐⭐ Alto
- **Tamanho:** Centenas mil registros
- **Uso:** Fatores externos integrados
- **URL:** https://www.kaggle.com/datasets/ziya07/high-dimensional-supply-chain-inventory-dataset

---

## PARTE 7: ROADMAP FINAL

### Semana 1 (ATÉ 06 NOV) - DEMODAY

- [ ] PM Canvas completo
- [ ] Protótipo ARIMA funcionando (Dataset Kaggle)
- [ ] Forecast 30 dias
- [ ] Cálculo PP + dias até ruptura
- [ ] Pitch 5 minutos

### Semana 2 (10-14 NOV) - PÓS-DEMODAY

- [ ] Dados reais da Nova Corrente integrados
- [ ] Validação contra MIT dataset
- [ ] MAPE < 15% alcançado
- [ ] Dashboard em tempo real

### Semana 3-4 (17-30 NOV)

- [ ] Múltiplos modelos testados
- [ ] Ensemble otimizado
- [ ] Alertas automáticos funcionando
- [ ] Relatórios semanais

### Dezembro+ - PRODUÇÃO

- [ ] API rodando
- [ ] Integração ERP
- [ ] A/B testing
- [ ] Feedback loop com suprimentos

---

**Documento Final:** 31 de outubro de 2025  
**Status:** Pronto para Demoday & Desenvolvimento  
**Versão:** 4.0 FINAL
