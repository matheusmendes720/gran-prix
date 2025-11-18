# Nova Corrente Batch Runbook

## Pré-requisitos
- Ambiente Conda `nova-corrente-gpu` instalado (`conda env create -f environment.local.yml`).
- Arquivo `.env.local` com tokens válidos (INMET, BACEN, IBGE, ANATEL) e variáveis Prefect.
- `docs/proj/dadosSuprimentos.xlsx` atualizado no diretório padrão.

## Execução Completa
1. Ative o ambiente: `conda activate nova-corrente-gpu`.
2. Exporte variáveis do `.env.local` (PowerShell: `Get-Content .env.local | foreach { if($_ -and $_ -notmatch '^#'){ $name, $value = $_.split('='); setx $name $value } }`).
3. Rode a esteira: `python scripts/run_batch_cycle.py`.
4. Verifique `logs/pipeline/runs.csv` para status `success`.

## Outputs Principais
- Forecasts + prescritivos: `data/outputs/nova_corrente/forecasts/`.
- Métricas agregadas: `data/outputs/nova_corrente/forecasts/metrics_summary.json`.
- Rolling CV: `logs/pipeline/metrics/rolling_metrics_<item_site>.parquet`.
- Logs de validação: `logs/pipeline/validation/`.

## Troubleshooting
- **Falha em ingestão**: confira log de validação correspondente em `logs/pipeline/validation/`.
- **Ausência de snapshot**: garanta que workbook está acessível e `data/landing/silver/` contém dados válidos.
- **GPU indisponível**: ajuste `devices` em `TFTConfig` ou use CPU (performance reduzida).
- **Tokens inválidos**: regenere credenciais e atualize `.env.local`.

## Reprocessamento Parcial
- Ingestão específica: `python scripts/run_ingestion_flows.py --climate --date YYYY-MM-DD`.
- Rebuild warehouse: `python scripts/build_warehouse.py`.
- Reexecutar treinamento/custom horizon: `python scripts/run_training_pipeline.py --horizon 45 --max-series 20`.

