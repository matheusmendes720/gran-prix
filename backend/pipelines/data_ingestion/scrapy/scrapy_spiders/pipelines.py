"""
Scrapy Pipelines para processar items
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from itemadapter import ItemAdapter

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


