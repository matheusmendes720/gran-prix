"""
Configurações do Scrapy para o projeto
"""
from pathlib import Path

# Scrapy settings
BOT_NAME = 'novacorrente_scrapy'

SPIDER_MODULES = ['src.scrapy.scrapy_spiders']
NEWSPIDER_MODULE = 'src.scrapy.scrapy_spiders'

# Obey robots.txt (pode ser desabilitado para scraping permitido)
ROBOTSTXT_OBEY = False

# Configure delays para respeitar sites
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = 0.5

# AutoThrottle settings
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
AUTOTHROTTLE_DEBUG = False

# Enable and configure the AutoThrottle extension
CONCURRENT_REQUESTS_PER_DOMAIN = 2
CONCURRENT_REQUESTS_PER_IP = 2

# User agent
USER_AGENT = 'NovaCorrente-DataCollector/1.0 (+https://github.com/novacorrente/demand-forecasting)'

# Enable pipelines
ITEM_PIPELINES = {
    'src.scrapy.scrapy_spiders.pipelines.ValidateFilePipeline': 300,
    'src.scrapy.scrapy_spiders.pipelines.DatasetMetadataPipeline': 800,
}

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = Path('data/raw/scrapy.log')

# Request settings
DOWNLOAD_TIMEOUT = 60
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# HTTP Cache (opcional - desabilitado por padrão)
HTTPCACHE_ENABLED = False

# Feed exports
FEEDS = {
    'data/raw/scrapy_items.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 2,
    },
}


