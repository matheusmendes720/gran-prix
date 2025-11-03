"""
Script para executar todos os spiders Scrapy para datasets configurados
"""
import json
import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from src.scrapy.scrapy_spiders.anatel_spider import AnatelSpider
from src.scrapy.scrapy_spiders.internet_aberta_spider import InternetAbertaSpider
from src.scrapy.scrapy_spiders.springer_spider import SpringerSpider
from src.scrapy.scrapy_spiders.github_spider import GitHubSpider

def load_datasets_config():
    """Carregar configuração de datasets"""
    config_path = project_root / 'config' / 'datasets_config.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config.get('datasets', {})

def get_spider_for_source(source, download_method):
    """Determinar qual spider usar baseado na fonte"""
    spider_map = {
        'anatel': ('anatel', AnatelSpider),
        'internet_aberta': ('internet_aberta', InternetAbertaSpider),
        'springer': ('springer', SpringerSpider),
        'github': ('github', GitHubSpider),
    }
    
    if download_method == 'scrape' or source in spider_map:
        return spider_map.get(source, None)
    return None

def main():
    """Executar todos os spiders necessários"""
    datasets = load_datasets_config()
    
    # Filtrar datasets que requerem scraping
    scrape_datasets = {}
    for dataset_id, dataset_info in datasets.items():
        source = dataset_info.get('source', '')
        download_method = dataset_info.get('download_method', '')
        
        spider_info = get_spider_for_source(source, download_method)
        if spider_info:
            scrape_datasets[dataset_id] = {
                'spider_name': spider_info[0],
                'spider_class': spider_info[1],
                'dataset_info': dataset_info,
                'url': dataset_info.get('url', '')
            }
    
    if not scrape_datasets:
        print("Nenhum dataset requer scraping")
        return
    
    print(f"\n{'='*70}")
    print(f"EXECUTANDO SPIDERS SCRAPY")
    print(f"{'='*70}")
    print(f"Total de datasets para scraping: {len(scrape_datasets)}")
    print(f"\nDatasets:")
    for dataset_id in scrape_datasets:
        print(f"  - {dataset_id}")
    print(f"{'='*70}\n")
    
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
    
    # Adicionar cada spider ao processo
    for dataset_id, spider_data in scrape_datasets.items():
        spider_class = spider_data['spider_class']
        url = spider_data['url']
        
        if url:
            process.crawl(spider_class, 
                         dataset_id=dataset_id,
                         dataset_url=url if spider_data['spider_name'] == 'anatel' else url,
                         pdf_url=url if spider_data['spider_name'] == 'internet_aberta' else None,
                         article_url=url if spider_data['spider_name'] == 'springer' else None,
                         repo_url=url if spider_data['spider_name'] == 'github' else None)
    
    # Executar todos os spiders
    process.start()

if __name__ == "__main__":
    main()


