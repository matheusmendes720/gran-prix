"""
Scrapy Spider para baixar dados do Internet Aberta (forecasts e relatórios)
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class InternetAbertaSpider(scrapy.Spider):
    name = 'internet_aberta'
    allowed_domains = ['internetaberta.com.br', 'internetaberta.com.br']
    
    def __init__(self, dataset_id=None, pdf_url=None, *args, **kwargs):
        super(InternetAbertaSpider, self).__init__(*args, **kwargs)
        self.dataset_id = dataset_id
        self.pdf_url = pdf_url
        self.start_urls = [pdf_url] if pdf_url else []
    
    def start_requests(self):
        """Iniciar requests"""
        for url in self.start_urls:
            if url.endswith('.pdf'):
                yield Request(url, callback=self.download_pdf, meta={'dont_cache': True})
            else:
                yield Request(url, callback=self.parse_page, meta={'dont_cache': True})
    
    def parse_page(self, response):
        """Parse da página para encontrar links de PDF"""
        logger.info(f"Parsing page: {response.url}")
        
        # Buscar links para PDFs
        pdf_links = response.css('a[href*=".pdf"]::attr(href)').getall()
        
        for link in pdf_links:
            absolute_url = response.urljoin(link)
            if 'forecast' in link.lower() or 'demand' in link.lower():
                yield Request(absolute_url, callback=self.download_pdf,
                             meta={'dataset_id': self.dataset_id})
    
    def download_pdf(self, response):
        """Download do arquivo PDF"""
        dataset_id = response.meta.get('dataset_id', 'internet_aberta_forecast')
        
        # Determinar filename
        filename = response.url.split('/')[-1].split('?')[0] or f"{dataset_id}.pdf"
        
        # Salvar arquivo
        output_dir = Path('data/raw') / dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded PDF: {output_path} ({len(response.body)} bytes)")
        
        yield {
            'dataset_id': dataset_id,
            'file_path': str(output_path),
            'url': response.url,
            'size': len(response.body),
            'filename': filename,
            'file_type': 'pdf'
        }


