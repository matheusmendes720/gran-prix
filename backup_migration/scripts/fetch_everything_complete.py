"""
Script Completo para Buscar, Baixar e Processar TODOS os Datasets
Integra todas as funcionalidades: descoberta, Scrapy, download, validação, registry
"""
import sys
from pathlib import Path
import logging
import json
from datetime import datetime

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.enhance_dataset_search import DatasetSearcher
from src.utils.dataset_registry import DatasetRegistry
from src.pipeline.download_datasets import DatasetDownloader
from src.pipeline.scrapy_integration import ScrapyIntegration
from src.utils.system_status_dashboard import SystemStatusDashboard
from src.utils.retry_handler import DownloadRetryHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Pipeline completo para buscar e baixar TODOS os datasets"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Buscar e baixar TODOS os datasets')
    parser.add_argument('--keywords', nargs='+', 
                       default=['telecom', 'demand', 'forecast', 'brazil', 'mobile', 'broadband', 'network', 'maintenance'],
                       help='Keywords para busca')
    parser.add_argument('--discover', action='store_true', default=True,
                       help='Descobrir novos datasets')
    parser.add_argument('--register', action='store_true', default=True,
                       help='Registrar datasets descobertos')
    parser.add_argument('--download', action='store_true', default=True,
                       help='Baixar datasets')
    parser.add_argument('--validate', action='store_true', default=True,
                       help='Validar datasets baixados')
    parser.add_argument('--max-datasets', type=int, default=None,
                       help='Máximo de datasets para processar (None = todos)')
    parser.add_argument('--force', action='store_true',
                       help='Forçar re-download mesmo se já existir')
    parser.add_argument('--sources', nargs='+',
                       choices=['zenodo', 'github', 'kaggle', 'anatel', 'all'],
                       default=['all'],
                       help='Fontes para buscar')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print("FETCH EVERYTHING COMPLETE - NOVA CORRENTE DATASETS")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    # Inicializar componentes
    registry = DatasetRegistry()
    dashboard = SystemStatusDashboard()
    
    results = {
        'discovery': {},
        'registration': {},
        'download': {},
        'validation': {},
        'statistics': {}
    }
    
    # Passo 1: Descobrir datasets
    if args.discover:
        print("\n" + "="*80)
        print("STEP 1: DISCOVERING DATASETS")
        print("="*80 + "\n")
        
        searcher = DatasetSearcher()
        
        # Filtrar fontes
        sources_to_search = ['zenodo', 'github', 'kaggle', 'anatel'] if 'all' in args.sources else args.sources
        
        print(f"Searching in sources: {', '.join(sources_to_search)}")
        print(f"Keywords: {', '.join(args.keywords)}")
        
        discovered = searcher.suggest_datasets(args.keywords)
        
        # Filtrar por fontes
        filtered_discovered = {}
        for source in sources_to_search:
            if source in discovered:
                filtered_discovered[source] = discovered[source]
        
        total_discovered = sum(len(datasets) for datasets in filtered_discovered.values())
        
        print(f"\n[OK] Discovered {total_discovered} potential datasets:")
        for source, datasets in filtered_discovered.items():
            print(f"  {source}: {len(datasets)} datasets")
        
        results['discovery'] = {
            'total': total_discovered,
            'by_source': {k: len(v) for k, v in filtered_discovered.items()}
        }
        
        # Salvar descobertos
        searcher.save_discovered_datasets(filtered_discovered, 'data/raw/discovered_datasets.json')
        print(f"[OK] Discovered datasets saved to: data/raw/discovered_datasets.json")
        
        discovered_datasets = filtered_discovered
    else:
        # Carregar descobertos existentes
        discovered_path = Path('data/raw/discovered_datasets.json')
        if discovered_path.exists():
            with open(discovered_path, 'r', encoding='utf-8') as f:
                discovered_datasets = json.load(f)
            print(f"[OK] Loaded existing discovered datasets from: {discovered_path}")
        else:
            discovered_datasets = {}
            print("[WARN] No discovered datasets found. Run with --discover first.")
    
    # Passo 2: Registrar datasets
    if args.register and discovered_datasets:
        print("\n" + "="*80)
        print("STEP 2: REGISTERING DATASETS")
        print("="*80 + "\n")
        
        registered_count = registry.discover_and_register(discovered_datasets)
        
        print(f"[OK] Registered {registered_count} new datasets")
        
        # Listar datasets registrados
        all_datasets = registry.list_datasets()
        print(f"\nTotal datasets in registry: {len(all_datasets)}")
        
        results['registration'] = {
            'new_registered': registered_count,
            'total_registered': len(all_datasets)
        }
    else:
        print("\n[SKIP] Skipping registration step")
    
    # Passo 3: Baixar datasets
    if args.download:
        print("\n" + "="*80)
        print("STEP 3: DOWNLOADING DATASETS")
        print("="*80 + "\n")
        
        downloader = DatasetDownloader()
        scrapy_integration = ScrapyIntegration()
        retry_handler = DownloadRetryHandler(max_retries=3)
        
        # Obter datasets para baixar
        if args.force:
            datasets_to_download = registry.list_datasets()
        else:
            # Apenas datasets não baixados
            datasets_to_download = registry.list_datasets(status='discovered')
        
        # Limitar quantidade se especificado
        if args.max_datasets:
            datasets_to_download = datasets_to_download[:args.max_datasets]
        
        print(f"[DOWNLOAD] Downloading {len(datasets_to_download)} datasets...")
        
        download_results = {}
        download_stats = {
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
        for i, dataset in enumerate(datasets_to_download, 1):
            dataset_id = dataset['id']
            source = dataset.get('source', 'unknown')
            url = dataset.get('url', '')
            
            print(f"\n{'='*80}")
            print(f"[{i}/{len(datasets_to_download)}] Processing: {dataset_id}")
            print(f"Source: {source}")
            print(f"URL: {url[:80]}..." if len(url) > 80 else f"URL: {url}")
            print(f"{'='*80}")
            
            # Verificar se já existe (a menos que force)
            raw_dir = Path('data/raw') / dataset_id
            if not args.force and raw_dir.exists() and any(raw_dir.iterdir()):
                print(f"  [SKIP] Already downloaded, skipping...")
                download_results[dataset_id] = True
                download_stats['skipped'] += 1
                continue
            
            if not url:
                print(f"  [WARN] No URL found, skipping...")
                download_results[dataset_id] = False
                download_stats['failed'] += 1
                continue
            
            # Preparar info de dataset
            dataset_info = {
                'name': dataset.get('title', dataset_id),
                'source': source,
                'url': url,
                'download_method': 'scrape' if source in ['anatel', 'internet_aberta', 'springer', 'github'] else 'direct'
            }
            
            try:
                # Baixar usando método apropriado
                if source in ['anatel', 'internet_aberta', 'springer', 'github']:
                    success = scrapy_integration.run_scrapy_spider(dataset_id, dataset_info)
                else:
                    # Usar download padrão com retry
                    try:
                        results = downloader.download_all_datasets(selected_datasets=[dataset_id])
                        success = results.get(dataset_id, False)
                    except Exception as e:
                        logger.error(f"Error downloading {dataset_id}: {e}")
                        success = False
                
                if success:
                    registry.update_dataset_status(dataset_id, 'downloaded')
                    print(f"  [OK] Download successful")
                    download_stats['success'] += 1
                else:
                    registry.update_dataset_status(dataset_id, 'download_failed')
                    print(f"  [FAIL] Download failed")
                    download_stats['failed'] += 1
                
                download_results[dataset_id] = success
                
            except Exception as e:
                logger.error(f"Unexpected error downloading {dataset_id}: {e}")
                registry.update_dataset_status(dataset_id, 'download_failed')
                download_results[dataset_id] = False
                download_stats['failed'] += 1
        
        results['download'] = {
            'total': len(datasets_to_download),
            **download_stats,
            'by_result': download_results
        }
        
        print(f"\n[SUMMARY] Download Summary:")
        print(f"  Success: {download_stats['success']}")
        print(f"  Failed: {download_stats['failed']}")
        print(f"  Skipped: {download_stats['skipped']}")
    
    # Passo 4: Validar datasets
    if args.validate:
        print("\n" + "="*80)
        print("STEP 4: VALIDATING DATASETS")
        print("="*80 + "\n")
        
        from scripts.validate_all_datasets import main as validate_main
        
        # Configurar argumentos
        import sys
        original_argv = sys.argv
        sys.argv = ['validate_all_datasets.py', '--update-registry']
        
        try:
            validate_main()
        finally:
            sys.argv = original_argv
        
        results['validation'] = {'completed': True}
    
    # Resumo final
        print("\n" + "="*80)
        print("FINAL SUMMARY")
        print("="*80)
    
    # Estatísticas gerais
    all_datasets = registry.list_datasets()
    status_counts = {}
    for dataset in all_datasets:
        status = dataset.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print(f"\nTotal datasets in registry: {len(all_datasets)}")
    print("\nBy Status:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    # Exibir dashboard
    print("\n" + "="*80)
    dashboard.print_dashboard()
    
    # Salvar resultados
    results_path = Path('data/registry/fetch_complete_results.json')
    results_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to: {results_path}")
    
    print("\n" + "="*80)
    print(f"COMPLETED AT: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")
    
    print("\nNext Steps:")
    print("1. Review downloaded datasets")
    print("2. Run preprocessing pipeline")
    print("3. Merge datasets")
    print("4. Add external factors")
    print("5. Train ML models")
    
    return results

if __name__ == "__main__":
    main()

