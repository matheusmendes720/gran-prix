"""
Sistema de Registro Unificado de Datasets
Gerencia descoberta, validação e configuração automática de datasets
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd

logger = logging.getLogger(__name__)

class DatasetRegistry:
    """Registro centralizado de todos os datasets do projeto"""
    
    def __init__(self, registry_path: str = 'data/registry/datasets_registry.json'):
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Carregar registro existente"""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading registry: {e}")
                return {'datasets': {}, 'metadata': {'version': '1.0', 'last_updated': None}}
        
        return {
            'datasets': {},
            'metadata': {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'last_updated': None
            }
        }
    
    def _save_registry(self):
        """Salvar registro"""
        self.registry['metadata']['last_updated'] = datetime.now().isoformat()
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)
    
    def register_dataset(self, dataset_id: str, dataset_info: Dict, source: str = 'unknown') -> bool:
        """Registrar novo dataset"""
        try:
            if dataset_id not in self.registry['datasets']:
                self.registry['datasets'][dataset_id] = {
                    'id': dataset_id,
                    'registered_at': datetime.now().isoformat(),
                    'source': source,
                    'status': 'discovered',
                    **dataset_info
                }
            else:
                # Atualizar informações existentes
                self.registry['datasets'][dataset_id].update({
                    'last_updated': datetime.now().isoformat(),
                    **dataset_info
                })
            
            self._save_registry()
            logger.info(f"Dataset {dataset_id} registered successfully")
            return True
        except Exception as e:
            logger.error(f"Error registering dataset {dataset_id}: {e}")
            return False
    
    def update_dataset_status(self, dataset_id: str, status: str, **kwargs):
        """Atualizar status do dataset"""
        if dataset_id in self.registry['datasets']:
            self.registry['datasets'][dataset_id]['status'] = status
            self.registry['datasets'][dataset_id]['last_updated'] = datetime.now().isoformat()
            
            for key, value in kwargs.items():
                self.registry['datasets'][dataset_id][key] = value
            
            self._save_registry()
            logger.info(f"Dataset {dataset_id} status updated to: {status}")
        else:
            logger.warning(f"Dataset {dataset_id} not found in registry")
    
    def get_dataset(self, dataset_id: str) -> Optional[Dict]:
        """Obter informações de um dataset"""
        return self.registry['datasets'].get(dataset_id)
    
    def list_datasets(self, status: Optional[str] = None, source: Optional[str] = None) -> List[Dict]:
        """Listar datasets com filtros opcionais"""
        datasets = list(self.registry['datasets'].values())
        
        if status:
            datasets = [d for d in datasets if d.get('status') == status]
        
        if source:
            datasets = [d for d in datasets if d.get('source') == source]
        
        return sorted(datasets, key=lambda x: x.get('registered_at', ''), reverse=True)
    
    def discover_and_register(self, discovered_datasets: Dict[str, List[Dict]]):
        """Registrar datasets descobertos automaticamente"""
        registered_count = 0
        
        for source, datasets in discovered_datasets.items():
            for dataset in datasets:
                # Gerar ID único baseado na fonte e título/URL
                dataset_id = self._generate_dataset_id(dataset, source)
                
                # Preparar informações do dataset
                dataset_info = {
                    'title': dataset.get('title') or dataset.get('name') or dataset.get('full_name', 'Unknown'),
                    'url': dataset.get('url', ''),
                    'description': dataset.get('description', ''),
                    'keywords': dataset.get('keywords', []),
                    'publication_date': dataset.get('publication_date') or dataset.get('updated_at', ''),
                }
                
                # Adicionar informações específicas da fonte
                if source == 'zenodo':
                    dataset_info['doi'] = dataset.get('doi', '')
                    dataset_info['zenodo_id'] = dataset.get('id', '')
                    dataset_info['csv_file'] = dataset.get('csv_file', '')
                elif source == 'github':
                    dataset_info['github_repo'] = dataset.get('full_name', '')
                    dataset_info['stars'] = dataset.get('stars', 0)
                elif source == 'kaggle':
                    dataset_info['kaggle_ref'] = dataset.get('ref', '')
                    dataset_info['download_count'] = dataset.get('download_count', 0)
                
                if self.register_dataset(dataset_id, dataset_info, source=source):
                    registered_count += 1
        
        logger.info(f"Registered {registered_count} new datasets")
        return registered_count
    
    def _generate_dataset_id(self, dataset: Dict, source: str) -> str:
        """Gerar ID único para dataset"""
        if source == 'zenodo':
            return f"zenodo_{dataset.get('id', 'unknown')}"
        elif source == 'github':
            full_name = dataset.get('full_name', '')
            return f"github_{full_name.replace('/', '_')}"
        elif source == 'kaggle':
            ref = dataset.get('ref', '').replace('/', '_')
            return f"kaggle_{ref}"
        elif source == 'anatel':
            title = dataset.get('title', 'unknown').lower().replace(' ', '_')
            return f"anatel_{title[:50]}"
        else:
            # ID genérico baseado em título
            title = str(dataset.get('title') or dataset.get('name') or 'unknown').lower()
            title = ''.join(c if c.isalnum() or c in '_-' else '_' for c in title)
            return f"{source}_{title[:50]}"
    
    def validate_dataset_file(self, dataset_id: str, file_path: Path) -> Dict[str, Any]:
        """Validar arquivo de dataset"""
        validation_result = {
            'valid': False,
            'errors': [],
            'warnings': [],
            'info': {}
        }
        
        if not file_path.exists():
            validation_result['errors'].append(f"File not found: {file_path}")
            return validation_result
        
        try:
            # Tentar ler como CSV
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path, nrows=1000)  # Ler apenas primeiras 1000 linhas para validação
                
                validation_result['info'] = {
                    'rows_checked': min(1000, len(df)),
                    'columns': list(df.columns),
                    'column_count': len(df.columns),
                    'dtypes': df.dtypes.astype(str).to_dict(),
                    'missing_values': df.isnull().sum().to_dict(),
                    'file_size_mb': file_path.stat().st_size / (1024 * 1024)
                }
                
                # Verificações básicas
                if len(df.columns) == 0:
                    validation_result['errors'].append("No columns found")
                
                if len(df) == 0:
                    validation_result['errors'].append("No rows found")
                
                # Verificar colunas esperadas
                expected_cols = ['date', 'item_id', 'quantity']
                found_cols = [col.lower() for col in df.columns]
                
                missing_cols = []
                for expected in expected_cols:
                    if not any(expected in col.lower() for col in df.columns):
                        missing_cols.append(expected)
                
                if missing_cols:
                    validation_result['warnings'].append(f"Missing expected columns: {missing_cols}")
                
                # Verificar valores nulos críticos
                if 'date' in [c.lower() for c in df.columns]:
                    date_col = df.columns[[c.lower() == 'date' for c in df.columns]][0]
                    null_dates = df[date_col].isnull().sum()
                    if null_dates > len(df) * 0.1:  # Mais de 10% de datas nulas
                        validation_result['warnings'].append(f"High percentage of null dates: {null_dates}/{len(df)}")
                
                if not validation_result['errors']:
                    validation_result['valid'] = True
                    
        except pd.errors.EmptyDataError:
            validation_result['errors'].append("File is empty")
        except Exception as e:
            validation_result['errors'].append(f"Error reading file: {e}")
        
        return validation_result
    
    def auto_generate_config(self, dataset_id: str) -> Optional[Dict]:
        """Gerar configuração automática para dataset"""
        dataset_info = self.get_dataset(dataset_id)
        
        if not dataset_info:
            logger.warning(f"Dataset {dataset_id} not found in registry")
            return None
        
        file_path = Path(f"data/raw/{dataset_id}")
        
        # Procurar arquivo
        csv_files = list(file_path.glob('*.csv'))
        if not csv_files:
            logger.warning(f"No CSV file found for {dataset_id}")
            return None
        
        file_path = csv_files[0]
        
        # Validar arquivo
        validation = self.validate_dataset_file(dataset_id, file_path)
        
        if not validation['valid']:
            logger.error(f"Dataset {dataset_id} validation failed: {validation['errors']}")
            return None
        
        # Tentar inferir mapeamento de colunas
        df = pd.read_csv(file_path, nrows=10)
        columns = df.columns.tolist()
        
        column_mapping = {}
        
        # Inferir coluna de data
        date_candidates = [c for c in columns if any(word in c.lower() for word in ['date', 'time', 'timestamp', 'step'])]
        if date_candidates:
            column_mapping['date'] = date_candidates[0]
        
        # Inferir coluna de item
        item_candidates = [c for c in columns if any(word in c.lower() for word in ['item', 'product', 'sku', 'id'])]
        if item_candidates:
            column_mapping['item_id'] = item_candidates[0]
        
        # Inferir coluna de quantidade
        quantity_candidates = [c for c in columns if any(word in c.lower() for word in ['quantity', 'demand', 'order', 'count', 'total', 'value'])]
        if quantity_candidates:
            column_mapping['quantity'] = quantity_candidates[0]
        
        # Criar configuração
        config = {
            'name': dataset_info.get('title', dataset_id),
            'source': dataset_info.get('source', 'unknown'),
            'url': dataset_info.get('url', ''),
            'description': dataset_info.get('description', ''),
            'columns_mapping': column_mapping,
            'preprocessing_notes': f"Auto-generated from discovery. Validation: {validation['info']}"
        }
        
        logger.info(f"Auto-generated config for {dataset_id}")
        return config
    
    def export_configs(self, output_path: str = 'config/auto_generated_configs.json'):
        """Exportar configurações geradas automaticamente"""
        configs = {}
        
        for dataset_id in self.registry['datasets'].keys():
            config = self.auto_generate_config(dataset_id)
            if config:
                configs[dataset_id] = config
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(configs, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(configs)} auto-generated configs to {output_path}")
        return configs

