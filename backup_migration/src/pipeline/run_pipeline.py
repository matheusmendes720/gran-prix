#!/usr/bin/env python3
"""
Main Pipeline Orchestrator for Nova Corrente Demand Forecasting System
Executes the complete data pipeline: Download -> Preprocess -> Merge -> Add Factors
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional
import time

# Import pipeline modules (relative imports)
from .download_datasets import DatasetDownloader
from .preprocess_datasets import DatasetPreprocessor
from .merge_datasets import DatasetMerger
from .add_external_factors import ExternalFactorsAdder

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(str(Path(__file__).parent.parent.parent / 'data' / 'pipeline.log')),
            logging.StreamHandler()
        ]
)
logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """Orchestrates the complete data pipeline"""
    
    def __init__(self, config_path: str = None):
        # Get project root (2 levels up from src/pipeline)
        project_root = Path(__file__).parent.parent.parent
        if config_path is None:
            config_path = str(project_root / "config" / "datasets_config.json")
        else:
            # If relative path, make it relative to project root
            if not Path(config_path).is_absolute():
                config_path = str(project_root / config_path)
        self.config_path = config_path
        self.downloader = DatasetDownloader(config_path=config_path)
        self.preprocessor = DatasetPreprocessor(config_path=config_path)
        self.merger = DatasetMerger(config_path=config_path)
        self.factors_adder = ExternalFactorsAdder(config_path=config_path)
        
        self.start_time = None
        self.results = {}
    
    def run_download_step(self, selected_datasets: Optional[List[str]] = None) -> dict:
        """Step 1: Download datasets"""
        logger.info("\n" + "="*70)
        logger.info("STEP 1: DOWNLOADING DATASETS")
        logger.info("="*70)
        
        self.start_time = time.time()
        results = self.downloader.download_all_datasets(selected_datasets=selected_datasets)
        elapsed = time.time() - self.start_time
        
        logger.info(f"\nDownload completed in {elapsed:.2f} seconds")
        self.results['download'] = results
        
        return results
    
    def run_preprocess_step(self, selected_datasets: Optional[List[str]] = None) -> dict:
        """Step 2: Preprocess datasets"""
        logger.info("\n" + "="*70)
        logger.info("STEP 2: PREPROCESSING DATASETS")
        logger.info("="*70)
        
        start_time = time.time()
        results = self.preprocessor.preprocess_all_datasets(selected_datasets=selected_datasets)
        elapsed = time.time() - start_time
        
        logger.info(f"\nPreprocessing completed in {elapsed:.2f} seconds")
        self.results['preprocess'] = {k: (v is not None) for k, v in results.items()}
        
        return results
    
    def run_merge_step(self, selected_datasets: Optional[List[str]] = None) -> bool:
        """Step 3: Merge datasets"""
        logger.info("\n" + "="*70)
        logger.info("STEP 3: MERGING DATASETS")
        logger.info("="*70)
        
        start_time = time.time()
        unified_df = self.merger.create_unified_dataset(selected_datasets=selected_datasets)
        elapsed = time.time() - start_time
        
        logger.info(f"\nMerge completed in {elapsed:.2f} seconds")
        self.results['merge'] = not unified_df.empty
        
        return not unified_df.empty
    
    def run_factors_step(self) -> bool:
        """Step 4: Add external factors"""
        logger.info("\n" + "="*70)
        logger.info("STEP 4: ADDING EXTERNAL FACTORS")
        logger.info("="*70)
        
        start_time = time.time()
        enriched_df = self.factors_adder.add_external_factors()
        elapsed = time.time() - start_time
        
        logger.info(f"\nExternal factors integration completed in {elapsed:.2f} seconds")
        self.results['factors'] = enriched_df is not None
        
        return enriched_df is not None
    
    def run_full_pipeline(
        self,
        selected_datasets: Optional[List[str]] = None,
        skip_download: bool = False,
        skip_preprocess: bool = False,
        skip_merge: bool = False,
        skip_factors: bool = False
    ) -> bool:
        """Run the complete pipeline"""
        logger.info("\n" + "="*70)
        logger.info("NOVA CORRENTE DEMAND FORECASTING DATA PIPELINE")
        logger.info("="*70)
        logger.info(f"Configuration: {self.config_path}")
        logger.info(f"Selected datasets: {selected_datasets or 'ALL'}")
        logger.info("="*70)
        
        pipeline_start = time.time()
        success = True
        
        # Step 1: Download
        if not skip_download:
            download_results = self.run_download_step(selected_datasets=selected_datasets)
            if not any(download_results.values()):
                logger.error("Download step failed! Cannot continue pipeline.")
                return False
        else:
            logger.info("\nSkipping download step (--skip-download)")
        
        # Step 2: Preprocess
        if not skip_preprocess:
            preprocess_results = self.run_preprocess_step(selected_datasets=selected_datasets)
            if not preprocess_results:
                logger.error("Preprocessing step failed! Cannot continue pipeline.")
                return False
        else:
            logger.info("\nSkipping preprocess step (--skip-preprocess)")
        
        # Step 3: Merge
        if not skip_merge:
            merge_success = self.run_merge_step(selected_datasets=selected_datasets)
            if not merge_success:
                logger.error("Merge step failed! Cannot continue pipeline.")
                return False
        else:
            logger.info("\nSkipping merge step (--skip-merge)")
        
        # Step 4: Add External Factors
        if not skip_factors:
            factors_success = self.run_factors_step()
            if not factors_success:
                logger.error("External factors step failed!")
                success = False
        else:
            logger.info("\nSkipping external factors step (--skip-factors)")
        
        # Pipeline summary
        total_elapsed = time.time() - pipeline_start
        logger.info("\n" + "="*70)
        logger.info("PIPELINE SUMMARY")
        logger.info("="*70)
        logger.info(f"Total execution time: {total_elapsed:.2f} seconds ({total_elapsed/60:.2f} minutes)")
        logger.info(f"\nStep results:")
        for step, result in self.results.items():
            status = "SUCCESS" if result else "FAILED"
            if isinstance(result, dict):
                successful = sum(1 for v in result.values() if v)
                total = len(result)
                logger.info(f"  {step}: {status} ({successful}/{total} datasets)")
            else:
                logger.info(f"  {step}: {status}")
        
        # Final output location (relative to project root)
        project_root = Path(__file__).parent.parent.parent
        final_dataset = project_root / "data" / "processed" / "unified_dataset_with_factors.csv"
        if final_dataset.exists():
            logger.info(f"\n✓ Final dataset ready at: {final_dataset}")
            logger.info(f"  File size: {final_dataset.stat().st_size / (1024*1024):.2f} MB")
        else:
            logger.warning(f"\n⚠ Final dataset not found at: {final_dataset}")
        
        return success

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Run complete data pipeline for Nova Corrente demand forecasting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full pipeline for all datasets
  python run_pipeline.py

  # Run for specific datasets only
  python run_pipeline.py --datasets kaggle_daily_demand kaggle_logistics_warehouse

  # Skip download and use existing preprocessed data
  python run_pipeline.py --skip-download --skip-preprocess

  # Only add external factors to existing unified dataset
  python run_pipeline.py --skip-download --skip-preprocess --skip-merge
        """
    )
    
    parser.add_argument(
        '--datasets',
        nargs='+',
        help='Specific datasets to process (by ID). If not specified, processes all.'
    )
    
    parser.add_argument(
        '--config',
        default='config/datasets_config.json',
        help='Path to datasets configuration file'
    )
    
    parser.add_argument(
        '--skip-download',
        action='store_true',
        help='Skip download step (use existing raw data)'
    )
    
    parser.add_argument(
        '--skip-preprocess',
        action='store_true',
        help='Skip preprocess step (use existing preprocessed data)'
    )
    
    parser.add_argument(
        '--skip-merge',
        action='store_true',
        help='Skip merge step (use existing unified dataset)'
    )
    
    parser.add_argument(
        '--skip-factors',
        action='store_true',
        help='Skip external factors step'
    )
    
    args = parser.parse_args()
    
    # Create orchestrator
    orchestrator = PipelineOrchestrator(config_path=args.config)
    
    # Run pipeline
    success = orchestrator.run_full_pipeline(
        selected_datasets=args.datasets,
        skip_download=args.skip_download,
        skip_preprocess=args.skip_preprocess,
        skip_merge=args.skip_merge,
        skip_factors=args.skip_factors
    )
    
    # Exit with appropriate code
    if success:
        logger.info("\nPipeline completed successfully!")
        sys.exit(0)
    else:
        logger.error("\nPipeline completed with errors. Check logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()


