# 📦 BREAKDOWN COMPLETO: GESTÃO DE ESTOQUE
## Análise Matemática Profunda - Nova Corrente

---

**Data:** Novembro 2025  
**Versão:** Inventory Breakdown v1.0  
**Status:** ✅ Breakdown Completo Expandido

---

## 📋 ÍNDICE EXPANDIDO

### Parte I: Fundamentos de Estoque
1. [Safety Stock (SS) - Completo](#1-safety-stock-completo)
2. [Reorder Point (PP) - Completo](#2-reorder-point-completo)
3. [Economic Order Quantity (EOQ)](#3-economic-order-quantity-eoq)
4. [Lead Time Variability](#4-lead-time-variability)
5. [Demand Variability](#5-demand-variability)

### Parte II: Matemática Profunda
6. [Derivação Completa Safety Stock](#6-derivação-safety-stock)
7. [Derivação Completa Reorder Point](#7-derivação-reorder-point)
8. [Derivação Completa EOQ](#8-derivação-eoq)
9. [Probabilistic Models](#9-probabilistic-models)
10. [Service Level Optimization](#10-service-level-optimization)

### Parte III: Fatores Externos
11. [Climatic Factors](#11-climatic-factors)
12. [Economic Factors](#12-economic-factors)
13. [Holiday Effects](#13-holiday-effects)
14. [SLA Renewals](#14-sla-renewals)
15. [5G Expansion Impact](#15-5g-expansion-impact)

### Parte IV: Modelos Avançados
16. [Multi-Item Models](#16-multi-item-models)
17. [Dynamic Safety Stock](#17-dynamic-safety-stock)
18. [Newsboy Problem](#18-newsboy-problem)
19. [ABC Analysis Integration](#19-abc-analysis)
20. [Real-Time Adjustments](#20-real-time-adjustments)

---

# 1. SAFETY STOCK (SS) - COMPLETO

## 1.1 Fórmula Básica

**Safety Stock com demanda e lead time variáveis:**

$$SS = Z_{\alpha} \sqrt{L \sigma_D^2 + D^2 \sigma_L^2}$$

onde:
- $Z_{\alpha}$: quantil normal padrão (ex: 1.65 para 95% service level)
- $L$: lead time médio (dias)
- $\sigma_D$: desvio padrão da demanda diária
- $D$: demanda média diária
- $\sigma_L$: desvio padrão do lead time (dias)

## 1.2 Casos Especiais

### Caso 1: Lead Time Constante
**Se $\sigma_L = 0$:**
$$SS = Z_{\alpha} \sigma_D \sqrt{L}$$

### Caso 2: Demanda Constante
**Se $\sigma_D = 0$:**
$$SS = Z_{\alpha} D \sigma_L$$

### Caso 3: Ambas Variáveis
**Fórmula completa:**
$$SS = Z_{\alpha} \sqrt{L \sigma_D^2 + D^2 \sigma_L^2}$$

## 1.3 Service Level

**Probabilidade de não ter ruptura:**
$$P(\text{Estoque} \geq \text{Demanda durante LT}) = \alpha$$

**Exemplos:**
- $\alpha = 0.95$ (95%) → $Z_{\alpha} = 1.65$
- $\alpha = 0.99$ (99%) → $Z_{\alpha} = 2.33$
- $\alpha = 0.999$ (99.9%) → $Z_{\alpha} = 3.09$

---

# 2. REORDER POINT (PP) - COMPLETO

## 2.1 Fórmula Básica

**Reorder Point = Demanda durante Lead Time + Safety Stock:**

$$PP = D \times L + SS$$

**Expandindo:**
$$PP = D \times L + Z_{\alpha} \sqrt{L \sigma_D^2 + D^2 \sigma_L^2}$$

## 2.2 Casos Especiais

### Caso 1: Lead Time Constante
$$PP = D \times L + Z_{\alpha} \sigma_D \sqrt{L}$$

### Caso 2: Demanda Constante
$$PP = D \times L + Z_{\alpha} D \sigma_L = D(L + Z_{\alpha} \sigma_L)$$

## 2.3 Interpretação

**Quando estoque atinge PP:**
1. **Comprar** quantidade $Q$ (EOQ)
2. **Tempo até chegada:** Lead Time $L$
3. **Consumo durante LT:** $D \times L$
4. **Proteção:** Safety Stock $SS$
5. **Estoque mínimo ao receber:** $SS$

---

# 3. ECONOMIC ORDER QUANTITY (EOQ)

## 3.1 Fórmula Básica

**EOQ clássico:**
$$Q^* = \sqrt{\frac{2DS}{H}}$$

onde:
- $D$: demanda anual (unidades/ano)
- $S$: custo de pedido (R$/pedido)
- $H$: custo de estoque anual (R$/unidade/ano)

## 3.2 Custo Total

**Custo total anual:**
$$TC(Q) = \frac{D}{Q} S + \frac{Q}{2} H$$

**Onde:**
- $\frac{D}{Q} S$: custo de pedido anual
- $\frac{Q}{2} H$: custo de estoque médio anual

**Otimização:** Derivando e igualando a zero:
$$\frac{dTC}{dQ} = -\frac{DS}{Q^2} + \frac{H}{2} = 0$$

**Resultado:**
$$Q^* = \sqrt{\frac{2DS}{H}}$$

## 3.3 EOQ com Desconto

**Se desconto por quantidade:**
$$TC(Q) = \frac{D}{Q} S + \frac{Q}{2} H + D \times P(Q)$$

onde $P(Q)$ é preço unitário (depende de $Q$).

**Avaliar:**
1. $EOQ$ padrão
2. Pontos de desconto
3. Escolher $Q$ que minimize $TC$

---

# 4. LEAD TIME VARIABILITY

## 4.1 Impacto na Safety Stock

**Variação no lead time aumenta SS:**
$$\Delta SS = Z_{\alpha} D \Delta \sigma_L$$

**Exemplo:**
- $D = 10$ unidades/dia
- $\sigma_L$ aumenta de 2 para 3 dias
- $Z_{\alpha} = 1.65$ (95%)
- $\Delta SS = 1.65 \times 10 \times 1 = 16.5$ unidades

## 4.2 Mitigação

**Estratégias:**
1. **Fornecedores múltiplos:** Reduz $\sigma_L$
2. **Contratos garantidos:** Fixa $L$
3. **Buffer de fornecedores:** Compensa variação

---

# 5. DEMAND VARIABILITY

## 5.1 Impacto na Safety Stock

**Variação na demanda aumenta SS:**
$$\Delta SS = Z_{\alpha} \sqrt{L} \Delta \sigma_D$$

**Exemplo:**
- $L = 7$ dias
- $\sigma_D$ aumenta de 2 para 3 unidades/dia
- $Z_{\alpha} = 1.65$
- $\Delta SS = 1.65 \times \sqrt{7} \times 1 = 4.4$ unidades

## 5.2 Redução de Variabilidade

**Estratégias:**
1. **Previsão melhor:** Reduz $\sigma_D$
2. **Agregação de itens:** Pooling effect
3. **Gestão de demanda:** Suaviza picos

---

# 6. DERIVAÇÃO COMPLETA SAFETY STOCK

## 6.1 Modelo Probabilístico

**Assumindo:**
- Demanda durante LT: $D_L \sim \mathcal{N}(\mu_L, \sigma_L^2)$
- Lead Time: $L \sim \mathcal{N}(\mu_L, \sigma_L^2)$

**Demanda total durante LT:**
$$D_{total} = \sum_{i=1}^{L} D_i$$

**Se $D_i \sim \mathcal{N}(\mu_D, \sigma_D^2)$ independentes:**
$$\mathbb{E}[D_{total}] = L \mu_D$$
$$\text{Var}(D_{total}) = L \sigma_D^2 + \mu_D^2 \sigma_L^2$$

**Aproximação normal:**
$$D_{total} \sim \mathcal{N}(L \mu_D, L \sigma_D^2 + \mu_D^2 \sigma_L^2)$$

## 6.2 Service Level Constraint

**Probabilidade de não ter ruptura:**
$$P(D_{total} \leq \text{Estoque}) = \alpha$$

**Normalizando:**
$$P\left(\frac{D_{total} - L\mu_D}{\sqrt{L\sigma_D^2 + \mu_D^2\sigma_L^2}} \leq \frac{SS}{\sqrt{L\sigma_D^2 + \mu_D^2\sigma_L^2}}\right) = \alpha$$

**Resultado:**
$$SS = Z_{\alpha} \sqrt{L\sigma_D^2 + \mu_D^2\sigma_L^2}$$

**Substituindo $\mu_D = D$:**
$$SS = Z_{\alpha} \sqrt{L \sigma_D^2 + D^2 \sigma_L^2}$$

---

# 7. DERIVAÇÃO COMPLETA REORDER POINT

## 7.1 Demanda Esperada durante LT

**Demanda esperada:**
$$\mathbb{E}[\text{Demanda durante LT}] = D \times L$$

**Variância:**
$$\text{Var}(\text{Demanda durante LT}) = L \sigma_D^2 + D^2 \sigma_L^2$$

## 7.2 Reorder Point

**Para garantir service level $\alpha$:**
$$PP = \mathbb{E}[\text{Demanda}] + SS$$
$$PP = D \times L + Z_{\alpha} \sqrt{L \sigma_D^2 + D^2 \sigma_L^2}$$

## 7.3 Interpretação Probabilística

**Probabilidade de ruptura durante LT:**
$$P(D_{total} > PP) = 1 - \alpha$$

**Exemplo:**
- $\alpha = 0.95$ (95%)
- $P(\text{Ruptura}) = 0.05$ (5%)

---

# 8. DERIVAÇÃO COMPLETA EOQ

## 8.1 Custo Total Anual

**Função objetivo:**
$$TC(Q) = \frac{D}{Q} S + \frac{Q}{2} H + D \times P$$

onde $P$ é preço unitário.

## 8.2 Otimização

**Derivando:**
$$\frac{dTC}{dQ} = -\frac{DS}{Q^2} + \frac{H}{2}$$

**Igualando a zero:**
$$-\frac{DS}{Q^2} + \frac{H}{2} = 0$$

**Resultado:**
$$Q^* = \sqrt{\frac{2DS}{H}}$$

## 8.3 Verificação (Segunda Derivada)

**Segunda derivada:**
$$\frac{d^2TC}{dQ^2} = \frac{2DS}{Q^3} > 0$$

**Confirmando mínimo!** ✅

## 8.4 Frequência Ótima

**Número de pedidos por ano:**
$$N^* = \frac{D}{Q^*} = \sqrt{\frac{DH}{2S}}$$

**Intervalo entre pedidos:**
$$T^* = \frac{365}{N^*} = \frac{365}{\sqrt{\frac{DH}{2S}}}$$

---

# 9. MODELS PROBABILÍSTICOS

## 9.1 Normal Distribution

**Assumindo demanda normal:**
$$D \sim \mathcal{N}(\mu_D, \sigma_D^2)$$

**Safety Stock:**
$$SS = Z_{\alpha} \sigma_D \sqrt{L}$$

## 9.2 Poisson Distribution

**Para demanda discreta/baixa:**
$$D \sim \text{Poisson}(\lambda)$$

**Safety Stock (aproximação):**
$$SS \approx Z_{\alpha} \sqrt{\lambda L}$$

## 9.3 Gamma Distribution

**Para demanda assimétrica:**
$$D \sim \text{Gamma}(\alpha, \beta)$$

**Safety Stock (numérico):**
$$SS = F^{-1}_{\text{Gamma}}(\alpha; \alpha_L, \beta_L) - \mathbb{E}[D_L]$$

onde $F^{-1}$ é função quantil inversa.

---

# 10. SERVICE LEVEL OPTIMIZATION

## 10.1 Trade-off

**Aumentar service level:**
- ✅ Reduz ruptura
- ❌ Aumenta estoque (custo)
- ❌ Aumenta obsolescência

**Balanceamento:**
$$\min_{SS} \left\{ C_{stock}(SS) + C_{shortage}(SS) \right\}$$

onde:
- $C_{stock}$: custo de estoque
- $C_{shortage}$: custo de ruptura

## 10.2 Custo de Ruptura

**Custo esperado de ruptura:**
$$C_{shortage} = \int_{SS}^{\infty} (d - SS) \times C_{unit} \times f(d) dd$$

onde:
- $C_{unit}$: custo unitário de ruptura
- $f(d)$: PDF da demanda

---

# 11. CLIMATIC FACTORS

## 11.1 Temperatura

**Impacto na demanda:**
$$D_t = D_{base} + \beta_{temp} (T_t - T_{mean}) + \epsilon_t$$

**Ajuste no Safety Stock:**
$$\Delta SS_{temp} = Z_{\alpha} \beta_{temp} \sigma_T \sqrt{L}$$

onde $\sigma_T$ é desvio padrão da temperatura.

## 11.2 Precipitação

**Impacto em tempestades:**
$$D_t = D_{base} + \beta_{rain} P_t + \epsilon_t$$

**Buffer adicional:**
$$SS_{rain} = SS_{base} + \beta_{rain} \times \max(P_{historical})$$

---

# 12. ECONOMIC FACTORS

## 12.1 Inflação

**Ajuste no preço:**
$$P_t = P_0 (1 + \pi)^t$$

**Impacto no EOQ:**
$$Q^* = \sqrt{\frac{2DS}{H(1+\pi)^t}}$$

## 12.2 Taxa de Câmbio

**Se importação:**
$$P_t = P_{USD} \times \text{USD/BRL}_t$$

**Variabilidade:**
$$\sigma_P = P_{USD} \times \sigma_{FX}$$

---

# 13. HOLIDAY EFFECTS

## 13.1 Feriados Brasileiros

**Impacto:**
$$D_t = D_{base} \times (1 + \beta_{holiday} \times I_{holiday})$$

onde $I_{holiday} = 1$ se feriado, $0$ caso contrário.

## 13.2 Ajuste no Safety Stock

**Adicionar buffer:**
$$SS_{holiday} = SS_{base} + \beta_{holiday} \times D_{base}$$

---

# 14. SLA RENEWALS

## 14.1 Ciclo de Renovação

**Impacto na demanda:**
$$D_t = D_{base} + \beta_{SLA} \times I_{renewal} \times \Delta_{contract}$$

onde $\Delta_{contract}$ é mudança no contrato.

## 14.2 Planejamento

**Antecipar renovações:**
$$SS_{SLA} = SS_{base} + \sum_{t \in T_{renewal}} \beta_{SLA} \times \Delta_{contract,t}$$

---

# 15. 5G EXPANSION IMPACT

## 15.1 Novos Sites

**Demanda adicional:**
$$\Delta D = \beta_{5G} \times N_{new\_sites}$$

**Ajuste no SS:**
$$SS_{5G} = SS_{base} + Z_{\alpha} \beta_{5G} \sigma_{sites} \sqrt{L}$$

---

# 16. MULTI-ITEM MODELS

## 16.1 Correlação entre Itens

**Safety Stock agregado:**
$$SS_{total} = Z_{\alpha} \sqrt{\sum_i SS_i^2 + 2\sum_{i<j} \rho_{ij} SS_i SS_j}$$

onde $\rho_{ij}$ é correlação entre itens $i$ e $j$.

## 16.2 Pooling Effect

**Se correlação negativa:**
$$SS_{pooled} < \sum_i SS_i$$

**Benefício do pooling!**

---

# 17. DYNAMIC SAFETY STOCK

## 17.1 Atualização Temporal

**SS varia no tempo:**
$$SS_t = Z_{\alpha} \sqrt{L_t \sigma_{D,t}^2 + D_t^2 \sigma_{L,t}^2}$$

**Atualização:**
- **Diária:** Recalcula com novos dados
- **Mensal:** Atualiza parâmetros do modelo

---

# 18. NEWSBoy PROBLEM

## 18.1 Modelo Clássico

**Otimização:**
$$\max_Q \left\{ \mathbb{E}[\pi(Q)] \right\}$$

onde:
- $\pi(Q)$: lucro
- $Q$: quantidade ordenada

## 18.2 Solução Ótima

**Quantidade crítica:**
$$F(Q^*) = \frac{c_u}{c_u + c_o}$$

onde:
- $c_u$: custo de understock (ruptura)
- $c_o$: custo de overstock (excesso)
- $F$: CDF da demanda

---

# 19. ABC ANALYSIS INTEGRATION

## 19.1 Classificação

**Classe A (alto valor):**
- Service level: 99%
- $Z_{\alpha} = 2.33$

**Classe B (médio valor):**
- Service level: 95%
- $Z_{\alpha} = 1.65$

**Classe C (baixo valor):**
- Service level: 90%
- $Z_{\alpha} = 1.28$

---

# 20. REAL-TIME ADJUSTMENTS

## 20.1 Sistema Adaptativo

**Atualização em tempo real:**
$$SS_t = f(D_{t-1}, L_{t-1}, \text{External Factors}_t)$$

**Machine Learning:**
- LSTM prevê demanda
- Atualiza SS automaticamente
- Alerta quando SS < threshold

---

# RESUMO FINAL

## Fórmulas Principais

| Conceito | Fórmula |
|----------|---------|
| **Safety Stock** | $SS = Z_{\alpha} \sqrt{L \sigma_D^2 + D^2 \sigma_L^2}$ |
| **Reorder Point** | $PP = D \times L + SS$ |
| **EOQ** | $Q^* = \sqrt{\frac{2DS}{H}}$ |
| **Service Level** | $P(D_L \leq PP) = \alpha$ |

---

**Nova Corrente Grand Prix SENAI**

**INVENTORY BREAKDOWN COMPLETE - Version 1.0**

*Novembro 2025*

