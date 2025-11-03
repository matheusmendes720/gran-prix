#!/usr/bin/env python3
"""
Data Loader for Expanded Brazilian Metrics
Nova Corrente ML System - Database Integration

Loads collected API data and scraped data into ML-ready database tables.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional
import json
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ExpandedMetricsLoader:
    """
    Loader for expanded Brazilian metrics into database
    """
    
    def __init__(self, db_config: Optional[Dict] = None):
        """
        Initialize loader with database configuration
        
        Args:
            db_config: Database configuration dict. If None, reads from env vars.
        """
        if db_config:
            self.db_config = db_config
        else:
            self.db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'database': os.getenv('DB_NAME', 'STOCK'),
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD', ''),
                'port': int(os.getenv('DB_PORT', 3306))
            }
        
        self.connection = None
        self.data_dir = Path("./data/raw/brazilian_apis")
    
    def connect(self):
        """Connect to database"""
        try:
            self.connection = mysql.connector.connect(**self.db_config)
            if self.connection.is_connected():
                logger.info("✅ Connected to database")
                return True
        except Error as e:
            logger.error(f"❌ Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("✅ Disconnected from database")
    
    # ============================================
    # LOAD EXTENDED ECONOMIC DATA
    # ============================================
    
    def load_bacen_extended(self, data: Dict) -> bool:
        """Load extended BACEN economic data"""
        logger.info("📊 Loading extended BACEN data...")
        
        try:
            cursor = self.connection.cursor()
            
            # Merge all BACEN series into single table
            all_series = []
            for series_name, df in data.items():
                if isinstance(df, pd.DataFrame) and not df.empty:
                    df['series_name'] = series_name
                    all_series.append(df)
            
            if all_series:
                combined_df = pd.concat(all_series, ignore_index=True)
                
                # Map to IndicadoresEconomicosExtended table
                for _, row in combined_df.iterrows():
                    insert_query = """
                    INSERT INTO IndicadoresEconomicosExtended (
                        data_referencia, taxa_inflacao, taxa_cambio_brl_usd, taxa_selic
                    ) VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        taxa_inflacao = VALUES(taxa_inflacao),
                        taxa_cambio_brl_usd = VALUES(taxa_cambio_brl_usd),
                        taxa_selic = VALUES(taxa_selic)
                    """
                    
                    # Extract values based on series name
                    values = (
                        row.get('date', datetime.now().date()),
                        row.get('value', 0) if row.get('series_name') == 'IPCA' else None,
                        row.get('value', 0) if row.get('series_name') == 'USD_BRL_Exchange' else None,
                        row.get('value', 0) if row.get('series_name') == 'SELIC_Rate' else None
                    )
                    
                    cursor.execute(insert_query, values)
                
                self.connection.commit()
                logger.info(f"   ✅ Loaded {len(combined_df)} BACEN records")
                return True
            else:
                logger.warning("   ⚠️ No BACEN data to load")
                return False
                
        except Error as e:
            logger.error(f"   ❌ Error loading BACEN data: {e}")
            return False
    
    # ============================================
    # LOAD TRADE DATA
    # ============================================
    
    def load_comex_data(self, df: pd.DataFrame) -> bool:
        """Load COMEX trade data"""
        logger.info("📊 Loading COMEX trade data...")
        
        if df.empty:
            logger.warning("   ⚠️ No COMEX data to load")
            return False
        
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO DadosComex (
                data_referencia, importacoes_volume, importacoes_valor,
                exportacoes_volume, exportacoes_valor, saldo_comercial,
                atividade_portuaria, atrasos_alfandega
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                importacoes_volume = VALUES(importacoes_volume),
                importacoes_valor = VALUES(importacoes_valor),
                exportacoes_volume = VALUES(exportacoes_volume),
                exportacoes_valor = VALUES(exportacoes_valor),
                saldo_comercial = VALUES(saldo_comercial),
                atividade_portuaria = VALUES(atividade_portuaria),
                atrasos_alfandega = VALUES(atrasos_alfandega)
            """
            
            for _, row in df.iterrows():
                values = (
                    row.get('data_referencia', datetime.now().date()),
                    row.get('importacoes_volume', 0),
                    row.get('importacoes_valor', 0),
                    row.get('exportacoes_volume', 0),
                    row.get('exportacoes_valor', 0),
                    row.get('saldo_comercial', 0),
                    row.get('atividade_portuaria', 0),
                    row.get('atrasos_alfandega', 0)
                )
                cursor.execute(insert_query, values)
            
            self.connection.commit()
            logger.info(f"   ✅ Loaded {len(df)} COMEX records")
            return True
            
        except Error as e:
            logger.error(f"   ❌ Error loading COMEX data: {e}")
            return False
    
    # ============================================
    # LOAD TRANSPORT DATA
    # ============================================
    
    def load_transport_data(self, antt_df: pd.DataFrame, antaq_df: pd.DataFrame) -> bool:
        """Load transport data (ANTT and ANTAQ)"""
        logger.info("📊 Loading transport data...")
        
        success = True
        
        # Load ANTT data
        if not antt_df.empty:
            try:
                cursor = self.connection.cursor()
                
                insert_query = """
                INSERT INTO DadosTransporte (
                    data_referencia, volume_frete_rodoviario, custo_transporte,
                    desempenho_logistica, congestionamento_rodovias
                ) VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    volume_frete_rodoviario = VALUES(volume_frete_rodoviario),
                    custo_transporte = VALUES(custo_transporte),
                    desempenho_logistica = VALUES(desempenho_logistica),
                    congestionamento_rodovias = VALUES(congestionamento_rodovias)
                """
                
                for _, row in antt_df.iterrows():
                    values = (
                        row.get('data_referencia', datetime.now().date()),
                        row.get('volume_frete_rodoviario', 0),
                        row.get('custo_transporte', 0),
                        row.get('desempenho_logistica', 0),
                        row.get('congestionamento_rodovias', 0)
                    )
                    cursor.execute(insert_query, values)
                
                self.connection.commit()
                logger.info(f"   ✅ Loaded {len(antt_df)} ANTT records")
                
            except Error as e:
                logger.error(f"   ❌ Error loading ANTT data: {e}")
                success = False
        
        # Load ANTAQ data
        if not antaq_df.empty:
            try:
                cursor = self.connection.cursor()
                
                insert_query = """
                INSERT INTO DadosPortuarios (
                    data_referencia, porto, atividade_porto, volume_carga,
                    movimentacao_conteineres, congestionamento_porto, tempo_espera_medio
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    atividade_porto = VALUES(atividade_porto),
                    volume_carga = VALUES(volume_carga),
                    movimentacao_conteineres = VALUES(movimentacao_conteineres),
                    congestionamento_porto = VALUES(congestionamento_porto),
                    tempo_espera_medio = VALUES(tempo_espera_medio)
                """
                
                for _, row in antaq_df.iterrows():
                    values = (
                        row.get('data_referencia', datetime.now().date()),
                        row.get('porto', ''),
                        row.get('atividade_porto', 0),
                        row.get('volume_carga', 0),
                        row.get('movimentacao_conteineres', 0),
                        row.get('congestionamento_porto', 0),
                        row.get('tempo_espera_medio', 0)
                    )
                    cursor.execute(insert_query, values)
                
                self.connection.commit()
                logger.info(f"   ✅ Loaded {len(antaq_df)} ANTAQ records")
                
            except Error as e:
                logger.error(f"   ❌ Error loading ANTAQ data: {e}")
                success = False
        
        return success
    
    # ============================================
    # LOAD ALL DATA
    # ============================================
    
    def load_all(self, data: Dict) -> Dict:
        """
        Load all collected data into database
        
        Args:
            data: Dictionary with collected data from all sources
        
        Returns:
            Dictionary with load results
        """
        logger.info("🚀 Starting data loading into database...")
        
        if not self.connect():
            return {'status': 'failed', 'error': 'Database connection failed'}
        
        start_time = datetime.now()
        results = {
            'successful': [],
            'failed': [],
            'total_records': 0
        }
        
        try:
            # Load extended economic data
            if 'bacen_extended' in data:
                if self.load_bacen_extended(data['bacen_extended']):
                    results['successful'].append('bacen_extended')
                else:
                    results['failed'].append('bacen_extended')
            
            # Load trade data
            if 'comex' in data:
                if self.load_comex_data(data.get('comex', pd.DataFrame())):
                    results['successful'].append('comex')
                else:
                    results['failed'].append('comex')
            
            # Load transport data
            if 'antt' in data or 'antaq' in data:
                antt_df = data.get('antt', pd.DataFrame())
                antaq_df = data.get('antaq', pd.DataFrame())
                if self.load_transport_data(antt_df, antaq_df):
                    if 'antt' in data:
                        results['successful'].append('antt')
                    if 'antaq' in data:
                        results['successful'].append('antaq')
                else:
                    if 'antt' in data:
                        results['failed'].append('antt')
                    if 'antaq' in data:
                        results['failed'].append('antaq')
            
            # Summary
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"\n{'='*60}")
            logger.info("📊 LOADING SUMMARY")
            logger.info(f"{'='*60}")
            logger.info(f"✅ Successful: {len(results['successful'])}")
            logger.info(f"❌ Failed: {len(results['failed'])}")
            logger.info(f"⏱️ Duration: {duration:.1f} seconds")
            
            results['status'] = 'success'
            results['duration'] = duration
            
        except Exception as e:
            logger.error(f"❌ Error during data loading: {e}")
            results['status'] = 'failed'
            results['error'] = str(e)
        
        finally:
            self.disconnect()
        
        return results


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    # Example usage
    loader = ExpandedMetricsLoader()
    
    # Load from collected data files
    data_dir = Path("./data/raw/brazilian_apis")
    
    # Collect data from files
    data = {}
    
    # Load BACEN data
    bacen_file = data_dir / "bacen_extended.json"
    if bacen_file.exists():
        with open(bacen_file, 'r') as f:
            data['bacen_extended'] = json.load(f)
    
    # Load COMEX data
    comex_file = data_dir / "comex_scraped.csv"
    if comex_file.exists():
        data['comex'] = pd.read_csv(comex_file)
    
    # Load all data
    if data:
        results = loader.load_all(data)
        print(f"\n🎉 Data loading complete!")
        print(f"Results: {results}")
    else:
        print("⚠️ No data files found. Run data collection first.")

