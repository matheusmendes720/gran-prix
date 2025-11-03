"""
Scrapy Spider para baixar datasets de repositórios GitHub
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import json
import re
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class GitHubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com', 'raw.githubusercontent.com']
    
    def __init__(self, repo_url=None, dataset_id=None, *args, **kwargs):
        super(GitHubSpider, self).__init__(*args, **kwargs)
        self.repo_url = repo_url
        self.dataset_id = dataset_id or 'github_dataset'
        self.start_urls = [repo_url] if repo_url else []
    
    def start_requests(self):
        """Iniciar requests"""
        for url in self.start_urls:
            if 'raw.githubusercontent.com' in url:
                # URL direta de arquivo raw
                yield Request(url, callback=self.download_file, meta={'dataset_id': self.dataset_id})
            else:
                # URL de repositório - buscar arquivos
                yield Request(url, callback=self.parse_repository, meta={'dataset_id': self.dataset_id})
    
    def parse_repository(self, response):
        """Parse do repositório GitHub"""
        logger.info(f"Parsing repository: {response.url}")
        
        # Buscar links para arquivos CSV, JSON, ZIP, etc.
        data_file_extensions = ['.csv', '.json', '.zip', '.parquet', '.tsv', '.xlsx']
        
        for ext in data_file_extensions:
            # Buscar links de arquivos
            file_links = response.css(f'a[href*="{ext}"]::attr(href)').getall()
            for link in file_links:
                # Converter para raw GitHub URL
                if '/blob/' in link:
                    raw_url = link.replace('/blob/', '/').replace('github.com', 'raw.githubusercontent.com')
                    yield Request(raw_url, callback=self.download_file,
                               meta={'dataset_id': self.dataset_id})
                else:
                    absolute_url = response.urljoin(link)
                    yield Request(absolute_url, callback=self.parse_repository,
                               meta={'dataset_id': self.dataset_id})
        
        # Buscar diretórios de dados
        data_dirs = response.css('a[title*="data"], a[title*="dataset"], a[title*="Data"]::attr(href)').getall()
        for dir_link in data_dirs:
            absolute_url = response.urljoin(dir_link)
            yield Request(absolute_url, callback=self.parse_repository,
                         meta={'dataset_id': self.dataset_id})
    
    def download_file(self, response):
        """Download de arquivo"""
        dataset_id = response.meta.get('dataset_id', 'github_dataset')
        
        # Determinar filename
        filename = response.url.split('/')[-1].split('?')[0]
        
        # Salvar arquivo
        output_dir = Path('data/raw') / dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded file: {output_path} ({len(response.body)} bytes)")
        
        yield {
            'dataset_id': dataset_id,
            'file_path': str(output_path),
            'url': response.url,
            'size': len(response.body),
            'filename': filename
        }


