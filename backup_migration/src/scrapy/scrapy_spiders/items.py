"""
Scrapy Items para estruturar dados extraídos
"""
import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join

class DatasetItem(scrapy.Item):
    """Item base para datasets"""
    dataset_id = scrapy.Field()
    file_path = scrapy.Field()
    url = scrapy.Field()
    size = scrapy.Field()
    filename = scrapy.Field()
    file_type = scrapy.Field()
    download_date = scrapy.Field()
    
class AnatelItem(DatasetItem):
    """Item específico para dados Anatel"""
    region = scrapy.Field()
    technology = scrapy.Field()
    subscribers = scrapy.Field()
    period = scrapy.Field()

class ZenodoItem(DatasetItem):
    """Item específico para dados Zenodo"""
    record_id = scrapy.Field()
    record_title = scrapy.Field()
    authors = scrapy.Field()
    description = scrapy.Field()

class RepositoryItem(scrapy.Item):
    """Item para links de repositórios"""
    repository_url = scrapy.Field()
    article_url = scrapy.Field()
    dataset_id = scrapy.Field()
    type = scrapy.Field()
