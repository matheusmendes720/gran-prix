"""Script rápido para verificar status do registry."""
import sys
from pathlib import Path
import json
from collections import defaultdict

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    # Verificar registry
    reg_path = Path('data/registry/datasets_registry.json')
    if reg_path.exists():
        with open(reg_path, 'r', encoding='utf-8') as f:
            reg = json.load(f)
        datasets = reg.get('datasets', {})
        
        print(f"\n=== REGISTRY STATUS ===")
        print(f"Total datasets: {len(datasets)}")
        
        # Por status
        status_counts = defaultdict(int)
        for ds in datasets.values():
            status = ds.get('status', 'unknown')
            status_counts[status] += 1
        
        print("\nBy Status:")
        for status, count in sorted(status_counts.items()):
            print(f"  {status}: {count}")
        
        # Por fonte
        source_counts = defaultdict(int)
        for ds in datasets.values():
            source = ds.get('source', 'unknown')
            source_counts[source] += 1
        
        print("\nBy Source:")
        for source, count in sorted(source_counts.items()):
            print(f"  {source}: {count}")
    
    # Verificar datasets baixados
    raw = Path('data/raw')
    if raw.exists():
        dirs = [d for d in raw.iterdir() if d.is_dir()]
        print(f"\nRaw datasets downloaded: {len(dirs)}")
        
        # Contar arquivos
        total_files = 0
        total_size = 0
        for d in dirs:
            files = list(d.rglob('*'))
            files = [f for f in files if f.is_file()]
            total_files += len(files)
            total_size += sum(f.stat().st_size for f in files)
        
        print(f"Total files: {total_files}")
        print(f"Total size: {total_size / (1024*1024):.2f} MB")
    
    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()

