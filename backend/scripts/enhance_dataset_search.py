"""Script para buscar e estruturar mais datasets de forma inteligente."""
import sys
from pathlib import Path
import json
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import Dict, List

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class DatasetSearcher:
    """Classe para buscar e descobrir datasets estruturados"""
    
    def __init__(self, config_path='config/datasets_config.json'):
        self.config_path = Path(config_path)
        self.config = {}
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
    
    def search_zenodo(self, query: str, max_results: int = 10) -> List[Dict]:
        """Buscar datasets no Zenodo por query"""
        results = []
        try:
            # Zenodo API
            api_url = "https://zenodo.org/api/records"
            params = {
                'q': query,
                'type': 'dataset',
                'size': max_results,
                'sort': 'mostrecent'
            }
            
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            hits = data.get('hits', {}).get('hits', [])
            
            for hit in hits:
                metadata = hit.get('metadata', {})
                record = {
                    'id': hit.get('id'),
                    'title': metadata.get('title', ''),
                    'doi': metadata.get('doi', ''),
                    'url': hit.get('links', {}).get('html', ''),
                    'download_url': hit.get('links', {}).get('self', ''),
                    'creators': [c.get('name', '') for c in metadata.get('creators', [])],
                    'description': metadata.get('description', ''),
                    'keywords': metadata.get('keywords', []),
                    'publication_date': metadata.get('publication_date', ''),
                }
                
                # Buscar links de arquivos CSV/JSON
                files = hit.get('files', [])
                for file_info in files:
                    file_type = file_info.get('type', '')
                    if 'csv' in file_type.lower() or file_info.get('key', '').endswith('.csv'):
                        record['csv_file'] = file_info.get('links', {}).get('self', '')
                        break
                
                results.append(record)
                
        except Exception as e:
            logger.error(f"Error searching Zenodo: {e}")
        
        return results
    
    def search_github(self, query: str, max_results: int = 10) -> List[Dict]:
        """Buscar repositórios GitHub com datasets"""
        results = []
        try:
            # GitHub API (requer token para rate limit maior)
            api_url = "https://api.github.com/search/repositories"
            params = {
                'q': f"{query} dataset",
                'sort': 'updated',
                'per_page': max_results
            }
            
            headers = {}
            # Tentar usar token se disponível
            github_token = None
            if github_token:
                headers['Authorization'] = f'token {github_token}'
            
            response = requests.get(api_url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            items = data.get('items', [])
            
            for item in items:
                # Verificar se contém arquivos CSV/JSON
                repo_url = item.get('html_url', '')
                if self._repo_has_data_files(repo_url):
                    record = {
                        'id': item.get('id'),
                        'name': item.get('name', ''),
                        'full_name': item.get('full_name', ''),
                        'url': repo_url,
                        'description': item.get('description', ''),
                        'language': item.get('language', ''),
                        'stars': item.get('stargazers_count', 0),
                        'updated_at': item.get('updated_at', ''),
                    }
                    results.append(record)
                    
        except Exception as e:
            logger.error(f"Error searching GitHub: {e}")
        
        return results
    
    def _repo_has_data_files(self, repo_url: str) -> bool:
        """Verificar se repositório contém arquivos de dados"""
        try:
            # Tentar acessar página do repositório
            response = requests.get(repo_url, timeout=10)
            if response.status_code == 200:
                # Buscar por indicadores de datasets
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar links para arquivos CSV, JSON, etc.
                data_extensions = ['.csv', '.json', '.parquet', '.tsv', '.xlsx']
                for ext in data_extensions:
                    links = soup.find_all('a', href=re.compile(f'{ext}'))
                    if links:
                        return True
                        
                # Buscar por palavras-chave
                text = soup.get_text().lower()
                keywords = ['dataset', 'data', 'telecom', 'demand', 'forecast']
                if any(keyword in text for keyword in keywords):
                    return True
                    
        except:
            pass
        
        return False
    
    def search_kaggle(self, query: str, max_results: int = 10) -> List[Dict]:
        """Buscar datasets no Kaggle"""
        results = []
        try:
            from kaggle.api.kaggle_api_extended import KaggleApi
            
            api = KaggleApi()
            api.authenticate()
            
            # Buscar datasets
            datasets = api.dataset_list(search=query, max_size=max_results)
            
            for dataset in datasets:
                record = {
                    'ref': dataset.ref,
                    'title': dataset.title,
                    'subtitle': dataset.subtitle,
                    'url': f"https://www.kaggle.com/datasets/{dataset.ref}",
                    'size': dataset.size,
                    'download_count': dataset.downloadCount,
                    'usability_rating': dataset.usabilityRating,
                }
                results.append(record)
                
        except ImportError:
            logger.warning("Kaggle API not available. Install: pip install kaggle")
        except Exception as e:
            logger.error(f"Error searching Kaggle: {e}")
        
        return results
    
    def discover_anatel_datasets(self) -> List[Dict]:
        """Descobrir datasets disponíveis na Anatel/Data Basis"""
        results = []
        try:
            # Data Basis base URL
            base_url = "https://data-basis.org"
            datasets_url = f"{base_url}/datasets"
            
            response = requests.get(datasets_url, timeout=30)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar links de datasets (pode variar conforme estrutura do site)
                dataset_links = soup.find_all('a', href=re.compile(r'/dataset/'))
                
                for link in dataset_links[:20]:  # Limitar a 20
                    dataset_url = urljoin(base_url, link.get('href', ''))
                    title = link.get_text(strip=True)
                    
                    if title and 'dataset' in dataset_url.lower():
                        record = {
                            'title': title,
                            'url': dataset_url,
                            'source': 'anatel',
                        }
                        results.append(record)
                        
        except Exception as e:
            logger.error(f"Error discovering Anatel datasets: {e}")
        
        return results
    
    def suggest_datasets(self, keywords: List[str]) -> Dict[str, List[Dict]]:
        """Buscar datasets em múltiplas fontes baseado em keywords"""
        results = {
            'zenodo': [],
            'github': [],
            'kaggle': [],
            'anatel': [],
        }
        
        query = ' '.join(keywords) + ' brazil telecom'
        
        logger.info(f"Searching for datasets with keywords: {query}")
        
        # Buscar em Zenodo
        logger.info("Searching Zenodo...")
        results['zenodo'] = self.search_zenodo(query, max_results=10)
        
        # Buscar no GitHub
        logger.info("Searching GitHub...")
        results['github'] = self.search_github(query, max_results=10)
        
        # Buscar no Kaggle
        logger.info("Searching Kaggle...")
        results['kaggle'] = self.search_kaggle(query, max_results=10)
        
        # Descobrir Anatel
        logger.info("Discovering Anatel datasets...")
        results['anatel'] = self.discover_anatel_datasets()
        
        return results
    
    def save_discovered_datasets(self, results: Dict, output_file: str = 'data/raw/discovered_datasets.json'):
        """Salvar datasets descobertos"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Discovered datasets saved to: {output_path}")

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Buscar e descobrir datasets estruturados')
    parser.add_argument('--keywords', nargs='+', default=['telecom', 'demand', 'forecast'],
                       help='Keywords para busca')
    parser.add_argument('--output', default='data/raw/discovered_datasets.json',
                       help='Arquivo de saída para resultados')
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("DATASET DISCOVERY AND SEARCH")
    print("="*70 + "\n")
    
    searcher = DatasetSearcher()
    results = searcher.suggest_datasets(args.keywords)
    
    # Exibir resumo
    print("\n" + "="*70)
    print("DISCOVERY SUMMARY")
    print("="*70)
    
    for source, datasets in results.items():
        print(f"\n{source.upper()}: {len(datasets)} datasets found")
        for i, dataset in enumerate(datasets[:5], 1):  # Mostrar top 5
            title = dataset.get('title') or dataset.get('name') or dataset.get('full_name', 'N/A')
            print(f"  {i}. {title}")
            if dataset.get('url'):
                print(f"     URL: {dataset['url']}")
    
    print("\n" + "="*70 + "\n")
    
    # Salvar resultados
    searcher.save_discovered_datasets(results, args.output)
    
    print(f"✅ Results saved to: {args.output}")

if __name__ == "__main__":
    main()


