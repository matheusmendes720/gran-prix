"""Script com visualização em tempo real, logs e barras de progresso."""
import sys
from pathlib import Path
import logging
import json
import time
from datetime import datetime
from typing import Dict, List
import threading
from queue import Queue

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.enhance_dataset_search import DatasetSearcher
from src.utils.dataset_registry import DatasetRegistry
from src.pipeline.download_datasets import DatasetDownloader
from src.pipeline.scrapy_integration import ScrapyIntegration

# Configurar logging com formato colorido
class ColoredFormatter(logging.Formatter):
    """Formatter com cores para logs"""
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)
if logger.handlers:
    handler = logger.handlers[0]
    handler.setFormatter(ColoredFormatter('%(asctime)s | %(levelname)s | %(message)s'))
else:
    handler = logging.StreamHandler()
    handler.setFormatter(ColoredFormatter('%(asctime)s | %(levelname)s | %(message)s'))
    logger.addHandler(handler)

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("[WARN] tqdm not available. Install with: pip install tqdm")

class LiveProgressTracker:
    """Rastreamento de progresso em tempo real"""
    
    def __init__(self):
        self.current_step = ""
        self.step_progress = 0
        self.step_total = 0
        self.overall_progress = 0
        self.overall_total = 0
        self.start_time = time.time()
        self.status_queue = Queue()
        
    def update_step(self, step_name: str, progress: int = 0, total: int = 0):
        """Atualizar etapa atual"""
        self.current_step = step_name
        self.step_progress = progress
        self.step_total = total
        
    def update_overall(self, progress: int, total: int):
        """Atualizar progresso geral"""
        self.overall_progress = progress
        self.overall_total = total
    
    def get_elapsed_time(self) -> str:
        """Tempo decorrido"""
        elapsed = time.time() - self.start_time
        mins = int(elapsed // 60)
        secs = int(elapsed % 60)
        return f"{mins:02d}:{secs:02d}"
    
    def print_status(self):
        """Imprimir status atual"""
        elapsed = self.get_elapsed_time()
        
        print("\r" + " " * 100, end="")  # Limpar linha
        
        if self.step_total > 0:
            step_pct = (self.step_progress / self.step_total * 100) if self.step_total > 0 else 0
            print(f"\r[{elapsed}] {self.current_step}: {self.step_progress}/{self.step_total} ({step_pct:.1f}%) | Overall: {self.overall_progress}/{self.overall_total}", end="", flush=True)
        else:
            print(f"\r[{elapsed}] {self.current_step}...", end="", flush=True)

def print_banner():
    """Imprimir banner"""
    banner = """
    ================================================================================
          NOVA CORRENTE - DATASET FETCH PIPELINE
          Live Progress & Real-time Logs
    ================================================================================
    """
    print(banner)

def print_step_header(step_name: str, step_num: int, total_steps: int):
    """Imprimir cabeçalho de etapa"""
    print(f"\n{'='*80}")
    print(f"STEP {step_num}/{total_steps}: {step_name.upper()}")
    print(f"{'='*80}\n")

def fetch_with_progress():
    """Buscar datasets com progresso visual"""
    print_banner()
    
    tracker = LiveProgressTracker()
    
    results = {
        'discovery': {},
        'registration': {},
        'download': {},
        'validation': {}
    }
    
    # STEP 1: Discovery
    print_step_header("DISCOVERING DATASETS", 1, 4)
    tracker.update_step("Searching Zenodo...", 0, 0)
    
    searcher = DatasetSearcher()
    keywords = ['telecom', 'demand', 'forecast', 'brazil', 'mobile', 'broadband']
    
    discovered_datasets = {}
    
    for i, keyword in enumerate(keywords, 1):
        tracker.update_step(f"Searching '{keyword}'...", i, len(keywords))
        tracker.print_status()
        
        try:
            datasets = searcher.search_zenodo(keyword, max_results=5)
            if datasets:
                if 'zenodo' not in discovered_datasets:
                    discovered_datasets['zenodo'] = []
                discovered_datasets['zenodo'].extend(datasets)
                print(f"\n[OK] Found {len(datasets)} datasets for '{keyword}'")
        except Exception as e:
            print(f"\n[ERROR] Error searching '{keyword}': {e}")
    
    # Remover duplicatas
    seen_ids = set()
    unique_datasets = []
    if 'zenodo' in discovered_datasets:
        for ds in discovered_datasets['zenodo']:
            ds_id = ds.get('id', str(ds.get('url', '')))
            if ds_id not in seen_ids:
                seen_ids.add(ds_id)
                unique_datasets.append(ds)
        discovered_datasets['zenodo'] = unique_datasets
    
    total_discovered = sum(len(datasets) for datasets in discovered_datasets.values())
    print(f"\n[OK] Total discovered: {total_discovered} unique datasets")
    results['discovery'] = {'total': total_discovered}
    
    # STEP 2: Registration
    print_step_header("REGISTERING DATASETS", 2, 4)
    
    registry = DatasetRegistry()
    
    if discovered_datasets:
        tracker.update_step("Registering datasets...", 0, total_discovered)
        
        registered_count = 0
        for i, (source, datasets) in enumerate(discovered_datasets.items(), 1):
            tracker.update_step(f"Registering {source} datasets...", i, len(discovered_datasets))
            tracker.print_status()
            
            count = registry.discover_and_register({source: datasets})
            registered_count += count
        
        print(f"\n[OK] Registered {registered_count} new datasets")
        results['registration'] = {'registered': registered_count}
    
    # STEP 3: Download
    print_step_header("DOWNLOADING DATASETS", 3, 4)
    
    datasets_to_download = registry.list_datasets(status='discovered')
    max_datasets = min(15, len(datasets_to_download))
    datasets_to_download = datasets_to_download[:max_datasets]
    
    print(f"[INFO] Downloading {max_datasets} datasets...\n")
    
    downloader = DatasetDownloader()
    scrapy_integration = ScrapyIntegration()
    
    download_results = {}
    download_stats = {'success': 0, 'failed': 0, 'skipped': 0}
    
    if HAS_TQDM:
        pbar = tqdm(total=max_datasets, desc="Downloading", unit="dataset", ncols=100, colour='green')
    else:
        tracker.update_step("Downloading...", 0, max_datasets)
    
    for i, dataset in enumerate(datasets_to_download, 1):
        dataset_id = dataset['id']
        source = dataset.get('source', 'unknown')
        url = dataset.get('url', '')
        
        if HAS_TQDM:
            pbar.set_description(f"Downloading {dataset_id[:30]}...")
        else:
            tracker.update_step(f"Downloading {dataset_id}...", i, max_datasets)
            tracker.print_status()
        
        if not url:
            if HAS_TQDM:
                pbar.write(f"[WARN] {dataset_id}: No URL found")
            else:
                print(f"\n[WARN] {dataset_id}: No URL found")
            download_stats['failed'] += 1
            download_results[dataset_id] = False
            if HAS_TQDM:
                pbar.update(1)
            continue
        
        # Verificar se já existe
        raw_dir = Path('data/raw') / dataset_id
        if raw_dir.exists() and any(raw_dir.iterdir()):
            if HAS_TQDM:
                pbar.write(f"[SKIP] {dataset_id}: Already downloaded")
            else:
                print(f"\n[SKIP] {dataset_id}: Already downloaded")
            download_stats['skipped'] += 1
            download_results[dataset_id] = True
            if HAS_TQDM:
                pbar.update(1)
            continue
        
        try:
            # Tentar download
            if source in ['anatel', 'internet_aberta', 'springer', 'github']:
                success = scrapy_integration.run_scrapy_spider(dataset_id, {
                    'name': dataset.get('title', dataset_id),
                    'source': source,
                    'url': url,
                    'download_method': 'scrape'
                })
            else:
                results_dict = downloader.download_all_datasets(selected_datasets=[dataset_id])
                success = results_dict.get(dataset_id, False)
            
            if success:
                registry.update_dataset_status(dataset_id, 'downloaded')
                if HAS_TQDM:
                    pbar.write(f"[OK] {dataset_id}: Download successful")
                else:
                    print(f"\n[OK] {dataset_id}: Download successful")
                download_stats['success'] += 1
            else:
                registry.update_dataset_status(dataset_id, 'download_failed')
                if HAS_TQDM:
                    pbar.write(f"[FAIL] {dataset_id}: Download failed")
                else:
                    print(f"\n[FAIL] {dataset_id}: Download failed")
                download_stats['failed'] += 1
            
            download_results[dataset_id] = success
            
        except Exception as e:
            logger.error(f"Error downloading {dataset_id}: {e}")
            download_stats['failed'] += 1
            download_results[dataset_id] = False
        
        if HAS_TQDM:
            pbar.update(1)
        else:
            tracker.print_status()
    
    if HAS_TQDM:
        pbar.close()
    
    results['download'] = {
        'total': max_datasets,
        **download_stats,
        'results': download_results
    }
    
    # STEP 4: Summary
    print_step_header("FINAL SUMMARY", 4, 4)
    
    elapsed = tracker.get_elapsed_time()
    
    print(f"\n{'='*80}")
    print(f"EXECUTION SUMMARY")
    print(f"{'='*80}")
    print(f"Total Time: {elapsed}")
    print(f"\nDiscovery:")
    print(f"  Datasets discovered: {results['discovery'].get('total', 0)}")
    print(f"\nRegistration:")
    print(f"  Datasets registered: {results['registration'].get('registered', 0)}")
    print(f"\nDownload:")
    print(f"  Success: {download_stats['success']}")
    print(f"  Failed: {download_stats['failed']}")
    print(f"  Skipped: {download_stats['skipped']}")
    print(f"{'='*80}\n")
    
    # Salvar resultados
    results_path = Path('data/registry/live_fetch_results.json')
    results_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Results saved to: {results_path}\n")
    
    return results

if __name__ == "__main__":
    try:
        fetch_with_progress()
    except KeyboardInterrupt:
        print("\n\n[WARN] Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)

