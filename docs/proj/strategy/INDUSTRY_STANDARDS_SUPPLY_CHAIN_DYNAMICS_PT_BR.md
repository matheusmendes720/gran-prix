# 🌐 PADRÕES DA INDÚSTRIA E DINÂMICAS DA CADEIA DE SUPRIMENTOS
## Previsibilidade de Demandas - Grand Prix SENAI

**Versão:** 1.0  
**Data:** Novembro 2025  
**Área:** Supply Chain & Inventory Management

---

## 📋 ÍNDICE

1. [Padrões Globais de Supply Chain](#padroes-globais)
2. [Dinâmicas B2B na Indústria de Telecomunicações](#dinamicas-b2b)
3. [Fatores Externos e Seus Impactos](#fatores-externos)
4. [Modelos de Referência Aplicáveis](#modelos-referencia)
5. [Melhores Práticas Tecnológicas](#melhores-praticas)
6. [Cases de Sucesso](#cases-sucesso)

---

<a name="padroes-globais"></a>
## 1. 🌍 PADRÕES GLOBAIS DE SUPPLY CHAIN

### 1.1 Modelo SCOR (Supply Chain Operations Reference)

**Definição:**  
Padrão global desenvolvido pelo Supply Chain Council para análise, implementação e benchmarking de processos de supply chain.

**Componentes Principais:**
1. **Planejamento:** Previsão, sourcing, produção
2. **Sourcing:** Aquisição de materiais e insumos
3. **Fabricação:** Produção/transformação
4. **Entregas:** Gestão de pedidos, transporte, logística reversa
5. **Retornos:** Recall de produtos, retornos de clientes

**Métricas SCOR:**
- **Reliability:** Performance in delivering on time
- **Responsiveness:** Speed of delivery
- **Agility:** Flexibility to adapt to change
- **Cost:** Total supply chain costs
- **Assets:** Management efficiency

**Aplicação à Nova Corrente:**
```
Planejamento: Previsão demanda → IA
Sourcing: Compras baseadas em PP
Fabricação: N/A (Nova Corrente não produz)
Entregas: Gestão de estoque e distribuição
Retornos: N/A (serviços, não produtos)

Foco: PLANEJAMENTO + SOURCING
```

### 1.2 CPFR (Collaborative Planning, Forecasting, and Replenishment)

**Definição:**  
Modelo colaborativo onde todas as partes da cadeia de suprimentos compartilham dados e decisões para melhorar precisão.

**Processos:**
1. **Strategy & Planning:** Alinhamento de objetivos
2. **Demand & Supply Management:** Compartilhamento de forecasts
3. **Execution:** Pedidos automáticos baseados em triggers
4. **Analysis:** Monitoramento e otimização contínua

**Aplicação à Nova Corrente:**
```
Estratégia: SLA 99% para todos
Demanda: IA prevê consumo
Oferta: Fornecedores ajustam capacidade
Execução: Alertas automáticos dispara pedidos
Análise: Feedback loop melhora modelo
```

### 1.3 VMI (Vendor Managed Inventory)

**Definição:**  
Modelo onde fornecedores gerenciam estoque do cliente, assumindo responsabilidade por reposição.

**Benefícios:**
- Redução de rupturas
- Otimização de níveis de estoque
- Menos burocracia
- Melhor relacionamento fornecedor-cliente

**Limitação para Nova Corrente:**
- Especificidade técnica (peças telecom)
- Múltiplos fornecedores
- Complexidade regulatória (Anatel)

**Aplicação Futura:**  
Possível para itens com demanda estável e fornecedores estratégicos.

### 1.4 Efeito Chicote (Bullwhip Effect)

**Definição:**  
Fenômeno onde pequenas variações na demanda do consumidor final amplificam-se ao longo da cadeia.

**Causas:**
1. Previsão de demanda inexata
2. Tempos de resposta longos
3. Lotes grandes de processamento
4. Flutuações de preço promocional
5. Racionalização de estoque

**Prevenção:**
- **Compartilhamento de dados** entre elos
- **Previsões colaborativas** (CPFR)
- **Redução de lead times**
- **Loteamento just-in-time**
- **Preços estáveis**

**Relevância para Nova Corrente:**
```
Consumo real em torres
  ↓
Nova Corrente planeja estoque
  ↓
Fornecedores ajustam produção
  ↓
Amplificação se não houver coordenação

Solução: IA prevê demanda real com precisão
```

---

<a name="dinamicas-b2b"></a>
## 2. 💼 DINÂMICAS B2B NA INDÚSTRIA DE TELECOMUNICAÇÕES

### 2.1 Características Únicas do Setor

**Infraestrutura Crítica:**
- **Uptime 99.99%+:** QoS essencial
- **SLA Penalties:** Multas por falhas
- **Network Availability:** Impacta milhares de usuários
- **Regulatory Compliance:** Anatel, AGERBA

**Padrões de Demanda B2B:**
- **Contratos de Longo Prazo:** Previsibilidade relativa
- **Planejamento Anual:** Budget aprovado antecipadamente
- **Sazonalidade Previsível:** Baseada em manutenções agendadas
- **Eventos Excepcionais:** Expansões, breakdowns

**Especificidade de Produtos:**
- **Peças Técnicas:** Códigos específicos de fabricantes
- **Baixa Substituibilidade:** Pouca flexibilidade
- **Lead Times Longos:** Dependência de importação/fornecedor
- **Custo Alto:** Itens podem custar R$ milhares

### 2.2 Dinâmicas de Consumo por Categoria

**Categoria 1: Alta Rotatividade (Fast-Moving)**
| Item | Demanda | Lead Time | Características |
|------|---------|-----------|-----------------|
| **Conectores Ópticos** | 5-10/dia | 10-14 dias | Consumo constante |
| **Cabo Óptico** | 20-50m/dia | 14-21 dias | Corte por necessidade |
| **Parafusos/Acessórios** | 50-100/dia | 7-10 dias | Consumo alto |

**Categoria 2: Baixa Rotatividade (Slow-Moving)**
| Item | Demanda | Lead Time | Características |
|------|---------|-----------|-----------------|
| **Refrigeração** | 0.1-0.5/dia | 21-30 dias | Raro, mas crítico |
| **Estrutura Metálica** | 0.2-1/semana | 30-45 dias | Projetos específicos |
| **Equipamentos RF** | 0.1-0.3/semana | 45-60 dias | Importação |

**Categoria 3: Eventos Esporádicos (Sporadic)**
| Item | Demanda | Lead Time | Características |
|------|---------|-----------|-----------------|
| **Breakdown Critical** | 0/dia, exceto eventos | 24-48h | Emergência total |
| **Expansion 5G** | Pico sazonal | 30-60 dias | Projetos agendados |
| **Upgrades** | Planejado | 60-90 dias | Ciclos tecnológicos |

### 2.3 Fatores que Influenciam Dinâmica B2B

**Internos (Nova Corrente):**
1. **Estratégia de Manutenção:** Preventiva vs. corretiva
2. **Capacidade de Equipes:** Técnicos disponíveis
3. **Orçamento:** Constraint financeiro
4. **Contratos:** Renovação de SLAs

**Externos (Fornecedores):**
1. **Capacidade de Produção:** Limites do fornecedor
2. **Estoque Próprio:** Gestão do fornecedor
3. **Condições Comerciais:** Preços, pagamentos
4. **Relacionamento:** Qualidade, confiabilidade

**Externos (Cliente/Mercado):**
1. **Crescimento de Rede:** Expansão operadora
2. **Migração Tecnológica:** 4G → 5G
3. **Mergers & Acquisitions:** Mudanças de ownership
4. **Regulatória:** Anatel, políticas governamentais

---

<a name="fatores-externos"></a>
## 3. 🌦️ FATORES EXTERNOS E SEUS IMPACTOS

### 3.1 Fatores Climáticos

**Impacto:** **ALTO** - Trabalho em campo, estruturas expostas

| Fator | Impacto Demanda | Lead Time Ajuste | Ação Preventiva |
|-------|----------------|------------------|-----------------|
| **Calor > 32°C** | +30% | +2-3 dias | Antecipar refrigeração |
| **Chuva Intensa** | +40% | +3-5 dias | Antecipar impermeabilização |
| **Umidade Alta** | +20% | +5-7 dias | Corrosão precoce |
| **Tempestades** | +50% URGENTE | +5-10 dias | Estoque emergência |
| **Ventos > 80 km/h** | +40% estrutural | +7-14 dias | Reforço preventivo |

**Fonte de Dados:**
- **INMET:** Previsão meteorológica oficial
- **API:** https://www.inmet.gov.br/

**Integração no Sistema:**
```python
# Pseudocódigo
alert_clima = fetch_inmet_forecast(region="bahia", days=7)
if alert_clima['tempestade']:
    demand_multiplier = 1.5  # +50%
    lead_time_adj = lead_time * 1.3
    trigger_urgent_alert()
```

### 3.2 Fatores Econômicos

**Impacto:** **MÉDIO-ALTO** - Afecta compras, importações, disponibilidade

| Fator | Impacto Demanda | Lead Time Ajuste | Ação Preventiva |
|-------|----------------|------------------|-----------------|
| **Desvalorização BRL** | +20% custo | 7→14 dias | Antecipar 3-5 dias |
| **Greve Transporte** | -100% entrega | 14→21+ dias | +50% safety stock |
| **Restrição Importação** | -100% componente | ×2-3 lead time | Comprar local/premium |
| **Inflação Alta** | +10-15% preço | +5 dias | Comprar antecipadamente |
| **Recessão** | -30% demanda | Lead time redução | Reduzir estoque |

**Fonte de Dados:**
- **BACEN:** Taxa de câmbio, Selic
- **IBGE:** Inflação (IPCA), PIB
- **Google News API:** Alertas greves, importação

**Integração no Sistema:**
```python
# Pseudocódigo
exchange_rate = fetch_bacen_rate()
if exchange_rate_volatility > 0.05:
    demand_multiplier = 1.2  # +20%
    safety_stock_multiplier = 1.3
    recommend_advance_purchase(days=7)
```

### 3.3 Fatores Tecnológicos

**Impacto:** **MÉDIO** - Mudanças de longo prazo, mas previsíveis

| Fator | Impacto Demanda | Lead Time Ajuste | Ação Preventiva |
|-------|----------------|------------------|-----------------|
| **Expansão 5G** | +15-20%/ano | +5-10 dias | Projeção anual |
| **Migração Fibra** | -30% cabo simples | +3-5 dias | Ajustar mix produtos |
| **Anatel Leilões** | Picos temporários | +10-20 dias | Planejamento por região |
| **Novos Padrões** | Substituição gradual | +30-60 dias | Ciclo de upgrades |

**Fonte de Dados:**
- **ANATEL:** Leilões, cobertura 5G
- **ABR Telecom:** Tendências setoriais
- **Agência Nacional de Telecomunicações:** Políticas públicas

**Integração no Sistema:**
```python
# Pseudocódigo
anatel_data = fetch_anatel_5g_coverage()
if anatel_data['new_municipalities'] > threshold:
    demand_multiplier = 1.2  # +20% expansão
    recommend_category_shift("5G equipment")
```

### 3.4 Fatores Operacionais

**Impacto:** **ALTO** - Parte do dia-a-dia da Nova Corrente

| Fator | Impacto Demanda | Lead Time Ajuste | Ação Preventiva |
|-------|----------------|------------------|-----------------|
| **Férias Julho** | -25% demanda | N/A | Reduzir previsão |
| **Feriados Prolongados** | -20% demanda | N/A | Ajustar PP downward |
| **Renovação SLA (Jan/Jul)** | +25% demanda | +5 dias | +Estoque 3-4 semanas |
| **Manutenções Agendadas** | +10-15% pontual | N/A | Planejamento mensal |
| **Eventos Especiais** | +100% pontual | +7-14 dias | Estoque emergência |

**Fonte de Dados:**
- **Calendário Nacional:** Feriados
- **Histórico Nova Corrente:** Padrões de renovação SLA
- **Agenda de Projetos:** Manutenções agendadas

**Integração no Sistema:**
```python
# Pseudocódigo
calendar = fetch_brazilian_holidays()
if is_holiday_period(date):
    demand_multiplier = 0.8  # -20%
elif is_sla_renewal_period(date):
    demand_multiplier = 1.25  # +25%
```

### 3.5 Fatores Regulatórios

**Impacto:** **BAIXO-MÉDIO** - Longo prazo, mas impacto significativo

| Fator | Impacto Demanda | Lead Time Ajuste | Ação Preventiva |
|-------|----------------|------------------|-----------------|
| **Novas Regras Anatel** | ±10-20% adaptação | +10-15 dias | Planejamento regulatório |
| **Inspeções Obrigatórias** | +30% pontual | N/A | Ciclo de inspeções |
| **Normas Ambientais** | Substituição gradual | +20-30 dias | Compliance antecipada |
| **Mudanças Código/Standards** | Substituição | +45-60 dias | Upgrade planejado |

---

<a name="modelos-referencia"></a>
## 4. 📐 MODELOS DE REFERÊNCIA APLICÁVEIS

### 4.1 ARIMA/SARIMA (AutoRegressive Integrated Moving Average)

**Categoria:** Time Series Clássico  
**Complexidade:** Baixa  
**Interpretabilidade:** Alta  

**Quando Usar:**
- Séries estacionárias ou que podem ser tornadas estacionárias
- Padrões lineares de tendência
- Dados com 2+ anos de histórico
- Baseline inicial

**Aplicação Nova Corrente:**
```
Conectores Ópticos (Fast-moving):
- Tendência linear estável
- Estacionária após diferenciação
- ARIMA(2,1,2) sugerido
- Previsão diária + confiança 95%
```

**Limitações:**
- Não captura não-linearidades complexas
- Sensível a outliers
- Requer estacionariedade

### 4.2 Prophet (Facebook)

**Categoria:** Time Series ML  
**Complexidade:** Média  
**Interpretabilidade:** Alta  

**Quando Usar:**
- Sazonalidades múltiplas (semanal, mensal, anual)
- Feriados e eventos conhecidos
- Missing data tolerante
- Trend não-linear

**Aplicação Nova Corrente:**
```
Consumo General:
- Sazonalidade semanal (segunda-feira pico)
- Sazonalidade mensal (última semana alto)
- Feriados brasileiros
- Expansão 5G (trend não-linear)
- Prophet recomendado
```

**Vantagens:**
- Múltiplas sazonalidades automáticas
- Eventos customizáveis
- Intervalos de confiança robustos

**Limitações:**
- Sensível a outliers extremos
- Computacionalmente mais pesado que ARIMA

### 4.3 LSTM (Long Short-Term Memory)

**Categoria:** Deep Learning  
**Complexidade:** Alta  
**Interpretabilidade:** Baixa  

**Quando Usar:**
- Padrões não-lineares complexos
- Múltiplas variáveis externas
- Grandes volumes de dados (>10k registros)
- Relacionamentos interdependentes

**Aplicação Nova Corrente:**
```
Ensemble com Fatores Externos:
- Demanda base (ARIMA)
- Clima (temperatura, chuva)
- Econômico (câmbio, inflação)
- Tecnológico (5G coverage)
- LSTM multivariado recomendado
```

**Vantagens:**
- Captura não-linearidades
- Aprende dependências temporais longas
- Escalável a múltiplos itens

**Desvantagens:**
- Computacionalmente pesado
- Requer muitos dados
- "Black box" (pouco interpretável)

### 4.4 Ensemble Methods

**Categoria:** Híbrido  
**Complexidade:** Média-Alta  
**Interpretabilidade:** Média  

**Quando Usar:**
- Robustez é crítica
- Diferentes modelos destacam em diferentes cenários
- Balanceamento entre precisão e confiança

**Aplicação Nova Corrente:**
```
Ensemble Recomendado:
- ARIMA: 30% peso (baseline robusto)
- Prophet: 30% peso (sazonalidades)
- LSTM: 40% peso (padrões complexos)
- Weighted Average final
- Confidence interval = min dos intervalos
```

**Benefícios:**
- Reduz variância de previsões
- Mais robusto a mudanças
- Melhor em cenários diversos

---

<a name="melhores-praticas"></a>
## 5. 🚀 MELHORES PRÁTICAS TECNOLÓGICAS

### 5.1 Internet das Coisas (IoT)

**Aplicação:**  
Sensores em estoque, torres e equipamentos fornecem dados em tempo real.

**Exemplos:**
- **Estoque:** Leitura RFID automática
- **Torres:** Sensores de temperatura, umidade
- **Equipamentos:** Telemetria de performance

**Benefícios:**
- Visibilidade em tempo real
- Alertas automáticos
- Redução de erro manual
- Enriquecimento de dados para ML

**Relevância Nova Corrente:**  
Média-alta (requer infraestrutura, mas baixo custo hoje).

### 5.2 Análise Preditiva Avançada

**AWS Supply Chain Demand Planning:**  
- 25 modelos integrados (ARIMA, LSTM, Prophet, etc.)
- Previsões rápidas e precisas
- UI de baixa latência

**Aplicação:**  
Benchmark para arquitetura Nova Corrente.

**Tesco/Walmart:**  
- Algoritmos ML 20x mais rápido
- Milhares de produtos previstos simultaneamente

**Aplicação:**  
Escalabilidade do sistema.

### 5.3 Modelos Avançados (Pesquisa Acadêmica)

**MCDFN (Multi-Channel Data Fusion Network):**
- CNN + LSTM + GRU integrados
- Captura padrões espaciais e temporais
- Aplicação: Ensemble avançado

**DeepAR+ (AWS):**
- Redes neurais multivariadas
- Previsão interdependente entre séries
- Aplicação: Previsão multi-item correlacionada

---

<a name="cases-sucesso"></a>
## 6. 🏆 CASES DE SUCESSO

### 6.1 Walmart

**Desafio:**  
Previsão demanda para milhares de produtos em milhares de lojas.

**Solução:**  
Bibliotecas ML para treinar algoritmos 20x mais rápido.

**Resultado:**
- Redução custos estoque
- Melhoria eficiência distribuição
- Decision-making data-driven

**Aplicação à Nova Corrente:**  
Escalar de 5 itens → 50+ itens com mesmo pipeline.

### 6.2 Tesco

**Desafio:**  
Gerenciar estoque e previsão em escala massiva.

**Solução:**  
Algoritmos ML avançados + IoT.

**Resultado:**
- Previsões precisas
- Otimização de inventário
- Redução desperdícios

**Aplicação à Nova Corrente:**  
Integrar IoT (sensores torres) para enriquecer previsões.

### 6.3 Amazon

**Desafio:**  
Previsão demanda global com múltiplos fatores.

**Solução:**  
AWS Supply Chain Planning (25 modelos).

**Resultado:**
- Previsões rápidas
- UI responsiva
- Integração seamless

**Aplicação à Nova Corrente:**  
Benchmark para arquitetura e UX.

---

## 📌 CONCLUSÃO

Este documento estabelece **padrões da indústria e dinâmicas** como base para desenvolvimento do sistema. SCOR, CPFR, fatores externos e cases de sucesso informam a solução.

**Próximos Passos:**
1. Aplicar framework SCOR para analisar processos
2. Mapear fatores externos relevantes
3. Selecionar modelos ML baseados em características de dados
4. Benchmark contra cases de sucesso

---

**Documento Final:** Novembro 2025  
**Versão:** 1.0  
**Status:** ✅ Referência Estratégica

