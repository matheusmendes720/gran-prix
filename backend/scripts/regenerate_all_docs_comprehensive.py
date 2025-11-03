"""
Regenera toda a documentação técnica com contexto profundo e completo
para todos os datasets em datasets_config.json
"""
import json
import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.pipelines.data_ingestion.scrapy_spiders.documentation_generator import TechnicalDocsGenerator
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def regenerate_all_docs_comprehensive():
    """Regenera documentação completa para todos os datasets"""
    config_path = Path('config/datasets_config.json')
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    docs_generator = TechnicalDocsGenerator()
    datasets = config.get('datasets', {})
    
    print("\n" + "="*80)
    print("REGENERATING COMPREHENSIVE TECHNICAL DOCUMENTATION")
    print("="*80)
    print(f"\nProcessing {len(datasets)} datasets...\n")
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    
    for dataset_id, dataset_config in datasets.items():
        dataset_dir = Path('data/raw') / dataset_id
        
        if not dataset_dir.exists():
            print(f"⚠️  SKIPPED: {dataset_id} - directory not found")
            skipped_count += 1
            continue
        
        try:
            # Preparar metadata rica
            metadata = {
                'url': dataset_config.get('url', ''),
                'source': dataset_config.get('source', 'unknown'),
                'status': '✅ Processed & Ready for ML',
                'relevance': dataset_config.get('relevance', '⭐⭐⭐')
            }
            
            # Adicionar source-specific metadata
            source = dataset_config.get('source', '')
            if source == 'zenodo':
                # Tentar extrair record_id da URL
                url = dataset_config.get('url', '')
                if url and '/records/' in url:
                    try:
                        record_id = url.split('/records/')[1].split('/')[0]
                        metadata['record_id'] = record_id
                        metadata['doi'] = f"10.5281/zenodo.{record_id}"
                    except:
                        pass
            
            if source == 'kaggle' and 'dataset' in dataset_config:
                metadata['kaggle_dataset'] = dataset_config['dataset']
            
            if 'series_code' in dataset_config:
                metadata['series_code'] = dataset_config['series_code']
            
            if 'table_id' in dataset_config:
                metadata['table_id'] = dataset_config['table_id']
            
            if 'region' in dataset_config:
                metadata['region'] = dataset_config['region']
            
            # Gerar documentação completa
            docs_path = docs_generator.generate_docs(
                dataset_id=dataset_id,
                dataset_dir=dataset_dir,
                metadata=metadata
            )
            
            print(f"✅ REGENERATED: {dataset_id}")
            print(f"   📄 {docs_path.name}")
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ ERROR: {dataset_id}")
            print(f"   {str(e)}")
            logger.error(f"Error regenerating {dataset_id}: {e}", exc_info=True)
            error_count += 1
    
    print("\n" + "="*80)
    print("REGENERATION SUMMARY")
    print("="*80)
    print(f"✅ Success: {success_count}")
    print(f"❌ Errors: {error_count}")
    print(f"⚠️  Skipped: {skipped_count}")
    print(f"📊 Total: {len(datasets)}")
    print("="*80 + "\n")
    
    if success_count > 0:
        print(f"✅ Successfully regenerated comprehensive docs for {success_count} datasets!")
        print(f"📁 Documentation files located in: data/raw/[dataset_id]/")
        print(f"\n💡 Each documentation includes:")
        print(f"   - Deep technical context")
        print(f"   - Academic references")
        print(f"   - Business use cases")
        print(f"   - ML algorithm recommendations")
        print(f"   - Case studies")
        print(f"   - Preprocessing notes")


if __name__ == '__main__':
    regenerate_all_docs_comprehensive()

