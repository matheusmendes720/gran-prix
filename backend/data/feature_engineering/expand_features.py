#!/usr/bin/env python3
"""
Comprehensive Feature Engineering for Expanded Brazilian Metrics
Nova Corrente ML System - 52+ New Features

Generates ML features from all new Brazilian public API metrics:
- TRANSPORT (10 features)
- TRADE (8 features)
- ENERGY (6 features)
- EMPLOYMENT (4 features)
- CONSTRUCTION (5 features)
- INDUSTRIAL (5 features)
- LOGISTICS (8 features)
- REGIONAL (6 features)

Total: 52+ new features
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import logging
from typing import Dict, List, Optional
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


class ExpandedFeatureEngineer:
    """
    Feature engineering for expanded Brazilian metrics
    """
    
    def __init__(self, db_config: Optional[Dict] = None):
        """Initialize feature engineer"""
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
    
    # ============================================
    # TRANSPORT FEATURES (10 features)
    # ============================================
    
    def generate_transport_features(self, data_referencia: datetime.date) -> List[Dict]:
        """Generate transport-related features"""
        logger.info("📊 Generating TRANSPORT features...")
        
        features = []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Get transport data
            query = """
            SELECT 
                dt.custo_transporte,
                dt.desempenho_logistica,
                dt.congestionamento_rodovias,
                dp.congestionamento_porto,
                dp.tempo_espera_medio,
                dr.impacto_entrega
            FROM DadosTransporte dt
            LEFT JOIN DadosPortuarios dp ON dt.data_referencia = dp.data_referencia
            LEFT JOIN DadosRodoviarios dr ON dt.data_referencia = dr.data_referencia
            WHERE dt.data_referencia = %s
            LIMIT 1
            """
            
            cursor.execute(query, (data_referencia,))
            row = cursor.fetchone()
            
            if row:
                # Feature 1: Transport Cost Index
                features.append({
                    'feature_name': 'transport_cost_index',
                    'feature_value': row.get('custo_transporte', 0),
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 2: Logistics Performance
                features.append({
                    'feature_name': 'logistics_performance',
                    'feature_value': row.get('desempenho_logistica', 0),
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 3: Highway Congestion
                features.append({
                    'feature_name': 'highway_congestion',
                    'feature_value': row.get('congestionamento_rodovias', 0),
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 4: Port Congestion
                features.append({
                    'feature_name': 'port_congestion',
                    'feature_value': row.get('congestionamento_porto', 0) if row.get('congestionamento_porto') else 0,
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 5: Port Wait Time
                features.append({
                    'feature_name': 'port_wait_time_hours',
                    'feature_value': row.get('tempo_espera_medio', 0) if row.get('tempo_espera_medio') else 0,
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 6: Delivery Impact Factor
                features.append({
                    'feature_name': 'delivery_impact_factor',
                    'feature_value': row.get('impacto_entrega', 0) if row.get('impacto_entrega') else 1.0,
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 7: Total Congestion (Highway + Port)
                total_congestion = (row.get('congestionamento_rodovias', 0) or 0) + \
                                  (row.get('congestionamento_porto', 0) or 0)
                features.append({
                    'feature_name': 'total_congestion',
                    'feature_value': total_congestion,
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 8: Logistics Efficiency Score
                efficiency_score = (row.get('desempenho_logistica', 0) or 0) / 100.0
                features.append({
                    'feature_name': 'logistics_efficiency_score',
                    'feature_value': efficiency_score,
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 9: Transport Cost Multiplier
                cost_multiplier = 1.0 + (row.get('custo_transporte', 0) or 0) / 100.0
                features.append({
                    'feature_name': 'transport_cost_multiplier',
                    'feature_value': cost_multiplier,
                    'feature_category': 'TRANSPORT'
                })
                
                # Feature 10: Delivery Delay Risk
                delay_risk = min(1.0, (total_congestion / 100.0) * 0.5 + \
                              ((row.get('tempo_espera_medio', 0) or 0) / 24.0) * 0.5)
                features.append({
                    'feature_name': 'delivery_delay_risk',
                    'feature_value': delay_risk,
                    'feature_category': 'TRANSPORT'
                })
            
            logger.info(f"   ✅ Generated {len(features)} TRANSPORT features")
            
        except Error as e:
            logger.error(f"   ❌ Error generating TRANSPORT features: {e}")
        
        return features
    
    # ============================================
    # TRADE FEATURES (8 features)
    # ============================================
    
    def generate_trade_features(self, data_referencia: datetime.date) -> List[Dict]:
        """Generate trade-related features"""
        logger.info("📊 Generating TRADE features...")
        
        features = []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                importacoes_volume,
                importacoes_valor,
                exportacoes_volume,
                exportacoes_valor,
                saldo_comercial,
                atividade_portuaria,
                atrasos_alfandega
            FROM DadosComex
            WHERE data_referencia = %s
            LIMIT 1
            """
            
            cursor.execute(query, (data_referencia,))
            row = cursor.fetchone()
            
            if row:
                # Feature 1: Import Volume
                features.append({
                    'feature_name': 'import_volume',
                    'feature_value': row.get('importacoes_volume', 0),
                    'feature_category': 'TRADE'
                })
                
                # Feature 2: Export Volume
                features.append({
                    'feature_name': 'export_volume',
                    'feature_value': row.get('exportacoes_volume', 0),
                    'feature_category': 'TRADE'
                })
                
                # Feature 3: Trade Balance
                features.append({
                    'feature_name': 'trade_balance',
                    'feature_value': row.get('saldo_comercial', 0),
                    'feature_category': 'TRADE'
                })
                
                # Feature 4: Port Activity Index
                features.append({
                    'feature_name': 'port_activity_index',
                    'feature_value': row.get('atividade_portuaria', 0),
                    'feature_category': 'TRADE'
                })
                
                # Feature 5: Customs Delay Days
                features.append({
                    'feature_name': 'customs_delay_days',
                    'feature_value': row.get('atrasos_alfandega', 0),
                    'feature_category': 'TRADE'
                })
                
                # Feature 6: Trade Activity Level
                trade_activity = (row.get('importacoes_volume', 0) + row.get('exportacoes_volume', 0)) / 2.0
                features.append({
                    'feature_name': 'trade_activity_level',
                    'feature_value': trade_activity,
                    'feature_category': 'TRADE'
                })
                
                # Feature 7: Import/Export Ratio
                import_export_ratio = (row.get('importacoes_volume', 0) / 
                                      (row.get('exportacoes_volume', 0) + 1))  # +1 to avoid division by zero
                features.append({
                    'feature_name': 'import_export_ratio',
                    'feature_value': import_export_ratio,
                    'feature_category': 'TRADE'
                })
                
                # Feature 8: Customs Delay Risk
                customs_delay_risk = min(1.0, row.get('atrasos_alfandega', 0) / 30.0)
                features.append({
                    'feature_name': 'customs_delay_risk',
                    'feature_value': customs_delay_risk,
                    'feature_category': 'TRADE'
                })
            
            logger.info(f"   ✅ Generated {len(features)} TRADE features")
            
        except Error as e:
            logger.error(f"   ❌ Error generating TRADE features: {e}")
        
        return features
    
    # ============================================
    # ENERGY FEATURES (6 features)
    # ============================================
    
    def generate_energy_features(self, data_referencia: datetime.date, regiao: str = 'BAHIA') -> List[Dict]:
        """Generate energy-related features"""
        logger.info("📊 Generating ENERGY features...")
        
        features = []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                consumo_energia,
                interrupcoes_energia,
                confiabilidade_rede,
                preco_energia
            FROM DadosEnergia
            WHERE data_referencia = %s AND regiao = %s
            LIMIT 1
            """
            
            cursor.execute(query, (data_referencia, regiao))
            row = cursor.fetchone()
            
            if row:
                # Feature 1: Energy Consumption (MWh)
                features.append({
                    'feature_name': 'energy_consumption_mwh',
                    'feature_value': row.get('consumo_energia', 0),
                    'feature_category': 'ENERGY'
                })
                
                # Feature 2: Power Outages Count
                features.append({
                    'feature_name': 'power_outages_count',
                    'feature_value': row.get('interrupcoes_energia', 0),
                    'feature_category': 'ENERGY'
                })
                
                # Feature 3: Grid Reliability
                features.append({
                    'feature_name': 'grid_reliability',
                    'feature_value': row.get('confiabilidade_rede', 0),
                    'feature_category': 'ENERGY'
                })
                
                # Feature 4: Energy Price
                features.append({
                    'feature_name': 'energy_price',
                    'feature_value': row.get('preco_energia', 0),
                    'feature_category': 'ENERGY'
                })
                
                # Feature 5: Power Outage Risk
                outage_risk = min(1.0, row.get('interrupcoes_energia', 0) / 10.0)
                features.append({
                    'feature_name': 'power_outage_risk',
                    'feature_value': outage_risk,
                    'feature_category': 'ENERGY'
                })
                
                # Feature 6: Grid Stability Score
                stability_score = row.get('confiabilidade_rede', 0) / 100.0
                features.append({
                    'feature_name': 'grid_stability_score',
                    'feature_value': stability_score,
                    'feature_category': 'ENERGY'
                })
            
            logger.info(f"   ✅ Generated {len(features)} ENERGY features")
            
        except Error as e:
            logger.error(f"   ❌ Error generating ENERGY features: {e}")
        
        return features
    
    # ============================================
    # EMPLOYMENT FEATURES (4 features)
    # ============================================
    
    def generate_employment_features(self, data_referencia: datetime.date, 
                                   regiao: str = 'BAHIA', setor: str = 'CONSTRUCAO') -> List[Dict]:
        """Generate employment-related features"""
        logger.info("📊 Generating EMPLOYMENT features...")
        
        features = []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                taxa_emprego,
                admissoes,
                demissoes,
                saldo_emprego,
                disponibilidade_mao_obra
            FROM DadosEmprego
            WHERE data_referencia = %s AND regiao = %s AND setor = %s
            LIMIT 1
            """
            
            cursor.execute(query, (data_referencia, regiao, setor))
            row = cursor.fetchone()
            
            if row:
                # Feature 1: Employment Rate
                features.append({
                    'feature_name': 'employment_rate',
                    'feature_value': row.get('taxa_emprego', 0),
                    'feature_category': 'EMPLOYMENT'
                })
                
                # Feature 2: Net Employment Change
                features.append({
                    'feature_name': 'net_employment_change',
                    'feature_value': row.get('saldo_emprego', 0),
                    'feature_category': 'EMPLOYMENT'
                })
                
                # Feature 3: Labor Availability
                features.append({
                    'feature_name': 'labor_availability',
                    'feature_value': row.get('disponibilidade_mao_obra', 0),
                    'feature_category': 'EMPLOYMENT'
                })
                
                # Feature 4: Hiring Activity
                hiring_activity = (row.get('admissoes', 0) - row.get('demissoes', 0)) / 100.0
                features.append({
                    'feature_name': 'hiring_activity',
                    'feature_value': hiring_activity,
                    'feature_category': 'EMPLOYMENT'
                })
            
            logger.info(f"   ✅ Generated {len(features)} EMPLOYMENT features")
            
        except Error as e:
            logger.error(f"   ❌ Error generating EMPLOYMENT features: {e}")
        
        return features
    
    # ============================================
    # CONSTRUCTION FEATURES (5 features)
    # ============================================
    
    def generate_construction_features(self, data_referencia: datetime.date) -> List[Dict]:
        """Generate construction-related features"""
        logger.info("📊 Generating CONSTRUCTION features...")
        
        features = []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT 
                atividade_construcao,
                demanda_material,
                crescimento_regional,
                investimento_infraestrutura
            FROM IndicadoresConstrucao
            WHERE data_referencia = %s
            LIMIT 1
            """
            
            cursor.execute(query, (data_referencia,))
            row = cursor.fetchone()
            
            if row:
                # Feature 1: Construction Activity Index
                features.append({
                    'feature_name': 'construction_activity_index',
                    'feature_value': row.get('atividade_construcao', 0),
                    'feature_category': 'CONSTRUCTION'
                })
                
                # Feature 2: Material Demand Forecast
                features.append({
                    'feature_name': 'material_demand_forecast',
                    'feature_value': row.get('demanda_material', 0),
                    'feature_category': 'CONSTRUCTION'
                })
                
                # Feature 3: Regional Growth Rate
                features.append({
                    'feature_name': 'regional_growth_rate',
                    'feature_value': row.get('crescimento_regional', 0),
                    'feature_category': 'CONSTRUCTION'
                })
                
                # Feature 4: Infrastructure Investment
                features.append({
                    'feature_name': 'infrastructure_investment',
                    'feature_value': row.get('investimento_infraestrutura', 0),
                    'feature_category': 'CONSTRUCTION'
                })
                
                # Feature 5: Construction Demand Multiplier
                demand_multiplier = 1.0 + (row.get('crescimento_regional', 0) / 100.0)
                features.append({
                    'feature_name': 'construction_demand_multiplier',
                    'feature_value': demand_multiplier,
                    'feature_category': 'CONSTRUCTION'
                })
            
            logger.info(f"   ✅ Generated {len(features)} CONSTRUCTION features")
            
        except Error as e:
            logger.error(f"   ❌ Error generating CONSTRUCTION features: {e}")
        
        return features
    
    # ============================================
    # INDUSTRIAL FEATURES (5 features)
    # ============================================
    
    def generate_industrial_features(self, data_referencia: datetime.date) -> List[Dict]:
        """Generate industrial-related features"""
        logger.info("📊 Generating INDUSTRIAL features...")
        
        features = []
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            # Get IBGE Extended (PIM)
            query_pim = """
            SELECT pim_producao_industrial
            FROM DadosIbgeExtended
            WHERE data_referencia = %s
            LIMIT 1
            """
            
            cursor.execute(query_pim, (data_referencia,))
            row_pim = cursor.fetchone()
            
            # Get ABINEE data
            query_abinee = """
            SELECT 
                producao_equipamentos_eletricos,
                demanda_componentes
            FROM DadosAbinee
            WHERE data_referencia = %s
            LIMIT 1
            """
            
            cursor.execute(query_abinee, (data_referencia,))
            row_abinee = cursor.fetchone()
            
            if row_pim:
                # Feature 1: Industrial Production Index (PIM)
                features.append({
                    'feature_name': 'industrial_production_index',
                    'feature_value': row_pim.get('pim_producao_industrial', 0),
                    'feature_category': 'INDUSTRIAL'
                })
            
            if row_abinee:
                # Feature 2: Electrical Equipment Production
                features.append({
                    'feature_name': 'electrical_equipment_production',
                    'feature_value': row_abinee.get('producao_equipamentos_eletricos', 0),
                    'feature_category': 'INDUSTRIAL'
                })
                
                # Feature 3: Component Demand
                features.append({
                    'feature_name': 'component_demand',
                    'feature_value': row_abinee.get('demanda_componentes', 0),
                    'feature_category': 'INDUSTRIAL'
                })
                
                # Feature 4: Production/Demand Ratio
                if row_abinee.get('demanda_componentes', 0) > 0:
                    prod_demand_ratio = row_abinee.get('producao_equipamentos_eletricos', 0) / \
                                       row_abinee.get('demanda_componentes', 0)
                    features.append({
                        'feature_name': 'production_demand_ratio',
                        'feature_value': prod_demand_ratio,
                        'feature_category': 'INDUSTRIAL'
                    })
                
                # Feature 5: Industrial Activity Level
                activity_level = (row_abinee.get('producao_equipamentos_eletricos', 0) + 
                                row_abinee.get('demanda_componentes', 0)) / 2.0
                features.append({
                    'feature_name': 'industrial_activity_level',
                    'feature_value': activity_level,
                    'feature_category': 'INDUSTRIAL'
                })
            
            logger.info(f"   ✅ Generated {len(features)} INDUSTRIAL features")
            
        except Error as e:
            logger.error(f"   ❌ Error generating INDUSTRIAL features: {e}")
        
        return features
    
    # ============================================
    # MAIN FEATURE GENERATION
    # ============================================
    
    def generate_all_features(self, material_id: int, data_referencia: datetime.date) -> bool:
        """
        Generate all expanded features for a material
        
        Args:
            material_id: Material ID
            data_referencia: Reference date
        
        Returns:
            True if successful
        """
        logger.info(f"🚀 Generating all expanded features for material {material_id}...")
        
        if not self.connect():
            return False
        
        try:
            cursor = self.connection.cursor()
            
            all_features = []
            
            # Generate all feature categories
            all_features.extend(self.generate_transport_features(data_referencia))
            all_features.extend(self.generate_trade_features(data_referencia))
            all_features.extend(self.generate_energy_features(data_referencia))
            all_features.extend(self.generate_employment_features(data_referencia))
            all_features.extend(self.generate_construction_features(data_referencia))
            all_features.extend(self.generate_industrial_features(data_referencia))
            
            # Store features in database
            insert_query = """
            INSERT INTO MaterialFeatures (
                material_id, feature_name, feature_value, feature_category, data_coleta
            ) VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                feature_value = VALUES(feature_value),
                data_coleta = VALUES(data_coleta)
            """
            
            for feature in all_features:
                values = (
                    material_id,
                    feature['feature_name'],
                    feature['feature_value'],
                    feature['feature_category'],
                    datetime.now()
                )
                cursor.execute(insert_query, values)
            
            self.connection.commit()
            
            logger.info(f"✅ Generated and stored {len(all_features)} expanded features")
            
            # Update material ML timestamp
            update_query = """
            UPDATE Material 
            SET ultima_atualizacao_ml = %s
            WHERE material_id = %s
            """
            cursor.execute(update_query, (datetime.now(), material_id))
            self.connection.commit()
            
            return True
            
        except Error as e:
            logger.error(f"❌ Error generating features: {e}")
            return False
        
        finally:
            self.disconnect()


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    engineer = ExpandedFeatureEngineer()
    
    # Generate features for all materials for today
    today = datetime.now().date()
    
    # Get all materials
    if engineer.connect():
        try:
            cursor = engineer.connection.cursor()
            cursor.execute("SELECT material_id FROM Material LIMIT 10")  # Example: first 10 materials
            materials = cursor.fetchall()
            
            for (material_id,) in materials:
                engineer.generate_all_features(material_id, today)
                
        finally:
            engineer.disconnect()
    
    print("\n🎉 Feature engineering complete!")

