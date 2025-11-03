"""
Script orquestrador completo para download, estruturação e documentação de datasets
Inclui integração automática de fatores externos
"""
import sys
from pathlib import Path
import json
import logging
from datetime import datetime
import pandas as pd

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.pipelines.data_processing.scrapy_integration import ScrapyIntegration
from backend.pipelines.data_processing.ml_data_structure import MLDataStructuringPipeline
from backend.pipelines.data_processing.external_factors_integration import ExternalFactorsIntegrationPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Pipeline completo de aquisição e estruturação de dados"""
    config_path = project_root / 'config' / 'datasets_config.json'
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    datasets = config.get('datasets', {})
    
    logger.info("="*80)
    logger.info("COMPREHENSIVE DATASET PIPELINE - FULLY EXPANDED")
    logger.info("="*80)
    logger.info(f"Total datasets to process: {len(datasets)}")
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Download phase
    logger.info("\n" + "="*80)
    logger.info("PHASE 1: DOWNLOADING DATASETS")
    logger.info("="*80)
    
    scrapy_integration = ScrapyIntegration(config_path=str(config_path))
    download_results = scrapy_integration.run_all_scrapy_datasets()
    
    successful_downloads = [k for k, v in download_results.items() if v]
    failed_downloads = [k for k, v in download_results.items() if not v]
    
    logger.info(f"\n✓ Successfully downloaded: {len(successful_downloads)}/{len(download_results)} datasets")
    if failed_downloads:
        logger.warning(f"✗ Failed downloads: {len(failed_downloads)} datasets")
        for ds_id in failed_downloads[:5]:  # Mostrar apenas os primeiros 5
            logger.warning(f"  - {ds_id}")
        if len(failed_downloads) > 5:
            logger.warning(f"  ... and {len(failed_downloads) - 5} more")
    
    # 2. Structuring phase
    logger.info("\n" + "="*80)
    logger.info("PHASE 2: STRUCTURING DATASETS FOR ML")
    logger.info("="*80)
    
    structuring_pipeline = MLDataStructuringPipeline()
    structuring_results = {}
    
    for dataset_id, dataset_info in datasets.items():
        raw_dir = project_root / 'data' / 'raw' / dataset_id
        if not raw_dir.exists():
            logger.warning(f"⚠ Raw data directory not found: {raw_dir}")
            continue
        
        # Encontrar arquivo raw
        raw_files = list(raw_dir.glob('*.csv')) + list(raw_dir.glob('*.json')) + list(raw_dir.glob('*.xlsx'))
        if not raw_files:
            logger.warning(f"⚠ No raw files found for {dataset_id}")
            continue
        
        raw_file = raw_files[0]  # Usar o primeiro arquivo encontrado
        
        try:
            structured_df = structuring_pipeline.structure_dataset(
                dataset_id=dataset_id,
                raw_file_path=str(raw_file),
                config=dataset_info
            )
            structuring_results[dataset_id] = True
            logger.info(f"✓ Structured {dataset_id}: {len(structured_df)} rows, {len(structured_df.columns)} columns")
        except Exception as e:
            logger.error(f"✗ Failed to structure {dataset_id}: {e}")
            structuring_results[dataset_id] = False
    
    successful_structures = [k for k, v in structuring_results.items() if v]
    logger.info(f"\n✓ Successfully structured: {len(successful_structures)}/{len(structuring_results)} datasets")
    
    # 3. External factors integration
    logger.info("\n" + "="*80)
    logger.info("PHASE 3: INTEGRATING EXTERNAL FACTORS")
    logger.info("="*80)
    
    external_factors_pipeline = ExternalFactorsIntegrationPipeline()
    
    enrichment_results = {}
    # Integrar fatores externos em cada dataset estruturado
    for dataset_id, success in structuring_results.items():
        if not success:
            continue
        
        structured_path = project_root / 'data' / 'processed' / 'ml_ready' / f"{dataset_id}_structured.csv"
        if not structured_path.exists():
            logger.warning(f"⚠ Structured file not found: {structured_path}")
            continue
        
        try:
            df = pd.read_csv(structured_path, parse_dates=['date'], low_memory=False)
            
            # Determinar região baseado no dataset_id
            region = 'bahia_salvador'
            if 'sao_paulo' in dataset_id or 'sp' in dataset_id:
                region = 'sp_sao_paulo'
            elif 'bahia' in dataset_id or 'salvador' in dataset_id:
                region = 'bahia_salvador'
            
            # Integrar fatores externos
            df_enriched = external_factors_pipeline.integrate_external_factors(df, region=region)
            
            # Salvar dataset enriquecido
            enriched_path = external_factors_pipeline.save_enriched_dataset(df_enriched, dataset_id)
            
            enrichment_results[dataset_id] = True
            logger.info(f"✓ Enriched {dataset_id} with external factors")
            logger.info(f"  - Original: {len(df)} rows, {len(df.columns)} columns")
            logger.info(f"  - Enriched: {len(df_enriched)} rows, {len(df_enriched.columns)} columns")
            
        except Exception as e:
            logger.error(f"✗ Failed to enrich {dataset_id}: {e}")
            enrichment_results[dataset_id] = False
    
    successful_enrichments = [k for k, v in enrichment_results.items() if v]
    logger.info(f"\n✓ Successfully enriched: {len(successful_enrichments)}/{len(enrichment_results)} datasets")
    
    # 4. Summary
    logger.info("\n" + "="*80)
    logger.info("PIPELINE SUMMARY")
    logger.info("="*80)
    logger.info(f"Total datasets in config: {len(datasets)}")
    logger.info(f"✓ Downloaded: {len(successful_downloads)}")
    logger.info(f"✓ Structured: {len(successful_structures)}")
    logger.info(f"✓ Enriched: {len(successful_enrichments)}")
    logger.info(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*80)
    
    # Save summary report
    summary = {
        'pipeline_run_date': datetime.now().isoformat(),
        'total_datasets': len(datasets),
        'downloaded': len(successful_downloads),
        'structured': len(successful_structures),
        'enriched': len(successful_enrichments),
        'successful_downloads': successful_downloads,
        'successful_structures': successful_structures,
        'successful_enrichments': successful_enrichments,
        'failed_downloads': failed_downloads
    }
    
    summary_path = project_root / 'data' / 'processed' / 'pipeline_summary.json'
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n✓ Pipeline summary saved to: {summary_path}")


if __name__ == '__main__':
    main()

