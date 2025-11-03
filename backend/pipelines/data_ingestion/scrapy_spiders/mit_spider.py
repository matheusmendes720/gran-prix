"""
Scrapy spider para dados do MIT (Massachusetts Institute of Technology)
Foco em datasets de supply chain, telecom spare parts, logistics research
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import json
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class MitSpider(scrapy.Spider):
    name = 'mit'
    allowed_domains = ['dspace.mit.edu', 'web.mit.edu', 'mit.edu']
    
    def __init__(self, dataset_id=None, paper_url=None, **kwargs):
        super().__init__(**kwargs)
        self.dataset_id = dataset_id or 'mit_data'
        self.paper_url = paper_url
    
    def start_requests(self):
        """Iniciar request para o paper MIT"""
        if not self.paper_url:
            # URL padrão do paper de telecom spare parts
            self.paper_url = "https://dspace.mit.edu/bitstream/handle/1721.1/142928/SCM15_Costa_Naithani_project.pdf"
        
        yield Request(
            url=self.paper_url,
            callback=self.download_pdf,
            meta={'dataset_id': self.dataset_id}
        )
    
    def download_pdf(self, response):
        """Download do PDF do MIT"""
        output_dir = Path('data/raw') / self.dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extrair título do paper da URL ou headers
        filename = f"{self.dataset_id}_mit_paper.pdf"
        if 'Content-Disposition' in response.headers:
            try:
                content_disp = response.headers['Content-Disposition'].decode('utf-8')
                match = re.search(r'filename[^;=\n]*=(([\'"]).*?\2|[^\s;]+)', content_disp)
                if match:
                    filename = match.group(1).strip('"\'')
            except Exception as e:
                logger.warning(f"Could not extract filename from headers: {e}")
        
        # Tentar extrair handle ID da URL para naming
        handle_match = re.search(r'handle/([\d.]+)', response.url)
        if handle_match:
            handle_id = handle_match.group(1).replace('.', '_')
            filename = f"{self.dataset_id}_mit_handle_{handle_id}.pdf"
        
        pdf_path = output_dir / filename
        with open(pdf_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded MIT paper: {pdf_path} ({len(response.body)} bytes)")
        
        # Extrair metadados básicos
        metadata = {
            'dataset_id': self.dataset_id,
            'file_path': str(pdf_path),
            'url': response.url,
            'size': len(response.body),
            'source': 'mit',
            'paper_type': 'supply_chain_telecom',
            'institution': 'MIT',
            'download_date': datetime.now().isoformat()
        }
        
        # Salvar metadados como JSON
        metadata_path = output_dir / f"{self.dataset_id}_mit_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        yield metadata
