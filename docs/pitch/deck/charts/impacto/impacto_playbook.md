# Impacto Financeiro — Playbook PrevIA

Este roteiro conecta os dados de `deck/impacto-financeiro-prevía.md`
às visualizações geradas por `impacto/impacto_charts.py`. Cada seção reforça
por que a PrevIA entrega o melhor ROI frente a qualquer alternativa.

## 📊 Estrutura do Documento

Este playbook integra:

1. **9 Gráficos Plotados** (`impacto_chart_1` a `impacto_chart_10`): Visualizações de dados geradas via Python/Matplotlib
2. **6 Infográficos Estruturados**: Visualizações conceituais que complementam a narrativa:
   - Problema Exemplo (Cenário Atual)
   - Comparação de Métricas Baseline
   - Melhorias Operacionais
   - Impacto na Gestão
   - Ganhos Operacionais
   - Próximos Passos e Cronograma

---

## 📑 Índice Rápido de Visualizações

### Gráficos Plotados (9)

1. **Custo da Ruptura**: Evento Manual vs. PrevIA
2. **Radar de KPIs**: Transformação Operacional
3. **Margem Operacional**: Antes vs. Depois
4. **Fluxo de Caixa**: Acumulado 24 meses
5. **Estratégias de Preço**: Cenários de Competitividade
6. **Estoque & Rupturas**: Gestão Otimizada
7. **ROI Comparado**: PrevIA vs. Concorrentes
8. **Matriz Risco × Retorno**: Posicionamento Estratégico
9. **KPI / OKR Timeline**: Evolução dos indicadores críticos

### Infográficos Complementares (6)

- **Problema Exemplo** (Seção 1): Cenário atual de ruptura e custos
- **Comparação de Métricas Baseline** (Seção 2): Estado atual vs. otimizado
- **Melhorias Operacionais** (Seção 2): Transformação dos indicadores
- **Impacto na Gestão** (Seção 4): Efeitos no fluxo de caixa e gestão
- **Ganhos Operacionais** (Seção 6): Resultados práticos de estoque
- **Próximos Passos e Cronograma** (Final): Roadmap de implementação

---

## 1. Custo da Ruptura vs. Operação Prevista

![Custo da Ruptura](./output/impacto_chart_1_cost_event.png)

- **Mensagem central**: Uma única ruptura custa três vezes mais do que operar com previsibilidade.
- **Insight técnico**: Caso manual soma frete emergencial + multa SLA = R$ 150K; com PrevIA, o evento custa somente R$ 50K (valores da simulação de conector óptico).
- **Gatilho persuasivo**: Mostrar desperdício direto em caixa — ninguém quer pagar 200% a mais sem necessidade.
- **Próximo gancho**: “Se o impacto unitário é absurdo, imagine a curva completa dos KPIs.”
- **Fonte**: Seção “Gestão Manual vs PrevIA” (linhas 11-80).

**Script sugerido**  
"Toda ruptura é um cheque de R$ 150 mil rasgado. Com PrevIA, o mesmo evento sai por R$ 50 mil. A pergunta deixa de ser 'vale a pena?' e vira 'quanto tempo vamos continuar perdendo esse dinheiro?'"

### Infográfico: Problema Exemplo

![Problema Exemplo](../../../image/impacto-financeiro-prevía/1_problema_ex.png)

**Contexto Visual Complementar**: Este infográfico detalha o cenário atual de gestão manual e reativa, mostrando a cascata de custos de uma ruptura típica (conector óptico) desde a detecção tardia até a multa de SLA, evidenciando que o custo total de uma ruptura pode ser 3x maior que o custo normal de operação.

---

## 2. Radar de KPIs Operacionais

![KPI Radar](./output/impacto_chart_2_kpi_radar.png)

- **Mensagem central**: PrevIA transforma indicadores críticos—rupturas, forecast, capital—em um círculo quase completo.
- **Insight técnico**: Índices calculados com base em MAPE (25% → 10%), rupturas (12 → 3), SLA (94% → 99,2%), custos, capital e days inventory.
- **Gatilho persuasivo**: Exibir melhoria sistêmica, não pontual; PrevIA não é um “patch”, é um motor.
- **Próximo gancho**: “Vamos ver como isso cai direto na margem mensal.”
- **Fonte**: Tabelas “Estado Atual/Otimizado” (linhas 36-94).

**Script sugerido**  
"Não é uma melhora pontual; é o tabuleiro inteiro virando. Rupturas despencam, SLA sobe, capital trava menos. A PrevIA é um motor que gira todos os indicadores na direção certa, ao mesmo tempo."

### Infográfico: Comparação de Métricas Baseline

![Comparação de Métricas Baseline](../../../image/impacto-financeiro-prevía/1_1-opcional-comparacao_metricas_baseline.png)

**Contexto Visual Complementar**: Visualização comparativa das métricas baseline (estado atual) versus o estado otimizado com PrevIA, destacando as melhorias percentuais em cada indicador crítico e facilitando a compreensão rápida do impacto transformacional da solução.

#### Diagnóstico Técnico das Métricas Baseline

Cada métrica abaixo funciona como um **indicador de diagnóstico** que revela sintomas específicos da gestão manual e reativa:

##### 1. Rupturas/mês: 12 eventos (🔴 Crítico)

- **O que mede**: Frequência de stock-outs (estoque zerado) que interrompem operações
- **Diagnóstico do problema**: 1 ruptura a cada 2,5 dias indica **ausência de buffer de segurança** e **falta de previsão de demanda**. Em B2B telecom, cada ruptura ativa cascata: manutenção parada → torre offline → SLA quebrado → multa contratual (2-10% do contrato)
- **Impacto financeiro direto**: 12 rupturas × R$ 150K (custo médio com frete emergencial + multa) = **R$ 1,8M/ano em custos evitáveis**
- **Causa raiz**: Gestão baseada em intuição, sem modelo preditivo para antecipar picos de demanda

##### 2. Forecast Accuracy: 25% MAPE (🔴 Crítico)

- **O que mede**: Mean Absolute Percentage Error — erro médio percentual entre demanda prevista e demanda real
- **Diagnóstico do problema**: MAPE de 25% significa que **3 em cada 4 previsões estão erradas em mais de 25%**, gerando decisões de compra sub-otimizadas. Benchmark de excelência para B2B é <10% MAPE
- **Impacto operacional**: Com 25% de erro, a empresa compra 25% a mais (ou menos) do necessário, resultando em **estoque excessivo ou rupturas frequentes**
- **Causa raiz**: Ausência de modelos estatísticos (ARIMA, Prophet, LSTM) e não consideração de fatores externos (clima, sazonalidade, eventos contratuais)

##### 3. SLA Compliance: 94% (🔴 Abaixo do target)

- **O que mede**: Percentual de tempo que as torres permanecem operacionais dentro do contrato (target: 99%)
- **Diagnóstico do problema**: 94% significa **6% de downtime não planejado**, equivalente a ~22 horas/mês de torre offline. Em contratos B2B telecom, cada 1% abaixo do target ativa penalidades de 2-10% do valor mensal
- **Impacto financeiro**: Para contrato de R$ 1M/mês, 5% de penalidade = **R$ 50K/mês em multas recorrentes**
- **Causa raiz**: Rupturas de estoque impedem manutenção preventiva e corretiva dentro do prazo contratual

##### 4. Capital em Estoque: R$ 400K (🔴 Excessivo)

- **O que mede**: Valor total de inventário parado em armazém
- **Diagnóstico do problema**: Capital 30% acima do ideal (R$ 320K) indica **compensação reativa**: empresa compra em excesso para evitar rupturas, travando R$ 80K desnecessariamente. Em telecom, estoque excessivo também aumenta risco de obsolescência tecnológica
- **Impacto financeiro**: R$ 80K de capital de giro travado = **oportunidade perdida de investimento** ou **custo de financiamento** (~R$ 8K/ano em juros)
- **Causa raiz**: Sem previsão precisa, a empresa usa "estoque de segurança" como única estratégia de mitigação de risco

##### 5. Days Inventory: 60 dias (🔴 Alto)

- **O que mede**: Tempo médio que um item permanece em estoque antes de ser consumido (inventory turnover = 365/60 = 6x/ano)
- **Diagnóstico do problema**: 60 dias de estoque indica **baixa rotação** e **capital imobilizado por longo período**. Benchmark para telecom é 40-45 dias (turnover 8-9x/ano)
- **Impacto operacional**: Itens ficam parados por 2 meses, aumentando risco de obsolescência e reduzindo flexibilidade para reagir a mudanças de demanda
- **Causa raiz**: Compras em lotes grandes para "garantir" disponibilidade, sem otimização baseada em demanda real

##### 6. Custo Emergência/mês: R$ 50K (🔴 Alto)

- **O que mede**: Despesas extras com frete aéreo, horas extras e compras urgentes para cobrir rupturas
- **Diagnóstico do problema**: R$ 50K/mês em "modo emergência" indica que **30-40% das compras são reativas** (não planejadas). Frete aéreo custa 2-3x mais que frete normal
- **Impacto financeiro**: R$ 600K/ano em custos evitáveis que poderiam ser investidos em crescimento ou retornados como margem
- **Causa raiz**: Ausência de planejamento preventivo força compras de última hora com prêmio de urgência

##### 7. Lead Time Médio: 21 dias (⚠️ Variável)

- **O que mede**: Tempo entre a decisão de compra e a chegada do item no estoque
- **Diagnóstico do problema**: Variação de ±50% (10-32 dias) cria **incerteza operacional** e impede planejamento confiável. Empresa não sabe se item chega em 2 ou 4 semanas
- **Impacto estratégico**: Com lead time imprevisível, empresa precisa manter estoques maiores como "seguro", travando capital desnecessariamente
- **Causa raiz**: Dependência de múltiplos fornecedores (locais e importados) sem visibilidade de capacidade e sem integração de dados de supply chain

##### 8. Margem Operacional: -2-3% (🔴 Erosão)

- **O que mede**: EBITDA como percentual da receita, após custos operacionais
- **Diagnóstico do problema**: Margem negativa indica que **custos de ineficiência (rupturas, emergências, multas) estão erodindo a rentabilidade**. Em operação saudável, margem deveria ser +1-2%
- **Impacto estratégico**: Cada ponto percentual de margem perdida = R$ 1M/ano em uma operação de R$ 100M. Margem negativa impede investimento em crescimento e reduz atratividade para investidores
- **Causa raiz**: Soma de todos os problemas acima: rupturas (R$ 1,8M/ano) + multas SLA (R$ 600K/ano) + custos emergência (R$ 600K/ano) = **R$ 3M/ano em custos evitáveis** que destroem margem

#### Síntese do Diagnóstico

As 8 métricas baseline revelam um **padrão sistêmico de gestão reativa**:

- **Sintoma primário**: 12 rupturas/mês (alta frequência de falhas)
- **Causa técnica**: Forecast accuracy de 25% MAPE (previsões imprecisas)
- **Consequência financeira**: Margem negativa de -2-3% (erosão de rentabilidade)
- **Ciclo vicioso**: Rupturas → compras emergenciais → estoque excessivo → capital travado → menos flexibilidade → mais rupturas

A PrevIA quebra esse ciclo ao transformar **gestão reativa em gestão preditiva**, reduzindo MAPE para 10% e rupturas para 3/mês, liberando R$ 3M/ano em custos evitáveis e restaurando margem positiva.

### Infográfico: Melhorias Operacionais

![Melhorias Operacionais](../../../image/impacto-financeiro-prevía/2_melhorias.png)

**Contexto Visual Complementar**: Este infográfico sintetiza as principais melhorias operacionais alcançadas com a implementação da PrevIA, transformando indicadores críticos como rupturas, SLA compliance, forecast accuracy e gestão de capital em vantagens competitivas mensuráveis.

---

## 3. Margem Operacional – Antes vs Depois

![Margem Operacional](./output/impacto_chart_3_margin.png)

- **Mensagem central**: Pequenas linhas de custo viram margem quando emergências somem.
- **Insight técnico**: EBITDA passa de R$ 450K/mês (45%) para R$ 475K/mês (47,5%) mesmo após custo SaaS de R$ 10K/mês.
- **Gatilho persuasivo**: CFO enxerga rápido +2,5 pp de margem; é dinheiro direto no resultado.
- **Próximo gancho**: "E esse ganho se acumula num payback relâmpago."
- **Fonte**: "Impacto em Margem Operacional" (linhas 101-122).

**Script sugerido**  
"O CFO enxerga rápido: cortar emergências de R$ 50 para R$ 15 mil por mês é margem pura. Mesmo pagando o SaaS, colocamos mais R$ 25 mil de lucro limpo todo mês. PrevIA compra margem com dinheiro que hoje é queimado em urgência."

### Análise Técnica Detalhada da Transformação de Margem

Este gráfico revela a **transformação estrutural da rentabilidade** através da eliminação de custos evitáveis. Cada linha de custo impacta diretamente o EBITDA, e a redução de emergências converte desperdício em lucro líquido.

#### Breakdown Estrutural: Antes vs. Depois

##### CENÁRIO ANTES (Gestão Manual - Reativa)

```text
Receita Operacional de Manutenção:    R$ 1.000K/mês (100%)
────────────────────────────────────────────────────────────
Custos Diretos (Materiais):          -R$ 300K  (30%)
  • Compras planejadas:               R$ 250K
  • Compras emergenciais:             R$ 50K   ← INEFICIÊNCIA

Custos de Emergência/Rupturas:       -R$ 50K   (5%)
  • Frete aéreo (2-3x normal):        R$ 30K
  • Multas SLA (2-10% contrato):      R$ 15K
  • Horas extras (equipe urgência):   R$ 5K
  ─────────────────────────────────────────────
  TOTAL DESPERDÍCIO:                  R$ 50K/mês = R$ 600K/ano

Custos Operacionais Fixos:           -R$ 200K  (20%)
  • Equipe planejamento (3 FTE):      R$ 120K
  • Infraestrutura/logística:         R$ 80K
────────────────────────────────────────────────────────────
EBITDA:                                R$ 450K  (45% margem)
```

**Diagnóstico do Problema**: A margem de 45% parece saudável, mas **5% da receita (R$ 50K/mês) é desperdiçada em custos evitáveis**. Em modelo B2B com preço fixo, esse desperdício não pode ser repassado ao cliente — ele corrói diretamente a rentabilidade.

##### CENÁRIO DEPOIS (Com PrevIA - Preditiva)

```text
Receita Operacional de Manutenção:    R$ 1.000K/mês (100%)
────────────────────────────────────────────────────────────
Custos Diretos (Materiais):          -R$ 300K  (30%)
  • Compras planejadas:               R$ 285K  (+14% planejadas)
  • Compras emergenciais:             R$ 15K   (-70% emergências)

Custos de Emergência/Rupturas:       -R$ 15K   (1.5%)
  • Frete aéreo (reduzido 70%):       R$ 9K
  • Multas SLA (eliminadas 90%):      R$ 1.5K
  • Horas extras (reduzidas 80%):     R$ 1K
  ─────────────────────────────────────────────
  TOTAL OTIMIZADO:                    R$ 15K/mês = R$ 180K/ano
  ECONOMIA:                           R$ 35K/mês = R$ 420K/ano

Custos Operacionais Fixos:           -R$ 200K  (20%)
  • Equipe planejamento (1 FTE):      R$ 40K   (-2 FTE liberados)
  • Infraestrutura/logística:         R$ 80K   (idem)
  • Custo PrevIA (SaaS):              R$ 10K   (1% receita)
────────────────────────────────────────────────────────────
EBITDA:                                R$ 475K  (47.5% margem)
```

**Transformação Realizada**: A margem sobe de 45% para 47,5% (+2,5 pontos percentuais), gerando **R$ 25K/mês adicionais de lucro líquido** mesmo após incluir o custo do SaaS da PrevIA.

#### Análise do Impacto Financeiro

##### 1. Multiplicador de Valor por Ponto Percentual

Em uma operação de R$ 1M/mês (R$ 12M/ano):

- **+1 ponto percentual de margem** = R$ 10K/mês = **R$ 120K/ano**
- **+2,5 pontos percentuais** = R$ 25K/mês = **R$ 300K/ano**

Em escala (18.000 torres, R$ 100M/ano):

- **+2,5 pontos percentuais** = **R$ 2,5M/ano de EBITDA adicional**

##### 2. Decomposição do Ganho de R$ 25K/mês

```text
Redução de custos emergência:         +R$ 35K/mês
  (R$ 50K → R$ 15K)

Custo PrevIA (SaaS):                  -R$ 10K/mês
────────────────────────────────────────────────
GANHO LÍQUIDO MENSAL:                 +R$ 25K/mês

GANHO ANUAL:                          +R$ 300K/ano
```

##### 3. ROI da Margem Adicional

- **Investimento PrevIA**: R$ 150K (one-time) + R$ 10K/mês (SaaS)
- **Ganho anual de margem**: R$ 300K/ano
- **Payback da margem**: 6 meses (R$ 150K ÷ R$ 25K/mês)
- **ROI anual da margem**: 200% (R$ 300K ÷ R$ 150K)

#### Impacto Estratégico em Modelo B2B Telecom

**Característica do Modelo B2B**: Preço fixo contratual (não negociável), margem depende exclusivamente da otimização de custos.

**Antes PrevIA**:

- Preço: R$ 100M/ano (fixo)
- Custo total: R$ 55M/ano (55%)
- **Margem real**: 45% (mas 5% desperdiçada = margem efetiva de 40%)
- **Vulnerabilidade**: Qualquer erro operacional corrói margem imediatamente

**Depois PrevIA**:

- Preço: R$ 100M/ano (fixo)
- Custo total: R$ 51,5M/ano (51,5%)
- **Margem real**: 48,5% (+3,5 pontos percentuais)
- **Robustez**: Buffer de 3,5pp protege contra volatilidade externa

**Implicação Estratégica**: Os **R$ 3,5M/ano em custos evitáveis** se transformam em **R$ 3,5M/ano de margem operacional adicional**, criando três opções estratégicas:

1. **Conservador**: Manter preço, capturar R$ 3,5M/ano de margem extra
2. **Agressivo**: Reduzir preço 5%, manter margem, ganhar market share
3. **Híbrido**: Reduzir preço 2%, aumentar margem 1,5pp, crescer competitivamente

#### Comparação com Benchmarks do Setor

**Benchmark de Margem Operacional (B2B Telecom)**:

- **Tier 1 (American Tower, IHS)**: 50-55% EBITDA margin
- **Tier 2 (Nova Corrente baseline)**: 40-45% EBITDA margin
- **Tier 3 (Operadoras regionais)**: 30-35% EBITDA margin

**Posicionamento com PrevIA**:

- **Antes**: 45% (margem aparente) / 40% (margem efetiva após desperdícios)
- **Depois**: 47,5% (margem real otimizada)
- **Gap para Tier 1**: Reduzido de 10-15pp para 2,5-7,5pp

**Interpretação**: A PrevIA eleva a Nova Corrente de **Tier 2 médio para Tier 2 superior**, aproximando-se da rentabilidade de Tier 1 sem necessidade de escala massiva.

#### Análise de Sensibilidade

**Cenário Conservador** (redução de 60% em emergências vs. 70%):

- Custo emergência: R$ 20K/mês (vs. R$ 15K)
- Ganho líquido: R$ 20K/mês (vs. R$ 25K)
- Margem final: 47% (vs. 47,5%)
- **Ainda positivo**: +R$ 240K/ano

**Cenário Otimista** (redução de 80% em emergências):

- Custo emergência: R$ 10K/mês
- Ganho líquido: R$ 30K/mês
- Margem final: 48% (+3 pontos percentuais)
- **Upside adicional**: +R$ 360K/ano

**Conclusão**: Mesmo no cenário conservador, a PrevIA gera **margem positiva significativa**, demonstrando robustez do modelo de negócio.

#### Implicações para Valuation e Investidores

**Multiplicador de EBITDA** (setor telecom B2B): 8-12x EBITDA

**Impacto no Valuation**:

- **Ganho anual de EBITDA**: R$ 300K/ano (conservador) a R$ 3,5M/ano (escala completa)
- **Valor criado** (múltiplo 10x): R$ 3M a R$ 35M em valor de empresa
- **ROI do investimento PrevIA**: 2.000% a 23.333% em valor criado

**Mensagem para Investidores**: A PrevIA não é apenas uma ferramenta operacional — é um **multiplicador de valor** que transforma custos evitáveis em valor de empresa através da melhoria estrutural de margem.

---

## 4. Fluxo de Caixa Acumulado (24 meses)

![Fluxo de Caixa](./output/impacto_chart_4_cashflow.png)

- **Mensagem central**: Payback chega antes do mês 7; depois disso, só caixa positivo.
- **Insight técnico**: Investimento de R$ 150K, mais capital liberado de R$ 80K e economia mensal (R$ 300K nos 12 primeiros meses, R$ 150K depois).
- **Gatilho persuasivo**: Visualizar montanha de caixa acumulando +R$ 5,33M em dois anos convence qualquer board.
- **Próximo gancho**: “Se temos folga de caixa, podemos decidir como competir no preço.”
- **Fonte**: “Cash Flow Analysis - 24 meses” (linhas 127-147).

**Script sugerido**  
"O investimento inicial some no mês seis. A partir daí o gráfico vira uma rampa de resultado: mais de R$ 5 milhões acumulados em dois anos. Em linguagem de conselho, é uma fábrica de caixa com payback relâmpago."

### Infográfico: Impacto na Gestão

![Impacto na Gestão](../../../image/impacto-financeiro-prevía/4_impacto_gestao.png)

**Contexto Visual Complementar**: Este infográfico detalha o impacto transformacional da PrevIA na gestão operacional e financeira, mostrando como a solução afeta positivamente o fluxo de caixa, a margem operacional e a capacidade de tomada de decisão estratégica, criando uma base sólida para crescimento sustentável.

---

## 5. Estratégias de Preço × Margem

![Cenários de Preço](./output/impacto_chart_5_price_strategies.png)

- **Mensagem central**: PrevIA permite escolher entre margem extra ou preço agressivo sem sacrificar rentabilidade.
- **Insight técnico**: Três cenários — manter preço (margem 48,5%), agressivo (-5% preço, margem 40%), híbrido (-2%, margem 43%).
- **Gatilho persuasivo**: “PrevIA transforma custo em arma comercial para ganhar market share.”
- **Próximo gancho**: “Operacionalmente, mantemos estoque e rupturas sob controle.”
- **Fonte**: “Cenário 1/2/3” (linhas 266-286).

**Script sugerido**  
“Graças à margem extra, podemos manter preço e levar o lucro, reduzir preço para ganhar market share ou fazer o meio-termo e dominar a categoria. PrevIA transforma custo em vantagem comercial — é um botão de competitividade.”

---

## 6. Estoque & Rupturas — Antes vs Depois

![Gestão de Estoque](./output/impacto_chart_6_inventory.png)

- **Mensagem central**: O modo “Goldilocks” (estoque no ponto certo) vira realidade.
- **Insight técnico**: Inventory turnover sobe 6x → 9x; stock-outs caem 12 → 3; capital em estoque cai R$ 400K → R$ 290K.
- **Gatilho persuasivo**: Libera capital de giro e reduz risco de back-orders; CFO+COO aplaudem juntos.
- **Próximo gancho**: “Na disputa com concorrentes, nossa proposta financeira é brutalmente melhor.”
- **Fonte**: “Métricas de Gestão” (linhas 198-205).

**Script sugerido**  
"Estoque deixa de ser bipolar. Giramos 50% mais rápido, reduzimos rupturas em 75% e liberamos R$ 110 mil de capital de giro. Isso significa menos dinheiro parado e mais obra entregue dentro do prazo."

### Infográfico: Ganhos Operacionais

![Ganhos Operacionais](../../../image/impacto-financeiro-prevía/6_ganhos_operacionais.png)

**Contexto Visual Complementar**: Visualização dos ganhos operacionais concretos alcançados com a PrevIA, destacando melhorias em turnover de estoque, redução de stock-outs, otimização de capital de giro e aumento da eficiência operacional, transformando a gestão de estoque de um problema em uma vantagem competitiva.

---

## 7. ROI Ano 1 vs Payback Competidores

![ROI Comparado](./output/impacto_chart_7_roi.png)

- **Mensagem central**: PrevIA entrega 1.587% de ROI no primeiro ano—10x melhor que Blue Yonder ou SAP.
- **Insight técnico**: Payback de 6 meses (vs 9, 12 ou 14), destacando economia absoluta de R$ 2,38M no Ano 1.
- **Gatilho persuasivo**: Bastam 10 segundos para o investidor ver que essa é a melhor aposta.
- **Próximo gancho**: “E ainda somos a escolha de menor risco.”
- **Fonte**: “ROI Calculado vs Concorrência” (linhas 334-354).

**Script sugerido**  
“Os gigantes pedem milhões e demoram um ano para devolver. PrevIA custa 150 mil, paga em seis meses e entrega 1.587% de ROI. É o tipo de múltiplo que faz qualquer CFO assinar na hora.”

---

## 8. Matriz Risco × Retorno

![Risco Retorno](./output/impacto_chart_8_risk_return.png)

- **Mensagem central**: PrevIA fica no quadrante ideal — risco baixo, retorno altíssimo.
- **Insight técnico**: Avaliação qualitativa baseada na seção “Portfólio de Risco-Retorno” (linhas 358-371).
- **Gatilho persuasivo**: Ajuda o CEO/CFO a defender a decisão como “melhor relação risco/retorno do portfólio”.
- **Próximo gancho**: “Com tudo isso, a escolha natural é executar já o MVP.”
- **Fonte**: “RISCO BAIXO / RETORNO ALTO” (linhas 358-371).

**Script sugerido**  
“Mesmo comparado a players globais, ficamos no quadrante dos sonhos: risco baixo, retorno altíssimo. Pouco investimento, payback rápido e escalabilidade pronta. A decisão mais segura do portfólio.”

---

## 9. KPI / OKR Evolution Timeline

![KPI Timeline](./output/impacto_chart_10_kpi_timeline.png)

- **Mensagem central**: Todos os KPIs críticos saltam do “modo sobrevivência” para o patamar meta em menos de seis meses após o go-live do PrevIA.
- **Insight técnico**: A série usa os números reais do baseline (`impacto_playbook`, Seção “Gestão Manual vs PrevIA”) — Forecast MAPE 25%→10%, rupturas 12→3 eventos/mês, capital travado R$ 400K→R$ 320K, SLA 94%→99,2%, custo emergencial R$ 50K→R$ 15K e ROI acumulado 0→1.587% no ano 1.
- **Gatilho persuasivo**: Mostra contraste visual entre o período “Antes” (meses 0-12) e “Depois” do lançamento PrevIA, com anotação dos valores absolutos nas extremidades para dar credibilidade executiva.
- **Próximo gancho**: “Com essa curva já comprovada, veja como estruturamos a governança de rollout e os pontos de controle por diretoria.”
- **Fonte**: Tabelas “Gestão Manual vs PrevIA” (linhas 11-205) e gráfico `impacto_chart_7_roi`.

**Script sugerido**  
“Antes do PrevIA todos os KPIs estavam achatados — MAPE alto, 12 rupturas por mês, SLA em 94%. Em seis meses, a curva muda de inclinação: o algoritmo derruba o MAPE para 10%, reduz as rupturas para 3, quase zera o custo emergencial e faz o ROI anual bater 1.587%. É uma mudança de regime operacional, não um ajuste cosmético.”

---

## Resumo Executivo

Com estes **nove gráficos plotados** e **seis infográficos complementares**, a narrativa de impacto financeiro fica irrefutável:

1. **A ruptura custa caro demais** e PrevIA elimina o desperdício — Gráfico 1 + Infográfico "Problema Exemplo".
2. **KPIs operacionais giram radicalmente** a favor da Nova Corrente — Gráfico 2 + Infográficos "Comparação Baseline" e "Melhorias".
3. **Margem aumenta** mesmo com custo SaaS adicional — Gráfico 3.
4. **Payback ocorre em meses**, acumulando +R$ 5,33M em 24 meses — Gráfico 4 + Infográfico "Impacto na Gestão".
5. **Estratégias de preço** passam a ser escolhas, não apostas — Gráfico 5.
6. **A gestão de estoque** sai do caos para o "ponto certo" — Gráfico 6 + Infográfico "Ganhos Operacionais".
7. **PrevIA supera concorrentes** em ROI e payback por larga margem — Gráfico 7.
8. **Risco baixo + retorno alto** deixam a decisão praticamente óbvia — Gráfico 8.
9. **Execução e curva de KPIs** comprovam o “antes vs depois” — Gráfico 10.
10. **Roadmap executável** com cronograma claro e marcos definidos — Infográfico "Próximos Passos".

**Total de Visualizações**: 14 elementos visuais (8 gráficos + 6 infográficos) que trabalham em conjunto para construir uma narrativa financeira persuasiva e baseada em dados.

Use este playbook como notas do apresentador, apêndice técnico ou "one pager"
para CFO/CEO/Investidores. O objetivo é transformar fatos em confiança — vender
PrevIA como o investimento estratégico mais inteligente para a Nova Corrente.

---

## Argumentação Persuasiva Complementar

### Para o CFO (Finanças)

- **Tese**: “Estamos devolvendo margem e caixa imediatamente.”
- **Call-to-action verbal**: “Você não precisa aprovar um CAPEX multimilionário; com R$ 150K o payback chega em seis meses e acrescenta +R$ 300K de EBITDA anual.”
- **Prova visual associada**: gráficos 3, 4 e 7 (margem, fluxo e ROI).

### Para o CEO (Estratégia)

- **Tese**: “PrevIA compra competitividade de mercado.”
- **Call-to-action verbal**: “Com a mesma equipe, operamos 50 posições a mais e podemos atacar preço com segurança, expandindo market share.”
- **Prova visual associada**: gráficos 5 e 6 (estratégias de preço e estoque).

### Para o COO (Operações)

- **Tese**: “Menos incêndios, mais execução.”
- **Call-to-action verbal**: “Reduzimos rupturas em 75% e liberamos duas pessoas para focar em expansão — deixe a PrevIA cuidar do previsível.”
- **Prova visual associada**: gráficos 1, 2 e 6 (custo da ruptura, radar e estoque).

### Para Investidores / Conselho

- **Tese**: “Melhor relação risco-retorno da carteira.”
- **Call-to-action verbal**: “PrevIA entrega 10x mais ROI que concorrentes globais, mantendo risco baixo e escalabilidade pronta para LATAM.”
- **Prova visual associada**: gráficos 4, 7 e 8 (cash flow, ROI competitivo e matriz risco-retorno).

---

### Como conduzir a narrativa em reunião

1. **Abertura**: Explicar a dor da ruptura (gráfico 1) e mostrar o radar (gráfico 2).
2. **Proposta de valor**: Expor o ganho de margem e o payback (gráficos 3 e 4).
3. **Estratégia comercial**: Demonstrar cenários de preço e ganhos operacionais (gráficos 5 e 6).
4. **Comparativo de mercado**: Fechar com ROI vs concorrência e matriz de risco (gráficos 7 e 8).
5. **Fechamento**: Solicitar aprovação para iniciar o MVP em quatro semanas, com marco de revisão no mês 3.

Use esses bullets como roteiro de fala para um pitch de 8–10 minutos, garantindo que cada slide gere uma pergunta "Quando implementamos?" em vez de "Por que implementar?".

---

## Próximos Passos e Cronograma

### Infográfico: Cronograma de Implementação

![Próximos Passos e Cronograma](../../../image/impacto-financeiro-prevía/7_proximos_passos_cronograma.png)

**Contexto Visual Complementar**: Roadmap visual detalhado dos próximos passos para implementação da PrevIA, incluindo marcos críticos, prazos, responsabilidades e métricas de sucesso. Este infográfico transforma a decisão estratégica em um plano de ação executável, facilitando a aprovação e o acompanhamento do projeto.

**Script sugerido**  
"O cronograma está claro: em quatro semanas iniciamos o MVP, com revisão no mês 3 e go-live completo no mês 6. Cada marco tem métricas definidas e responsáveis designados. Não é um projeto de longo prazo — é execução imediata com resultados mensuráveis."
