"""
Scrapy Spider para baixar dados econômicos do BACEN
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import json
from datetime import datetime, timedelta
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class BacenSpider(scrapy.Spider):
    name = 'bacen'
    allowed_domains = ['api.bcb.gov.br', 'www.bcb.gov.br']
    
    def __init__(self, dataset_id=None, series_code=None, start_date=None, end_date=None, *args, **kwargs):
        super(BacenSpider, self).__init__(*args, **kwargs)
        self.dataset_id = dataset_id or 'bacen_economic'
        self.series_code = series_code
        self.end_date = end_date or datetime.now().strftime('%d/%m/%Y')
        self.start_date = start_date or (datetime.now() - timedelta(days=365*5)).strftime('%d/%m/%Y')
    
    def start_requests(self):
        """Gerar URLs para API BACEN"""
        # Séries econômicas principais do BACEN
        series = {
            'exchange_rate_usd': '1',  # Taxa de câmbio USD (venda)
            'exchange_rate_eur': '21619',  # Taxa de câmbio EUR
            'selic_rate': '11',  # Taxa SELIC
            'selic_daily': '432',  # Taxa SELIC diária
            'ipca_12m': '433',  # IPCA acumulado 12 meses
            'ipca_monthly': '433',  # IPCA mensal
            'igp_m': '189',  # IGP-M
            'igp_di': '190',  # IGP-DI
            'pib': '4380',  # PIB
            'currency_base': '7',  # Base monetária
            'reserves': '13621',  # Reservas internacionais
        }
        
        # Filtrar por series_code se especificado
        if self.series_code:
            series = {self.dataset_id: self.series_code}
        
        for series_name, code in series.items():
            # API BACEN SGS (Sistema Gerenciador de Séries Temporais)
            url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados"
            params = {
                'dataInicial': self.start_date,
                'dataFinal': self.end_date,
                'formato': 'json'
            }
            
            yield Request(
                f"{url}?{urlencode(params)}",
                callback=self.parse_economic_data,
                meta={
                    'dataset_id': f"{self.dataset_id}_{series_name}",
                    'series_code': code,
                    'series_name': series_name
                },
                headers={'Accept': 'application/json'},
                errback=self.errback_bacen
            )
    
    def parse_economic_data(self, response):
        """Parse dados econômicos do JSON"""
        dataset_id = response.meta.get('dataset_id', self.dataset_id)
        series_name = response.meta.get('series_name', 'unknown')
        series_code = response.meta.get('series_code', '')
        
        try:
            data = json.loads(response.text)
            
            # Verificar se recebemos dados válidos
            if not isinstance(data, list) or len(data) == 0:
                logger.warning(f"No data received for {series_name} (code {series_code})")
                return
            
            # Salvar JSON bruto
            output_dir = Path('data/raw') / dataset_id
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"bacen_{series_name}.json"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Downloaded economic data: {output_path} ({len(data)} records)")
            
            yield {
                'dataset_id': dataset_id,
                'file_path': str(output_path),
                'url': response.url,
                'size': len(response.text),
                'filename': output_path.name,
                'file_type': 'json',
                'source': 'bacen',
                'series_name': series_name,
                'series_code': series_code,
                'records_count': len(data),
                'date_range': f"{self.start_date} to {self.end_date}"
            }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse BACEN JSON for {series_name}: {e}")
            logger.error(f"Response text (first 500 chars): {response.text[:500]}")
        except Exception as e:
            logger.error(f"Error processing BACEN data for {series_name}: {e}")
    
    def errback_bacen(self, failure):
        """Tratamento de erros"""
        series_name = failure.request.meta.get('series_name', 'unknown')
        logger.error(f"Failed to download BACEN data for {series_name}: {failure.request.url}")
        logger.error(f"Error: {failure.value}")

