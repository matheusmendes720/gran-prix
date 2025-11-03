"""Script para buscar todos os datasets usando Scrapy."""
import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline.scrapy_integration import ScrapyIntegration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Buscar todos os datasets que requerem scraping"""
    print("\n" + "="*70)
    print("FETCHING ALL DATASETS WITH SCRAPY")
    print("="*70 + "\n")
    
    integration = ScrapyIntegration()
    results = integration.run_all_scrapy_datasets()
    
    print("\n" + "="*70)
    print("DOWNLOAD SUMMARY")
    print("="*70)
    
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"Successful: {successful}/{total}")
    
    for dataset_id, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {status}: {dataset_id}")
    
    print("="*70 + "\n")
    
    return results

if __name__ == "__main__":
    main()


