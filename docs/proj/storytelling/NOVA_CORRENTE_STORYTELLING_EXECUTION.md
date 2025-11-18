# Nova Corrente – Plano de Storytelling & Dashboards (Fase 5.5)

## 1. Objetivo
Transformar os outputs atualizados do pipeline (backfill + forecasts/prescrição) em narrativas visuais e dashboards executivos que suportem decisões de estoque, SLA e ROI.

## 2. Fontes de Dados
- **Snapshot Gold (13/11/2025):** `data/warehouse/gold/20251111T164236/FactDemand.parquet`
  - Fact principal com histórico real + backfill 2019-01-01 → 2025-11 (includes `qty_consumed`, `lead_time_days`, joias externas).
- **Forecasts & Prescriptions:** `data/outputs/nova_corrente/forecasts/`
  - `item*_site*.parquet` → previsões (ARIMA/XGBoost) com colunas `ds`, `forecast`, `arima_forecast`, `xgboost_forecast`.
  - `item*_site*_prescriptive.json` → estoque atual, ROP, safety stock, dias até ruptura.
  - `*_forecast_20251111_134330.csv` → agregados por família (EPI, FERRO_E_AÇO, etc.).
- **Documentação de suporte:** `docs/pipeline/`, `docs/reports/NOVA_CORRENTE_PRESCRIPTIVE_BRIEF.md`, `COMPLETE_PIPELINE_REPORT.json`.

## 3. Estrutura de Dashboards
1. **Painel Executivo**
   - KPIs: % redução estimada de stockouts, capital liberado, SLA projetado, ROI estimado.
   - Alertas visuais para famílias HIGH risk (EPI, FERRO E AÇO, MATERIAL ELÉTRICO).
   - Cards com status das dependências (Prophet/LSTM desativados, métricas agregadas pendentes).

2. **Forecast vs. Real**
   - Série histórica (real) x forecast 30 dias por família/SKU.
   - Bandas inferior/superior (quando Prophet habilitado; por ora replicar arima forecast).
   - Erro recente (MAE/MAPE) assim que métricas forem calculadas.

3. **Prescrição Operacional**
   - Estoque atual vs. reorder point & safety stock (por site/item).
   - Dias até ruptura (`days_until_stockout` do JSON).
   - Recomendações de compra (quantidade sugerida x urgência).

4. **Macroeconomia & Logística**
   - Indicadores chave do Gold (PTAX, SELIC, ANP fuel, freight rates) correlacionados com demanda.
   - Heatmap de impacto (volatilidade > threshold).

5. **ROI & Finance**
   - Gráficos de sensibilidade (melhor/base/pior) com base nos parâmetros do brief.
   - Evolução de capital investido vs. capital otimizado.

## 4. Pipeline de Storytelling
1. **ETL Visual**
   - Criar notebook `notebooks/storytelling/nova_corrente_dashboards.ipynb` (ou script equivalente).
   - Carregar Parquets/JSON, normalizar colunas (`ds` → `date`, `forecast` → `forecast_qty`, etc.).
   - Preparar tabelas intermediárias:
     - `viz_forecasts_family.parquet`
     - `viz_prescriptive_alerts.parquet`
     - `viz_macro_signals.parquet`

2. **Publicação**
   - **Metabase/Grafana:** conectar diretório `viz_*` ou utilizar views SQL/duckdb.
   - **Narrativa executiva:** gerar PDF/Markdown resumo (ex.: `docs/reports/NOVA_CORRENTE_STORYTELLING_SUMMARY.md`).
   - Atualizar `NOVA_CORRENTE_NOTE_INDEX.md` com links para dashboards/notebooks.

3. **Governança**
   - Versionar notebooks e scripts em `notebooks/storytelling/`.
   - Registrar execuções em `logs/storytelling/` (timestamp, dados carregados, outputs gerados).

## 5. Roadmap de Storytelling
| Passo | Responsável | Artefatos | Prazo sugerido |
|-------|-------------|-----------|----------------|
| Preparar datasets viz (`viz_*`) | Data Engineering | `notebooks/storytelling/...` | D+1 |
| Montar dashboards executivos | Analytics / BI | Metabase/Grafana | D+2 |
| Validar com stakeholders | Operações & Finanças | Checklist piloto | D+3 |
| Publicar narrativa final | Data & AI | `docs/reports/NOVA_CORRENTE_STORYTELLING_SUMMARY.md` | D+4 |

## 6. Pendências e Riscos
- **Métricas agregadas indisponíveis:** `metrics.json` vazio; atualizar assim que dependências (CmdStan/TensorFlow) estiverem instaladas.
- **Dependências opcionais:** Documentar quando Prophet/LSTM forem reativados para refletir bandas de confiança.
- **Sanitização de arquivos antigos:** remover/archivar Parquets com nomes não padronizados antes de publicar.

## 7. Próximos Passos Imediatos
1. Criar notebook/base ETL para dashboards (carregar Gold + forecasts).
2. Definir plataforma final (Metabase/Grafana) e credenciais de acesso.
3. Gerar mockups/dashboards MVP e validar com stakeholders.

---
*Documento criado em 2025-11-11 para guiar a execução da fase 5.5 (Storytelling & Dashboards).*

