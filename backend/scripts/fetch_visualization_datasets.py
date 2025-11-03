"""Script para buscar e baixar datasets específicos para visualização de telecom brasileira."""
import sys
from pathlib import Path
import logging
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline.download_datasets import DatasetDownloader
from src.utils.dataset_registry import DatasetRegistry
from scripts.enhance_dataset_search import DatasetSearcher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class VisualizationDatasetFetcher:
    """Classe especializada para buscar datasets de visualização de telecom brasileira"""
    
    def __init__(self):
        self.registry = DatasetRegistry()
        self.downloader = DatasetDownloader()
        self.searcher = DatasetSearcher()
        
        # Fontes específicas para visualização
        self.visualization_sources = {
            'anatel_mobile': {
                'name': 'Anatel Mobile Accesses',
                'url': 'https://data-basis.org/dataset/d3c86a88-d9a4-4fc0-bdec-08ab61e8f63c',
                'description': 'Mobile phone accesses by technology and region',
                'type': 'csv',
                'columns': ['Date', 'Subscribers', 'Technology', 'State', 'Region']
            },
            'anatel_broadband': {
                'name': 'Anatel Fixed Broadband',
                'url': 'https://data-basis.org/dataset',
                'description': 'Fixed broadband connections by speed and municipality',
                'type': 'csv',
                'columns': ['Date', 'Speed', 'Municipality', 'State', 'Connections']
            },
            'brazil_geojson': {
                'name': 'Brazil States GeoJSON',
                'url': 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.json',
                'description': 'GeoJSON file for Brazilian states map visualization',
                'type': 'geojson'
            },
            'brazil_topojson': {
                'name': 'Brazil States TopoJSON',
                'url': 'https://github.com/topojson/world-atlas',
                'description': 'TopoJSON for efficient map rendering',
                'type': 'topojson'
            },
            'net_data_directory': {
                'name': 'Net Data Directory Brazil',
                'url': 'https://netdatadirectory.org/node/2336',
                'description': 'Network data directory with Brazilian telecom metrics',
                'type': 'web'
            },
            'teleco_statistics': {
                'name': 'Teleco Mobile Statistics',
                'url': 'https://www.teleco.com.br/en/en_ncel.asp',
                'description': 'Mobile statistics and trends',
                'type': 'web'
            },
            'internet_aberta_forecast': {
                'name': 'Data Traffic Demand Forecast Brazil',
                'url': 'https://internetaberta.com.br/wp-content/uploads/2024/05/Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf',
                'description': 'Long-term forecast projections',
                'type': 'pdf'
            },
            'zenodo_broadband_customers': {
                'name': 'Broadband Customers Brazil',
                'url': 'https://zenodo.org/records/10482897',
                'description': 'Real dataset from Brazilian operator with customer metrics',
                'type': 'csv'
            }
        }
    
    def fetch_all_visualization_datasets(self):
        """Buscar e baixar todos os datasets de visualização"""
        print("\n" + "="*80)
        print("FETCHING VISUALIZATION DATASETS FOR BRAZILIAN TELECOM")
        print("="*80 + "\n")
        
        results = {
            'discovered': [],
            'downloaded': [],
            'failed': []
        }
        
        # Buscar em Zenodo por keywords específicas
        print("\n" + "="*80)
        print("STEP 1: SEARCHING ZENODO FOR VISUALIZATION DATASETS")
        print("="*80 + "\n")
        
        zenodo_keywords = [
            'brazil telecom',
            'brazil broadband',
            'brazil mobile',
            'anatel',
            'brazil network',
            'brazil 5G'
        ]
        
        zenodo_datasets = []
        for keyword in zenodo_keywords:
            print(f"Searching Zenodo for: {keyword}")
            datasets = self.searcher.search_zenodo(keyword, max_results=5)
            zenodo_datasets.extend(datasets)
            print(f"  Found {len(datasets)} datasets")
        
        # Remover duplicatas
        seen_ids = set()
        unique_datasets = []
        for ds in zenodo_datasets:
            ds_id = ds.get('id', str(ds.get('url', '')))
            if ds_id not in seen_ids:
                seen_ids.add(ds_id)
                unique_datasets.append(ds)
        
        print(f"\n[OK] Found {len(unique_datasets)} unique Zenodo datasets")
        results['discovered'].extend(unique_datasets)
        
        # Buscar datasets conhecidos
        print("\n" + "="*80)
        print("STEP 2: FETCHING KNOWN VISUALIZATION DATASETS")
        print("="*80 + "\n")
        
        for dataset_id, dataset_info in self.visualization_sources.items():
            print(f"\nProcessing: {dataset_info['name']}")
            print(f"URL: {dataset_info['url']}")
            
            try:
                success = self._fetch_visualization_dataset(dataset_id, dataset_info)
                if success:
                    results['downloaded'].append(dataset_id)
                    print(f"  [OK] Successfully fetched")
                else:
                    results['failed'].append(dataset_id)
                    print(f"  [FAIL] Failed to fetch")
            except Exception as e:
                logger.error(f"Error fetching {dataset_id}: {e}")
                results['failed'].append(dataset_id)
                print(f"  [ERROR] {e}")
        
        # Registrar datasets descobertos
        if unique_datasets:
            discovered_dict = {'zenodo': unique_datasets}
            self.registry.discover_and_register(discovered_dict)
        
        # Resumo
        print("\n" + "="*80)
        print("FETCH SUMMARY")
        print("="*80)
        print(f"Discovered: {len(results['discovered'])}")
        print(f"Downloaded: {len(results['downloaded'])}")
        print(f"Failed: {len(results['failed'])}")
        print("="*80 + "\n")
        
        return results
    
    def _fetch_visualization_dataset(self, dataset_id: str, dataset_info: dict) -> bool:
        """Buscar dataset específico de visualização"""
        url = dataset_info['url']
        dataset_type = dataset_info.get('type', 'csv')
        output_dir = Path('data/raw') / f'visualization_{dataset_id}'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            if dataset_type == 'csv':
                # Tentar download direto
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    # Verificar se é CSV
                    if 'csv' in response.headers.get('content-type', '').lower() or url.endswith('.csv'):
                        output_path = output_dir / f"{dataset_id}.csv"
                        with open(output_path, 'wb') as f:
                            f.write(response.content)
                        return True
            
            elif dataset_type in ['geojson', 'topojson', 'json']:
                # Download de arquivos geoespaciais
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    ext = '.json' if dataset_type == 'geojson' else '.topojson'
                    output_path = output_dir / f"{dataset_id}{ext}"
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    return True
            
            elif dataset_type == 'pdf':
                # Download de PDF
                response = requests.get(url, timeout=60)
                if response.status_code == 200:
                    output_path = output_dir / f"{dataset_id}.pdf"
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    return True
            
            elif dataset_type == 'web':
                # Web scraping para extrair dados
                return self._scrape_web_dataset(url, dataset_id, output_dir)
            
        except Exception as e:
            logger.error(f"Error fetching {dataset_id}: {e}")
            return False
        
        return False
    
    def _scrape_web_dataset(self, url: str, dataset_id: str, output_dir: Path) -> bool:
        """Fazer scraping de página web para extrair dados"""
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                return False
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar links para CSV ou dados
            csv_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                if any(ext in href.lower() for ext in ['.csv', '.xlsx', '.json', '.data']):
                    full_url = urljoin(url, href)
                    csv_links.append(full_url)
            
            if csv_links:
                # Baixar primeiro link encontrado
                csv_url = csv_links[0]
                csv_response = requests.get(csv_url, timeout=30)
                if csv_response.status_code == 200:
                    output_path = output_dir / f"{dataset_id}.csv"
                    with open(output_path, 'wb') as f:
                        f.write(csv_response.content)
                    return True
            
            # Tentar extrair tabelas HTML
            tables = soup.find_all('table')
            if tables:
                import pandas as pd
                df = pd.read_html(str(tables[0]))[0]
                output_path = output_dir / f"{dataset_id}.csv"
                df.to_csv(output_path, index=False)
                return True
            
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
        
        return False
    
    def fetch_geospatial_data(self):
        """Buscar dados geoespaciais para visualização"""
        print("\n" + "="*80)
        print("FETCHING GEOSPATIAL DATA FOR VISUALIZATIONS")
        print("="*80 + "\n")
        
        geospatial_dir = Path('data/raw/geospatial')
        geospatial_dir.mkdir(parents=True, exist_ok=True)
        
        geospatial_sources = {
            'brazil_states_geojson': {
                'url': 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.json',
                'filename': 'brazil-states.json'
            },
            'brazil_municipalities': {
                'url': 'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojson-uf/',
                'filename': 'brazil-municipalities.json'
            },
            'world_atlas_topojson': {
                'url': 'https://cdn.jsdelivr.net/npm/world-atlas@2/world/110m.json',
                'filename': 'world-110m.json'
            }
        }
        
        results = []
        
        for name, source in geospatial_sources.items():
            print(f"Downloading: {name}")
            try:
                response = requests.get(source['url'], timeout=30)
                if response.status_code == 200:
                    output_path = geospatial_dir / source['filename']
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"  [OK] Saved to: {output_path}")
                    results.append(name)
                else:
                    print(f"  [FAIL] HTTP {response.status_code}")
            except Exception as e:
                print(f"  [ERROR] {e}")
        
        print(f"\n[OK] Downloaded {len(results)} geospatial files")
        return results

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Buscar datasets de visualização')
    parser.add_argument('--geospatial', action='store_true',
                       help='Buscar dados geoespaciais')
    parser.add_argument('--visualization', action='store_true', default=True,
                       help='Buscar datasets de visualização')
    
    args = parser.parse_args()
    
    fetcher = VisualizationDatasetFetcher()
    
    if args.visualization:
        fetcher.fetch_all_visualization_datasets()
    
    if args.geospatial:
        fetcher.fetch_geospatial_data()
    
    print("\n[OK] Fetch complete!")

if __name__ == "__main__":
    main()

