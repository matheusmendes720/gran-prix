"""Script para registrar automaticamente datasets descobertos."""
import sys
from pathlib import Path
import logging
import json

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.dataset_registry import DatasetRegistry
from scripts.enhance_dataset_search import DatasetSearcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Registrar datasets descobertos automaticamente"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Registrar datasets descobertos')
    parser.add_argument('--keywords', nargs='+', default=['telecom', 'demand', 'forecast', 'brazil'],
                       help='Keywords para busca')
    parser.add_argument('--discovered-file', default='data/raw/discovered_datasets.json',
                       help='Arquivo JSON com datasets descobertos')
    parser.add_argument('--auto-config', action='store_true',
                       help='Gerar configurações automaticamente para datasets válidos')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("AUTO-REGISTER DISCOVERED DATASETS")
    print("="*70 + "\n")
    
    registry = DatasetRegistry()
    
    # Verificar se arquivo de descobertos existe
    discovered_path = Path(args.discovered_file)
    
    if discovered_path.exists():
        logger.info(f"Loading discovered datasets from: {discovered_path}")
        with open(discovered_path, 'r', encoding='utf-8') as f:
            discovered_datasets = json.load(f)
    else:
        logger.info("No discovered datasets file found. Running search...")
        searcher = DatasetSearcher()
        discovered_datasets = searcher.suggest_datasets(args.keywords)
        searcher.save_discovered_datasets(discovered_datasets, args.discovered_file)
    
    # Registrar datasets
    print("\n" + "="*70)
    print("REGISTERING DATASETS")
    print("="*70 + "\n")
    
    registered_count = registry.discover_and_register(discovered_datasets)
    
    print(f"\n✅ Registered {registered_count} datasets")
    
    # Listar datasets registrados
    all_datasets = registry.list_datasets()
    print(f"\nTotal datasets in registry: {len(all_datasets)}")
    
    # Mostrar por status
    statuses = {}
    for dataset in all_datasets:
        status = dataset.get('status', 'unknown')
        statuses[status] = statuses.get(status, 0) + 1
    
    print("\nDatasets by status:")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")
    
    # Mostrar por fonte
    sources = {}
    for dataset in all_datasets:
        source = dataset.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print("\nDatasets by source:")
    for source, count in sorted(sources.items()):
        print(f"  {source}: {count}")
    
    # Gerar configurações automáticas se solicitado
    if args.auto_config:
        print("\n" + "="*70)
        print("GENERATING AUTO-CONFIGS")
        print("="*70 + "\n")
        
        configs = registry.export_configs()
        
        print(f"✅ Generated {len(configs)} auto-configurations")
        print(f"   Saved to: config/auto_generated_configs.json")
        
        print("\nTo integrate these configs:")
        print("1. Review auto_generated_configs.json")
        print("2. Merge selected configs into datasets_config.json")
        print("3. Run download pipeline with new configs")
    
    print("\n" + "="*70)
    print("REGISTRY SUMMARY")
    print("="*70)
    print(f"Total datasets: {len(all_datasets)}")
    print(f"Newly registered: {registered_count}")
    print(f"Registry file: {registry.registry_path}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

