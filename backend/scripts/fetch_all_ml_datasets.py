"""
Script para buscar todos os datasets diversos para ML training
"""
import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import logging
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Importar todos os spiders
from backend.pipelines.data_ingestion.scrapy_spiders.inmet_spider import InmetSpider
from backend.pipelines.data_ingestion.scrapy_spiders.bacen_spider import BacenSpider
from backend.pipelines.data_ingestion.scrapy_spiders.ibge_spider import IbgeSpider
from backend.pipelines.data_ingestion.scrapy_spiders.zenodo_spider import ZenodoSpider
from backend.pipelines.data_ingestion.scrapy_spiders.anatel_spider import AnatelSpider
from backend.pipelines.data_ingestion.scrapy_spiders.github_spider import GitHubSpider

def main():
    """Executar todos os spiders para datasets ML"""
    
    print("\n" + "="*80)
    print("DOWNLOADING DIVERSE DATASETS FOR ML TRAINING")
    print("="*80)
    
    # Configurar Scrapy
    settings = get_project_settings()
    project_settings = {
        'USER_AGENT': 'NovaCorrente-DataCollector/1.0',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'LOG_LEVEL': 'INFO',
    }
    settings.update(project_settings)
    
    process = CrawlerProcess(settings)
    
    # Calcular datas (último ano)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # 1. Dados Climáticos (INMET) - Principais regiões
    print("\n" + "="*80)
    print("1. DOWNLOADING CLIMATE DATA (INMET)")
    print("="*80)
    
    regions = ['bahia_salvador', 'sp_sao_paulo', 'rj_rio', 'mg_belo_horizonte']
    for region in regions:
        print(f"  - Downloading climate data for: {region}")
        process.crawl(
            InmetSpider, 
            dataset_id='inmet_climate_all',
            region=region,
            start_date=start_date,
            end_date=end_date
        )
    
    # 2. Dados Econômicos (BACEN) - Principais séries
    print("\n" + "="*80)
    print("2. DOWNLOADING ECONOMIC DATA (BACEN)")
    print("="*80)
    
    economic_series = [
        ('exchange_rate_usd', '1'),  # Taxa de câmbio USD
        ('selic_rate', '11'),  # Taxa SELIC
        ('ipca_12m', '433'),  # IPCA acumulado 12 meses
    ]
    
    for series_name, series_code in economic_series:
        print(f"  - Downloading {series_name} (code: {series_code})")
        process.crawl(
            BacenSpider,
            dataset_id='bacen_economic_all',
            series_code=series_code,
            start_date=(datetime.now() - timedelta(days=365*5)).strftime('%d/%m/%Y'),
            end_date=datetime.now().strftime('%d/%m/%Y')
        )
    
    # 3. Dados IBGE - Principais tabelas
    print("\n" + "="*80)
    print("3. DOWNLOADING IBGE STATISTICS")
    print("="*80)
    
    ibge_tables = [
        ('pib_quarterly', '5932'),  # PIB trimestral
        ('ipca_monthly', '1737'),  # IPCA mensal
    ]
    
    for table_name, table_id in ibge_tables:
        print(f"  - Downloading {table_name} (table: {table_id})")
        process.crawl(
            IbgeSpider,
            dataset_id='ibge_stats_all',
            table_id=table_id
        )
    
    # 4. Datasets Zenodo - Principais datasets acadêmicos
    print("\n" + "="*80)
    print("4. DOWNLOADING ZENODO ACADEMIC DATASETS")
    print("="*80)
    
    zenodo_datasets = [
        {'dataset_id': 'zenodo_milan_telecom', 'record_id': '14012612'},
        {'dataset_id': 'zenodo_broadband_brazil', 'record_id': '10482897'},
        {'dataset_id': 'zenodo_bgsmt_mobility', 'record_id': '8178782'},
    ]
    
    for dataset_info in zenodo_datasets:
        if dataset_info.get('record_id'):
            print(f"  - Downloading Zenodo record: {dataset_info['record_id']}")
            process.crawl(ZenodoSpider, **dataset_info)
    
    # 5. Executar todos
    print("\n" + "="*80)
    print("STARTING ALL DOWNLOADS...")
    print("="*80 + "\n")
    
    try:
        process.start()
        print("\n" + "="*80)
        print("✅ ALL DOWNLOADS COMPLETED!")
        print("="*80)
        print("\nDatasets saved to: data/raw/")
        print("\nNext step: Run ML data structuring pipeline to prepare data for training")
    except Exception as e:
        logger.error(f"Error during downloads: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

