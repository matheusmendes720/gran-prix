"""
Integração Scrapy com o pipeline de download de datasets
"""
import sys
from pathlib import Path
import logging
import json
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)

class ScrapyIntegration:
    """Classe para integrar spiders Scrapy com o pipeline de download"""
    
    def __init__(self, config_path: str = 'config/datasets_config.json'):
        self.config_path = Path(config_path)
        self.config = {}
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
    
    def get_datasets_for_scraping(self) -> Dict:
        """Identificar datasets que requerem scraping"""
        datasets = self.config.get('datasets', {})
        scrape_datasets = {}
        
        for dataset_id, dataset_info in datasets.items():
            source = dataset_info.get('source', '')
            download_method = dataset_info.get('download_method', '')
            
            # Identificar datasets que requerem scraping
            scrape_sources = ['anatel', 'internet_aberta', 'springer', 'github', 'inmet', 'bacen', 'ibge', 'zenodo', 'gsma', 'mit', 'ieee']
            if download_method == 'scrape' or source in scrape_sources:
                scrape_datasets[dataset_id] = dataset_info
        
        return scrape_datasets
    
    def run_scrapy_spider(self, dataset_id: str, dataset_info: Dict) -> bool:
        """Executar spider Scrapy para um dataset específico"""
        try:
            from scrapy.crawler import CrawlerProcess
            from scrapy.utils.project import get_project_settings
            
            # Importar spiders
            from backend.pipelines.data_ingestion.scrapy_spiders.anatel_spider import AnatelSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.internet_aberta_spider import InternetAbertaSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.springer_spider import SpringerSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.github_spider import GitHubSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.inmet_spider import InmetSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.bacen_spider import BacenSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.ibge_spider import IbgeSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.zenodo_spider import ZenodoSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.gsma_spider import GsmaSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.mit_spider import MitSpider
            from backend.pipelines.data_ingestion.scrapy_spiders.ieee_spider import IeeeSpider
            
            source = dataset_info.get('source', '')
            url = dataset_info.get('url', '')
            
            # Alguns spiders podem funcionar sem URL (ex: INMET com região)
            if not url and source not in ['inmet', 'gsma', 'mit']:
                logger.warning(f"No URL found for {dataset_id}")
                return False
            
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
            
            # Mapear fonte para spider
            spider_map = {
                'anatel': (AnatelSpider, {'dataset_id': dataset_id, 'dataset_url': url}),
                'internet_aberta': (InternetAbertaSpider, {'dataset_id': dataset_id, 'pdf_url': url}),
                'springer': (SpringerSpider, {'dataset_id': dataset_id, 'article_url': url}),
                'github': (GitHubSpider, {'dataset_id': dataset_id, 'repo_url': url}),
                'inmet': (InmetSpider, {'dataset_id': dataset_id, 'region': dataset_info.get('region')}),
                'bacen': (BacenSpider, {'dataset_id': dataset_id, 'series_code': dataset_info.get('series_code')}),
                'ibge': (IbgeSpider, {'dataset_id': dataset_id, 'table_id': dataset_info.get('table_id')}),
                'zenodo': (ZenodoSpider, {'dataset_id': dataset_id, 'record_id': dataset_info.get('record_id'), 'url': url}),
                'gsma': (GsmaSpider, {'dataset_id': dataset_id, 'report_type': dataset_info.get('report_type'), 'region': dataset_info.get('region', 'brazil')}),
                'mit': (MitSpider, {'dataset_id': dataset_id, 'paper_url': url}),
                'ieee': (IeeeSpider, {'dataset_id': dataset_id, 'paper_url': url, 'document_number': dataset_info.get('document_number')}),
            }
            
            if source not in spider_map:
                logger.warning(f"No spider found for source: {source}")
                return False
            
            spider_class, spider_kwargs = spider_map[source]
            
            logger.info(f"Running Scrapy spider: {spider_class.__name__} for {dataset_id}")
            
            # Executar spider
            process.crawl(spider_class, **spider_kwargs)
            process.start()
            
            # Verificar se arquivo foi baixado
            output_dir = Path('data/raw') / dataset_id
            if output_dir.exists() and any(output_dir.iterdir()):
                logger.info(f"Successfully downloaded dataset {dataset_id} using Scrapy")
                return True
            else:
                logger.warning(f"No files found after Scrapy download for {dataset_id}")
                return False
                
        except ImportError as e:
            logger.error(f"Scrapy not installed or import error: {e}")
            logger.info("Install Scrapy: pip install scrapy")
            return False
        except Exception as e:
            logger.error(f"Error running Scrapy spider for {dataset_id}: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return False
    
    def run_all_scrapy_datasets(self) -> Dict[str, bool]:
        """Executar spiders Scrapy para todos os datasets que requerem scraping"""
        scrape_datasets = self.get_datasets_for_scraping()
        
        if not scrape_datasets:
            logger.info("No datasets require scraping")
            return {}
        
        logger.info(f"Found {len(scrape_datasets)} datasets requiring scraping")
        
        results = {}
        for dataset_id, dataset_info in scrape_datasets.items():
            logger.info(f"\n{'='*70}")
            logger.info(f"Processing: {dataset_info.get('name', dataset_id)}")
            logger.info(f"{'='*70}")
            
            success = self.run_scrapy_spider(dataset_id, dataset_info)
            results[dataset_id] = success
        
        return results


