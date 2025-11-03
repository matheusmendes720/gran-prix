"""
Scrapy spider para dados da GSMA (Global System for Mobile Communications Association)
Foco em dados de mobile connectivity, 5G coverage, IoT connections, Mobile Economy reports
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class GsmaSpider(scrapy.Spider):
    name = 'gsma'
    allowed_domains = ['gsma.com', 'gsmaintelligence.com', 'mobileconnectivityindex.com', 'gsma.com.br']
    
    def __init__(self, dataset_id=None, report_type=None, region='brazil', **kwargs):
        super().__init__(**kwargs)
        self.dataset_id = dataset_id or 'gsma_data'
        self.report_type = report_type or 'mobile_connectivity_index'
        self.region = region or 'brazil'
    
    def start_requests(self):
        """Iniciar requests baseado no tipo de relatório"""
        urls_map = {
            'mobile_connectivity_index': f'https://www.mobileconnectivityindex.com/api/countries/{self.region}',
            '5g_coverage': 'https://www.gsmaintelligence.com/api/reports/5g-coverage',
            'iot_connections': 'https://www.gsmaintelligence.com/api/reports/iot-connections',
            'mobile_economy': 'https://www.gsma.com/mobileeconomy/wp-content/uploads/2024/02/Mobile-Economy-Brazil-2024.pdf',
            'mobile_economy_latam': 'https://www.gsma.com/mobileeconomy/wp-content/uploads/2024/06/Mobile-Economy-Latin-America-2024.pdf',
            'mobile_connectivity_brazil': 'https://www.gsma.com/mobileconnectivity/wp-content/uploads/2024/03/Mobile-Connectivity-Index-Brazil-2024.pdf'
        }
        
        url = urls_map.get(self.report_type, urls_map['mobile_connectivity_index'])
        
        if 'api' in url:
            yield Request(
                url=url,
                callback=self.parse_api,
                meta={'dataset_id': self.dataset_id, 'report_type': self.report_type}
            )
        else:
            yield Request(
                url=url,
                callback=self.parse_pdf,
                meta={'dataset_id': self.dataset_id, 'report_type': self.report_type}
            )
    
    def parse_api(self, response):
        """Parse de resposta JSON da API"""
        try:
            data = json.loads(response.text)
            
            # Salvar JSON bruto
            output_dir = Path('data/raw') / self.dataset_id
            output_dir.mkdir(parents=True, exist_ok=True)
            
            json_path = output_dir / f"{self.dataset_id}_gsma_{self.report_type}_raw.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Downloaded GSMA API data: {json_path}")
            
            # Tentar converter para CSV se possível
            try:
                import pandas as pd
                if isinstance(data, list) and len(data) > 0:
                    df = pd.DataFrame(data)
                    csv_path = output_dir / f"{self.dataset_id}_gsma_{self.report_type}.csv"
                    df.to_csv(csv_path, index=False, encoding='utf-8')
                    logger.info(f"Converted to CSV: {csv_path}")
            except Exception as e:
                logger.warning(f"Could not convert to CSV: {e}")
            
            yield {
                'dataset_id': self.dataset_id,
                'file_path': str(json_path),
                'url': response.url,
                'size': len(response.body),
                'source': 'gsma',
                'report_type': self.report_type,
                'region': self.region
            }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            # Salvar resposta bruta para debugging
            output_dir = Path('data/raw') / self.dataset_id
            output_dir.mkdir(parents=True, exist_ok=True)
            raw_path = output_dir / f"{self.dataset_id}_gsma_{self.report_type}_raw.txt"
            with open(raw_path, 'wb') as f:
                f.write(response.body)
            logger.info(f"Saved raw response to: {raw_path}")
    
    def parse_pdf(self, response):
        """Download de PDF"""
        output_dir = Path('data/raw') / self.dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        pdf_path = output_dir / f"{self.dataset_id}_gsma_{self.report_type}.pdf"
        with open(pdf_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded GSMA PDF: {pdf_path} ({len(response.body)} bytes)")
        
        yield {
            'dataset_id': self.dataset_id,
            'file_path': str(pdf_path),
            'url': response.url,
            'size': len(response.body),
            'source': 'gsma',
            'report_type': self.report_type,
            'region': self.region
        }

