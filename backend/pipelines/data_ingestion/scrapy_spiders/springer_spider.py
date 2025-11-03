"""
Scrapy Spider para extrair links de dados de artigos Springer
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import re

logger = logging.getLogger(__name__)

class SpringerSpider(scrapy.Spider):
    name = 'springer'
    allowed_domains = ['springeropen.com', 'epjdatascience.springeropen.com']
    
    def __init__(self, dataset_id=None, article_url=None, *args, **kwargs):
        super(SpringerSpider, self).__init__(*args, **kwargs)
        self.dataset_id = dataset_id
        self.article_url = article_url
        self.start_urls = [article_url] if article_url else []
    
    def start_requests(self):
        """Iniciar requests"""
        for url in self.start_urls:
            yield Request(url, callback=self.parse_article, meta={'dont_cache': True})
    
    def parse_article(self, response):
        """Parse do artigo científico para encontrar links de dados"""
        logger.info(f"Parsing article: {response.url}")
        
        # Buscar links para datasets suplementares
        data_links = response.css('a[href*="data"], a[href*="dataset"], a[href*="supplement"]::attr(href)').getall()
        download_links = response.css('a[href*="download"], a[href*=".csv"], a[href*=".zip"]::attr(href)').getall()
        
        # Buscar em seções específicas (materials and methods, data availability)
        text_content = response.css('body').get()
        if text_content:
            # Buscar padrões de URLs de dados
            data_urls = re.findall(r'https?://[^\s<>"\'{}|\\^`\[\]]+\.(?:csv|zip|json|parquet)', text_content)
            data_links.extend(data_urls)
        
        all_links = data_links + download_links
        
        for link in set(all_links):  # Remover duplicatas
            absolute_url = response.urljoin(link)
            # Filtrar links relevantes
            if any(ext in link.lower() for ext in ['.csv', '.zip', '.json', 'data', 'dataset']):
                yield Request(absolute_url, callback=self.download_data,
                             meta={'dataset_id': self.dataset_id})
        
        # Buscar referências a repositórios externos (Zenodo, GitHub, etc.)
        repo_links = response.css('a[href*="zenodo"], a[href*="github"], a[href*="figshare"]::attr(href)').getall()
        for link in repo_links:
            logger.info(f"Found repository link: {link}")
            yield {
                'dataset_id': self.dataset_id,
                'repository_url': link,
                'article_url': response.url,
                'type': 'repository_link'
            }
    
    def download_data(self, response):
        """Download de arquivos de dados"""
        dataset_id = response.meta.get('dataset_id', 'springer_digital_divide')
        
        # Determinar filename e tipo
        content_type = response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore')
        url_path = response.url.split('/')[-1]
        
        if '.csv' in url_path.lower() or 'csv' in content_type.lower():
            ext = 'csv'
        elif '.zip' in url_path.lower():
            ext = 'zip'
        elif '.json' in url_path.lower():
            ext = 'json'
        else:
            ext = 'csv'  # Default
        
        filename = url_path.split('?')[0] or f"{dataset_id}_data.{ext}"
        if not filename.endswith(f'.{ext}'):
            filename = f"{filename}.{ext}"
        
        # Salvar arquivo
        output_dir = Path('data/raw') / dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded data file: {output_path} ({len(response.body)} bytes)")
        
        yield {
            'dataset_id': dataset_id,
            'file_path': str(output_path),
            'url': response.url,
            'size': len(response.body),
            'filename': filename,
            'file_type': ext
        }


