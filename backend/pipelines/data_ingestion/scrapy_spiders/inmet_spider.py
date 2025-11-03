"""
Scrapy Spider para baixar dados climáticos do INMET
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import json
from datetime import datetime, timedelta
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class InmetSpider(scrapy.Spider):
    name = 'inmet'
    allowed_domains = ['portal.inmet.gov.br', 'tempo.inmet.gov.br', 'api.inmet.gov.br']
    
    def __init__(self, dataset_id=None, station_id=None, start_date=None, end_date=None, region=None, *args, **kwargs):
        super(InmetSpider, self).__init__(*args, **kwargs)
        self.dataset_id = dataset_id or 'inmet_weather'
        self.station_id = station_id
        self.region = region
        self.end_date = end_date or datetime.now().strftime('%Y-%m-%d')
        self.start_date = start_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    def start_requests(self):
        """Gerar URLs para download de dados climáticos"""
        # Lista de estações INMET principais por região
        stations = {
            'bahia_salvador': {'code': 'A001', 'lat': -12.9714, 'lon': -38.5014},
            'sp_sao_paulo': {'code': 'A701', 'lat': -23.5505, 'lon': -46.6333},
            'rj_rio': {'code': 'A652', 'lat': -22.9068, 'lon': -43.1729},
            'mg_belo_horizonte': {'code': 'A804', 'lat': -19.9167, 'lon': -43.9345},
            'rs_porto_alegre': {'code': 'A839', 'lat': -30.0346, 'lon': -51.2177},
            'pr_curitiba': {'code': 'A838', 'lat': -25.4284, 'lon': -49.2733},
            'ce_fortaleza': {'code': 'A603', 'lat': -3.7172, 'lon': -38.5433},
            'pe_recife': {'code': 'A608', 'lat': -8.0476, 'lon': -34.8770},
        }
        
        # Filtrar por região se especificado
        if self.region:
            if self.region in stations:
                stations = {self.region: stations[self.region]}
            else:
                logger.warning(f"Unknown region: {self.region}. Using all stations.")
        
        # Filtrar por station_id se especificado
        if self.station_id:
            stations = {k: v for k, v in stations.items() if v['code'] == self.station_id}
        
        for region, station_info in stations.items():
            station_code = station_info['code']
            
            # API INMET para dados históricos (URLs alternativas)
            urls_to_try = [
                # Tentar API REST do INMET
                f"https://api.inmet.gov.br/dados_historicos/{self.start_date[:4]}/{station_code}.csv",
                # URL portal antigo
                f"https://portal.inmet.gov.br/uploads/dadoshistoricos/{self.start_date[:4]}/{station_code}.csv",
                # URL alternativa
                f"https://tempo.inmet.gov.br/dados_historicos/{self.start_date[:4]}/{station_code}.csv",
            ]
            
            for url in urls_to_try:
                yield Request(
                    url,
                    callback=self.parse_weather_data,
                    meta={
                        'dataset_id': f"{self.dataset_id}_{region}",
                        'station_code': station_code,
                        'region': region,
                        'lat': station_info['lat'],
                        'lon': station_info['lon'],
                        'url_index': urls_to_try.index(url)
                    },
                    errback=self.errback_inmet,
                    dont_filter=True
                )
    
    def parse_weather_data(self, response):
        """Parse dados climáticos do CSV"""
        dataset_id = response.meta.get('dataset_id', self.dataset_id)
        region = response.meta.get('region', 'unknown')
        station_code = response.meta.get('station_code', '')
        
        # Verificar se recebemos dados válidos
        if response.status != 200:
            logger.warning(f"Failed to download INMET data for {region}: HTTP {response.status}")
            return
        
        if len(response.body) < 100:  # Arquivo muito pequeno provavelmente está vazio/erro
            logger.warning(f"Received empty or invalid data for {region}")
            return
        
        # Salvar CSV bruto
        output_dir = Path('data/raw') / dataset_id
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"inmet_{region}_{self.start_date[:4]}.csv"
        
        with open(output_path, 'wb') as f:
            f.write(response.body)
        
        logger.info(f"Downloaded weather data: {output_path} ({len(response.body)} bytes)")
        
        yield {
            'dataset_id': dataset_id,
            'file_path': str(output_path),
            'url': response.url,
            'size': len(response.body),
            'filename': output_path.name,
            'file_type': 'csv',
            'source': 'inmet',
            'region': region,
            'station_code': station_code,
            'date_range': f"{self.start_date} to {self.end_date}",
            'lat': response.meta.get('lat'),
            'lon': response.meta.get('lon')
        }
    
    def errback_inmet(self, failure):
        """Tratamento de erros"""
        region = failure.request.meta.get('region', 'unknown')
        url_index = failure.request.meta.get('url_index', 0)
        
        logger.warning(f"Failed to download INMET data for {region} (URL {url_index}): {failure.request.url}")
        
        # Tentar próxima URL se houver
        if url_index < 2:  # Ainda temos URLs para tentar
            return
        
        logger.error(f"All URL attempts failed for region {region}")
        logger.error(f"Error: {failure.value}")

