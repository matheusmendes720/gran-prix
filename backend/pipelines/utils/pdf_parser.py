"""PDF parsing utilities for extracting tables and data from PDF datasets."""
import logging
from pathlib import Path
from typing import List, Optional, Dict
import pandas as pd

logger = logging.getLogger(__name__)

class PDFParser:
    """Parse PDF files to extract tables and data"""
    
    def __init__(self):
        self.supported_libraries = []
        self._check_libraries()
    
    def _check_libraries(self):
        """Check which PDF parsing libraries are available"""
        libraries = {
            'pdfplumber': False,
            'tabula': False,
            'camelot': False,
            'PyPDF2': False
        }
        
        for lib in libraries:
            try:
                if lib == 'tabula':
                    import tabula
                elif lib == 'pdfplumber':
                    import pdfplumber
                elif lib == 'camelot':
                    import camelot
                elif lib == 'PyPDF2':
                    import PyPDF2
                
                libraries[lib] = True
                self.supported_libraries.append(lib)
                logger.info(f"PDF library available: {lib}")
            except ImportError:
                logger.warning(f"PDF library not available: {lib}")
        
        if not self.supported_libraries:
            logger.error("No PDF parsing libraries available. Install pdfplumber, tabula-py, or camelot-py")
    
    def extract_tables_pdfplumber(self, pdf_path: Path, pages: Optional[List[int]] = None) -> List[pd.DataFrame]:
        """Extract tables from PDF using pdfplumber"""
        try:
            import pdfplumber
            
            tables = []
            with pdfplumber.open(str(pdf_path)) as pdf:
                page_numbers = pages if pages else range(len(pdf.pages))
                
                for page_num in page_numbers:
                    page = pdf.pages[page_num]
                    page_tables = page.extract_tables()
                    
                    for table in page_tables:
                        if table:
                            # Convert to DataFrame
                            df = pd.DataFrame(table[1:], columns=table[0])
                            tables.append(df)
                            logger.info(f"Extracted table from page {page_num + 1}: {df.shape}")
            
            return tables
        except Exception as e:
            logger.error(f"Error extracting tables with pdfplumber: {e}")
            return []
    
    def extract_tables_tabula(self, pdf_path: Path, pages: Optional[List[int]] = None) -> List[pd.DataFrame]:
        """Extract tables from PDF using tabula-py"""
        try:
            import tabula
            
            pages_str = ','.join(map(str, pages)) if pages else 'all'
            tables = tabula.read_pdf(str(pdf_path), pages=pages_str, multiple_tables=True)
            
            logger.info(f"Extracted {len(tables)} table(s) with tabula")
            return tables
        except Exception as e:
            logger.error(f"Error extracting tables with tabula: {e}")
            return []
    
    def extract_tables_camelot(self, pdf_path: Path, pages: Optional[str] = None) -> List[pd.DataFrame]:
        """Extract tables from PDF using camelot"""
        try:
            import camelot
            
            tables = camelot.read_pdf(str(pdf_path), pages=pages or 'all')
            
            dfs = [table.df for table in tables]
            logger.info(f"Extracted {len(dfs)} table(s) with camelot")
            return dfs
        except Exception as e:
            logger.error(f"Error extracting tables with camelot: {e}")
            return []
    
    def extract_tables(self, pdf_path: Path, method: str = 'auto', pages: Optional[List[int]] = None) -> List[pd.DataFrame]:
        """Extract tables from PDF using specified method
        
        Args:
            pdf_path: Path to PDF file
            method: Extraction method ('pdfplumber', 'tabula', 'camelot', or 'auto')
            pages: List of page numbers to extract (None for all pages)
        
        Returns:
            List of extracted DataFrames
        """
        if not pdf_path.exists():
            logger.error(f"PDF file not found: {pdf_path}")
            return []
        
        if method == 'auto':
            # Try libraries in order of preference
            if 'pdfplumber' in self.supported_libraries:
                method = 'pdfplumber'
            elif 'tabula' in self.supported_libraries:
                method = 'tabula'
            elif 'camelot' in self.supported_libraries:
                method = 'camelot'
            else:
                logger.error("No PDF parsing libraries available")
                return []
        
        logger.info(f"Extracting tables from PDF using {method}: {pdf_path}")
        
        if method == 'pdfplumber':
            return self.extract_tables_pdfplumber(pdf_path, pages)
        elif method == 'tabula':
            return self.extract_tables_tabula(pdf_path, pages)
        elif method == 'camelot':
            pages_str = ','.join(map(str, pages)) if pages else None
            return self.extract_tables_camelot(pdf_path, pages_str)
        else:
            logger.error(f"Unknown extraction method: {method}")
            return []
    
    def extract_text(self, pdf_path: Path, pages: Optional[List[int]] = None) -> str:
        """Extract text from PDF"""
        try:
            import pdfplumber
            
            text = ""
            with pdfplumber.open(str(pdf_path)) as pdf:
                page_numbers = pages if pages else range(len(pdf.pages))
                
                for page_num in page_numbers:
                    page = pdf.pages[page_num]
                    text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""
    
    def save_tables_to_csv(self, tables: List[pd.DataFrame], output_dir: Path, prefix: str = "table") -> List[Path]:
        """Save extracted tables to CSV files"""
        output_dir.mkdir(parents=True, exist_ok=True)
        saved_files = []
        
        for i, table in enumerate(tables):
            output_path = output_dir / f"{prefix}_{i+1}.csv"
            table.to_csv(output_path, index=False)
            saved_files.append(output_path)
            logger.info(f"Saved table {i+1} to: {output_path}")
        
        return saved_files

def main():
    """Test PDF parsing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Parse PDF files to extract tables')
    parser.add_argument('pdf_path', type=str, help='Path to PDF file')
    parser.add_argument('--method', choices=['pdfplumber', 'tabula', 'camelot', 'auto'], 
                       default='auto', help='Extraction method')
    parser.add_argument('--pages', type=str, help='Page numbers (comma-separated, e.g., "1,2,3")')
    parser.add_argument('--output', type=str, help='Output directory for CSV files')
    
    args = parser.parse_args()
    
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        return
    
    parser_obj = PDFParser()
    
    pages = None
    if args.pages:
        pages = [int(p) for p in args.pages.split(',')]
    
    tables = parser_obj.extract_tables(pdf_path, method=args.method, pages=pages)
    
    if tables:
        print(f"\nExtracted {len(tables)} table(s)")
        for i, table in enumerate(tables):
            print(f"\nTable {i+1}:")
            print(table.head())
        
        if args.output:
            output_dir = Path(args.output)
            saved_files = parser_obj.save_tables_to_csv(tables, output_dir)
            print(f"\nSaved {len(saved_files)} CSV file(s) to {output_dir}")
    else:
        print("No tables extracted from PDF")

if __name__ == "__main__":
    main()

