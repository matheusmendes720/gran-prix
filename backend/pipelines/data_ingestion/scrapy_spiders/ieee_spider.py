"""
Scrapy spider para papers IEEE Xplore
Foco em papers de telecom, predictive maintenance, infrastructure, ML forecasting
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import json
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class IeeeSpider(scrapy.Spider):
    name = 'ieee'
    allowed_domains = ['ieeexplore.ieee.org', 'ieee.org']
    
    def __init__(self, dataset_id=None, paper_url=None, document_number=None, **kwargs):
        super().__init__(**kwargs)
        self.dataset_id = dataset_id or 'ieee_data'
        self.paper_url = paper_url
        self.document_number = document_number
    
    def start_requests(self):
        """Iniciar request para paper IEEE"""
        if not self.paper_url:
            logger.warning("No IEEE paper URL provided")
            return
        
        yield Request(
            url=self.paper_url,
            callback=self.parse_ieee_page,
            meta={'dataset_id': self.dataset_id, 'document_number': self.document_number}
        )
    
    def parse_ieee_page(self, response):
        """Parse página IEEE para encontrar link do PDF"""
        output_dir = Path('data/raw') / self.dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Tentar encontrar link direto para PDF
        pdf_links = []
        
        # Múltiplas estratégias para encontrar PDF
        # 1. Links diretos com .pdf
        pdf_links.extend(response.css('a[href*=".pdf"]::attr(href)').getall())
        
        # 2. Links em botões de download
        pdf_links.extend(response.css('a[href*="download"]::attr(href)').getall())
        pdf_links.extend(response.css('a[href*="pdf"]::attr(href)').getall())
        
        # 3. Meta tags ou data attributes
        pdf_links.extend(response.css('[data-pdf-url]::attr(data-pdf-url)').getall())
        
        # 4. JavaScript embutido (procurar por URLs de PDF)
        js_content = ''.join(response.css('script::text').getall())
        pdf_matches = re.findall(r'["\']([^"\']*\.pdf[^"\']*)["\']', js_content, re.IGNORECASE)
        pdf_links.extend(pdf_matches)
        
        # 5. Tentar construir URL padrão do IEEE
        doc_number = response.meta.get('document_number')
        if doc_number:
            pdf_links.append(f"https://ieeexplore.ieee.org/ielx7/6287639/{doc_number}.pdf")
        
        # Remover duplicatas e converter para URLs absolutas
        pdf_links = list(set(pdf_links))
        pdf_urls = [response.urljoin(link) for link in pdf_links if link]
        
        # Tentar cada link de PDF encontrado
        if pdf_urls:
            for pdf_url in pdf_urls[:3]:  # Tentar apenas os primeiros 3
                yield Request(
                    url=pdf_url,
                    callback=self.download_pdf,
                    meta={'dataset_id': self.dataset_id, 'document_number': doc_number},
                    errback=self.fallback_save_html,
                    dont_filter=True
                )
            return
        
        # Se não encontrou PDF, salvar HTML como fallback
        yield from self.fallback_save_html(response)
    
    def download_pdf(self, response):
        """Download do PDF do IEEE"""
        output_dir = Path('data/raw') / self.dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Verificar content-type
        content_type = response.headers.get('Content-Type', b'').decode('utf-8', errors='ignore')
        
        if 'pdf' in content_type.lower() or response.url.endswith('.pdf'):
            # É um PDF válido
            doc_number = response.meta.get('document_number')
            if doc_number:
                filename = f"{self.dataset_id}_ieee_{doc_number}.pdf"
            else:
                # Extrair document number da URL
                doc_match = re.search(r'/(\d{8,})', response.url)
                if doc_match:
                    filename = f"{self.dataset_id}_ieee_{doc_match.group(1)}.pdf"
                else:
                    filename = f"{self.dataset_id}_ieee_paper.pdf"
        else:
            # Não é PDF, tentar parse novamente
            yield from self.parse_ieee_page(response)
            return
        
        file_path = output_dir / filename
        with open(file_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded IEEE paper: {file_path} ({len(response.body)} bytes)")
        
        metadata = {
            'dataset_id': self.dataset_id,
            'file_path': str(file_path),
            'url': response.url,
            'size': len(response.body),
            'source': 'ieee',
            'paper_type': 'research',
            'document_number': response.meta.get('document_number'),
            'download_date': datetime.now().isoformat()
        }
        
        # Salvar metadados
        metadata_path = output_dir / f"{self.dataset_id}_ieee_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        yield metadata
    
    def fallback_save_html(self, response):
        """Fallback: salvar HTML se PDF não disponível"""
        output_dir = Path('data/raw') / self.dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.dataset_id}_ieee_page.html"
        file_path = output_dir / filename
        
        with open(file_path, 'wb') as f:
            f.write(response.body)
        
        logger.warning(f"PDF not found, saved HTML page: {file_path}")
        
        metadata = {
            'dataset_id': self.dataset_id,
            'file_path': str(file_path),
            'url': response.url,
            'size': len(response.body),
            'source': 'ieee',
            'paper_type': 'research',
            'format': 'html',
            'note': 'PDF download may require authentication or subscription',
            'download_date': datetime.now().isoformat()
        }
        
        metadata_path = output_dir / f"{self.dataset_id}_ieee_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        yield metadata

