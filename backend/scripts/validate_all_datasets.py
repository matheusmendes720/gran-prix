"""
Script para validar qualidade de todos os datasets processados
"""
import sys
from pathlib import Path
import json
import logging
import pandas as pd

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.pipelines.data_processing.data_quality_validator import DataQualityValidator
from backend.pipelines.data_processing.ml_data_structure import MLDataStructuringPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Validar todos os datasets processados"""
    config_path = project_root / 'config' / 'datasets_config.json'
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    datasets = config.get('datasets', {})
    
    logger.info("="*80)
    logger.info("DATASET QUALITY VALIDATION")
    logger.info("="*80)
    logger.info(f"Total datasets to validate: {len(datasets)}")
    
    validator = DataQualityValidator()
    validation_results = {}
    
    for dataset_id, dataset_info in datasets.items():
        logger.info(f"\n{'='*70}")
        logger.info(f"Validating: {dataset_id}")
        logger.info(f"{'='*70}")
        
        # Tentar encontrar dataset estruturado
        structured_path = project_root / 'data' / 'processed' / 'ml_ready' / f"{dataset_id}_structured.csv"
        enriched_path = project_root / 'data' / 'processed' / 'ml_ready' / f"{dataset_id}_enriched.csv"
        
        df_path = enriched_path if enriched_path.exists() else structured_path
        
        if not df_path.exists():
            logger.warning(f"⚠ Dataset not found: {df_path}")
            continue
        
        try:
            df = pd.read_csv(df_path, parse_dates=['date'] if 'date' in pd.read_csv(df_path, nrows=1).columns else [], low_memory=False)
            
            results = validator.validate_dataset(df, dataset_id, dataset_info)
            validation_results[dataset_id] = results
            
            quality_score = results.get('quality_score', 0)
            logger.info(f"✓ Validation complete - Quality Score: {quality_score:.2%}")
            
        except Exception as e:
            logger.error(f"✗ Failed to validate {dataset_id}: {e}")
            validation_results[dataset_id] = {
                'error': str(e),
                'quality_score': 0.0
            }
    
    # Resumo geral
    logger.info("\n" + "="*80)
    logger.info("VALIDATION SUMMARY")
    logger.info("="*80)
    
    valid_datasets = [k for k, v in validation_results.items() if v.get('quality_score', 0) >= 0.7]
    warning_datasets = [k for k, v in validation_results.items() if 0.5 <= v.get('quality_score', 0) < 0.7]
    fail_datasets = [k for k, v in validation_results.items() if v.get('quality_score', 0) < 0.5]
    
    logger.info(f"✓ Pass (≥70%): {len(valid_datasets)} datasets")
    logger.info(f"⚠ Warning (50-70%): {len(warning_datasets)} datasets")
    logger.info(f"✗ Fail (<50%): {len(fail_datasets)} datasets")
    
    if fail_datasets:
        logger.warning("\nDatasets with quality issues:")
        for ds_id in fail_datasets:
            score = validation_results[ds_id].get('quality_score', 0)
            logger.warning(f"  - {ds_id}: {score:.2%}")
    
    # Salvar resumo
    summary = {
        'validation_date': pd.Timestamp.now().isoformat(),
        'total_datasets': len(validation_results),
        'valid_count': len(valid_datasets),
        'warning_count': len(warning_datasets),
        'fail_count': len(fail_datasets),
        'valid_datasets': valid_datasets,
        'warning_datasets': warning_datasets,
        'fail_datasets': fail_datasets,
        'scores': {k: v.get('quality_score', 0) for k, v in validation_results.items()}
    }
    
    summary_path = project_root / 'data' / 'processed' / 'quality_reports' / 'validation_summary.json'
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n✓ Validation summary saved: {summary_path}")


if __name__ == '__main__':
    main()
