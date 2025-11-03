"""
Parser Avançado de PDFs com Múltiplas Bibliotecas
Tenta múltiplas estratégias para extrair dados de PDFs
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

class AdvancedPDFParser:
    """Parser avançado de PDFs usando múltiplas bibliotecas"""
    
    def __init__(self):
        self.parsers_available = self._check_available_parsers()
    
    def _check_available_parsers(self) -> Dict[str, bool]:
        """Verificar quais parsers estão disponíveis"""
        parsers = {
            'pdfplumber': False,
            'tabula': False,
            'camelot': False,
            'pypdf2': False,
        }
        
        try:
            import pdfplumber
            parsers['pdfplumber'] = True
        except ImportError:
            pass
        
        try:
            import tabula
            parsers['tabula'] = True
        except ImportError:
            pass
        
        try:
            import camelot
            parsers['camelot'] = True
        except ImportError:
            pass
        
        try:
            import PyPDF2
            parsers['pypdf2'] = True
        except ImportError:
            pass
        
        logger.info(f"Available PDF parsers: {[k for k, v in parsers.items() if v]}")
        
        return parsers
    
    def parse_pdf(self, pdf_path: Path, 
                  strategy: str = 'auto',
                  page_range: Optional[Tuple[int, int]] = None) -> pd.DataFrame:
        """
        Parsear PDF usando estratégia especificada ou auto-detectar melhor método
        
        Args:
            pdf_path: Caminho para arquivo PDF
            strategy: Estratégia ('auto', 'pdfplumber', 'tabula', 'camelot', 'combined')
            page_range: Tupla (start_page, end_page) ou None para todas
        
        Returns:
            DataFrame com dados extraídos
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        logger.info(f"Parsing PDF: {pdf_path.name}")
        logger.info(f"Strategy: {strategy}")
        
        if strategy == 'auto':
            # Tentar estratégias na ordem de preferência
            for parser_name in ['pdfplumber', 'tabula', 'camelot']:
                if self.parsers_available.get(parser_name):
                    try:
                        logger.info(f"Trying {parser_name}...")
                        df = self._parse_with_strategy(pdf_path, parser_name, page_range)
                        if df is not None and len(df) > 0:
                            logger.info(f"Successfully parsed with {parser_name}")
                            return df
                    except Exception as e:
                        logger.warning(f"{parser_name} failed: {e}")
                        continue
            
            # Fallback para PyPDF2 (extração de texto)
            if self.parsers_available.get('pypdf2'):
                logger.info("Falling back to PyPDF2 text extraction...")
                return self._parse_with_strategy(pdf_path, 'pypdf2', page_range)
        
        else:
            return self._parse_with_strategy(pdf_path, strategy, page_range)
        
        raise RuntimeError("No available PDF parser could extract data")
    
    def _parse_with_strategy(self, pdf_path: Path,
                             strategy: str,
                             page_range: Optional[Tuple[int, int]] = None) -> Optional[pd.DataFrame]:
        """Parsear usando estratégia específica"""
        
        if strategy == 'pdfplumber':
            return self._parse_pdfplumber(pdf_path, page_range)
        elif strategy == 'tabula':
            return self._parse_tabula(pdf_path, page_range)
        elif strategy == 'camelot':
            return self._parse_camelot(pdf_path, page_range)
        elif strategy == 'pypdf2':
            return self._parse_pypdf2(pdf_path, page_range)
        elif strategy == 'combined':
            return self._parse_combined(pdf_path, page_range)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _parse_pdfplumber(self, pdf_path: Path,
                         page_range: Optional[Tuple[int, int]] = None) -> pd.DataFrame:
        """Parsear com pdfplumber"""
        import pdfplumber
        
        all_tables = []
        
        with pdfplumber.open(pdf_path) as pdf:
            start_page = page_range[0] if page_range else 0
            end_page = page_range[1] if page_range else len(pdf.pages)
            
            for i in range(start_page, end_page):
                page = pdf.pages[i]
                tables = page.extract_tables()
                
                for table in tables:
                    if table:
                        df = pd.DataFrame(table[1:], columns=table[0] if table[0] else None)
                        all_tables.append(df)
        
        if all_tables:
            result = pd.concat(all_tables, ignore_index=True)
            return self._clean_extracted_data(result)
        
        return pd.DataFrame()
    
    def _parse_tabula(self, pdf_path: Path,
                     page_range: Optional[Tuple[int, int]] = None) -> pd.DataFrame:
        """Parsear com tabula-py"""
        import tabula
        
        start_page = (page_range[0] + 1) if page_range else 1
        end_page = (page_range[1] + 1) if page_range else None
        
        tables = tabula.read_pdf(
            str(pdf_path),
            pages=f"{start_page}-{end_page}" if end_page else str(start_page),
            multiple_tables=True
        )
        
        if tables:
            result = pd.concat(tables, ignore_index=True)
            return self._clean_extracted_data(result)
        
        return pd.DataFrame()
    
    def _parse_camelot(self, pdf_path: Path,
                      page_range: Optional[Tuple[int, int]] = None) -> pd.DataFrame:
        """Parsear com camelot"""
        import camelot
        
        pages = None
        if page_range:
            pages = ','.join(str(p + 1) for p in range(page_range[0], page_range[1] + 1))
        
        tables = camelot.read_pdf(str(pdf_path), pages=pages, flavor='lattice')
        
        if len(tables) > 0:
            all_tables = [table.df for table in tables]
            result = pd.concat(all_tables, ignore_index=True)
            return self._clean_extracted_data(result)
        
        return pd.DataFrame()
    
    def _parse_pypdf2(self, pdf_path: Path,
                     page_range: Optional[Tuple[int, int]] = None) -> pd.DataFrame:
        """Parsear com PyPDF2 (extração de texto)"""
        import PyPDF2
        
        text_data = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            start_page = page_range[0] if page_range else 0
            end_page = page_range[1] if page_range else len(pdf_reader.pages)
            
            for i in range(start_page, end_page):
                page = pdf_reader.pages[i]
                text = page.extract_text()
                
                # Tentar extrair tabelas do texto
                lines = text.split('\n')
                for line in lines:
                    # Buscar linhas que parecem dados tabulares
                    if '\t' in line or '  ' in line:
                        parts = [p.strip() for p in line.replace('\t', ' ').split('  ') if p.strip()]
                        if len(parts) > 1:
                            text_data.append(parts)
        
        if text_data:
            # Tentar criar DataFrame
            max_cols = max(len(row) for row in text_data)
            result = pd.DataFrame(text_data, columns=[f'col_{i}' for i in range(max_cols)])
            return self._clean_extracted_data(result)
        
        return pd.DataFrame()
    
    def _parse_combined(self, pdf_path: Path,
                       page_range: Optional[Tuple[int, int]] = None) -> pd.DataFrame:
        """Combinar resultados de múltiplos parsers"""
        all_results = []
        
        for parser_name in ['pdfplumber', 'tabula', 'camelot']:
            if self.parsers_available.get(parser_name):
                try:
                    df = self._parse_with_strategy(pdf_path, parser_name, page_range)
                    if df is not None and len(df) > 0:
                        all_results.append(df)
                except Exception as e:
                    logger.debug(f"{parser_name} failed: {e}")
        
        if all_results:
            # Combinar e remover duplicatas
            combined = pd.concat(all_results, ignore_index=True)
            combined = combined.drop_duplicates()
            return self._clean_extracted_data(combined)
        
        return pd.DataFrame()
    
    def _clean_extracted_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpar e estruturar dados extraídos"""
        if df.empty:
            return df
        
        # Remover linhas completamente vazias
        df = df.dropna(how='all')
        
        # Remover colunas completamente vazias
        df = df.dropna(axis=1, how='all')
        
        # Limpar espaços em branco
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        
        # Remover linhas duplicadas
        df = df.drop_duplicates()
        
        # Tentar converter tipos numéricos
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except:
                pass
        
        logger.info(f"Cleaned data: {len(df)} rows, {len(df.columns)} columns")
        
        return df
    
    def extract_tables_from_pdf(self, pdf_path: Path,
                                output_dir: Path,
                                page_range: Optional[Tuple[int, int]] = None) -> List[Path]:
        """
        Extrair todas as tabelas de um PDF e salvar como CSVs
        
        Returns:
            Lista de caminhos para CSVs criados
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        
        csv_files = []
        
        try:
            # Tentar extrair com pdfplumber primeiro
            if self.parsers_available.get('pdfplumber'):
                import pdfplumber
                
                with pdfplumber.open(pdf_path) as pdf:
                    start_page = page_range[0] if page_range else 0
                    end_page = page_range[1] if page_range else len(pdf.pages)
                    
                    table_num = 0
                    for i in range(start_page, end_page):
                        page = pdf.pages[i]
                        tables = page.extract_tables()
                        
                        for table in tables:
                            if table:
                                df = pd.DataFrame(table[1:], columns=table[0] if table[0] else None)
                                df = self._clean_extracted_data(df)
                                
                                if len(df) > 0:
                                    csv_path = output_dir / f"table_{i+1}_{table_num}.csv"
                                    df.to_csv(csv_path, index=False)
                                    csv_files.append(csv_path)
                                    table_num += 1
                                    
        except Exception as e:
            logger.error(f"Error extracting tables: {e}")
        
        logger.info(f"Extracted {len(csv_files)} tables from PDF")
        
        return csv_files

