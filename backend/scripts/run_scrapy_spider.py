"""Script para executar spiders Scrapy."""
import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Importar spiders
from src.scrapy.scrapy_spiders.anatel_spider import AnatelSpider
from src.scrapy.scrapy_spiders.internet_aberta_spider import InternetAbertaSpider
from src.scrapy.scrapy_spiders.springer_spider import SpringerSpider
from src.scrapy.scrapy_spiders.github_spider import GitHubSpider

import argparse

def run_spider(spider_name, dataset_id=None, url=None):
    """Executar um spider específico"""
    settings = get_project_settings()
    
    # Carregar configurações do projeto
    project_settings = {
        'USER_AGENT': 'NovaCorrente-DataCollector/1.0',
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'LOG_LEVEL': 'INFO',
    }
    settings.update(project_settings)
    
    process = CrawlerProcess(settings)
    
    spider_map = {
        'anatel': (AnatelSpider, {'dataset_id': dataset_id, 'dataset_url': url}),
        'internet_aberta': (InternetAbertaSpider, {'dataset_id': dataset_id, 'pdf_url': url}),
        'springer': (SpringerSpider, {'dataset_id': dataset_id, 'article_url': url}),
        'github': (GitHubSpider, {'dataset_id': dataset_id, 'repo_url': url}),
    }
    
    if spider_name not in spider_map:
        print(f"❌ Spider '{spider_name}' não encontrado")
        print(f"Spiders disponíveis: {', '.join(spider_map.keys())}")
        return
    
    spider_class, spider_kwargs = spider_map[spider_name]
    
    print(f"\n{'='*70}")
    print(f"EXECUTANDO SPIDER: {spider_name}")
    print(f"{'='*70}")
    print(f"Dataset ID: {dataset_id}")
    print(f"URL: {url}")
    print(f"{'='*70}\n")
    
    process.crawl(spider_class, **spider_kwargs)
    process.start()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Executar spiders Scrapy')
    parser.add_argument('spider', choices=['anatel', 'internet_aberta', 'springer', 'github'],
                       help='Nome do spider para executar')
    parser.add_argument('--dataset-id', default=None,
                       help='ID do dataset (ex: anatel_mobile_brazil)')
    parser.add_argument('--url', required=True,
                       help='URL para processar')
    
    args = parser.parse_args()
    
    run_spider(args.spider, args.dataset_id, args.url)

if __name__ == "__main__":
    main()


