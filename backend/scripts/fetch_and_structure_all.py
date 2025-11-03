"""Script completo para buscar, baixar e estruturar todos os datasets."""
import sys
from pathlib import Path
import logging

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline.download_datasets import DatasetDownloader
from src.pipeline.scrapy_integration import ScrapyIntegration
from scripts.enhance_dataset_search import DatasetSearcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Pipeline completo: descoberta → download → estruturação"""
    
    print("\n" + "="*70)
    print("COMPLETE DATASET FETCH AND STRUCTURE PIPELINE")
    print("="*70 + "\n")
    
    # Passo 1: Descobrir novos datasets
    print("\n" + "="*70)
    print("STEP 1: DISCOVERING DATASETS")
    print("="*70 + "\n")
    
    searcher = DatasetSearcher()
    keywords = ['telecom', 'demand', 'forecast', 'brazil', 'mobile', 'broadband']
    discovered = searcher.suggest_datasets(keywords)
    
    total_discovered = sum(len(datasets) for datasets in discovered.values())
    print(f"\n✅ Discovered {total_discovered} potential datasets across all sources")
    
    # Passo 2: Download usando Scrapy (para datasets que requerem scraping)
    print("\n" + "="*70)
    print("STEP 2: DOWNLOADING WITH SCRAPY")
    print("="*70 + "\n")
    
    scrapy_integration = ScrapyIntegration()
    scrapy_results = scrapy_integration.run_all_scrapy_datasets()
    
    scrapy_success = sum(1 for v in scrapy_results.values() if v)
    print(f"\n✅ Scrapy downloads: {scrapy_success}/{len(scrapy_results)} successful")
    
    # Passo 3: Download usando métodos padrão
    print("\n" + "="*70)
    print("STEP 3: DOWNLOADING WITH STANDARD METHODS")
    print("="*70 + "\n")
    
    downloader = DatasetDownloader()
    standard_results = downloader.download_all_datasets()
    
    standard_success = sum(1 for v in standard_results.values() if v)
    print(f"\n✅ Standard downloads: {standard_success}/{len(standard_results)} successful")
    
    # Resumo final
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"Discovered datasets: {total_discovered}")
    print(f"Scrapy downloads: {scrapy_success}/{len(scrapy_results)}")
    print(f"Standard downloads: {standard_success}/{len(standard_results)}")
    print(f"Total successful: {scrapy_success + standard_success}")
    print("="*70 + "\n")
    
    # Verificar arquivos baixados
    raw_data_dir = Path('data/raw')
    if raw_data_dir.exists():
        datasets_found = []
        for dataset_dir in raw_data_dir.iterdir():
            if dataset_dir.is_dir():
                files = list(dataset_dir.glob('*'))
                if files:
                    datasets_found.append({
                        'name': dataset_dir.name,
                        'files': len(files),
                        'total_size': sum(f.stat().st_size for f in files if f.is_file())
                    })
        
        if datasets_found:
            print("DOWNLOADED DATASETS:")
            print("-" * 70)
            for dataset in sorted(datasets_found, key=lambda x: x['total_size'], reverse=True):
                size_mb = dataset['total_size'] / (1024 * 1024)
                print(f"  {dataset['name']:30s} - {dataset['files']:3d} files - {size_mb:7.2f} MB")
            print("="*70 + "\n")

if __name__ == "__main__":
    main()


