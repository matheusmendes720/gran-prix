"""Testar parsing de PDFs."""
import sys
from pathlib import Path

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.pdf_parser import PDFParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_pdf_parsing(pdf_path: Path):
    """Testar parsing de um PDF"""
    print(f"\n{'='*70}")
    print(f"TESTANDO PARSING DE PDF")
    print(f"{'='*70}")
    print(f"PDF: {pdf_path}")
    
    if not pdf_path.exists():
        print(f"❌ Arquivo não encontrado: {pdf_path}")
        return False
    
    parser = PDFParser()
    
    if not parser.supported_libraries:
        print(f"❌ Nenhuma biblioteca de PDF disponível")
        print(f"Instale: pip install pdfplumber")
        return False
    
    print(f"\nBibliotecas disponíveis: {', '.join(parser.supported_libraries)}")
    
    # Tentar extrair tabelas
    print(f"\nExtraindo tabelas...")
    try:
        tables = parser.extract_tables(pdf_path, method='auto', pages=[0, 1, 2])
        
        if tables:
            print(f"\n✅ {len(tables)} tabela(s) extraída(s)")
            for i, table in enumerate(tables, 1):
                print(f"\nTabela {i}:")
                print(f"  Shape: {table.shape}")
                print(f"  Colunas: {list(table.columns)[:5]}...")  # Primeiras 5 colunas
                print(f"\n  Primeiras 3 linhas:")
                print(table.head(3).to_string())
        else:
            print(f"\n⚠️  Nenhuma tabela extraída")
            print(f"Tentando extrair texto...")
            text = parser.extract_text(pdf_path, pages=[0, 1])
            if text:
                print(f"\n✅ Texto extraído ({len(text)} caracteres)")
                print(f"\nPrimeiros 500 caracteres:")
                print(text[:500])
        
        return len(tables) > 0 or len(text) > 0 if 'text' in locals() else len(tables) > 0
        
    except Exception as e:
        print(f"\n❌ Erro durante parsing: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Testar parsing do PDF do Internet Aberta"""
    pdf_path = project_root / 'data/raw/internet_aberta_forecast' / 'Paper-1-EN-Data-Traffic-Demand-Forecast-for-Brazil.pdf'
    
    print("\n" + "="*70)
    print("TESTE DE PARSING DE PDF - Internet Aberta Forecast")
    print("="*70)
    
    success = test_pdf_parsing(pdf_path)
    
    print("\n" + "="*70)
    print("RESULTADO")
    print("="*70)
    if success:
        print("✅ Parsing bem-sucedido!")
        print("\nPróximos passos:")
        print("  1. Salvar tabelas extraídas como CSV")
        print("  2. Integrar ao preprocessing")
        print("  3. Mapear colunas para schema unificado")
    else:
        print("⚠️  Parsing pode ter falhado ou não encontrou tabelas")
        print("\nAlternativas:")
        print("  1. Instalar bibliotecas: pip install pdfplumber tabula-py")
        print("  2. Verificar se o PDF tem tabelas estruturadas")
        print("  3. Considerar extração manual para este dataset")

if __name__ == "__main__":
    main()

