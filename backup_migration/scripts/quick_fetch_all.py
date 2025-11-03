"""Script rápido para buscar e baixar todos os datasets configurados."""
import sys
from pathlib import Path
import logging

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline.download_datasets import DatasetDownloader
from src.pipeline.scrapy_integration import ScrapyIntegration
from src.utils.dataset_registry import DatasetRegistry

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Buscar e baixar todos os datasets configurados rapidamente"""
    import json
    
    print("\n" + "="*80)
    print("QUICK FETCH ALL DATASETS")
    print("="*80 + "\n")
    
    registry = DatasetRegistry()
    downloader = DatasetDownloader()
    scrapy_integration = ScrapyIntegration()
    
    # Obter todos os datasets configurados
    with open('config/datasets_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    datasets = config.get('datasets', {})
    
    print(f"Found {len(datasets)} configured datasets\n")
    
    # Baixar todos
    print("Starting downloads...\n")
    
    download_results = {}
    
    for i, (dataset_id, dataset_info) in enumerate(datasets.items(), 1):
        source = dataset_info.get('source', 'unknown')
        url = dataset_info.get('url', '')
        download_method = dataset_info.get('download_method', 'direct')
        
        print(f"[{i}/{len(datasets)}] {dataset_id} ({source})...", end=' ')
        
        try:
            if download_method == 'scrape' or source in ['anatel', 'internet_aberta', 'springer', 'github']:
                success = scrapy_integration.run_scrapy_spider(dataset_id, dataset_info)
            else:
                results = downloader.download_all_datasets(selected_datasets=[dataset_id])
                success = results.get(dataset_id, False)
            
            if success:
                print("[OK]")
                registry.update_dataset_status(dataset_id, 'downloaded')
            else:
                print("[FAIL]")
                registry.update_dataset_status(dataset_id, 'download_failed')
            
            download_results[dataset_id] = success
            
        except Exception as e:
            print(f"❌ ({e})")
            download_results[dataset_id] = False
    
    # Resumo
    successful = sum(1 for v in download_results.values() if v)
    total = len(download_results)
    
    print(f"\n{'='*80}")
    print(f"[OK] Success: {successful}/{total}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()

