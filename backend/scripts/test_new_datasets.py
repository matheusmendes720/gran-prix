"""Testar downloads dos novos datasets brasileiros."""
import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.pipeline.download_datasets import DatasetDownloader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_download(dataset_id: str):
    """Testar download de um dataset específico"""
    print(f"\n{'='*70}")
    print(f"TESTANDO DOWNLOAD: {dataset_id}")
    print(f"{'='*70}")
    
    downloader = DatasetDownloader()
    
    # Verificar se dataset existe no config
    datasets = downloader.config.get('datasets', {})
    if dataset_id not in datasets:
        print(f"❌ Dataset '{dataset_id}' não encontrado no config")
        print(f"Datasets disponíveis: {', '.join(datasets.keys())}")
        return False
    
    dataset_info = datasets[dataset_id]
    print(f"\nDataset: {dataset_info.get('name', dataset_id)}")
    print(f"Source: {dataset_info.get('source', 'N/A')}")
    print(f"URL: {dataset_info.get('url', 'N/A')}")
    print(f"Download Method: {dataset_info.get('download_method', 'direct')}")
    print(f"File Format: {dataset_info.get('file_format', 'N/A')}")
    
    # Tentar download
    try:
        result = downloader.download_all_datasets(selected_datasets=[dataset_id])
        success = result.get(dataset_id, False)
        
        if success:
            print(f"\n✅ Download bem-sucedido!")
            output_dir = downloader.raw_data_dir / dataset_id
            files = list(output_dir.glob('*')) if output_dir.exists() else []
            if files:
                print(f"Arquivos baixados:")
                for f in files:
                    size = f.stat().st_size / 1024  # KB
                    print(f"  - {f.name} ({size:.2f} KB)")
        else:
            print(f"\n❌ Download falhou")
            print(f"Verifique os logs para detalhes")
        
        return success
    except Exception as e:
        print(f"\n❌ Erro durante download: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Testar downloads dos datasets brasileiros"""
    
    # Datasets brasileiros para testar
    brazilian_datasets = [
        'zenodo_broadband_brazil',  # Deve funcionar (Zenodo)
        'anatel_mobile_brazil',      # Requer scraping
        'internet_aberta_forecast',   # PDF
        'springer_digital_divide',    # Artigo científico
    ]
    
    print("\n" + "="*70)
    print("TESTE DE DOWNLOADS - DATASETS BRASILEIROS")
    print("="*70)
    
    results = {}
    for dataset_id in brazilian_datasets:
        results[dataset_id] = test_download(dataset_id)
        print("\n")
    
    # Resumo
    print("\n" + "="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    successful = sum(1 for v in results.values() if v)
    total = len(results)
    
    for dataset_id, success in results.items():
        status = "✅ SUCESSO" if success else "❌ FALHOU"
        print(f"{status}: {dataset_id}")
    
    print(f"\nTotal: {successful}/{total} downloads bem-sucedidos")
    
    if successful < total:
        print("\n⚠️  Alguns downloads falharam. Isso é esperado para:")
        print("  - Anatel: Pode requerer scraping refinado")
        print("  - Internet Aberta: PDF requer parsing adicional")
        print("  - Springer: Pode requerer acesso/acordo")

if __name__ == "__main__":
    main()

