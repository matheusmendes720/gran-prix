"""
Script para estruturar todos os datasets brutos em formato ML-ready
"""
import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import json
import logging
from pathlib import Path
from backend.pipelines.data_processing.ml_data_structure import MLDataStructuringPipeline

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Estruturar todos os datasets para ML"""
    
    print("\n" + "="*80)
    print("STRUCTURING DATASETS FOR ML TRAINING")
    print("="*80)
    
    # Carregar configuração
    config_path = Path('config/datasets_config.json')
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Inicializar pipeline
    pipeline = MLDataStructuringPipeline()
    
    datasets = config.get('datasets', {})
    structured_datasets = {}
    
    print(f"\nProcessing {len(datasets)} datasets...\n")
    
    for dataset_id, dataset_info in datasets.items():
        print(f"\n{'='*80}")
        print(f"Processing: {dataset_id}")
        print(f"Name: {dataset_info.get('name', 'Unknown')}")
        print(f"{'='*80}")
        
        # Buscar arquivos brutos
        raw_dir = Path('data/raw') / dataset_id
        if not raw_dir.exists():
            logger.warning(f"Raw directory not found: {raw_dir}")
            continue
        
        # Encontrar arquivos de dados
        data_files = []
        for ext in ['.csv', '.json', '.xlsx', '.xls']:
            data_files.extend(list(raw_dir.glob(f"*{ext}")))
        
        if not data_files:
            logger.warning(f"No data files found in {raw_dir}")
            continue
        
        logger.info(f"Found {len(data_files)} data files")
        
        # Processar cada arquivo
        for data_file in data_files:
            try:
                logger.info(f"Structuring file: {data_file.name}")
                structured_df = pipeline.structure_dataset(
                    dataset_id=f"{dataset_id}_{data_file.stem}",
                    raw_file_path=str(data_file),
                    config=dataset_info
                )
                
                # Armazenar dataset estruturado
                key = f"{dataset_id}_{data_file.stem}"
                structured_datasets[key] = structured_df
                
                print(f"✅ Structured: {key} ({len(structured_df)} rows)")
                
            except Exception as e:
                logger.error(f"Failed to structure {data_file}: {e}")
                import traceback
                traceback.print_exc()
                continue
    
    # Mesclar com fatores externos
    print("\n" + "="*80)
    print("MERGING WITH EXTERNAL FACTORS")
    print("="*80)
    
    for dataset_id, df in structured_datasets.items():
        try:
            logger.info(f"Merging external factors for: {dataset_id}")
            df_with_factors = pipeline.merge_with_external_factors(df)
            structured_datasets[dataset_id] = df_with_factors
            print(f"✅ Merged external factors: {dataset_id}")
        except Exception as e:
            logger.error(f"Failed to merge external factors for {dataset_id}: {e}")
    
    # Combinar todos os datasets
    print("\n" + "="*80)
    print("COMBINING ALL DATASETS")
    print("="*80)
    
    try:
        combined_df = pipeline.combine_all_datasets(structured_datasets)
        print(f"✅ Combined dataset: {len(combined_df)} rows, {len(combined_df.columns)} columns")
        print(f"✅ Saved to: {pipeline.output_dir}/all_datasets_combined.csv")
    except Exception as e:
        logger.error(f"Failed to combine datasets: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("✅ DATASET STRUCTURING COMPLETE!")
    print("="*80)
    print(f"\nStructured datasets saved to: {pipeline.output_dir}")
    print(f"Combined dataset: {pipeline.output_dir}/all_datasets_combined.csv")
    print("\nNext step: Use structured data for ML model training")

if __name__ == "__main__":
    main()

