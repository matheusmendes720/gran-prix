# 📥 ÍNDICE COMPLETO — TODOS OS ARQUIVOS DE REFERÊNCIA

## 🎯 Arquivos Criados para Nova Corrente

### 1️⃣ **dados-download-links.md** ✅
   - **Conteúdo:** Links organizados por instituição (IBGE, BACEN, INMET, ANATEL, etc)
   - **Uso:** Ir copiar e colar diretamente no navegador
   - **Seções:**
     * MACRO-Econômico (PIB, IPCA, Câmbio, Selic)
     * Fiscal (ICMS, PIS/COFINS, ISS, tributos)
     * Telecom Específico (ANATEL, 5G)
     * Clima (INMET)
     * Logística (Frete, Portos)
     * Comércio Internacional (Comtrade, MDIC)
     * Índices Agregados (IMF, World Bank)

### 2️⃣ **batch_downloader.py** ✅
   - **Conteúdo:** Código Python pronto para produção
   - **Uso:** Executar scripts para automatizar downloads
   - **Classes:**
     * `IBGEConnector` → IPCA, PIB, Desemprego
     * `BACENConnector` → Câmbio PTAX, Selic
     * `INMETConnector` → Dados climáticos
     * `ANATELConnector` → 5G, cobertura
     * `ComtradeConnector` → Imports/Exports
     * `ReceitaFederalConnector` → Impostos
     * `FreightConnector` → Fretes globais
     * `DataPipelineOrchestrator` → Orquestrador master
   - **Função principal:** `run_daily_batch()`, `run_monthly_batch()`, `run_quarterly_batch()`

### 3️⃣ **quick-links-todos.md** ✅
   - **Conteúdo:** Tabelão master com todos os 27+ dados
   - **Uso:** Referência rápida (ctrl+F para buscar)
   - **Tabelas:**
     * Links críticos (atualizar diário/semanal)
     * Links altos (atualizar mensal)
     * Links médios (atualizar trimestral)
     * Links extras (atualizar anual)
     * Scripts rápidos em Python/Bash
     * Checklist de implementação

### 4️⃣ **master_download_links.csv** ✅
   - **Conteúdo:** Tabela em CSV com 27 fontes
   - **Colunas:** Data Category, URL, Fonte, Frequência, Autenticação, Tipo Download, Notas
   - **Uso:** Importar no Excel, filtrar, organizar por prioridade
   - **Vantagem:** Fácil para buscar, filtrar, enviar para equipe

### 5️⃣ **api-copy-paste-examples.md** ✅
   - **Conteúdo:** Exemplos prontos de curl e Python para cada API
   - **Uso:** Copy-paste direto no terminal ou IDE
   - **Seções:**
     * IBGE (IPCA, PIB, Desemprego)
     * BACEN (Câmbio, Selic)
     * AliceWeb (Importação/Exportação)
     * UN Comtrade
     * INMET (Clima)
     * ANATEL (5G, Investimentos)
     * Freightos / Drewry (Frete)
     * Receita Federal (Tributos)
     * Trading Economics
     * IMF / World Bank
     * Script orquestrador completo
     * Tabela resumida (quick reference)

---

## 🗺️ COMO USAR ESTES ARQUIVOS (Passo a Passo)

### Cenário 1: "Preciso AGORA de um dado específico" ⚡
1. Abra **quick-links-todos.md** ou **dados-download-links.md**
2. Procure (Ctrl+F) o dado (ex: "IPCA", "Câmbio")
3. Copie o URL
4. Cole no navegador → Download manual
5. **OU** use comando curl/Python do **api-copy-paste-examples.md**

### Cenário 2: "Quero automatizar downloads mensais" 🤖
1. Abra **batch_downloader.py**
2. Copie a classe relev ante (ex: `IBGEConnector`, `BACENConnector`)
3. Adapte para sua infraestrutura (Airflow, Cronjob, Lambda)
4. Configure autenticação (se necessário)
5. Teste com `run_monthly_batch()`
6. Schedule com cron: `0 2 1 * * python batch_downloader.py`

### Cenário 3: "Preciso organizar tudo para a equipe" 📊
1. Exporte **master_download_links.csv** para Excel
2. Adicione coluna "Status" (Implementado / Em Progress / TODO)
3. Adicione coluna "Responsável" (quem implementa)
4. Adicione coluna "Data Target" (quando implementar)
5. Compartilhe com equipe para rastreamento

### Cenário 4: "Vou integrar com o Feature Store" 🏗️
1. Use **batch_downloader.py** como base
2. Adapte outputs para enviar direto para:
   - Feast (open-source)
   - Hopsworks (managed)
   - Databricks Feature Store
   - AWS SageMaker Feature Store
3. Configure pipeline: Download → Validação → Feature Store → ML Models

### Cenário 5: "Preciso de relatório executivo" 📈
1. Use **master_download_links.csv** como base
2. Filtre por "Autenticação" = "Pública" (dados gratuitos)
3. Filtre por "Frequência" = "Mensal" (dados mais atualizados)
4. Priorize por "Fonte Oficial" (IBGE, BACEN, ANATEL)
5. Crie apresentação com essas ~10-15 principais

---

## ✅ DADOS CRÍTICOS (Comece por aqui)

### Tier 1 - ESSENCIAL (Implementar imediatamente)
```
1. IPCA Mensal (IBGE SIDRA 1737) → Inflação
2. Câmbio PTAX (BACEN OData) → USD/BRL diária
3. Selic (BACEN GSC 432) → Taxa de juros
4. Alíquotas ICMS (CONFAZ/SEFAZ) → Impostos estado
```

### Tier 2 - IMPORTANTE (Implementar em 2-4 semanas)
```
5. PIB Trimestral (IBGE SIDRA 12462) → Crescimento econômico
6. Desemprego (IBGE SIDRA 6385) → Mercado de trabalho
7. Cobertura 5G (ANATEL Painéis) → Tecnologia setor
8. Drawback (MDIC Portal) → Regime tributário
9. Fretes (Drewry, Freightos) → Logística global
```

### Tier 3 - COMPLEMENTAR (Implementar em 2-3 meses)
```
10. Clima INMET (BDMEP) → Impactos operacionais
11. Comtrade Imports (UN) → Competitividade global
12. PPP/CDS (IMF/Trading Econ) → Risco soberano
13. Investimentos Telecom (ANATEL) → Capex setor
```

---

## 🔧 CONFIGURAÇÃO MÍNIMA (Quick Start)

### Python + Dependências
```bash
pip install pandas requests python-dotenv
pip install apache-airflow  # Orquestração (opcional)
pip install great_expectations  # Validação (opcional)
```

### Estrutura de Pastas
```
/nova_corrente_pipeline/
├── batch_downloader.py          (este código)
├── requirements.txt
├── config/
│   └── sources.json             (URLs e parâmetros)
├── dados/
│   ├── raw/                     (downloads brutos)
│   ├── processed/               (após limpeza)
│   └── logs/
├── dags/
│   └── daily_pipeline.py        (Airflow DAG)
└── README.md
```

### requirements.txt
```
pandas>=1.3.0
requests>=2.25.0
python-dotenv>=0.19.0
apache-airflow>=2.2.0  # Opcional
great-expectations>=0.13.0  # Opcional
```

### Script Simplificado (Primeira Execução)
```bash
# 1. Clonar/criar diretórios
mkdir -p nova_corrente_dados/{raw,processed,logs}

# 2. Copiar batch_downloader.py

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar
python batch_downloader.py

# Output esperado: ./nova_corrente_dados/
#   ├── ptax_30d_20251108.csv
#   ├── selic_historico.csv
#   ├── ipca_monthly_20251108.csv
#   └── execution_summary_20251108.json
```

---

## 🚀 PRÓXIMAS FASES

### Fase 1 (Semana 1-2): Setup
- [ ] Download manual de todos os 27 dados
- [ ] Validar estrutura de cada arquivo
- [ ] Documentar transformações necessárias

### Fase 2 (Semana 3-4): Automação
- [ ] Conectar APIs em batch_downloader.py
- [ ] Testar cada conector isoladamente
- [ ] Criar Airflow DAGs para orquestração

### Fase 3 (Semana 5-6): Feature Store
- [ ] Importar dados no Feast/Hopsworks
- [ ] Criar features derivadas (lags, rolling windows)
- [ ] Validar schema com Great Expectations

### Fase 4 (Semana 7-8): ML Integration
- [ ] Conectar Feature Store ao Prophet/ARIMAX/TFT
- [ ] Testar modelos com dados históricos
- [ ] Calibrar previsões (MAPE target <15%)

### Fase 5 (Semana 9-12): Production
- [ ] Deploy em Kubernetes / Cloud
- [ ] Monitoramento com Prometheus/Grafana
- [ ] A/B testing de modelos
- [ ] Feedback loop com negócio

---

## 📞 TROUBLESHOOTING COMUM

### "API retorna 403 Forbidden"
- ✅ Solução: Adicionar User-Agent no header
- `headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}`

### "Comtrade está lento/timeout"
- ✅ Solução: Usar Comtrade Plus (API key) ou AliceWeb2 (MDIC)
- `requests.get(url, timeout=60)`  # Aumentar timeout

### "INMET BDMEP requer cadastro"
- ✅ Solução: Registrar em https://bdmep.inmet.gov.br/ (gratuito)
- OU baixar diretamente via FTP: `ftp://ftp1.inmet.gov.br/`

### "Dados históricos desatualizados"
- ✅ Solução: Usar lag structure em features (esperar 30-45 dias após mês)
- IPCA, PIB liberados ~45 dias após período fim

### "ICMS varia por estado / município"
- ✅ Solução: Usar lookup table local (SEFAZ de cada estado)
- Manter tabela sincronizada anualmente

---

## 📋 CHECKLIST DE IMPLEMENTAÇÃO

- [ ] Todos os 5 arquivos downloaded e revisados
- [ ] Python 3.8+ instalado
- [ ] Dependências (`pip install -r requirements.txt`)
- [ ] Pastas criadas (`mkdir -p dados/{raw,processed,logs}`)
- [ ] Teste simples executado (`python batch_downloader.py`)
- [ ] Pelo menos 1 API funcionando (começar com IPCA ou PTAX)
- [ ] Dados salvos em CSV para validação manual
- [ ] Documentação atualizada no README
- [ ] Cron/Airflow configurado para execução automática
- [ ] Alertas configurados para falhas de download
- [ ] Feature Store conectado (Feast ou similar)
- [ ] Modelos ML consumindo dados
- [ ] Dashboard criado para monitoramento
- [ ] Documentação compartilhada com equipe

---

## 💡 DICAS DE OURO

1. **Começar pequeno:** Implementar IPCA + Câmbio + Selic primeiro (3 dados)
2. **Validar schema:** Cada API pode ter mudanças (versionamento)
3. **Cache agressivo:** Guardar últimos 30 dias localmente (reduz API calls)
4. **Alertas:** Notificar se falta dado no pipeline (Slack/Email)
5. **Documentação:** Cada mudança em API = atualizar código + docs
6. **Versionamento:** Git commit com `data_version` em cada download
7. **Redundância:** Ter fallback (ex: IBGE primária, Trading Econ secundária)
8. **Testing:** Sempre testar com dados históricos antes de colocar em produção
9. **Monitoring:** Grafana dashboard com status de cada fonte
10. **Community:** Participar de grupos de Data Science BR para atualizações

---

**Última Atualização:** 8 Novembro 2025  
**Mantido por:** Nova Corrente Intelligence Team  
**Contato Técnico:** supply-chain-ml@novacorrente.com.br

## 🎉 Você tem TUDO que precisa para começar!

Próximo passo: Abra **quick-links-todos.md** e escolha seu primeiro dado para baixar.
