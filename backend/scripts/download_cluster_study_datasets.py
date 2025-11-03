"""
Download Cluster Study Datasets - Comprehensive download of all evaluated datasets
Downloads datasets from cluster study evaluation, organized by tier
"""
import sys
from pathlib import Path
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.pipelines.data_processing.download_datasets import DatasetDownloader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_tier_config(tier: str) -> Dict:
    """Load tier configuration from cluster study"""
    tier_config_path = project_root / 'docs' / 'documentation' / 'cluster_study' / 'datasets_config' / f'{tier}_config.json'
    
    if not tier_config_path.exists():
        logger.warning(f"Tier config not found: {tier_config_path}")
        return {}
        
    with open(tier_config_path, 'r', encoding='utf-8') as f:
        tier_config = json.load(f)
        
    return tier_config.get('datasets', {})


def download_tier_datasets(tier: str, tier_config: Dict, downloader: DatasetDownloader, output_base: Path):
    """Download all datasets for a tier"""
    logger.info(f"\n{'='*80}")
    logger.info(f"Downloading {tier.replace('_', ' ').title()} Datasets")
    logger.info(f"{'='*80}")
    
    tier_output = output_base / tier
    tier_output.mkdir(parents=True, exist_ok=True)
    
    downloaded = []
    failed = []
    skipped = []
    
    for dataset_id, dataset_info in tier_config.items():
        logger.info(f"\nProcessing: {dataset_id}")
        logger.info(f"  Name: {dataset_info.get('name', 'N/A')}")
        logger.info(f"  Source: {dataset_info.get('source', 'unknown')}")
        
        # Check if already downloaded
        raw_dir = project_root / 'data' / 'raw' / dataset_id
        if raw_dir.exists() and any(raw_dir.iterdir()):
            logger.info(f"  [SKIP] Already downloaded: {dataset_id}")
            skipped.append(dataset_id)
            continue
        
        try:
            # Use the main downloader - call download_all_datasets with single dataset
            # First, add this dataset to the config temporarily
            original_config = downloader.config.get('datasets', {})
            downloader.config['datasets'] = {dataset_id: dataset_info}
            
            # Download using the main downloader
            results = downloader.download_all_datasets(selected_datasets=[dataset_id])
            success = results.get(dataset_id, False)
            
            # Restore original config
            downloader.config['datasets'] = original_config
            
            if success:
                downloaded.append(dataset_id)
                logger.info(f"  [OK] Downloaded: {dataset_id}")
            else:
                failed.append(dataset_id)
                logger.warning(f"  [FAILED] Failed: {dataset_id}")
                
        except Exception as e:
            failed.append(dataset_id)
            logger.error(f"  ✗ Error downloading {dataset_id}: {e}")
    
    # Save download summary
    summary = {
        'tier': tier,
        'download_date': datetime.now().isoformat(),
        'total_datasets': len(tier_config),
        'downloaded': len(downloaded),
        'failed': len(failed),
        'skipped': len(skipped),
        'downloaded_datasets': downloaded,
        'failed_datasets': failed,
        'skipped_datasets': skipped
    }
    
    summary_path = tier_output / f'{tier}_download_summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    logger.info(f"\n[OK] Download summary saved: {summary_path}")
    
    logger.info(f"\n{tier.replace('_', ' ').title()} Download Summary:")
    logger.info(f"  Total: {len(tier_config)}")
    logger.info(f"  Downloaded: {len(downloaded)}")
    logger.info(f"  Skipped: {len(skipped)}")
    logger.info(f"  Failed: {len(failed)}")
    
    return summary


def main():
    """Main execution - Download all cluster study datasets"""
    logger.info("="*80)
    logger.info("CLUSTER STUDY DATASET DOWNLOAD - COMPREHENSIVE")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize downloader
    config_path = project_root / 'config' / 'datasets_config.json'
    downloader = DatasetDownloader(config_path=str(config_path))
    
    # Create output structure
    output_base = project_root / 'data' / 'cluster_study'
    output_base.mkdir(parents=True, exist_ok=True)
    
    # Define tiers to download (in priority order)
    tiers = ['hell_yes', 'high_priority']  # Start with critical ones
    
    all_summaries = {}
    
    for tier in tiers:
        # Load tier config
        tier_config = load_tier_config(tier)
        
        if not tier_config:
            logger.warning(f"No datasets found for tier: {tier}")
            continue
            
        # Download tier datasets
        summary = download_tier_datasets(tier, tier_config, downloader, output_base)
        all_summaries[tier] = summary
    
    # Generate overall summary
    overall_summary = {
        'download_date': datetime.now().isoformat(),
        'tiers_processed': list(all_summaries.keys()),
        'tier_summaries': all_summaries,
        'total_datasets': sum(s['total_datasets'] for s in all_summaries.values()),
        'total_downloaded': sum(s['downloaded'] for s in all_summaries.values()),
        'total_skipped': sum(s['skipped'] for s in all_summaries.values()),
        'total_failed': sum(s['failed'] for s in all_summaries.values())
    }
    
    summary_path = output_base / 'overall_download_summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(overall_summary, f, indent=2, ensure_ascii=False)
    logger.info(f"\n[OK] Overall download summary saved: {summary_path}")
    
    logger.info("\n" + "="*80)
    logger.info("DOWNLOAD COMPLETE")
    logger.info("="*80)
    logger.info(f"Total datasets: {overall_summary['total_datasets']}")
    logger.info(f"Downloaded: {overall_summary['total_downloaded']}")
    logger.info(f"Skipped: {overall_summary['total_skipped']}")
    logger.info(f"Failed: {overall_summary['total_failed']}")
    logger.info(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
