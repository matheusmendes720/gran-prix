# 🔍 DISCOVERY CODING - INSIGHTS E APRENDIZADOS
## Nova Corrente Grand Prix - Compreender através da Implementação

---

**Filosofia:** Descobrir o problema escrevendo código, não planejando primeiro.  
**Arquivo de Referência:** Discovery Coding.md  
**Aplicado:** Nova Corrente Forecasting System

---

## 🎯 PRINCÍPIO CENTRAL

> "Understanding a problem by writing code first, rather than attempting to do some design process or thinking beforehand."

**Tradução:** Compreender o problema escrevendo código primeiro, ao invés de tentar fazer design ou pensar antes.

---

## 💡 DESCOBERTAS ATRAVÉS DO CÓDIGO

### Descoberta 1: Previsões Negativas Mostram Assumptions Incorretos

**O que aconteceu:**
- Código gerou previsões negativas: -10.50 ± 10.63
- Sistema apontava "demanda negativa de conectores"

**O que aprendemos:**
- Médias móveis curtas capturam volatilidade, não tendência
- Random seeds específicos geram cenários não representativos
- Demanda sempre ≥ 0 (constraint físico importante)

**Ação tomada:**
```python
# ANTES (gerava negativos)
forecast.append(ma_7 + trend * i + noise)

# DEPOIS (constraint físico)
value = max(0, ma_7 + trend * i + noise)
```

**Insight:** O código revelou que faltava constraint de domínio.

---

### Descoberta 2: Safety Stock Varia Muito por Escala

**Testando diferentes materiais:**

```python
# CONN-001: Demanda alta (8/dia), LT longo (14)
SS = 25.0, PP = 137.0

# CABLE-001: Demanda baixa (2/dia), LT muito longo (21)
SS = 6.0, PP = 48.0

# ESTR-001: Demanda média (3/dia), LT curto (10)
SS = 6.2, PP = 36.2
```

**O que aprendemos:**
- Lead time longo → Safety Stock maior
- Demanda alta → PP mais alto
- Não existe "one size fits all"

**Insight:** Fórmula universal precisa de parâmetros customizados por material.

---

### Descoberta 3: Dias até Ruptura Mostram Urgências Escondidas

**Resultado do teste:**
- CONN-001: 7.5 dias → 🟢 MONITORAR (mas quase ATENÇÃO!)
- CABLE-001: 22.0 dias → ✅ OK
- ESTR-001: 7.9 dias → 🟢 MONITORAR (mas quase ATENÇÃO!)

**O que aprendemos:**
- Estoque de 85 parece OK
- Mas com PP=137, já deveria alertar há dias!
- Threshold de 7 dias é crítico para ação

**Insight:** Visualizar "dias até ruptura" > apenas "stock < PP"

---

### Descoberta 4: Simulação Revela Cenários Extremos

**Histograma mostrou:**
- Min: 4.85 unidades
- Max: 20.83 unidades
- Range: 4.3x entre min e max!

**O que aprendemos:**
- Variabilidade é ENORME
- Safety Stock precisa absorver isso
- Reorder Point deve considerar piores casos

**Insight:** Estatísticas descritivas revelam necessidade de buffers maiores.

---

## 🔄 PROCESSO DE DESCOBERTA

### Iteração 1: Código Inicial
```python
def calculate_safety_stock(avg, std, lt):
    return Z * std * np.sqrt(lt)
```
✅ **Funcionou!** SS = 25.0 calculado corretamente

### Iteração 2: Sistema de Alertas
```python
def check_inventory_alert(current, pp, avg_demand, ss):
    days = (current - ss) / avg_demand
```
✅ **Funcionou!** Dias até ruptura calculado

### Iteração 3: Previsões ARIMA Simples
```python
def simulate_demand_arima_simple(data, horizon):
    ma_7 = np.mean(data[-7:])
    return forecast
```
⚠️ **Problema:** Previsões negativas

### Iteração 4: Fix com Constraint
```python
value = max(0, ma_7 + trend * i + noise)
```
✅ **Funcionou!** Previsões >= 0

**Próxima descoberta:** Precisamos de melhor modelo que MA simples!

---

## 🧪 DESCOBERTAS ATRAVÉS DE TESTES

### Teste: "E se Lead Time Variar?"

```python
# ANTES
SS_basic = Z * σ * √LT = 11.48

# DEPOIS (com variabilidade)
SS_advanced = Z * √(LT×σ² + D²×σ_LT²) = 25.0
```

**Descoberta:** Variabilidade aumenta SS em 2.18x!

**Insight prático:** Operações com múltiplos fornecedores precisam SS avançado.

---

### Teste: "Impacto de Fatores Externos?"

```python
# Sem ajuste
base_demand = 8
pp = (8 × 14) + 25 = 137

# Com tempestade (+50% demanda)
adjusted_demand = 8 × 1.5 = 12
pp_adjusted = (12 × 14) + 25 = 193
```

**Descoberta:** PP aumenta 41% com evento climático!

**Insight prático:** Sistema precisa recalcular PP dinamicamente.

---

## 📊 PATTERNS DESCOBERTOS

### Pattern 1: Demanda tem Múltiplas Sazonalidades

```python
# Discovered through visualization
weekly_pattern = sin(2π * day / 7)    # Ciclo semanal
annual_pattern = sin(2π * day / 365)  # Ciclo anual
trend = linear growth                  # Tendência
noise = random                         # Ruído
```

**Insight:** Modelos simples (ARIMA básico) não capturam tudo.

---

### Pattern 2: Alertas Binary não Capturam Gradualidade

```python
# Nossa implementação inicial
if stock <= pp:
    status = "🔴 CRÍTICO"
else:
    status = "✅ OK"
```

**Problema descoberto:**
- Stock = 137.1 → ✅ OK
- Stock = 136.9 → 🔴 CRÍTICO
- Diferença de 0.2 unidades muda tudo!

**Correção:**
```python
# Gradual
if days_until <= 3:   status = "🔴 CRÍTICO"
elif days_until <= 7: status = "🟡 ATENÇÃO"
elif days_until <= 10: status = "🟢 MONITORAR"
else:                  status = "✅ OK"
```

**Insight:** Gradual thresholds melhor que binary.

---

### Pattern 3: Histogramas Revelam Assimetrias

```
Demanda 4.9 - 5.7: ████
Demanda 10.4-11.2: ████████████████████████████████████████ (pico!)
Demanda 19.2-20.0: █
```

**Descoberta:** 
- Distribuição não normal
- Picos em torno de 10-11
- Cauda longa rara (20+)

**Implicação:** Safety Stock formula assume normal → subestima cauda!

**Insight:** Precisa de distribuições mais robustas (Poisson, Negative Binomial?).

---

## 🎓 LIÇÕES APRENDIDAS

### Lição 1: Code Reveals Hidden Assumptions

**Antes de codar:** "Demanda é previsível e estacionária"  
**Depois de codar:** "Variabilidade 4.3x, padrões complexos, não estacionária"

**Ação:** Rever todas as assumptions teóricas.

---

### Lição 2: Simple Models Expose Limitations

**Tentativa:** ARIMA super simples (MA 7 dias)  
**Resultado:** Não captura sazonalidade semanal/anual  
**Descoberta:** Precisa SARIMAX ou Prophet

**Ação:** Usar modelos sazonais adequados.

---

### Lição 3: Constraints are Fundamental

**Sem constraint:** Previsões negativas  
**Com constraint:** Previsões válidas

**Insight:** Domínio sempre tem regras (demanda ≥ 0, estoque ≥ 0, etc.)

**Ação:** Sempre adicionar constraints de domínio.

---

### Lição 4: Visualization Accelerates Discovery

**Histograma mostrou:**
- Distribuição real
- Outliers visíveis
- Assimetria clara

**Insight:** Grafos revelam insights que estatísticas ocultam.

**Ação:** Sempre visualizar dados.

---

## 🚀 PRÓXIMAS ITERAÇÕES (Discovery Roadmap)

### Iteração 5: Integrar Prophet
**O que descobrir:** Se Prophet captura sazonalidades melhor

### Iteração 6: Dados Reais
**O que descobrir:** Como dados reais diferem de sintéticos

### Iteração 7: Ensemble
**O que descobrir:** Se combinar modelos melhora previsão

### Iteração 8: Fatores Externos
**O que descobrir:** Impacto real de clima/economia/tecnologia

---

## 💬 QUOTE FINAL

> "Discovery coding does not have a solution to offer, so the code we begin writing is instead about poking the system and understanding how it works."

**Nossa tradução:** Discovery coding não oferece solução, então o código que escrevemos é sobre investigar o sistema e entender como funciona.

---

## ✅ CONCLUSÃO

**O que Discovery Coding nos ensinou:**

1. ✅ Escrever código revela problemas real-world
2. ✅ Constraints de domínio são críticos
3. ✅ Visualização acelera compreensão
4. ✅ Modelos simples expõem limitações
5. ✅ Iteração > Planejamento teórico

**Próximo passo:** Continuar descobrindo com código!

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

**DISCOVERY CODING INSIGHTS - Version 1.0**

*Keep discovering through code! 🧪*


