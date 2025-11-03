"""
Scrapy Pipelines para processar items
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from itemadapter import ItemAdapter
import sys
from pathlib import Path as PathLib

# Adicionar path para importar documentation_generator
sys.path.insert(0, str(PathLib(__file__).parent))

try:
    from documentation_generator import TechnicalDocsGenerator
    DOCS_GENERATOR_AVAILABLE = True
except ImportError:
    logger = logging.getLogger(__name__)
    logger.warning("TechnicalDocsGenerator not available - docs will not be auto-generated")
    DOCS_GENERATOR_AVAILABLE = False

logger = logging.getLogger(__name__)

class DatasetMetadataPipeline:
    """Pipeline para salvar metadados dos datasets baixados"""
    
    def __init__(self):
        self.metadata_file = Path('data/raw/download_metadata.json')
        self.metadata = {}
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
    
    def process_item(self, item, spider):
        """Processar item e adicionar metadados"""
        adapter = ItemAdapter(item)
        
        dataset_id = adapter.get('dataset_id', 'unknown')
        if dataset_id not in self.metadata:
            self.metadata[dataset_id] = []
        
        item_data = {
            'file_path': adapter.get('file_path'),
            'url': adapter.get('url'),
            'filename': adapter.get('filename'),
            'size': adapter.get('size'),
            'file_type': adapter.get('file_type'),
            'download_date': datetime.now().isoformat(),
            'spider': spider.name
        }
        
        # Adicionar campos específicos
        if 'record_id' in adapter:
            item_data['record_id'] = adapter.get('record_id')
        if 'repository_url' in adapter:
            item_data['repository_url'] = adapter.get('repository_url')
        
        self.metadata[dataset_id].append(item_data)
        
        # Salvar metadata
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        
        return item


class TechnicalDocsPipeline:
    """
    Pipeline que gera automaticamente documentação técnica rica em contexto
    quando um novo dataset é baixado
    """
    
    def __init__(self):
        if DOCS_GENERATOR_AVAILABLE:
            try:
                self.docs_generator = TechnicalDocsGenerator()
                self.enabled = True
            except Exception as e:
                logger.error(f"Failed to initialize TechnicalDocsGenerator: {e}")
                self.enabled = False
        else:
            self.enabled = False
            logger.warning("TechnicalDocsGenerator not available - docs generation disabled")
        
        self.generated_docs = []
    
    def process_item(self, item, spider):
        """Processa item e gera documentação técnica completa"""
        if not self.enabled:
            return item
        
        adapter = ItemAdapter(item)
        
        dataset_id = adapter.get('dataset_id', 'unknown')
        file_path = adapter.get('file_path')
        
        if not file_path:
            return item
        
        dataset_dir = Path(file_path).parent
        
        # Preparar metadata rica do item
        metadata = {
            'url': adapter.get('url'),
            'filename': adapter.get('filename'),
            'size': adapter.get('size'),
            'download_date': adapter.get('download_date', datetime.now().isoformat()),
            'status': '✅ Processed & Ready for ML',
            'pending_parsing': False
        }
        
        # Adicionar source-specific metadata
        if hasattr(spider, 'source'):
            metadata['source'] = spider.source
        elif hasattr(spider, 'name'):
            # Tentar inferir source do spider name
            spider_name = spider.name.lower()
            if 'anatel' in spider_name:
                metadata['source'] = 'anatel'
            elif 'zenodo' in spider_name:
                metadata['source'] = 'zenodo'
            elif 'github' in spider_name:
                metadata['source'] = 'github'
            elif 'bacen' in spider_name:
                metadata['source'] = 'bacen'
            elif 'ibge' in spider_name:
                metadata['source'] = 'ibge'
            elif 'inmet' in spider_name:
                metadata['source'] = 'inmet'
        
        if hasattr(spider, 'record_id'):
            metadata['record_id'] = spider.record_id
            metadata['doi'] = f"10.5281/zenodo.{spider.record_id}"
        
        if hasattr(spider, 'kaggle_dataset'):
            metadata['kaggle_dataset'] = spider.kaggle_dataset
        
        # Adicionar metadata do dataset baixado
        if 'record_title' in adapter:
            metadata['title'] = adapter.get('record_title')
        if 'record_doi' in adapter:
            metadata['doi'] = adapter.get('record_doi')
        if 'series_code' in adapter:
            metadata['series_code'] = adapter.get('series_code')
        if 'series_name' in adapter:
            metadata['series_name'] = adapter.get('series_name')
        if 'region' in adapter:
            metadata['region'] = adapter.get('region')
        if 'station_code' in adapter:
            metadata['station_code'] = adapter.get('station_code')
        
        # Gerar documentação técnica completa
        try:
            docs_path = self.docs_generator.generate_docs(
                dataset_id=dataset_id,
                dataset_dir=dataset_dir,
                metadata=metadata
            )
            
            self.generated_docs.append({
                'dataset_id': dataset_id,
                'docs_path': str(docs_path),
                'generated_at': datetime.now().isoformat()
            })
            
            logger.info(f"✅ Generated comprehensive technical docs for {dataset_id}: {docs_path.name}")
            
        except Exception as e:
            logger.error(f"❌ Error generating docs for {dataset_id}: {e}")
            import traceback
            logger.debug(traceback.format_exc())
        
        return item
    
    def close_spider(self, spider):
        """Salva registro de documentação gerada"""
        if self.generated_docs:
            registry_file = Path('data/raw/generated_docs_registry.json')
            registry = []
            
            if registry_file.exists():
                with open(registry_file, 'r', encoding='utf-8') as f:
                    registry = json.load(f)
            
            registry.extend(self.generated_docs)
            
            with open(registry_file, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📝 Registered {len(self.generated_docs)} generated documentation files")

class ValidateFilePipeline:
    """Pipeline para validar arquivos baixados"""
    
    def process_item(self, item, spider):
        """Validar arquivo baixado"""
        adapter = ItemAdapter(item)
        file_path = adapter.get('file_path')
        
        if file_path:
            path = Path(file_path)
            if not path.exists():
                logger.warning(f"File not found after download: {file_path}")
                return None
            
            # Verificar tamanho
            size = adapter.get('size', 0)
            actual_size = path.stat().st_size
            
            if actual_size != size:
                logger.warning(f"Size mismatch: expected {size}, got {actual_size} for {file_path}")
            
            # Verificar extensão esperada
            file_type = adapter.get('file_type', '')
            if file_type and not path.suffix.endswith(f'.{file_type}'):
                logger.warning(f"File type mismatch: expected {file_type}, got {path.suffix} for {file_path}")
        
        return item


