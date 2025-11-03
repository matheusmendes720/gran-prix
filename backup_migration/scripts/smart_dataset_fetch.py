"""Script inteligente para buscar, baixar, validar e configurar datasets automaticamente."""
import sys
from pathlib import Path
import logging

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.enhance_dataset_search import DatasetSearcher
from src.utils.dataset_registry import DatasetRegistry
from src.pipeline.download_datasets import DatasetDownloader
from src.pipeline.scrapy_integration import ScrapyIntegration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Pipeline inteligente completo"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Pipeline inteligente de datasets')
    parser.add_argument('--keywords', nargs='+', default=['telecom', 'demand', 'forecast', 'brazil'],
                       help='Keywords para busca')
    parser.add_argument('--auto-download', action='store_true',
                       help='Baixar automaticamente datasets descobertos')
    parser.add_argument('--auto-validate', action='store_true',
                       help='Validar automaticamente após download')
    parser.add_argument('--auto-config', action='store_true',
                       help='Gerar configurações automaticamente')
    parser.add_argument('--max-datasets', type=int, default=10,
                       help='Máximo de datasets para processar')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("🤖 SMART DATASET FETCH PIPELINE")
    print("="*70 + "\n")
    
    registry = DatasetRegistry()
    
    # Passo 1: Descobrir datasets
    print("\n" + "="*70)
    print("STEP 1: DISCOVERING DATASETS")
    print("="*70 + "\n")
    
    searcher = DatasetSearcher()
    discovered = searcher.suggest_datasets(args.keywords)
    
    total_discovered = sum(len(datasets) for datasets in discovered.values())
    print(f"✅ Discovered {total_discovered} potential datasets")
    
    # Passo 2: Registrar datasets
    print("\n" + "="*70)
    print("STEP 2: REGISTERING DATASETS")
    print("="*70 + "\n")
    
    registered_count = registry.discover_and_register(discovered)
    print(f"✅ Registered {registered_count} datasets")
    
    # Passo 3: Baixar datasets (se solicitado)
    if args.auto_download:
        print("\n" + "="*70)
        print("STEP 3: DOWNLOADING DATASETS")
        print("="*70 + "\n")
        
        # Obter datasets não baixados ainda
        unprocessed = registry.list_datasets(status='discovered')
        unprocessed = unprocessed[:args.max_datasets]  # Limitar quantidade
        
        print(f"Downloading {len(unprocessed)} datasets...")
        
        downloader = DatasetDownloader()
        scrapy_integration = ScrapyIntegration()
        
        download_results = {}
        
        for dataset in unprocessed:
            dataset_id = dataset['id']
            source = dataset.get('source', '')
            url = dataset.get('url', '')
            
            if not url:
                continue
            
            print(f"\n  Processing: {dataset_id}")
            
            # Preparar info de dataset para download
            dataset_info = {
                'name': dataset.get('title', dataset_id),
                'source': source,
                'url': url,
                'download_method': 'scrape' if source in ['anatel', 'internet_aberta'] else 'direct'
            }
            
            # Tentar download
            if source in ['anatel', 'internet_aberta', 'springer', 'github']:
                success = scrapy_integration.run_scrapy_spider(dataset_id, dataset_info)
            else:
                # Usar método padrão de download
                results = downloader.download_all_datasets(selected_datasets=[dataset_id])
                success = results.get(dataset_id, False)
            
            download_results[dataset_id] = success
            
            if success:
                registry.update_dataset_status(dataset_id, 'downloaded')
                print(f"    ✅ Download successful")
            else:
                registry.update_dataset_status(dataset_id, 'download_failed')
                print(f"    ❌ Download failed")
        
        successful_downloads = sum(1 for v in download_results.values() if v)
        print(f"\n✅ Downloads: {successful_downloads}/{len(download_results)} successful")
    
    # Passo 4: Validar datasets (se solicitado)
    if args.auto_validate:
        print("\n" + "="*70)
        print("STEP 4: VALIDATING DATASETS")
        print("="*70 + "\n")
        
        from scripts.validate_all_datasets import main as validate_main
        import sys
        # Simular argumentos de linha de comando
        sys.argv = ['validate_all_datasets.py', '--update-registry']
        validate_main()
    
    # Passo 5: Gerar configurações (se solicitado)
    if args.auto_config:
        print("\n" + "="*70)
        print("STEP 5: GENERATING CONFIGURATIONS")
        print("="*70 + "\n")
        
        configs = registry.export_configs()
        print(f"✅ Generated {len(configs)} auto-configurations")
    
    # Resumo final
    print("\n" + "="*70)
    print("🎯 FINAL SUMMARY")
    print("="*70)
    
    all_datasets = registry.list_datasets()
    status_counts = {}
    for dataset in all_datasets:
        status = dataset.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print(f"Total datasets in registry: {len(all_datasets)}")
    print("\nBy status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    print("\n" + "="*70)
    print("✅ Smart pipeline completed!")
    print("="*70 + "\n")
    
    print("\n📋 Next steps:")
    print("1. Review auto-generated configs (if generated)")
    print("2. Merge configs into datasets_config.json")
    print("3. Run preprocessing pipeline")
    print("4. Train ML models")

if __name__ == "__main__":
    main()

