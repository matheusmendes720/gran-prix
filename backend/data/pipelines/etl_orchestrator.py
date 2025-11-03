#!/usr/bin/env python3
"""
ETL Pipeline Orchestrator for Expanded Brazilian APIs
Nova Corrente ML System - Automated Daily Collection

Orchestrates complete ETL pipeline:
1. Extract: Collect from 25+ APIs
2. Transform: Web scraping, data cleaning
3. Load: Load into database
4. Feature Engineering: Generate 52+ new features

Runs daily automatically (can be scheduled with cron/celery)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
import pandas as pd

# Import collectors
from backend.data.collectors.brazilian_apis_expanded import ExpandedBrazilianAPICollector
from backend.data.collectors.web_scrapers import BrazilianWebScrapers
from backend.data.loaders.load_expanded_metrics import ExpandedMetricsLoader
from backend.data.feature_engineering.expand_features import ExpandedFeatureEngineer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/etl_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ETLOchestrator:
    """
    Complete ETL pipeline orchestrator
    """
    
    def __init__(self):
        self.collector = ExpandedBrazilianAPICollector()
        self.scrapers = BrazilianWebScrapers()
        self.loader = ExpandedMetricsLoader()
        self.feature_engineer = ExpandedFeatureEngineer()
        
        self.results = {
            'extract': {},
            'transform': {},
            'load': {},
            'feature_engineering': {},
            'start_time': None,
            'end_time': None,
            'duration': None,
            'status': 'pending'
        }
    
    def run_full_pipeline(self, date: Optional[datetime.date] = None) -> Dict:
        """
        Run complete ETL pipeline
        
        Args:
            date: Date to process (default: today)
        
        Returns:
            Dictionary with pipeline results
        """
        if not date:
            date = datetime.now().date()
        
        logger.info("="*80)
        logger.info("🚀 STARTING COMPLETE ETL PIPELINE")
        logger.info("="*80)
        logger.info(f"Date: {date}")
        logger.info(f"Time: {datetime.now()}")
        
        self.results['start_time'] = datetime.now()
        self.results['date'] = date
        
        try:
            # STEP 1: EXTRACT - API Collection
            logger.info("\n" + "="*80)
            logger.info("STEP 1: EXTRACT - API Collection")
            logger.info("="*80)
            
            extract_results = self._extract_phase()
            self.results['extract'] = extract_results
            
            # STEP 2: TRANSFORM - Web Scraping & Cleaning
            logger.info("\n" + "="*80)
            logger.info("STEP 2: TRANSFORM - Web Scraping & Data Cleaning")
            logger.info("="*80)
            
            transform_results = self._transform_phase()
            self.results['transform'] = transform_results
            
            # STEP 3: LOAD - Database Loading
            logger.info("\n" + "="*80)
            logger.info("STEP 3: LOAD - Database Loading")
            logger.info("="*80)
            
            load_results = self._load_phase()
            self.results['load'] = load_results
            
            # STEP 4: FEATURE ENGINEERING
            logger.info("\n" + "="*80)
            logger.info("STEP 4: FEATURE ENGINEERING - Generate ML Features")
            logger.info("="*80)
            
            feature_results = self._feature_engineering_phase(date)
            self.results['feature_engineering'] = feature_results
            
            # SUCCESS
            self.results['status'] = 'success'
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed: {str(e)}")
            self.results['status'] = 'failed'
            self.results['error'] = str(e)
        
        finally:
            self.results['end_time'] = datetime.now()
            if self.results['start_time']:
                self.results['duration'] = (
                    self.results['end_time'] - self.results['start_time']
                ).total_seconds()
            
            self._print_summary()
        
        return self.results
    
    def _extract_phase(self) -> Dict:
        """Extract data from APIs"""
        logger.info("📊 Extracting data from 25+ APIs...")
        
        try:
            # Collect from APIs (those with direct APIs)
            api_sources = [
                'bacen_extended',
                'ibge_extended',
                'ipea'
            ]
            
            api_results = self.collector.collect_all(sources=api_sources)
            
            logger.info(f"✅ API extraction complete: {len(api_results)} sources")
            
            return {
                'status': 'success',
                'sources': api_results,
                'count': len(api_results)
            }
            
        except Exception as e:
            logger.error(f"❌ Extraction failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def _transform_phase(self) -> Dict:
        """Transform data (web scraping, cleaning)"""
        logger.info("📊 Transforming data (web scraping)...")
        
        try:
            # Scrape from sources without direct APIs
            scraping_sources = [
                'comex',
                'antt',
                'antaq',
                'aneel',
                'anp',
                'caged',
                'cbic',
                'abinee'
            ]
            
            scrape_results = self.scrapers.scrape_all(sources=scraping_sources)
            
            logger.info(f"✅ Transformation complete: {len(scrape_results)} sources scraped")
            
            return {
                'status': 'success',
                'sources': scrape_results,
                'count': len(scrape_results)
            }
            
        except Exception as e:
            logger.error(f"❌ Transformation failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def _load_phase(self) -> Dict:
        """Load data into database"""
        logger.info("📊 Loading data into database...")
        
        try:
            # Combine API and scraped data
            all_data = {}
            
            # Add API data
            if 'extract' in self.results and 'sources' in self.results['extract']:
                all_data.update(self.results['extract']['sources'])
            
            # Add scraped data
            if 'transform' in self.results and 'sources' in self.results['transform']:
                for source, data in self.results['transform']['sources'].items():
                    if isinstance(data, pd.DataFrame):
                        all_data[source] = data
            
            # Load all data
            load_results = self.loader.load_all(all_data)
            
            logger.info(f"✅ Database loading complete")
            
            return load_results
            
        except Exception as e:
            logger.error(f"❌ Loading failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def _feature_engineering_phase(self, date: datetime.date) -> Dict:
        """Generate ML features"""
        logger.info("📊 Generating ML features...")
        
        try:
            # Get all materials
            if not self.feature_engineer.connect():
                return {'status': 'failed', 'error': 'Database connection failed'}
            
            cursor = self.feature_engineer.connection.cursor()
            cursor.execute("SELECT material_id FROM Material")
            materials = cursor.fetchall()
            self.feature_engineer.disconnect()
            
            successful = 0
            failed = 0
            
            for (material_id,) in materials:
                try:
                    if self.feature_engineer.generate_all_features(material_id, date):
                        successful += 1
                    else:
                        failed += 1
                except Exception as e:
                    logger.error(f"   ❌ Failed for material {material_id}: {e}")
                    failed += 1
            
            logger.info(f"✅ Feature engineering complete: {successful} successful, {failed} failed")
            
            return {
                'status': 'success',
                'successful': successful,
                'failed': failed,
                'total': len(materials)
            }
            
        except Exception as e:
            logger.error(f"❌ Feature engineering failed: {e}")
            return {'status': 'failed', 'error': str(e)}
    
    def _print_summary(self):
        """Print pipeline summary"""
        logger.info("\n" + "="*80)
        logger.info("📊 ETL PIPELINE SUMMARY")
        logger.info("="*80)
        logger.info(f"Status: {self.results['status'].upper()}")
        logger.info(f"Date: {self.results.get('date', 'N/A')}")
        logger.info(f"Duration: {self.results.get('duration', 0):.1f} seconds")
        
        if self.results.get('extract'):
            logger.info(f"\nEXTRACT:")
            logger.info(f"  Status: {self.results['extract'].get('status', 'N/A')}")
            logger.info(f"  Sources: {self.results['extract'].get('count', 0)}")
        
        if self.results.get('transform'):
            logger.info(f"\nTRANSFORM:")
            logger.info(f"  Status: {self.results['transform'].get('status', 'N/A')}")
            logger.info(f"  Sources: {self.results['transform'].get('count', 0)}")
        
        if self.results.get('load'):
            logger.info(f"\nLOAD:")
            logger.info(f"  Status: {self.results['load'].get('status', 'N/A')}")
            logger.info(f"  Successful: {len(self.results['load'].get('successful', []))}")
            logger.info(f"  Failed: {len(self.results['load'].get('failed', []))}")
        
        if self.results.get('feature_engineering'):
            logger.info(f"\nFEATURE ENGINEERING:")
            logger.info(f"  Status: {self.results['feature_engineering'].get('status', 'N/A')}")
            logger.info(f"  Successful: {self.results['feature_engineering'].get('successful', 0)}")
            logger.info(f"  Failed: {self.results['feature_engineering'].get('failed', 0)}")
        
        logger.info("="*80)


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    orchestrator = ETLOchestrator()
    
    # Run full pipeline
    results = orchestrator.run_full_pipeline()
    
    print("\n🎉 ETL Pipeline Complete!")
    print(f"Status: {results['status']}")
    print(f"Duration: {results.get('duration', 0):.1f} seconds")

