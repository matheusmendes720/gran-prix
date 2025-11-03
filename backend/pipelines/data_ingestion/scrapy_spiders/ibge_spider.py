"""
Scrapy Spider para baixar dados do IBGE
"""
import scrapy
from scrapy.http import Request
from pathlib import Path
import logging
import json
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class IbgeSpider(scrapy.Spider):
    name = 'ibge'
    allowed_domains = ['api.ibge.gov.br', 'apisidra.ibge.gov.br', 'www.ibge.gov.br']
    
    def __init__(self, dataset_id=None, table_id=None, *args, **kwargs):
        super(IbgeSpider, self).__init__(*args, **kwargs)
        self.dataset_id = dataset_id or 'ibge_stats'
        self.table_id = table_id
    
    def start_requests(self):
        """Gerar URLs para API IBGE"""
        # Tabelas principais IBGE SIDRA
        tables = {
            'pib_quarterly': '5932',  # PIB trimestral
            'pib_annual': '5938',  # PIB anual
            'ipca_monthly': '1737',  # IPCA mensal
            'ipca15': '1705',  # IPCA-15
            'inpc': '1736',  # INPC
            'igp_m': '190',  # IGP-M
            'population': '29168',  # População estimada
            'unemployment': '6385',  # Taxa de desocupação
        }
        
        # Filtrar por table_id se especificado
        if self.table_id:
            tables = {self.dataset_id: self.table_id}
        
        for table_name, table_id in tables.items():
            # API IBGE SIDRA para tabelas
            # n1 = Brasil (nível nacional)
            # v/all = todas variáveis
            # p/all = todos períodos
            url = f"https://apisidra.ibge.gov.br/values/t/{table_id}/n1/all/v/all/p/all"
            
            yield Request(
                url,
                callback=self.parse_ibge_data,
                meta={
                    'dataset_id': f"{self.dataset_id}_{table_name}",
                    'table_id': table_id,
                    'table_name': table_name
                },
                headers={'Accept': 'application/json'},
                errback=self.errback_ibge
            )
    
    def parse_ibge_data(self, response):
        """Parse dados IBGE do JSON"""
        dataset_id = response.meta.get('dataset_id', self.dataset_id)
        table_name = response.meta.get('table_name', 'unknown')
        table_id = response.meta.get('table_id', '')
        
        try:
            data = json.loads(response.text)
            
            # IBGE retorna lista de objetos, primeiro item pode ser header
            if isinstance(data, list) and len(data) > 0:
                # Verificar se primeiro item é header
                if isinstance(data[0], dict) and 'D1N' in data[0]:
                    # Remover header se presente
                    if 'D1N' in data[0] and data[0].get('D1N') == 'Brasil':
                        pass  # Manter todos os dados
                
                if len(data) == 0:
                    logger.warning(f"No data received for {table_name} (table {table_id})")
                    return
            else:
                logger.warning(f"Unexpected data format for {table_name}")
                return
            
            # Salvar JSON bruto
            output_dir = Path('data/raw') / dataset_id
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"ibge_{table_name}.json"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Downloaded IBGE data: {output_path} ({len(data)} records)")
            
            yield {
                'dataset_id': dataset_id,
                'file_path': str(output_path),
                'url': response.url,
                'size': len(response.text),
                'filename': output_path.name,
                'file_type': 'json',
                'source': 'ibge',
                'table_name': table_name,
                'table_id': table_id,
                'records_count': len(data)
            }
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse IBGE JSON for {table_name}: {e}")
            logger.error(f"Response text (first 500 chars): {response.text[:500]}")
        except Exception as e:
            logger.error(f"Error processing IBGE data for {table_name}: {e}")
    
    def errback_ibge(self, failure):
        """Tratamento de erros"""
        table_name = failure.request.meta.get('table_name', 'unknown')
        logger.error(f"Failed to download IBGE data for {table_name}: {failure.request.url}")
        logger.error(f"Error: {failure.value}")

