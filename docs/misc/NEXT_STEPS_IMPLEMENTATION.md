# 🚀 Próximos Passos - Implementação

## Nova Corrente - Demand Forecasting System

---

## ✅ Progresso Atual

### Concluído:
1. ✅ **18 datasets configurados** (incluindo 4 brasileiros)
2. ✅ **Pipeline corrigido** (Zenodo funcionando)
3. ✅ **Training datasets atualizados** (valores corretos)
4. ✅ **Documentação criada** (guia completo de datasets brasileiros)
5. ✅ **Suporte GitHub implementado** (download de repositórios)

### Em Progresso:
1. ⏳ **Suporte para downloads diretos** (Anatel, Internet Aberta, Springer)
2. ⏳ **Parsing de PDFs** (Internet Aberta forecast)
3. ⏳ **Scraping de sites regulatórios** (Anatel)

---

## 📋 Implementações Realizadas

### 1. Suporte para Downloads Diretos

**Arquivo:** `src/pipeline/download_datasets.py`

**Melhorias:**
- ✅ Suporte para sources: `anatel`, `internet_aberta`, `springer`
- ✅ Detecção automática de formato de arquivo (PDF, CSV, etc.)
- ✅ Tratamento de query parameters em URLs
- ✅ Suporte para `file_format` no config

**Implementação:**
```python
elif source in ['mit', 'direct', 'anatel', 'internet_aberta', 'springer']:
    # Download direto com suporte para PDFs
    if file_format == 'pdf':
        # Download PDF e preparar para parsing
        logger.info("PDF downloaded. Consider using PDF parsing tools")
```

---

### 2. Parsing de PDFs

**Arquivo:** `src/utils/pdf_parser.py` ⭐ NOVO

**Funcionalidades:**
- ✅ Extração de tabelas de PDFs usando múltiplas bibliotecas:
  - `pdfplumber` (preferencial)
  - `tabula-py`
  - `camelot-py`
- ✅ Extração de texto
- ✅ Suporte para páginas específicas
- ✅ Conversão automática para CSV

**Uso:**
```python
from src.utils.pdf_parser import PDFParser

parser = PDFParser()
tables = parser.extract_tables(pdf_path, method='auto')
# Salvar tabelas extraídas
csv_files = parser.save_tables_to_csv(tables, output_dir)
```

**Dependências Adicionadas ao `requirements.txt`:**
- `pdfplumber>=0.10.0`
- `PyPDF2>=3.0.0`
- `tabula-py>=2.5.0`
- `camelot-py[cv]>=0.11.0`

---

### 3. Download de Datasets Anatel

**Arquivo:** `src/pipeline/download_datasets.py`

**Método:** `download_anatel_dataset()` ⭐ NOVO

**Funcionalidades:**
- ✅ Scraping da página Data Basis para encontrar links CSV
- ✅ Fallback para API Data Basis
- ✅ Detecção automática de links de download
- ✅ Suporte para URLs relativas/absolutas

**Implementação:**
```python
def download_anatel_dataset(self, url: str, output_dir: Path, dataset_info: Dict) -> bool:
    # Scraping da página Data Basis
    # Busca por links CSV
    # Fallback para API
```

---

## 🎯 Próximos Passos Detalhados

### Passo 1: Testar Downloads dos Novos Datasets

**Ação:** Testar downloads dos datasets brasileiros

```bash
# Testar download do Zenodo Broadband Brasil (já funciona)
python -m src.pipeline.download_datasets --datasets zenodo_broadband_brazil

# Testar download direto (Anatel, Internet Aberta, Springer)
python -m src.pipeline.download_datasets --datasets anatel_mobile_brazil
python -m src.pipeline.download_datasets --datasets internet_aberta_forecast
python -m src.pipeline.download_datasets --datasets springer_digital_divide
```

**Resultado Esperado:**
- ✅ Zenodo Broadband Brasil: Download CSV direto
- ⏳ Anatel: Pode requerer scraping refinado
- ⏳ Internet Aberta: PDF baixado, requer parsing
- ⏳ Springer: Artigo, pode requerer acesso especial

---

### Passo 2: Parsing de PDFs (Internet Aberta)

**Ação:** Extrair tabelas do PDF do Internet Aberta

```bash
# Após download do PDF
python -m src.utils.pdf_parser data/raw/internet_aberta_forecast/ --method pdfplumber --output data/processed/internet_aberta_forecast/
```

**Processo:**
1. Download do PDF
2. Parsing com pdfplumber/tabula
3. Extração de tabelas
4. Conversão para CSV
5. Preprocessing padrão

---

### Passo 3: Melhorar Scraping Anatel

**Ação:** Refinar scraping para encontrar links CSV corretos

**Melhorias Necessárias:**
1. Verificar estrutura real da página Data Basis
2. Adicionar seletores CSS mais específicos
3. Suporte para autenticação se necessário
4. Fallback para download manual com instruções

---

### Passo 4: Integrar ao Pipeline Completo

**Ação:** Adicionar parsing de PDFs ao pipeline de preprocessing

**Modificações:**
- Adicionar passo de parsing de PDFs antes de preprocessing
- Detectar arquivos PDF e extrair tabelas automaticamente
- Integrar tabelas extraídas ao fluxo normal

---

### Passo 5: Preprocessing Específico Brasileiro

**Ação:** Criar preprocessing específico para contexto brasileiro

**Features Especiais:**
- Tratamento de datas no formato brasileiro (DD/MM/YYYY)
- Normalização de nomes de regiões/estados
- Mapeamento de tecnologias (GSM, 3G, 4G, 5G)
- Agregações por região/município

---

## 🔧 Instalação de Dependências

**Instalar bibliotecas de PDF parsing:**

```bash
pip install pdfplumber PyPDF2 tabula-py camelot-py[cv]
```

**Nota:** `camelot-py` requer OpenCV, pode ser mais complexo de instalar:
```bash
# Linux/Mac
pip install camelot-py[cv]

# Windows (pode requerer binários OpenCV)
pip install camelot-py
```

**Alternativa mais leve:**
```bash
# Usar apenas pdfplumber (mais fácil)
pip install pdfplumber
```

---

## 📊 Status de Implementação

| Funcionalidade | Status | Prioridade |
|----------------|--------|------------|
| **Downloads Diretos** | ✅ Implementado | Alta |
| **Parsing de PDFs** | ✅ Implementado | Alta |
| **Download Anatel** | ✅ Implementado | Média |
| **Teste Downloads** | ⏳ Pendente | Alta |
| **Integração Pipeline** | ⏳ Pendente | Alta |
| **Preprocessing Brasileiro** | ⏳ Pendente | Média |

---

## 🧪 Testes Recomendados

### Teste 1: Download Zenodo Broadband Brasil

```bash
python -m src.pipeline.download_datasets --datasets zenodo_broadband_brazil
```

**Verificar:**
- ✅ CSV baixado corretamente
- ✅ Formato esperado
- ✅ Preprocessing funciona

---

### Teste 2: Download e Parsing PDF (Internet Aberta)

```bash
# 1. Download PDF
python -m src.pipeline.download_datasets --datasets internet_aberta_forecast

# 2. Parsing PDF
python -m src.utils.pdf_parser data/raw/internet_aberta_forecast/*.pdf --method pdfplumber --output data/processed/internet_aberta_forecast/
```

**Verificar:**
- ✅ PDF baixado
- ✅ Tabelas extraídas corretamente
- ✅ CSVs gerados e válidos

---

### Teste 3: Download Anatel (com scraping)

```bash
python -m src.pipeline.download_datasets --datasets anatel_mobile_brazil
```

**Verificar:**
- ✅ Scraping encontra links CSV
- ✅ Download funciona
- ✅ Dados no formato esperado

---

## 🎯 Resultado Final Esperado

### Datasets Prontos para Uso:

1. **zenodo_broadband_brazil** ✅
   - Download direto via Zenodo
   - Preprocessing padrão
   - Pronto para ML

2. **internet_aberta_forecast** ⏳
   - Download PDF ✅
   - Parsing de tabelas ⏳
   - Preprocessing específico ⏳

3. **anatel_mobile_brazil** ⏳
   - Scraping Data Basis ⏳
   - Download CSV ⏳
   - Preprocessing brasileiro ⏳

4. **springer_digital_divide** ⏳
   - Download (pode requerer acesso)
   - Preprocessing massivo (~100M registros)
   - Amostragem inicial ⏳

---

## 📝 Notas Importantes

### 1. PDF Parsing
- **pdfplumber** é mais confiável para tabelas simples
- **tabula-py** funciona melhor para tabelas complexas
- **camelot-py** é mais pesado mas mais preciso
- **Recomendação:** Começar com pdfplumber, usar tabula como fallback

### 2. Scraping Anatel
- Data Basis pode mudar estrutura do site
- Pode requerer autenticação em alguns casos
- **Fallback:** Instruções para download manual

### 3. Dataset Springer (~100M registros)
- Requer Dask para processamento
- **Recomendação:** Amostrar 1-5M registros inicialmente
- Processar em batches
- Usar sampling estratificado

---

## ✅ Checklist de Implementação

- [x] Suporte downloads diretos (Anatel, Internet Aberta, Springer)
- [x] Parsing de PDFs implementado
- [x] Download Anatel com scraping
- [ ] Testar downloads de todos os datasets brasileiros
- [ ] Validar parsing de PDFs
- [ ] Integrar parsing de PDFs ao pipeline
- [ ] Preprocessing específico brasileiro
- [ ] Documentar processos e limitações

---

**Status:** 🚀 **IMPLEMENTAÇÃO INICIADA - Pronto para Testes**

**Próximo:** Testar downloads e validar funcionalidades!

---

**Nova Corrente Grand Prix SENAI - Demand Forecasting System**

