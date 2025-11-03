"""
Scrapy Spider para baixar datasets do Zenodo
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import json
import re

logger = logging.getLogger(__name__)

class ZenodoSpider(scrapy.Spider):
    name = 'zenodo'
    allowed_domains = ['zenodo.org']
    
    def __init__(self, dataset_id=None, record_id=None, url=None, *args, **kwargs):
        super(ZenodoSpider, self).__init__(*args, **kwargs)
        self.dataset_id = dataset_id or 'zenodo_dataset'
        
        # Extrair record_id da URL se fornecido
        if url and not record_id:
            match = re.search(r'/records/(\d+)', url)
            if match:
                record_id = match.group(1)
        
        self.record_id = record_id
        
        if record_id:
            # API Zenodo para buscar record
            self.start_urls = [f"https://zenodo.org/api/records/{record_id}"]
        elif url:
            # Tentar extrair record_id da URL
            match = re.search(r'/records/(\d+)', url)
            if match:
                self.record_id = match.group(1)
                self.start_urls = [f"https://zenodo.org/api/records/{self.record_id}"]
            else:
                # URL pode ser página web do Zenodo
                self.start_urls = [url]
        else:
            logger.warning("No record_id or url provided for Zenodo spider")
    
    def start_requests(self):
        """Iniciar requests para Zenodo"""
        for url in self.start_urls:
            if '/api/records/' in url:
                # API JSON
                yield Request(
                    url,
                    callback=self.parse_zenodo_record,
                    meta={'dataset_id': self.dataset_id},
                    headers={'Accept': 'application/json'}
                )
            else:
                # Página web - tentar extrair record_id
                yield Request(
                    url,
                    callback=self.parse_zenodo_page,
                    meta={'dataset_id': self.dataset_id}
                )
    
    def parse_zenodo_page(self, response):
        """Parse página web do Zenodo para extrair record_id"""
        # Buscar links para API ou record_id no HTML
        api_links = response.css('a[href*="/api/records/"]::attr(href)').getall()
        record_links = response.css('a[href*="/records/"]::attr(href)').getall()
        
        # Extrair record_id de links
        record_ids = set()
        for link in api_links + record_links:
            match = re.search(r'/records/(\d+)', link)
            if match:
                record_ids.add(match.group(1))
        
        # Buscar no texto também
        text_match = re.search(r'zenodo\.org/record[s]?/(\d+)', response.text)
        if text_match:
            record_ids.add(text_match.group(1))
        
        if record_ids:
            for record_id in record_ids:
                api_url = f"https://zenodo.org/api/records/{record_id}"
                yield Request(
                    api_url,
                    callback=self.parse_zenodo_record,
                    meta={'dataset_id': self.dataset_id},
                    headers={'Accept': 'application/json'}
                )
        else:
            logger.warning(f"Could not extract record_id from Zenodo page: {response.url}")
    
    def parse_zenodo_record(self, response):
        """Parse record do Zenodo (API JSON)"""
        dataset_id = response.meta.get('dataset_id', self.dataset_id)
        
        try:
            data = json.loads(response.text)
            
            # Extrair informações do record
            record_id = data.get('id', '')
            record_title = data.get('metadata', {}).get('title', '')
            record_doi = data.get('doi', '')
            
            # Extrair links de download
            files = data.get('files', [])
            
            if not files:
                logger.warning(f"No files found in Zenodo record {record_id}")
                return
            
            logger.info(f"Found {len(files)} files in Zenodo record {record_id}: {record_title}")
            
            for file_info in files:
                file_url = file_info.get('links', {}).get('self', '')
                filename = file_info.get('key', '')
                file_size = file_info.get('size', 0)
                file_type = file_info.get('type', '')
                
                # Filtrar apenas arquivos de dados
                data_extensions = ['.csv', '.json', '.parquet', '.zip', '.xlsx', '.xls', '.tsv', '.txt']
                if any(ext in filename.lower() for ext in data_extensions):
                    yield Request(
                        file_url,
                        callback=self.download_zenodo_file,
                        meta={
                            'dataset_id': dataset_id,
                            'filename': filename,
                            'record_id': record_id,
                            'record_title': record_title,
                            'record_doi': record_doi,
                            'file_size': file_size,
                            'file_type': file_type
                        },
                        headers={'Accept': '*/*'}
                    )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Zenodo JSON: {e}")
            logger.error(f"Response text (first 500 chars): {response.text[:500]}")
        except Exception as e:
            logger.error(f"Error processing Zenodo record: {e}")
    
    def download_zenodo_file(self, response):
        """Download de arquivo do Zenodo"""
        dataset_id = response.meta.get('dataset_id', self.dataset_id)
        filename = response.meta.get('filename', 'zenodo_file')
        record_id = response.meta.get('record_id', '')
        record_title = response.meta.get('record_title', '')
        
        # Determinar extensão do arquivo
        file_ext = Path(filename).suffix or '.dat'
        
        # Salvar arquivo
        output_dir = Path('data/raw') / dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded Zenodo file: {output_path} ({len(response.body)} bytes)")
        
        yield {
            'dataset_id': dataset_id,
            'file_path': str(output_path),
            'url': response.url,
            'size': len(response.body),
            'filename': filename,
            'file_type': file_ext[1:] if file_ext else 'unknown',
            'source': 'zenodo',
            'record_id': record_id,
            'record_title': record_title,
            'record_doi': response.meta.get('record_doi', '')
        }

