
## Slide 7 · Arquitetura integrada & decisão estratégica

| Visual | Como conduzir a fala |
| --- | --- |
| **Fragmentado × Integrado** | “Hoje Sapiens e o sistema proprietário não conversam; cada workaround consome R$ 50–80K/mês. O PrevIA Hub liga Sapiens, ANATEL, INMET, BACEN e CRM via API, alimenta o pipeline ARIMA+Prophet+LSTM e entrega um dashboard único.” |
| **Otimizando Estratégias (4 filtros)** | “Explico que guiamos o cliente por quatro filtros: atualizar Sapiens, resolver fragmentação, acelerar speed-to-value e chegar à liderança de custo.” |
| **Desafios na Gestão de Torres** | “Painel estilo Tetris mostra os blocos que o cliente equilibra (impacto financeiro, mercado em expansão, dados de suporte, fatores externos). O PrevIA organiza tudo numa base só.” |
| **Decision Tree** | “Comparo as alternativas: Upgrade Sapiens (6–12m, R$ 400–800K, 25% MAPE), adicionar Blue Yonder (6–12m, R$ 500K–1,5M, novo silo), construir custom (12–24m, alto risco) ou PrevIA (2–3m, R$ 150K, 9% MAPE, R$ 2,4M de economia).” |
| **Amplitude de Fatores Externos** | “Fecho com o gráfico que mostra cobertura equilibrada entre econômico/financeiro (35%), climático (25%), temporal/operacional (20%) e regulatório (20%).” |

### Referências

```text
232:335:deck/pitch_8_slides_rascunho_expandido.md
Decisao-Infograficos-v3-PT-BR-Corrigido.md (decision tree, fatores externos)
```

### Roteiro rápido (Slide 7)

1. **Arquitetura:** “Começo com o ‘antes/depois’: dois sistemas isolados vs. o hub que conecta clima, economia e telecom.”
2. **Jornada estratégica:** “Os quatro filtros provam que não é só tecnologia; é plano de ganho de velocidade e custo.”
3. **Decisão racional:** “A árvore evidencia custo/tempo/risco dos caminhos. O verde (PrevIA) entrega em 2-3 meses e economiza R$ 2,4M.”
4. **Cobertura de sinais:** “O gráfico de amplitude justifica a precisão: nenhum concorrente rastreia todos esses fatores.”

---

## Slide 8 · Otimizando estratégias

| Visual | Como conduzir a fala |
| --- | --- |
| **Círculos dos 4 filtros** | “Mostro que o método segue uma sequência: atualizar Sapiens com dados confiáveis, resolver a fragmentação, acelerar o speed-to-value e chegar à liderança de custo.” |
| **Setas de fluxo** | “Refaço o loop completo para reforçar que é um ciclo contínuo, não um projeto pontual.” |

### Referências

```text
253:270:deck/pitch_8_slides_rascunho_expandido.md
```

### Roteiro rápido (Slide 8)

1. **Contexto:** “Depois da integração, não largamos o cliente — guiamos pelas quatro etapas.”
2. **Filtro por filtro:** explique rapidamente o ganho em cada círculo.
3. **Mensagem final:** “É assim que garantimos captura de valor em 90 dias, não 12 meses.”

---

## Slide 9 · Cobertura de fatores externos

| Visual | Como conduzir a fala |
| --- | --- |
| **Barras horizontais (35/25/20/20%)** | “Destaque que cada barra representa recursos dedicados a sinais econômico-financeiros, climáticos, operacionais e regulatórios.” |
| **Tabela de sinais monitorados** | “Liste exemplos concretos: câmbio, diesel, IPCA; chuva INMET; calendário SLA/backlog; ANATEL 5G, ICMS.” |

### Referências

```text
273:291:deck/pitch_8_slides_rascunho_expandido.md
```

### Roteiro rápido (Slide 9)

1. **Amplitude:** “Nenhum concorrente cobre todos esses sinais, por isso mantemos 92%+ de precisão.”
2. **Exemplos vivos:** cite um caso climático e um econômico para tornar concreto.
3. **Gancho:** “Essa cobertura completa é o que transforma ruptura em oportunidade.”

---

## Slide 10 · Próximos passos modulares

| Visual | Ponto de fala |
| --- | --- |
| **Fluxo Integração → Training → Deploy → Streaming** | “Mostre que os módulos são independentes, mas o fast-track entrega os quatro em 90 dias.” |
| **Ícones batch vs streaming / MLOps** | “Explique que começamos em batch diário (semanas 1-4) e migramos para streaming + MLOps até o dia 90.” |

### Referências

```text
294:312:deck/pitch_8_slides_rascunho_expandido.md
```

### Roteiro rápido (Slide 10)

1. **Semana 1-4:** plugamos dados, rodamos batch e provamos MAPE ≤9%.
2. **Dias 30-60:** ativamos fatores externos e automação de compras.
3. **Dia 90:** streaming ativo, alertas em tempo real, pipeline pronto para escalar.

---

## Slide 11 · Dream team + call-to-action

| Visual | Ponto de fala |
| --- | --- |
| **Fotos/ícones do time** | “Apresente rapidamente funções: Filipe (dados), Samara & Jônatas (produto/UI), Matheus & Lucas (engenharia).” |
| **Diagrama SaaS → ROI** | “Explique o modelo de assinatura por posição, onboarding faseado e payback em 6–8 meses / ROI 728%.” |
| **QR code com 3 opções** | “Convide a escolher na hora: Piloto Express (30 dias), PoC 60 dias com TCO, Fast-Track 90 dias com rollout completo.” |

### Referências

```text
314:335:deck/pitch_8_slides_rascunho_expandido.md
```

### Roteiro rápido (Slide 11)

1. **Confiança:** “Mostre o time responsável pelo hub e o histórico de implementações.”
2. **Modelo claro:** “Explique SaaS + onboarding em fases + garantia de MAPE ≤9%.”
3. **CTA:** “Escaneie o QR code agora e decidimos qual rota (Piloto, PoC, Fast-Track) vocês preferem.”

---
# Script de Pitch

[1 tool called]

## Slide 1

### Identificação dos gráficos e blocos de texto de referência

1. **Painel “O Paradoxo do Setor: Investimento vs. Multas”**

   - Mostra duas barras (CAPEX anual R$ 34,6 bi vs. multas de qualidade R$ 34,2 mi).
   - Relaciona-se diretamente com o script que abre o pitch ao enfatizar perdas mesmo com alto investimento.

   ```25:31:deck/pitch_8_slides_rascunho_expandido.md

   ```

> "Você já imaginou... 80% das empresas... R$ 1,2 milhão em ineficiências..."

1. **Painel “Expansão do Mercado de Telecom (Últimos 12 Meses)”**  
   - Barras horizontais para Fibra Óptica (+13,5%), Banda Larga Fixa (+10,1%), Antenas 5G (+100%), Cidades com 5G (+131%).  
   - Serve como contexto do crescimento acelerado que exige previsibilidade (mesmo bloco textual do script e objetivos).

1. **Bloco “Desafios Operacionais Específicos”**  
   - Dois donuts destacando:
     - “+50–200% Picos de Demanda Sazonal – Eventos previsíveis geram picos de demanda.”
     - “+50% Expansão até 2026 – Expansão de 50 posições até 2026 exige precisão.”  
   - Texto de apoio na base: “A falta de previsibilidade da demanda leva a desafios operacionais significativos...”  
   - Referenciado na seção de objetivos do slide e complementa os dados do script.

1. **Gráfico “Distribuição de Torres de Telecom no Brasil (81.567)”**  
   - Donut com fatias: Nova Corrente (22,1% / 18.000 torres – destaque central), American Tower (28,0% / 22.800), Outros Players (50% / 40.767).  
   - Sustenta a narrativa sobre relevância da Nova Corrente e reforça a pergunta retórica inicial (mesma seção do script).

#### Blocos textuais completos para o slide

- Objetivos do slide: prender atenção, criar expectativa, estabelecer conexão emocional.
- Script sugerido (perguntas e dados sobre perdas de R$ 120 mil/ano e R$ 1,2 mi em ineficiências).
- Elementos visuais e técnicas de impacto listados logo após o script.

Tudo isso está agrupado na seção do arquivo `pitch_8_slides_rascunho_expandido.md` referente ao Slide 1 (linhas 11–47).

---

## Slide 2

### 1. Cadeia quebrada (topo esquerdo)

**Gráfico:** `Falta de Peças Críticas Interrompe a Manutenção da Torre`

- Cada elo da cadeia representa uma consequência em cascata:
  1. **Manutenção interrompida/atrasada** – “A torre sai do ar.”
  2. **Falha na torre** – “Falha no SLA de 99%.”
  3. **Multa contratual** – “Multa de 2-10% do contrato.”
  4. **Perda de cliente B2B** – “Perda de receita recorrente massiva.”
  5. **Dano reputacional** – “Dano à reputação no mercado.”
- Usado para explicar verbalmente que uma única peça crítica indisponível desencadeia múltiplos riscos simultâneos.

### 2. Barras de custo (topo direito)

**Gráfico:** `Custo de Reposição de Item Crítico`

- Barra verde: **Reposição planejada** → R$ 1.000.
- Barra vermelha: **Reposição emergencial** → R$ 3.000 (observação: inclui frete aéreo e contingências +200%).
- Serve para quantificar financeiramente o slide anterior: “cada ruptura triplica o custo.”

### 3. Donut KPMG (centro inferior esquerdo)

**Gráfico:** `Impacto de Falhas na Previsibilidade (Estudo KPMG, 2025)`

- 76% das empresas perdem valor de mercado quando falham na previsão.
- 21% reportam quedas superiores a 10% nas ações.
- 24% “sem impacto claro”.
- Reforça que a dor não é apenas operacional — vira perda de valuation.

### 4. Balde vazando (centro inferior direito)

**Gráfico:** `Conectores Ópticos: Um Desastre na Cadeia de Suprimentos`

- Quatro “jatos” saindo do balde com rótulos:
  - **Previsão imprecisa** – níveis de estoque não confiáveis
  - **Compras de emergência** – frete aéreo aumenta custos
  - **Multas de SLA** – impacto negativo no contrato mensal
  - **Rupturas frequentes** – ocorrem várias vezes por mês
  - **Erosão da margem** – perdas financeiras anuais significativas
- Ajuda a “pintar” visualmente a drenagem contínua de caixa.

---

### Blocos de texto do arquivo `pitch_8_slides_rascunho_expandido.md` que sustentam o slide

```53:75:deck/pitch_8_slides_rascunho_expandido.md
### Objetivo:
- Identificar claramente o problema
- Quantificar o impacto financeiro
- Mostrar oportunidades de melhoria e superar concorrência

### Script Sugerido:
> "A gestão da Nova Corrente custa R$ 1,2 milhão por ano em ineficiências...
> ...Enquanto isso, seus concorrentes que usam gestão inteligente estão ganhando market share..."
```

```77:84:deck/pitch_8_slides_rascunho_expandido.md
### Elementos Visuais:
- Vídeo: Apresentando o desafio
- Gráficos de cascata
- Comparação antes vs depois
- Mapa de calor
- Cores vermelho/amarelo para alertas
```

```85:91:deck/pitch_8_slides_rascunho_expandido.md
### Dados-Chave:
- R$ 1,2 milhão/ano em ineficiências
- 60% rupturas por planilhas manuais
- 35% capital travado
- 12 rupturas/mês
- 94% SLA (target: 99%)
```

---

### Roteiro de fala sugerido (seguindo a ordem do screenshot)

1. **Apontar a cadeia quebrada:**“Quando uma peça crítica atrasa, a manutenção sai do ar. Isso derruba o SLA de 99%, gera multa contratual de até 10% e cria uma experiência ruim que custa clientes B2B inteiros, além de manchar a reputação.”
2. **Comparar custos planejado vs emergencial:**“Se eu planejo, cada reposição custa mil reais. Mas cada emergência custa três mil, porque envolve frete aéreo e contingências. É um custo 200% maior – e acontece justamente quando a torre já está no chão.”
3. **Levar o olhar para o estudo da KPMG:**“Não é só caixa do mês: 76% das empresas perdem valor de mercado quando falham na previsão. Um quinto delas vê queda de mais de 10% nas ações. Ou seja, a bolsa pune quem não tem previsibilidade.”
4. **Fechar com o balde vazando (efeito cumulativo):**
   “É um balde furado: previsão imprecisa → compras de emergência → multas de SLA → rupturas frequentes → erosão da margem. Tudo isso acontece várias vezes por mês. É a definição de perder dinheiro dormindo.”

Esse roteiro cobre o slide completo e mantém a exposição 100% visual, sem necessidade de texto extra na tela.

---

## Slide 3 · Solução previsível e sazonal

| Zona visual | Como conduzir a fala |
| --- | --- |
| **Linha do tempo animada** | “Antes: produto parado, caminhão perdido, capital indo embora. Depois de ligar o PrevIA: tudo fica verde, caminhão sai com destino certo.” |
| **Marcadores de tempo (30s / 2 min)** | “Em 30 segundos eu sei o que vai faltar nos próximos 30 dias; em 2 minutos recebo a recomendação completa de compra.” |
| **Painel dos 4 fatores** | Explicar o “motor”: fatores sazonais (+40% chuva Nov–Abr), econômicos (Selic, câmbio, greves), tecnológicos (5G, leilões), operacionais (SLA, penalidades). Tudo alimenta o ensemble ARIMA + Prophet + LSTM com dados do INMET, BACEN e ANATEL. |
| **Heatmap/cascata** | Mostrar o fluxo “alerta → recomendação → execução”: áreas vermelhas viram verdes porque a ação já vem pronta. |

### Referências no deck (Slide 3)

```text
95:137:deck/pitch_8_slides_rascunho_expandido.md
Objetivo: Apresentar a solução, destacar fatores previsíveis, mostrar como resolvemos a dor.
Script: “Em 30s você visualiza... em 2 min recebe recomendações... modelos ML com fatores sazonais/econômicos/tecnológicos/operacionais... Tudo integrado aos sistemas atuais.”
Elementos visuais: vídeo antes/depois, gráfico preenchendo, infográfico dos 4 fatores.
Diferenciais técnicos: Integrações INMET/BACEN/ANATEL + ensemble ARIMA/Prophet/LSTM.
```

### Roteiro rápido (Slide 3)

1. **Antes vs. depois:** “Hoje o gestor vê data vermelha e dinheiro voando. Com o PrevIA, o mesmo cenário fica verde e executável.”
2. **Radar em tempo real:** “30 segundos para detectar a ruptura futura; 2 minutos para a recomendação automática. Zero planilhas.”
3. **Motor inteligente:** “A precisão vem porque cruzamos chuva, Selic, 5G e o SLA da própria Nova Corrente. Não é feeling; é telemetria.”
4. **Execução guiada:** “Cada alerta já sai com ação. O gestor só aprova e executa. Resultado: desperdício cai e a demanda é antecipada.”

---

## Slide 4 · Demonstração e prova visual

| Visual | Mensagem-chave na fala |
| --- | --- |
| **Seta “Melhorias Operacionais com PrevIA”** | Percorra as etapas: rupturas caem de 12→3/mês, SLA sobe 94%→99,2%, MAPE cai 25%→10%, margem muda de -2/-3pp para +1/+2pp, capital de estoque reduz -20%, custo emergencial cai R$ 50K→R$ 15K/mês, dias de estoque 60→48. Mostra que cada parte da operação melhora de forma mensurável. |
| **Fluxo de Caixa Acumulado (24 meses)** | Mostrar curva verde crescente com payback ~mês 1. “O investimento se paga no primeiro ciclo e gera R$ 5M+ em 24 meses.” |
| **Radar PrevIA vs concorrentes** | Destaque que o polígono azul domina accuracy, ROI time, fatores externos, customização e UX; concorrentes têm buracos (SAP IBP, Blue Yonder, Kinaxis, Proteus, NetSuite). Compara de forma instantânea. |
| **Waveform ‘Impacto da demanda em fatores externos’** | Explicar que tratamos diferentes horizontes: tecnológico (planejado), climático (sazonal), eventos locais (flutuação pós-evento) até tempestades (urgente). Mostra como a plataforma ajusta o modelo conforme o grau de urgência. |

### Referências no deck (Slide 4)

```text
140:185:deck/pitch_8_slides_rascunho_expandido.md
Objetivo: mostrar a solução em ação e comprovar 92%+ de precisão.
Script: walkthrough das telas (mapa ao vivo, forecast 30 dias, recomendação automática, simulação de economia).
Elementos visuais: vídeo rápido com dashboard, alertas, recomendações, dinheiro economizado, escudo de segurança.
Métricas: 92%+ precisão, 30s para visualizar, 2min para agir, R$ 18.5K/mês economia, 35% redução custo em 90 dias.
```

### Roteiro rápido (Slide 4)

1. **Passe pela seta:** “Cada bloco aqui é um KPI real: rupturas -75%, SLA +5,2pp, MAPE cai 60%, margem vira positiva, capital e custo emergencial despencam.”
2. **Aponte para o fluxo de caixa:** “Esse ganho vira dinheiro em caixa. Payback praticamente no mês 1 e acumulado de mais de R$ 5 milhões em dois anos.”
3. **Mostre o radar:** “Enquanto isso, o PrevIA lidera em accuracy, velocidade de ROI, customização e fatores externos. Os concorrentes deixam lacunas.”
4. **Conclua com o waveform:** “Fazemos isso porque entendemos o espectro completo de demanda, do previsível ao urgente. Cada fator externo já vem parametrizado e o time só executa.”

---

## Slide 5 · Diferencial operacional e ROI

| Visual | Ponto de fala |
| --- | --- |
| **Dinâmica B2B Telecom (quatro estágios)** | “Renovações SLA (jan–jul) puxam +25% demanda; expansões 5G adicionam +15–20% anual; manutenção preventiva mantém demanda contínua; emergências podem gerar +50–100% picos. A PrevIA cobre todos esses regimes.” |
| **Comparativo de Custo Total de Propriedade (3 anos)** | Mostre a barra verde do PrevIA (R$ 390K) vs. SAP IBP (R$ 3,7M), Blue Yonder (R$ 2,9M), Kinaxis (R$ 1,4M), NetSuite (R$ 1,05M), Proteus (R$ 550K). “Somos 3–9x mais acessíveis com escopo específico.” |
| **Cronograma de Implementação e Retorno** | Percorra as fases: Semana 1-4 (MVP), Mês 1-3 (Fase 1), Mês 3-6 (Fase 2), Mês 6-8 (payback), Mês 6+ (Fase 3 escalável). Reforce recuperação do investimento < 3 meses. |
| **Evolução de KPIs (24 meses)** | Use os quatro gráficos: MAPE cai 25→10%; rupturas 12→3/mês; capital estoque 400K→320K; custo emergencial 50K→15K. Mostra trajetória sustentada. |

### Referências no deck (Slide 5)

```text
189:235:deck/pitch_8_slides_rascunho_expandido.md
Objetivo atual: destacar amplitude e diferenciais competitivos.
Atualizar texto para incluir dinâmica B2B, TCO, timeline e KPIs de 24 meses.
```

### Roteiro rápido (Slide 5)

1. **Contextualize os regimes de demanda:** “Toda a operação B2B gira em picos previsíveis e imprevisíveis. O PrevIA entende cada janela e ajusta o estoque antes do pico.”
2. **Comparativo financeiro:** “Enquanto concorrentes custam de R$ 550K a R$ 3,7M em 3 anos, o PrevIA entrega o mesmo resultado — focado em telecom — por R$ 390K.”
3. **Timeline de implementação:** “Em 4 semanas temos o MVP; em 3 meses a operação já está integrada; no mês 6 batemos payback e abrimos espaço para 50 posições.”
4. **Trajetória de KPIs:** “MAPE, rupturas, capital e custos emergenciais caem trimestre a trimestre. Esse slide mostra a prova gráfica do ROI composto.”
