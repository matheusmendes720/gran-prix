"""
Scrapy Spider para baixar datasets da Anatel (Data Basis)
"""
import scrapy
from scrapy.http import Request
import json
import re
from urllib.parse import urljoin, urlparse
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class AnatelSpider(scrapy.Spider):
    name = 'anatel'
    allowed_domains = ['data-basis.org', 'basedosdados.org']
    
    def __init__(self, dataset_id=None, dataset_url=None, *args, **kwargs):
        super(AnatelSpider, self).__init__(*args, **kwargs)
        self.dataset_id = dataset_id
        self.dataset_url = dataset_url
        self.start_urls = [dataset_url] if dataset_url else []
        
    def start_requests(self):
        """Iniciar requests"""
        for url in self.start_urls:
            yield Request(url, callback=self.parse_dataset_page, meta={'dont_cache': True})
    
    def parse_dataset_page(self, response):
        """Parse da página do dataset no Data Basis"""
        logger.info(f"Parsing dataset page: {response.url}")
        
        # Tentar encontrar links CSV diretos
        csv_links = response.css('a[href*=".csv"]::attr(href)').getall()
        download_links = response.css('a[href*="download"]::attr(href)').getall()
        
        # Buscar em scripts JavaScript (Data Basis usa React)
        scripts = response.css('script::text').getall()
        for script in scripts:
            # Buscar JSON embutido com informações do dataset
            if '__NEXT_DATA__' in script or 'props' in script:
                try:
                    # Tentar extrair dados do script
                    json_match = re.search(r'__NEXT_DATA__.*?({.+?})', script, re.DOTALL)
                    if json_match:
                        data = json.loads(json_match.group(1))
                        # Processar dados do dataset
                        dataset_info = data.get('props', {}).get('pageProps', {}).get('dataset', {})
                        if dataset_info:
                            logger.info(f"Found dataset info: {dataset_info.get('name', 'Unknown')}")
                except:
                    pass
        
        # Buscar links de download CSV
        all_links = csv_links + download_links
        for link in all_links:
            absolute_url = urljoin(response.url, link)
            if '.csv' in absolute_url.lower() or 'download' in absolute_url.lower():
                yield Request(absolute_url, callback=self.download_csv, meta={'dataset_id': self.dataset_id})
        
        # Fallback: tentar API do Data Basis
        dataset_match = re.search(r'/dataset/([^/]+)', response.url)
        if dataset_match:
            dataset_uuid = dataset_match.group(1)
            api_url = f"https://data-basis.org/api/datasets/{dataset_uuid}/download"
            yield Request(api_url, callback=self.download_csv, 
                         meta={'dataset_id': self.dataset_id}, 
                         dont_filter=True)
    
    def download_csv(self, response):
        """Download do arquivo CSV"""
        dataset_id = response.meta.get('dataset_id', 'anatel')
        
        # Determinar filename
        content_disposition = response.headers.get('Content-Disposition', b'').decode('utf-8', errors='ignore')
        if 'filename=' in content_disposition:
            filename = content_disposition.split('filename=')[1].strip('"')
        else:
            filename = response.url.split('/')[-1].split('?')[0] or f"{dataset_id}.csv"
        
        # Salvar arquivo
        output_dir = Path('data/raw') / dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded CSV: {output_path}")
        
        yield {
            'dataset_id': dataset_id,
            'file_path': str(output_path),
            'url': response.url,
            'size': len(response.body),
            'filename': filename
        }


