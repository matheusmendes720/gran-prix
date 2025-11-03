"""
Script para análise estatística completa de todos os datasets
"""
import sys
from pathlib import Path
import json
import logging
import pandas as pd

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.pipelines.data_processing.data_analyzer import DataAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Analisar todos os datasets processados"""
    config_path = project_root / 'config' / 'datasets_config.json'
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    datasets = config.get('datasets', {})
    
    logger.info("="*80)
    logger.info("COMPREHENSIVE DATASET ANALYSIS")
    logger.info("="*80)
    logger.info(f"Total datasets to analyze: {len(datasets)}")
    
    analyzer = DataAnalyzer()
    analysis_results = {}
    
    for dataset_id, dataset_info in datasets.items():
        logger.info(f"\n{'='*70}")
        logger.info(f"Analyzing: {dataset_id}")
        logger.info(f"{'='*70}")
        
        # Tentar encontrar dataset enriquecido ou estruturado
        enriched_path = project_root / 'data' / 'processed' / 'ml_ready' / f"{dataset_id}_enriched.csv"
        structured_path = project_root / 'data' / 'processed' / 'ml_ready' / f"{dataset_id}_structured.csv"
        
        df_path = enriched_path if enriched_path.exists() else structured_path
        
        if not df_path.exists():
            logger.warning(f"⚠ Dataset not found: {df_path}")
            continue
        
        try:
            # Detectar coluna de data
            sample_df = pd.read_csv(df_path, nrows=1)
            date_cols = [col for col in sample_df.columns if 'date' in col.lower()]
            
            if date_cols:
                df = pd.read_csv(df_path, parse_dates=[date_cols[0]], low_memory=False)
            else:
                df = pd.read_csv(df_path, low_memory=False)
            
            # Identificar target column
            target_col = None
            if 'quantity' in df.columns:
                target_col = 'quantity'
            elif 'demand' in df.columns:
                target_col = 'demand'
            
            analysis = analyzer.analyze_dataset(df, dataset_id, target_col)
            analysis_results[dataset_id] = analysis
            
            # Mostrar insights
            insights = analysis.get('insights', [])
            logger.info(f"✓ Analysis complete - {len(insights)} insights:")
            for insight in insights[:5]:  # Mostrar primeiros 5
                logger.info(f"  - {insight}")
            
        except Exception as e:
            logger.error(f"✗ Failed to analyze {dataset_id}: {e}")
            import traceback
            logger.debug(traceback.format_exc())
    
    # Resumo geral
    logger.info("\n" + "="*80)
    logger.info("ANALYSIS SUMMARY")
    logger.info("="*80)
    
    analyzed_count = len([k for k, v in analysis_results.items() if v])
    logger.info(f"✓ Successfully analyzed: {analyzed_count}/{len(datasets)} datasets")
    
    # Estatísticas agregadas
    total_rows = sum(v.get('basic_stats', {}).get('shape', {}).get('rows', 0) 
                     for v in analysis_results.values() if isinstance(v, dict))
    total_columns = sum(v.get('basic_stats', {}).get('shape', {}).get('columns', 0) 
                       for v in analysis_results.values() if isinstance(v, dict))
    
    logger.info(f"Total rows analyzed: {total_rows:,}")
    logger.info(f"Total columns analyzed: {total_columns:,}")
    
    # Salvar resumo
    summary = {
        'analysis_date': pd.Timestamp.now().isoformat(),
        'total_datasets': len(analysis_results),
        'analyzed_count': analyzed_count,
        'total_rows': total_rows,
        'total_columns': total_columns,
        'datasets': list(analysis_results.keys())
    }
    
    summary_path = project_root / 'data' / 'processed' / 'analysis_reports' / 'analysis_summary.json'
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n✓ Analysis summary saved: {summary_path}")


if __name__ == '__main__':
    main()
