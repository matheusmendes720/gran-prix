#!/usr/bin/env python3
"""
Integration Example - Complete Workflow
Nova Corrente ML System - Expanded Brazilian APIs

Example showing complete workflow:
1. Collect data from APIs
2. Scrape additional data
3. Load into database
4. Generate features
5. Use features for ML
"""

from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from datetime import datetime
import logging

from backend.data.collectors.brazilian_apis_expanded import ExpandedBrazilianAPICollector
from backend.data.collectors.web_scrapers import BrazilianWebScrapers
from backend.data.loaders.load_expanded_metrics import ExpandedMetricsLoader
from backend.data.feature_engineering.expand_features import ExpandedFeatureEngineer
from backend.data.pipelines.etl_orchestrator import ETLOchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_1_manual_collection():
    """Example 1: Manual step-by-step collection"""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 1: Manual Step-by-Step Collection")
    logger.info("="*80)
    
    # Step 1: Collect from APIs
    logger.info("\n📊 Step 1: Collecting from APIs...")
    collector = ExpandedBrazilianAPICollector()
    api_data = collector.collect_all(['bacen_extended', 'ibge_extended'])
    
    # Step 2: Scrape additional data
    logger.info("\n📊 Step 2: Scraping additional data...")
    scrapers = BrazilianWebScrapers()
    scraped_data = scrapers.scrape_all(['comex', 'antt'])
    
    # Step 3: Load into database
    logger.info("\n📊 Step 3: Loading into database...")
    loader = ExpandedMetricsLoader()
    
    # Combine data
    all_data = {**api_data, **scraped_data}
    load_results = loader.load_all(all_data)
    
    logger.info(f"✅ Load results: {load_results}")
    
    return load_results


def example_2_feature_engineering():
    """Example 2: Feature engineering for a material"""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 2: Feature Engineering")
    logger.info("="*80)
    
    material_id = 1  # Example material
    date = datetime.now().date()
    
    engineer = ExpandedFeatureEngineer()
    
    logger.info(f"\n📊 Generating features for material {material_id}...")
    success = engineer.generate_all_features(material_id, date)
    
    if success:
        logger.info("✅ Features generated successfully!")
    else:
        logger.error("❌ Feature generation failed!")
    
    return success


def example_3_complete_pipeline():
    """Example 3: Complete automated pipeline"""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 3: Complete Automated Pipeline")
    logger.info("="*80)
    
    orchestrator = ETLOchestrator()
    results = orchestrator.run_full_pipeline()
    
    logger.info(f"\n✅ Pipeline complete!")
    logger.info(f"Status: {results['status']}")
    logger.info(f"Duration: {results.get('duration', 0):.1f} seconds")
    
    return results


def example_4_query_features():
    """Example 4: Query generated features for ML"""
    logger.info("\n" + "="*80)
    logger.info("EXAMPLE 4: Query Features for ML")
    logger.info("="*80)
    
    import mysql.connector
    from mysql.connector import Error
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'STOCK'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Query features for a material
            query = """
            SELECT 
                feature_name,
                feature_value,
                feature_category
            FROM MaterialFeatures
            WHERE material_id = 1
            AND feature_category IN ('TRANSPORT', 'TRADE', 'ENERGY', 'CONSTRUCTION', 'INDUSTRIAL')
            ORDER BY feature_category, feature_name
            """
            
            cursor.execute(query)
            features = cursor.fetchall()
            
            logger.info(f"\n📊 Found {len(features)} features:")
            for feature in features[:10]:  # Show first 10
                logger.info(f"   {feature['feature_category']}: {feature['feature_name']} = {feature['feature_value']}")
            
            return features
            
    except Error as e:
        logger.error(f"❌ Database error: {e}")
        return []
    
    finally:
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    logger.info("🚀 Starting Integration Examples...")
    
    # Run examples
    try:
        # Example 1: Manual collection
        # example_1_manual_collection()
        
        # Example 2: Feature engineering
        # example_2_feature_engineering()
        
        # Example 3: Complete pipeline (recommended)
        example_3_complete_pipeline()
        
        # Example 4: Query features
        # example_4_query_features()
        
    except Exception as e:
        logger.error(f"❌ Example failed: {e}")
    
    logger.info("\n✅ Examples complete!")

