"""Script para validar todos os datasets baixados."""
import sys
from pathlib import Path
import logging
import json
from collections import defaultdict

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.dataset_registry import DatasetRegistry

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Validar todos os datasets"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validar todos os datasets baixados')
    parser.add_argument('--update-registry', action='store_true',
                       help='Atualizar status no registry após validação')
    parser.add_argument('--output', default='data/registry/validation_report.json',
                       help='Arquivo de saída para relatório')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("DATASET VALIDATION")
    print("="*70 + "\n")
    
    registry = DatasetRegistry()
    raw_data_dir = Path('data/raw')
    
    validation_results = {
        'valid': [],
        'invalid': [],
        'warnings': [],
        'statistics': defaultdict(int)
    }
    
    # Encontrar todos os datasets baixados
    if not raw_data_dir.exists():
        print("❌ No raw data directory found")
        return
    
    dataset_dirs = [d for d in raw_data_dir.iterdir() if d.is_dir()]
    
    if not dataset_dirs:
        print("❌ No datasets found in raw data directory")
        return
    
    print(f"Found {len(dataset_dirs)} dataset directories\n")
    
    # Validar cada dataset
    for dataset_dir in sorted(dataset_dirs):
        dataset_id = dataset_dir.name
        print(f"\n{'='*70}")
        print(f"Validating: {dataset_id}")
        print(f"{'='*70}")
        
        # Encontrar arquivos CSV
        csv_files = list(dataset_dir.glob('*.csv'))
        
        if not csv_files:
            print(f"  ⚠️  No CSV files found")
            validation_results['warnings'].append({
                'dataset_id': dataset_id,
                'issue': 'No CSV files found'
            })
            validation_results['statistics']['no_files'] += 1
            continue
        
        # Validar primeiro arquivo CSV encontrado
        csv_file = csv_files[0]
        print(f"  File: {csv_file.name}")
        
        validation = registry.validate_dataset_file(dataset_id, csv_file)
        
        # Exibir resultados
        if validation['valid']:
            print(f"  ✅ VALID")
            validation_results['valid'].append({
                'dataset_id': dataset_id,
                'file': str(csv_file),
                'info': validation['info']
            })
            validation_results['statistics']['valid'] += 1
            
            if args.update_registry:
                registry.update_dataset_status(dataset_id, 'validated', validation_info=validation['info'])
        else:
            print(f"  ❌ INVALID")
            print(f"     Errors: {validation['errors']}")
            validation_results['invalid'].append({
                'dataset_id': dataset_id,
                'file': str(csv_file),
                'errors': validation['errors'],
                'warnings': validation['warnings']
            })
            validation_results['statistics']['invalid'] += 1
            
            if args.update_registry:
                registry.update_dataset_status(dataset_id, 'validation_failed', errors=validation['errors'])
        
        if validation['warnings']:
            print(f"  ⚠️  Warnings: {validation['warnings']}")
            validation_results['warnings'].append({
                'dataset_id': dataset_id,
                'warnings': validation['warnings']
            })
            validation_results['statistics']['with_warnings'] += 1
        
        # Exibir informações
        if validation['info']:
            info = validation['info']
            print(f"  📊 Columns: {info.get('column_count', 0)}")
            print(f"  📊 Rows checked: {info.get('rows_checked', 0)}")
            print(f"  📊 File size: {info.get('file_size_mb', 0):.2f} MB")
    
    # Resumo final
    print("\n" + "="*70)
    print("VALIDATION SUMMARY")
    print("="*70)
    print(f"Total datasets: {len(dataset_dirs)}")
    print(f"✅ Valid: {validation_results['statistics']['valid']}")
    print(f"❌ Invalid: {validation_results['statistics']['invalid']}")
    print(f"⚠️  With warnings: {validation_results['statistics']['with_warnings']}")
    print(f"📁 No files: {validation_results['statistics']['no_files']}")
    print("="*70 + "\n")
    
    # Salvar relatório
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(validation_results, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Validation report saved to: {output_path}")

if __name__ == "__main__":
    main()

