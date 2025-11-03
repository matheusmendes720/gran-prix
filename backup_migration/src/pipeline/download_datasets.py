#!/usr/bin/env python3
"""
Dataset Download Script for Nova Corrente Demand Forecasting System
Downloads datasets from Kaggle API, Zenodo, MIT, and other sources
"""

import os
import json
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional
from tqdm import tqdm
import time

# Lazy import for Kaggle API (only import when needed)
KaggleApi = None

# Setup logging
project_root = Path(__file__).parent.parent.parent
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(project_root / 'data' / 'download.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatasetDownloader:
    """Main class for downloading datasets from multiple sources"""
    
    def __init__(self, config_path: str = None):
        # Get project root (2 levels up from src/pipeline)
        project_root = Path(__file__).parent.parent.parent
        if config_path is None:
            config_path = str(project_root / "config" / "datasets_config.json")
        else:
            # If relative path, make it relative to project root
            if not Path(config_path).is_absolute():
                config_path = str(project_root / config_path)
        self.config_path = config_path
        self.project_root = project_root
        self.raw_data_dir = project_root / "data" / "raw"
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # Initialize Kaggle API if available
        self.kaggle_api = None
        self._init_kaggle_api()
    
    def _init_kaggle_api(self):
        """Initialize Kaggle API with credentials"""
        global KaggleApi
        
        project_root = Path(__file__).parent.parent.parent
        kaggle_config_path = project_root / "config" / "kaggle_config.json"
        
        if not kaggle_config_path.exists():
            logger.warning(
                f"Kaggle config not found at {kaggle_config_path}. "
                "Kaggle datasets will be skipped. "
                "See config/kaggle_config.json.template for instructions."
            )
            self.kaggle_api = None
            return
        
        try:
            # Lazy import Kaggle API
            if KaggleApi is None:
                from kaggle.api.kaggle_api_extended import KaggleApi
            
            with open(kaggle_config_path, 'r') as f:
                kaggle_creds = json.load(f)
            
            # Set environment variables for Kaggle API
            os.environ['KAGGLE_USERNAME'] = kaggle_creds['username']
            os.environ['KAGGLE_KEY'] = kaggle_creds['key']
            
            self.kaggle_api = KaggleApi()
            self.kaggle_api.authenticate()
            logger.info("Kaggle API authenticated successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kaggle API: {e}")
            self.kaggle_api = None
    
    def download_kaggle_dataset(self, dataset_name: str, output_dir: Path) -> bool:
        """Download dataset from Kaggle"""
        if not self.kaggle_api:
            logger.warning(f"Skipping Kaggle dataset {dataset_name} - API not initialized")
            return False
        
        try:
            logger.info(f"Downloading Kaggle dataset: {dataset_name}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Download dataset
            self.kaggle_api.dataset_download_files(
                dataset_name,
                path=str(output_dir),
                unzip=True
            )
            
            logger.info(f"Successfully downloaded {dataset_name} to {output_dir}")
            return True
        except Exception as e:
            logger.error(f"Failed to download Kaggle dataset {dataset_name}: {e}")
            return False
    
    def download_direct_url(self, url: str, output_path: Path, max_retries: int = 3) -> bool:
        """Download file from direct URL"""
        for attempt in range(max_retries):
            try:
                logger.info(f"Downloading from URL: {url} (attempt {attempt + 1}/{max_retries})")
                response = requests.get(url, stream=True, timeout=60)
                response.raise_for_status()
                
                # Get file size if available
                total_size = int(response.headers.get('content-length', 0))
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f, tqdm(
                    desc=output_path.name,
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024
                ) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
                
                logger.info(f"Successfully downloaded to {output_path}")
                return True
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to download from {url} after {max_retries} attempts")
                    return False
        
        return False
    
    def download_zenodo_dataset(self, record_url: str, output_dir: Path, dataset_info: Dict) -> bool:
        """Download dataset from Zenodo - extracts CSV file URL from record page"""
        try:
            import re
            from bs4 import BeautifulSoup
            
            logger.info(f"Downloading Zenodo dataset from: {record_url}")
            
            # Get record ID from URL
            record_match = re.search(r'/records/(\d+)', record_url)
            if not record_match:
                logger.error(f"Could not extract record ID from URL: {record_url}")
                return False
            
            record_id = record_match.group(1)
            
            # Try to extract CSV file URL from HTML
            # First, download the record page
            response = requests.get(record_url, timeout=60)
            response.raise_for_status()
            
            # Look for CSV file in the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find CSV download link
            csv_url = None
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if 'download=1' in href and '.csv' in href:
                    csv_url = href
                    if not csv_url.startswith('http'):
                        csv_url = f"https://zenodo.org{csv_url}"
                    break
            
            # Fallback: Try standard Zenodo download pattern
            if not csv_url:
                # Common pattern: /records/{id}/files/{filename}?download=1
                # Try to find filename from meta tags or use default
                filename = dataset_info.get('filename', 'output-step-bsId_1-2023_9_28_12_50_10.csv')
                csv_url = f"https://zenodo.org/records/{record_id}/files/{filename}?download=1"
                logger.info(f"Using fallback URL pattern: {csv_url}")
            else:
                logger.info(f"Found CSV URL in HTML: {csv_url}")
            
            # Download the CSV file
            filename = dataset_info.get('filename', csv_url.split('/')[-1].split('?')[0])
            output_path = output_dir / filename
            output_dir.mkdir(parents=True, exist_ok=True)
            
            return self.download_direct_url(csv_url, output_path)
            
        except ImportError:
            logger.warning("BeautifulSoup not available. Using simple URL pattern for Zenodo.")
            # Fallback without BeautifulSoup
            record_match = re.search(r'/records/(\d+)', record_url)
            if record_match:
                record_id = record_match.group(1)
                filename = dataset_info.get('filename', 'output-step-bsId_1-2023_9_28_12_50_10.csv')
                csv_url = f"https://zenodo.org/records/{record_id}/files/{filename}?download=1"
                output_path = output_dir / filename
                output_dir.mkdir(parents=True, exist_ok=True)
                return self.download_direct_url(csv_url, output_path)
            
            return False
        except Exception as e:
            logger.error(f"Failed to download Zenodo dataset: {e}")
            return False
    
    def download_github_dataset(self, repo_url: str, output_dir: Path, dataset_info: Dict) -> bool:
        """Download dataset from GitHub repository
        
        Handles different GitHub URL formats:
        - Repository URL: https://github.com/user/repo
        - Raw file URL: https://raw.githubusercontent.com/user/repo/branch/file
        - File in repo: https://github.com/user/repo/blob/branch/file
        """
        try:
            import re
            from urllib.parse import urlparse, unquote
            
            logger.info(f"Downloading GitHub dataset from: {repo_url}")
            
            # Check if URL is already a raw file
            if 'raw.githubusercontent.com' in repo_url:
                # Direct raw file download
                filename = repo_url.split('/')[-1] or "dataset.csv"
                output_path = output_dir / filename
                output_dir.mkdir(parents=True, exist_ok=True)
                return self.download_direct_url(repo_url, output_path)
            
            # Parse GitHub repository URL
            # Pattern: https://github.com/user/repo
            # Or: https://github.com/user/repo/tree/branch/path
            # Or: https://github.com/user/repo/blob/branch/path/file
            github_match = re.search(r'github\.com/([^/]+)/([^/]+)', repo_url)
            if not github_match:
                logger.error(f"Could not parse GitHub URL: {repo_url}")
                return False
            
            owner = github_match.group(1)
            repo = github_match.group(2).split('/')[0]  # Remove path after repo name
            
            # Check if URL points to a specific file
            if '/blob/' in repo_url or '/tree/' in repo_url:
                # Extract branch and file path
                path_match = re.search(r'/(?:blob|tree)/([^/]+)(?:/(.+))?', repo_url)
                if path_match:
                    branch = path_match.group(1)
                    file_path = path_match.group(2) if path_match.group(2) else ""
                    
                    # Construct raw GitHub URL
                    if file_path:
                        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
                        filename = file_path.split('/')[-1] or "dataset.csv"
                        output_path = output_dir / filename
                        output_dir.mkdir(parents=True, exist_ok=True)
                        return self.download_direct_url(raw_url, output_path)
            
            # Try to find data files in repository using GitHub API
            try:
                # Try to get repository contents
                api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
                response = requests.get(api_url, timeout=60)
                response.raise_for_status()
                contents = response.json()
                
                # Look for CSV, data, or dataset directories/files
                data_files = []
                for item in contents:
                    if item['type'] == 'file':
                        if item['name'].endswith(('.csv', '.json', '.parquet', '.zip', '.tar.gz')):
                            data_files.append(item)
                    elif item['type'] == 'dir':
                        if item['name'].lower() in ['data', 'dataset', 'datasets', 'files', 'sampledata']:
                            # Recursively search in data directory
                            sub_url = f"{api_url}/{item['name']}"
                            sub_response = requests.get(sub_url, timeout=60)
                            if sub_response.status_code == 200:
                                sub_contents = sub_response.json()
                                # Add files from subdirectory
                                data_files.extend([item for item in sub_contents if item['type'] == 'file' and 
                                                  item['name'].endswith(('.csv', '.json', '.parquet', '.zip', '.tar.gz', '.tsv'))])
                                # Recursively search subdirectories (like RAN_level, container_level, etc.)
                                for sub_item in sub_contents:
                                    if sub_item['type'] == 'dir':
                                        sub_sub_url = f"{sub_url}/{sub_item['name']}"
                                        try:
                                            sub_sub_response = requests.get(sub_sub_url, timeout=60)
                                            if sub_sub_response.status_code == 200:
                                                sub_sub_contents = sub_sub_response.json()
                                                data_files.extend([item for item in sub_sub_contents if item['type'] == 'file' and 
                                                                  item['name'].endswith(('.csv', '.json', '.parquet', '.zip', '.tar.gz', '.tsv'))])
                                        except:
                                            pass
                
                if data_files:
                    logger.info(f"Found {len(data_files)} data file(s) in repository")
                    # Download the first suitable file (or all if specified)
                    success_count = 0
                    for file_info in data_files[:5]:  # Limit to first 5 files
                        download_url = file_info['download_url']
                        if download_url:
                            filename = file_info['name']
                            output_path = output_dir / filename
                            output_dir.mkdir(parents=True, exist_ok=True)
                            if self.download_direct_url(download_url, output_path):
                                success_count += 1
                                logger.info(f"Downloaded: {filename}")
                    
                    return success_count > 0
                else:
                    logger.warning(f"No data files found in repository {owner}/{repo}")
                    logger.info(f"Repository URL: {repo_url}")
                    logger.info("You may need to manually specify the file path or download it manually")
                    return False
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"GitHub API request failed: {e}")
                # Fallback: try common file patterns
                logger.info("Trying common file patterns...")
                common_files = ['data.csv', 'dataset.csv', 'data.zip', 'dataset.zip']
                for filename in common_files:
                    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{filename}"
                    output_path = output_dir / filename
                    output_dir.mkdir(parents=True, exist_ok=True)
                    if self.download_direct_url(raw_url, output_path):
                        logger.info(f"Successfully downloaded using pattern: {filename}")
                        return True
                    # Try master branch
                    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{filename}"
                    if self.download_direct_url(raw_url, output_path):
                        logger.info(f"Successfully downloaded using pattern: {filename}")
                        return True
                
                logger.error(f"Could not download from GitHub repository: {repo_url}")
                logger.info("Please provide direct raw file URL or manual download may be required")
                return False
                
        except Exception as e:
            logger.error(f"Failed to download GitHub dataset: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return False
    
    def download_anatel_dataset(self, url: str, output_dir: Path, dataset_info: Dict) -> bool:
        """Download dataset from Anatel (Data Basis or similar)
        
        Anatel datasets are typically available via Data Basis portal
        which may require scraping or direct CSV download.
        """
        try:
            from bs4 import BeautifulSoup
            import re
            
            logger.info(f"Attempting to download Anatel dataset from: {url}")
            
            # Try to find direct CSV download link on the page
            response = requests.get(url, timeout=60)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for CSV download links
            csv_url = None
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text().lower()
                
                # Check for CSV download links
                if ('.csv' in href.lower() or 
                    'download' in text or 
                    'csv' in text or
                    'data' in text):
                    csv_url = href
                    if not csv_url.startswith('http'):
                        # Relative URL, make it absolute
                        from urllib.parse import urljoin
                        csv_url = urljoin(url, csv_url)
                    break
            
            # Fallback: try to find Data Basis API endpoint
            if not csv_url:
                # Data Basis often uses patterns like /api/datasets/{id}/download
                api_match = re.search(r'/dataset/([^/]+)', url)
                if api_match:
                    dataset_id = api_match.group(1)
                    api_url = f"https://data-basis.org/api/datasets/{dataset_id}/download"
                    logger.info(f"Trying Data Basis API: {api_url}")
                    csv_url = api_url
            
            if csv_url:
                filename = csv_url.split('/')[-1].split('?')[0] or f"{dataset_info.get('name', 'anatel_data')}.csv"
                output_path = output_dir / filename
                output_dir.mkdir(parents=True, exist_ok=True)
                
                logger.info(f"Found download URL: {csv_url}")
                return self.download_direct_url(csv_url, output_path)
            else:
                logger.warning(f"Could not find CSV download link for Anatel dataset")
                logger.info(f"URL: {url}")
                logger.info("You may need to manually download the CSV file from the Data Basis portal")
                return False
                
        except Exception as e:
            logger.error(f"Failed to download Anatel dataset: {e}")
            import traceback
            logger.debug(traceback.format_exc())
            return False
    
    def download_all_datasets(self, selected_datasets: Optional[List[str]] = None) -> Dict[str, bool]:
        """Download all datasets from configuration"""
        results = {}
        datasets = self.config.get('datasets', {})
        
        # Filter selected datasets if specified
        if selected_datasets:
            datasets = {k: v for k, v in datasets.items() if k in selected_datasets}
        
        logger.info(f"Starting download of {len(datasets)} datasets...")
        
        for dataset_id, dataset_info in datasets.items():
            source = dataset_info.get('source', 'unknown')
            output_dir = self.raw_data_dir / dataset_id
            success = False
            
            logger.info(f"\n{'='*70}")
            logger.info(f"Processing: {dataset_info.get('name', dataset_id)}")
            logger.info(f"Source: {source}")
            logger.info(f"{'='*70}")
            
            try:
                if source == 'kaggle':
                    dataset_name = dataset_info.get('dataset')
                    if dataset_name:
                        success = self.download_kaggle_dataset(dataset_name, output_dir)
                    else:
                        logger.warning(f"No dataset name found for {dataset_id}")
                
                elif source == 'zenodo':
                    url = dataset_info.get('url')
                    if url:
                        success = self.download_zenodo_dataset(url, output_dir, dataset_info)
                    else:
                        logger.warning(f"No URL found for {dataset_id}")
                        success = False
                
                elif source == 'github':
                    url = dataset_info.get('url')
                    if url:
                        success = self.download_github_dataset(url, output_dir, dataset_info)
                    else:
                        logger.warning(f"No URL found for {dataset_id}")
                        success = False
                
                elif source in ['mit', 'direct', 'anatel', 'internet_aberta', 'springer']:
                    url = dataset_info.get('url')
                    download_method = dataset_info.get('download_method', 'direct')
                    file_format = dataset_info.get('file_format', None)
                    
                    if not url:
                        logger.warning(f"No URL found for {dataset_id}")
                        continue
                    
                    if download_method == 'direct':
                        # Try to get filename from URL or use default
                        filename = url.split('/')[-1] or f"{dataset_id}.zip"
                        # Remove query parameters
                        filename = filename.split('?')[0]
                        
                        # Use file_format from config if specified
                        if file_format and not filename.endswith(f'.{file_format}'):
                            filename = f"{dataset_id}.{file_format}"
                        
                        output_path = output_dir / filename
                        output_dir.mkdir(parents=True, exist_ok=True)
                        success = self.download_direct_url(url, output_path)
                        
                        # If PDF, attempt to extract tables
                        if success and file_format == 'pdf':
                            logger.info(f"PDF downloaded. Consider using PDF parsing tools for {dataset_id}")
                            logger.info(f"Tools: pdfplumber, tabula-py, or camelot for table extraction")
                    
                    elif download_method == 'scrape':
                        # Use Scrapy integration for scraping
                        try:
                            from src.pipeline.scrapy_integration import ScrapyIntegration
                            scrapy_integration = ScrapyIntegration(config_path=self.config_path)
                            success = scrapy_integration.run_scrapy_spider(dataset_id, dataset_info)
                            
                            if not success:
                                # Fallback to manual scraping methods
                                if source == 'anatel':
                                    success = self.download_anatel_dataset(url, output_dir, dataset_info)
                                else:
                                    logger.warning(f"Scraping failed for {dataset_id}")
                                    logger.info(f"Manual download may be required from: {url}")
                        except ImportError:
                            logger.warning("Scrapy not available, using fallback methods")
                            if source == 'anatel':
                                success = self.download_anatel_dataset(url, output_dir, dataset_info)
                            else:
                                logger.warning(f"Scraping not yet implemented for {dataset_id}")
                                success = False
                    else:
                        output_path = output_dir / "dataset.zip"
                        output_dir.mkdir(parents=True, exist_ok=True)
                        success = self.download_direct_url(url, output_path)
                
                else:
                    logger.warning(f"Unknown source type: {source} for {dataset_id}")
                
            except Exception as e:
                logger.error(f"Unexpected error downloading {dataset_id}: {e}")
                success = False
            
            results[dataset_id] = success
            
            # Brief pause between downloads to be respectful
            time.sleep(1)
        
        # Summary
        logger.info(f"\n{'='*70}")
        logger.info("DOWNLOAD SUMMARY")
        logger.info(f"{'='*70}")
        successful = sum(1 for v in results.values() if v)
        total = len(results)
        logger.info(f"Successful: {successful}/{total}")
        
        for dataset_id, success in results.items():
            status = "SUCCESS" if success else "FAILED"
            logger.info(f"  {status}: {dataset_id}")
        
        return results

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Download datasets for Nova Corrente demand forecasting'
    )
    parser.add_argument(
        '--datasets',
        nargs='+',
        help='Specific datasets to download (by ID). If not specified, downloads all.'
    )
    parser.add_argument(
        '--config',
        default='config/datasets_config.json',
        help='Path to datasets configuration file'
    )
    
    args = parser.parse_args()
    
    downloader = DatasetDownloader(config_path=args.config)
    results = downloader.download_all_datasets(selected_datasets=args.datasets)
    
    # Exit with error if any downloads failed
    if not all(results.values()):
        logger.warning("Some downloads failed. Check logs for details.")
        exit(1)

if __name__ == "__main__":
    main()


