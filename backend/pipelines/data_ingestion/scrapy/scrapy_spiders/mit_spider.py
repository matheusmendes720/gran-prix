"""
Scrapy Spider for MIT Telecom Parts Dataset
Note: MIT dataset is in PDF format, so this spider provides framework
for potential web scraping if PDF content is published online.
"""

import scrapy
from scrapy.http import Request
from scrapy_spiders.items import DatasetItem


class MITTelecomSpider(scrapy.Spider):
    """
    Spider for extracting MIT Telecom Spare Parts data.
    
    Note: The MIT dataset is primarily in PDF format at:
    https://dspace.mit.edu/bitstream/handle/1721.1/142919/SCM12_Mamakos_project.pdf
    
    This spider provides a framework for:
    1. Downloading the PDF if hosted as web resource
    2. Parsing HTML versions if available
    3. Extracting metadata from MIT repository pages
    """
    
    name = 'mit_telecom'
    allowed_domains = ['dspace.mit.edu', 'mit.edu']
    start_urls = [
        'https://dspace.mit.edu/bitstream/handle/1721.1/142919/SCM12_Mamakos_project.pdf'
    ]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy_spiders.pipelines.MITDatasetPipeline': 300
        },
        'DOWNLOAD_DELAY': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': 0.5
    }
    
    def parse(self, response):
        """
        Parse MIT repository page or download PDF.
        
        For PDF files, scrapy will download them directly.
        For HTML pages, extract links to data files.
        """
        self.logger.info(f'Processing URL: {response.url}')
        
        # Check if response is PDF
        if response.headers.get('Content-Type', b'').decode().startswith('application/pdf'):
            self.logger.info('PDF file detected - saving for manual processing')
            
            # Save PDF file
            filename = 'SCM12_Mamakos_project.pdf'
            filepath = f'data/raw/mit_telecom_parts/{filename}'
            
            with open(filepath, 'wb') as f:
                f.write(response.body)
            
            self.logger.info(f'PDF saved to {filepath}')
            self.logger.warning(
                'PDF extraction requires manual processing or PDF parsing libraries. '
                'Consider using: PyPDF2, pdfplumber, or tabula-py'
            )
            
            yield {
                'type': 'pdf_downloaded',
                'filepath': filepath,
                'url': response.url
            }
            
        else:
            # Try to extract data links from HTML
            data_links = response.css('a[href*=".csv"], a[href*=".xlsx"], a[href*=".xls"]::attr(href)').getall()
            
            if data_links:
                for link in data_links:
                    yield Request(
                        response.urljoin(link),
                        callback=self.parse_data_file
                    )
            else:
                self.logger.warning('No data files found on page. PDF extraction may be required.')
    
    def parse_data_file(self, response):
        """Parse downloaded data files (CSV, Excel)"""
        self.logger.info(f'Parsing data file: {response.url}')
        
        # For CSV files, read and yield items
        if response.url.endswith('.csv'):
            # Note: Scrapy can handle CSV, but for large files,
            # consider saving directly and processing separately
            content = response.text
            lines = content.split('\n')
            
            # Skip header
            headers = lines[0].split(',') if lines else []
            
            for line in lines[1:]:
                if not line.strip():
                    continue
                
                values = line.split(',')
                if len(values) >= len(headers):
                    item = DatasetItem()
                    item['source'] = 'mit_telecom'
                    # Map CSV columns to item fields
                    # Adjust based on actual CSV structure
                    if 'Date' in headers:
                        item['date'] = values[headers.index('Date')]
                    if 'Part_ID' in headers or 'Item_ID' in headers:
                        col_name = 'Part_ID' if 'Part_ID' in headers else 'Item_ID'
                        item['item_id'] = values[headers.index(col_name)]
                    if 'Demand' in headers or 'Quantity' in headers:
                        col_name = 'Demand' if 'Demand' in headers else 'Quantity'
                        item['quantity'] = values[headers.index(col_name)]
                    if 'Site_ID' in headers:
                        item['site_id'] = values[headers.index('Site_ID')]
                    
                    yield item
        
        # For Excel files, save for processing
        elif response.url.endswith(('.xlsx', '.xls')):
            filename = response.url.split('/')[-1]
            filepath = f'data/raw/mit_telecom_parts/{filename}'
            
            with open(filepath, 'wb') as f:
                f.write(response.body)
            
            self.logger.info(f'Excel file saved to {filepath}')
            yield {
                'type': 'excel_downloaded',
                'filepath': filepath,
                'url': response.url
            }


class MITDatasetPipeline:
    """Pipeline for processing MIT dataset items"""
    
    def process_item(self, item, spider):
        # Additional processing can be added here
        return item



