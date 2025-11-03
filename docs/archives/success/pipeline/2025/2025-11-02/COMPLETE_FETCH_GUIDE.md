# 🚀 Guia Completo de Busca e Download de Datasets

## Nova Corrente - Demand Forecasting System

---

## 📋 Visão Geral

Guia completo para buscar, baixar e processar todos os datasets do sistema usando os scripts mais avançados.

---

## 🎯 Scripts Disponíveis

### 1. **Script Completo - `fetch_everything_complete.py`**

**O mais poderoso!** Integra todas as funcionalidades:
- ✅ Descoberta inteligente de datasets
- ✅ Registro automático
- ✅ Download com retry
- ✅ Validação automática
- ✅ Dashboard de status
- ✅ Relatórios detalhados

**Uso:**
```bash
# Pipeline completo (recomendado)
python scripts/fetch_everything_complete.py

# Buscar apenas em fontes específicas
python scripts/fetch_everything_complete.py --sources zenodo github

# Limitar quantidade
python scripts/fetch_everything_complete.py --max-datasets 10

# Forçar re-download
python scripts/fetch_everything_complete.py --force

# Customizar keywords
python scripts/fetch_everything_complete.py --keywords telecom brazil mobile 5G

# Apenas descoberta e registro
python scripts/fetch_everything_complete.py --download --validate

# Apenas download (sem descoberta)
python scripts/fetch_everything_complete.py --discover --register
```

**Opções:**
- `--keywords`: Keywords para busca (default: telecom, demand, forecast, brazil, etc.)
- `--sources`: Fontes para buscar (zenodo, github, kaggle, anatel, all)
- `--max-datasets`: Limitar quantidade de datasets
- `--force`: Forçar re-download mesmo se já existir
- `--discover`: Habilitar descoberta (default: True)
- `--register`: Habilitar registro (default: True)
- `--download`: Habilitar download (default: True)
- `--validate`: Habilitar validação (default: True)

---

### 2. **Script Rápido - `quick_fetch_all.py`**

**Rápido e direto!** Baixa todos os datasets configurados sem descoberta.

**Uso:**
```bash
python scripts/quick_fetch_all.py
```

**Quando usar:**
- ✅ Já sabe quais datasets quer
- ✅ Quer download rápido sem descoberta
- ✅ Está usando datasets pré-configurados

---

### 3. **Script Inteligente - `smart_dataset_fetch.py`**

**Inteligente e automatizado!** Pipeline completo de descoberta a configuração.

**Uso:**
```bash
# Pipeline completo automático
python scripts/smart_dataset_fetch.py --auto-download --auto-validate --auto-config

# Apenas descoberta e registro
python scripts/smart_dataset_fetch.py --keywords telecom brazil
```

---

## 🚀 Fluxo Recomendado

### Para Novos Projetos

```bash
# 1. Descoberta completa
python scripts/fetch_everything_complete.py --discover --register

# 2. Revisar datasets descobertos
cat data/raw/discovered_datasets.json

# 3. Download selecionado
python scripts/fetch_everything_complete.py --max-datasets 20

# 4. Validar downloads
python scripts/validate_all_datasets.py --update-registry

# 5. Ver status
python scripts/show_system_status.py
```

### Para Datasets Já Configurados

```bash
# Download rápido de todos
python scripts/quick_fetch_all.py

# Ou com validação
python scripts/fetch_everything_complete.py --discover --register --download --validate
```

---

## 📊 Estrutura de Resultados

### Arquivos Gerados

```
data/
├── raw/
│   ├── discovered_datasets.json          # Datasets descobertos
│   └── {dataset_id}/                      # Datasets baixados
│       └── *.csv, *.pdf, etc.
│
└── registry/
    ├── datasets_registry.json            # Registry principal
    ├── validation_report.json            # Relatório de validação
    ├── system_status.json                # Status do sistema
    └── fetch_complete_results.json        # Resultados do fetch completo
```

---

## 🎯 Casos de Uso

### Caso 1: Buscar Novos Datasets

```bash
python scripts/fetch_everything_complete.py \
  --keywords telecom maintenance brazil 5G \
  --sources zenodo github anatel \
  --max-datasets 15
```

### Caso 2: Download Rápido

```bash
python scripts/quick_fetch_all.py
```

### Caso 3: Pipeline Completo com Validação

```bash
python scripts/fetch_everything_complete.py \
  --discover \
  --register \
  --download \
  --validate \
  --max-datasets 20
```

### Caso 4: Forçar Re-download

```bash
python scripts/fetch_everything_complete.py --force
```

---

## 📈 Estatísticas e Monitoramento

### Ver Status do Sistema

```bash
python scripts/show_system_status.py
```

### Ver Registry

```python
from src.utils.dataset_registry import DatasetRegistry

registry = DatasetRegistry()
datasets = registry.list_datasets()

print(f"Total: {len(datasets)}")
for dataset in datasets:
    print(f"{dataset['id']}: {dataset.get('status')}")
```

### Ver Resultados

```bash
cat data/registry/fetch_complete_results.json | python -m json.tool
```

---

## 🔧 Configurações Avançadas

### Customizar Keywords

Editar `scripts/fetch_everything_complete.py`:
```python
parser.add_argument('--keywords', nargs='+', 
                   default=['telecom', 'demand', 'forecast', 'brazil', 
                            'mobile', 'broadband', 'network', 'maintenance'],
                   help='Keywords para busca')
```

### Customizar Fontes

```bash
python scripts/fetch_everything_complete.py --sources zenodo github kaggle
```

### Limitar Quantidade

```bash
python scripts/fetch_everything_complete.py --max-datasets 10
```

---

## ✅ Checklist de Execução

### Antes de Começar

- [ ] Verificar conexão com internet
- [ ] Verificar espaço em disco (recomendado: >5GB)
- [ ] Configurar APIs (Kaggle, GitHub - opcional)
- [ ] Instalar dependências (`pip install -r requirements.txt`)

### Durante Execução

- [ ] Monitorar logs
- [ ] Verificar progresso periodicamente
- [ ] Verificar erros e warnings

### Após Execução

- [ ] Verificar status do sistema
- [ ] Revisar datasets baixados
- [ ] Validar datasets críticos
- [ ] Verificar espaço em disco
- [ ] Salvar relatórios

---

## 🚨 Troubleshooting

### Problema: Download falha

**Solução:**
```bash
# Tentar novamente com retry automático
python scripts/fetch_everything_complete.py --force

# Ou usar script com retry handler
python scripts/smart_dataset_fetch.py --auto-download
```

### Problema: Muitos datasets descobertos

**Solução:**
```bash
# Limitar quantidade
python scripts/fetch_everything_complete.py --max-datasets 10

# Filtrar por fonte
python scripts/fetch_everything_complete.py --sources zenodo
```

### Problema: Sem espaço em disco

**Solução:**
```bash
# Limpar datasets antigos
rm -rf data/raw/{dataset_id}

# Limitar downloads
python scripts/fetch_everything_complete.py --max-datasets 5
```

### Problema: Timeout em downloads grandes

**Solução:**
```bash
# Usar retry handler (já integrado)
python scripts/fetch_everything_complete.py
```

---

## 📊 Métricas Esperadas

### Datasets Esperados

- **Zenodo**: 10-20 datasets relevantes
- **GitHub**: 5-15 repositórios relevantes
- **Kaggle**: 5-10 datasets relevantes
- **Anatel**: 3-5 datasets oficiais
- **Total**: 20-50 datasets potenciais

### Tempo de Execução

- **Descoberta**: 2-5 minutos
- **Download**: 10-30 minutos (depende do tamanho)
- **Validação**: 1-3 minutos
- **Total**: 15-40 minutos

---

## 🎉 Resultados Esperados

Após execução completa, você terá:

✅ Datasets descobertos e registrados  
✅ Datasets baixados e validados  
✅ Registry completo  
✅ Relatórios detalhados  
✅ Dashboard de status atualizado  

---

## 📝 Próximos Passos

Após busca e download:

1. **Revisar Datasets**
   ```bash
   python scripts/show_system_status.py
   ```

2. **Validar Qualidade**
   ```bash
   python scripts/validate_all_datasets.py
   ```

3. **Preprocessar**
   ```bash
   python src/pipeline/preprocess_datasets.py
   ```

4. **Treinar Modelos**
   ```bash
   python src/models/train_models.py
   ```

---

**Status:** ✅ **GUIA COMPLETO DE BUSCA E DOWNLOAD**

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**





