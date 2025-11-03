"""
Dashboard de Status do Sistema
Visualiza status de datasets, pipeline e componentes do sistema
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class SystemStatusDashboard:
    """Dashboard de status do sistema"""
    
    def __init__(self, registry_path: str = 'data/registry/datasets_registry.json'):
        self.registry_path = Path(registry_path)
        self.raw_data_dir = Path('data/raw')
        self.processed_data_dir = Path('data/processed')
    
    def generate_status_report(self) -> Dict:
        """Gerar relatório completo de status"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'datasets': self._get_datasets_status(),
            'pipeline': self._get_pipeline_status(),
            'storage': self._get_storage_status(),
            'system_health': self._get_system_health(),
        }
        
        return report
    
    def _get_datasets_status(self) -> Dict:
        """Status dos datasets"""
        status = {
            'total_registered': 0,
            'by_status': defaultdict(int),
            'by_source': defaultdict(int),
            'download_status': {
                'downloaded': 0,
                'not_downloaded': 0,
                'failed': 0,
            },
            'validation_status': {
                'valid': 0,
                'invalid': 0,
                'not_validated': 0,
            }
        }
        
        # Ler registry se existir
        if self.registry_path.exists():
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            
            datasets = registry.get('datasets', {})
            status['total_registered'] = len(datasets)
            
            for dataset_id, dataset_info in datasets.items():
                # Por status
                ds_status = dataset_info.get('status', 'unknown')
                status['by_status'][ds_status] += 1
                
                # Por fonte
                source = dataset_info.get('source', 'unknown')
                status['by_source'][source] += 1
                
                # Download status
                if ds_status == 'downloaded':
                    status['download_status']['downloaded'] += 1
                elif ds_status == 'download_failed':
                    status['download_status']['failed'] += 1
                else:
                    status['download_status']['not_downloaded'] += 1
                
                # Validation status
                if ds_status == 'validated':
                    status['validation_status']['valid'] += 1
                elif ds_status == 'validation_failed':
                    status['validation_status']['invalid'] += 1
                else:
                    status['validation_status']['not_validated'] += 1
        
        return status
    
    def _get_pipeline_status(self) -> Dict:
        """Status do pipeline"""
        status = {
            'download': {
                'ready': True,
                'datasets_available': 0,
            },
            'preprocess': {
                'ready': False,
                'datasets_preprocessed': 0,
                'datasets_pending': 0,
            },
            'merge': {
                'ready': False,
                'unified_dataset_exists': False,
            },
            'external_factors': {
                'ready': False,
                'enriched_dataset_exists': False,
            },
        }
        
        # Contar datasets baixados
        if self.raw_data_dir.exists():
            dataset_dirs = [d for d in self.raw_data_dir.iterdir() if d.is_dir()]
            status['download']['datasets_available'] = len(dataset_dirs)
        
        # Contar datasets preprocessados
        if self.processed_data_dir.exists():
            preprocessed_files = list(self.processed_data_dir.glob("*_preprocessed.csv"))
            status['preprocess']['datasets_preprocessed'] = len(preprocessed_files)
            
            if self.raw_data_dir.exists():
                total_raw = len([d for d in self.raw_data_dir.iterdir() if d.is_dir()])
                status['preprocess']['datasets_pending'] = total_raw - len(preprocessed_files)
            
            status['preprocess']['ready'] = status['preprocess']['datasets_preprocessed'] > 0
        
        # Verificar dataset unificado
        unified_path = self.processed_data_dir / 'unified_dataset.csv'
        if unified_path.exists():
            status['merge']['unified_dataset_exists'] = True
            status['merge']['ready'] = True
        
        # Verificar dataset enriquecido
        enriched_path = self.processed_data_dir / 'unified_dataset_with_factors.csv'
        if enriched_path.exists():
            status['external_factors']['enriched_dataset_exists'] = True
            status['external_factors']['ready'] = True
        
        return status
    
    def _get_storage_status(self) -> Dict:
        """Status de armazenamento"""
        status = {
            'raw_data_size_mb': 0,
            'processed_data_size_mb': 0,
            'total_size_mb': 0,
            'datasets_count': {
                'raw': 0,
                'processed': 0,
            }
        }
        
        # Calcular tamanho de dados brutos
        if self.raw_data_dir.exists():
            for file_path in self.raw_data_dir.rglob('*'):
                if file_path.is_file():
                    status['raw_data_size_mb'] += file_path.stat().st_size / (1024 * 1024)
            
            dataset_dirs = [d for d in self.raw_data_dir.iterdir() if d.is_dir()]
            status['datasets_count']['raw'] = len(dataset_dirs)
        
        # Calcular tamanho de dados processados
        if self.processed_data_dir.exists():
            for file_path in self.processed_data_dir.glob('*.csv'):
                if file_path.is_file():
                    status['processed_data_size_mb'] += file_path.stat().st_size / (1024 * 1024)
            
            processed_files = list(self.processed_data_dir.glob("*_preprocessed.csv"))
            status['datasets_count']['processed'] = len(processed_files)
        
        status['total_size_mb'] = status['raw_data_size_mb'] + status['processed_data_size_mb']
        
        return status
    
    def _get_system_health(self) -> Dict:
        """Health check do sistema"""
        health = {
            'overall': 'unknown',
            'components': {},
            'warnings': [],
            'errors': [],
        }
        
        # Verificar componentes
        components = {
            'registry': self.registry_path.exists(),
            'raw_data_dir': self.raw_data_dir.exists(),
            'processed_data_dir': self.processed_data_dir.exists(),
            'config_file': Path('config/datasets_config.json').exists(),
        }
        
        health['components'] = components
        
        # Verificar warnings
        if not self.registry_path.exists():
            health['warnings'].append('Registry file not found')
        
        if not self.raw_data_dir.exists():
            health['warnings'].append('Raw data directory not found')
        
        # Calcular health geral
        all_ok = all(components.values())
        some_ok = any(components.values())
        
        if all_ok:
            health['overall'] = 'healthy'
        elif some_ok:
            health['overall'] = 'degraded'
        else:
            health['overall'] = 'unhealthy'
        
        return health
    
    def print_dashboard(self):
        """Imprimir dashboard no terminal"""
        report = self.generate_status_report()
        
        print("\n" + "="*80)
        print("SYSTEM STATUS DASHBOARD")
        print("="*80)
        print(f"Timestamp: {report['timestamp']}")
        
        # Datasets Status
        print("\n" + "-"*80)
        print("DATASETS STATUS")
        print("-"*80)
        ds_status = report['datasets']
        print(f"Total Registered: {ds_status['total_registered']}")
        
        print("\nBy Status:")
        for status_name, count in sorted(ds_status['by_status'].items()):
            print(f"  {status_name}: {count}")
        
        print("\nBy Source:")
        for source, count in sorted(ds_status['by_source'].items()):
            print(f"  {source}: {count}")
        
        print("\nDownload Status:")
        dl_status = ds_status['download_status']
        print(f"  Downloaded: {dl_status['downloaded']}")
        print(f"  Not Downloaded: {dl_status['not_downloaded']}")
        print(f"  Failed: {dl_status['failed']}")
        
        # Pipeline Status
        print("\n" + "-"*80)
        print("PIPELINE STATUS")
        print("-"*80)
        pipeline = report['pipeline']
        
        print(f"Download: {'OK' if pipeline['download']['ready'] else 'NO'} ({pipeline['download']['datasets_available']} datasets)")
        print(f"Preprocess: {'OK' if pipeline['preprocess']['ready'] else 'NO'} ({pipeline['preprocess']['datasets_preprocessed']} preprocessed, {pipeline['preprocess']['datasets_pending']} pending)")
        print(f"Merge: {'OK' if pipeline['merge']['ready'] else 'NO'} ({'Unified dataset exists' if pipeline['merge']['unified_dataset_exists'] else 'Not created'})")
        print(f"External Factors: {'OK' if pipeline['external_factors']['ready'] else 'NO'} ({'Enriched dataset exists' if pipeline['external_factors']['enriched_dataset_exists'] else 'Not created'})")
        
        # Storage Status
        print("\n" + "-"*80)
        print("STORAGE STATUS")
        print("-"*80)
        storage = report['storage']
        print(f"Raw Data: {storage['raw_data_size_mb']:.2f} MB ({storage['datasets_count']['raw']} datasets)")
        print(f"Processed Data: {storage['processed_data_size_mb']:.2f} MB ({storage['datasets_count']['processed']} datasets)")
        print(f"Total: {storage['total_size_mb']:.2f} MB")
        
        # System Health
        print("\n" + "-"*80)
        print("SYSTEM HEALTH")
        print("-"*80)
        health = report['system_health']
        print(f"Overall: {health['overall'].upper()}")
        
        print("\nComponents:")
        for component, status in health['components'].items():
            print(f"  {component}: {'OK' if status else 'NO'}")
        
        if health['warnings']:
            print("\nWarnings:")
            for warning in health['warnings']:
                print(f"  ⚠ {warning}")
        
        print("\n" + "="*80 + "\n")
    
    def save_report(self, output_path: Optional[Path] = None):
        """Salvar relatório em JSON"""
        if output_path is None:
            output_path = Path('data/registry/system_status.json')
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = self.generate_status_report()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Status report saved to: {output_path}")

