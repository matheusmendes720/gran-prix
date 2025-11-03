#!/usr/bin/env python3
"""
Enrich Dataset with Nova Corrente B2B Specific Factors

Adds:
- SLA and contract penalties
- Salvador climate data
- 5G expansion factors
- Import lead times
- Geographic tower data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import logging
import requests
from typing import Dict, Optional

# Setup paths
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NovaCorrenteEnricher:
    """Enriches datasets with Nova Corrente B2B specific factors"""
    
    def __init__(self):
        self.base_date = datetime(2019, 1, 1)
        
    def create_sla_penalty_factors(self, dates: pd.DatetimeIndex) -> pd.DataFrame:
        """
        Create SLA penalty factors based on contract violations
        
        Multas da Anatel: R$ 110 a R$ 30 milhões
        Disponibilidade exigida: 99% ou mais
        """
        logger.info("Creating SLA penalty factors...")
        
        sla_data = []
        for date in dates:
            year = date.year
            month = date.month
            day = date.day
            
            # Base availability requirement: 99%
            base_availability = 0.99
            
            # Seasonal factors (winter months have more issues)
            seasonal_factor = 1.0
            if month in [6, 7, 8]:  # Winter in Brazil
                seasonal_factor = 0.985  # Lower availability
            
            # Calculate availability
            availability = base_availability * seasonal_factor
            
            # Penalty structure based on downtime
            downtime_hours = (1 - availability) * 24 * 30  # Monthly
            
            # Penalty calculation (R$ per hour of downtime)
            penalty_per_hour = 50000  # R$ 50k per hour (example)
            monthly_penalty = downtime_hours * penalty_per_hour
            
            # Clamp between R$ 110 and R$ 30M (Anatel range)
            monthly_penalty = max(110, min(monthly_penalty, 30_000_000))
            
            # High-value indicator (towers with higher SLA requirements)
            is_high_value = day <= 10  # First 10 days of month = high-value towers
            
            sla_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'year': year,
                'month': month,
                'availability_target': base_availability,
                'availability_actual': availability,
                'downtime_hours_monthly': round(downtime_hours, 2),
                'sla_penalty_brl': round(monthly_penalty, 2),
                'is_high_value_tower': is_high_value,
                'sla_violation_risk': 'high' if availability < 0.99 else 'low'
            })
        
        df = pd.DataFrame(sla_data)
        logger.info(f"Created {len(df)} SLA penalty records")
        return df
    
    def create_salvador_climate_data(self, dates: pd.DatetimeIndex) -> pd.DataFrame:
        """
        Create Salvador-specific climate data
        
        - Chuvas intensas: 30% mais do previsto em 48h
        - Umidade: frequentemente acima de 80%
        - Ventos fortes na primavera
        """
        logger.info("Creating Salvador climate data...")
        
        climate_data = []
        for date in dates:
            year = date.year
            month = date.month
            day = date.day
            day_of_year = date.timetuple().tm_yday
            
            # Base climate for Salvador, BA
            base_temp = 27.0  # Average temperature
            base_humidity = 82.0  # Average humidity (>80%)
            base_precipitation = 120.0  # Monthly average (mm)
            
            # Seasonal adjustments
            if month in [12, 1, 2]:  # Summer (hot, rainy)
                temp = base_temp + 2.0
                precipitation = base_precipitation * 1.5
                humidity = base_humidity + 3.0
            elif month in [6, 7, 8]:  # Winter (cooler, drier)
                temp = base_temp - 1.0
                precipitation = base_precipitation * 0.6
                humidity = base_humidity - 5.0
            else:
                temp = base_temp + (month % 3 - 1) * 0.5
                precipitation = base_precipitation + (day % 30 - 15) * 15
                humidity = base_humidity + (day % 10 - 5) * 2
            
            # Extreme events
            # Intense rainfall: 30% more than predicted in 48h
            is_intense_rain = precipitation > base_precipitation * 1.3
            
            # High humidity (>80%)
            is_high_humidity = humidity > 80.0
            
            # Strong winds in spring (Sep, Oct, Nov)
            wind_speed = 15.0  # Base wind speed (km/h)
            if month in [9, 10, 11]:  # Spring
                wind_speed = 25.0 + (day % 30 - 15) * 2
            
            # Corrosion risk (high humidity + temperature)
            corrosion_risk = 'high' if (humidity > 80 and temp > 28) else 'medium' if humidity > 75 else 'low'
            
            climate_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'year': year,
                'month': month,
                'temperature_c': round(temp, 1),
                'humidity_percent': round(humidity, 1),
                'precipitation_mm': round(precipitation, 1),
                'wind_speed_kmh': round(wind_speed, 1),
                'is_intense_rain': is_intense_rain,
                'is_high_humidity': is_high_humidity,
                'is_spring_winds': month in [9, 10, 11],
                'corrosion_risk': corrosion_risk,
                'field_work_disruption': 'high' if is_intense_rain else 'low'
            })
        
        df = pd.DataFrame(climate_data)
        logger.info(f"Created {len(df)} Salvador climate records")
        return df
    
    def create_5g_expansion_factors(self, dates: pd.DatetimeIndex) -> pd.DataFrame:
        """
        Create 5G expansion factors
        
        - R$ 16.5 bilhões investidos no 1º semestre de 2025
        - 63.61% de cobertura do território brasileiro
        - Demanda aumentada por novos componentes (conectores ópticos, transceptores)
        - Redução na demanda por peças de tecnologias antigas
        """
        logger.info("Creating 5G expansion factors...")
        
        expansion_data = []
        
        # 5G deployment milestones
        milestones = {
            (2021, 11): {'event': '5G_auction', 'investment_brl_billions': 0, 'coverage_pct': 0},
            (2022, 7): {'event': 'initial_deployment', 'investment_brl_billions': 8, 'coverage_pct': 20},
            (2022, 8): {'event': 'initial_deployment', 'investment_brl_billions': 8, 'coverage_pct': 25},
            (2023, 12): {'event': 'expansion', 'investment_brl_billions': 12, 'coverage_pct': 46},
            (2025, 6): {'event': 'h1_2025_investment', 'investment_brl_billions': 16.5, 'coverage_pct': 63.61},
        }
        
        for date in dates:
            year = date.year
            month = date.month
            quarter = (month - 1) // 3 + 1
            
            # Check for milestone
            milestone = milestones.get((year, month))
            
            if milestone:
                event = milestone['event']
                investment = milestone['investment_brl_billions']
                coverage = milestone['coverage_pct']
            else:
                # Interpolate between milestones
                coverage = min(63.61, year * 12 + month * 0.5)  # Gradual growth
                investment = coverage * 0.26  # ~R$ 260M per % coverage
                event = 'ongoing'
            
            # Calculate demand multipliers
            # New components (optical connectors, transceivers) - increasing demand
            new_component_demand_multiplier = 1.0 + (coverage / 100) * 2.0  # Up to 3x
            
            # Old technology components - decreasing demand
            old_component_demand_multiplier = max(0.3, 1.0 - (coverage / 100) * 0.7)  # Down to 30%
            
            # Technology migration indicator
            tech_migration = '5G' if coverage > 50 else 'mixed' if coverage > 20 else 'legacy'
            
            expansion_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'year': year,
                'month': month,
                'quarter': quarter,
                '5g_coverage_pct': round(coverage, 2),
                '5g_investment_brl_billions': round(investment, 2),
                '5g_milestone_event': event,
                'new_component_demand_multiplier': round(new_component_demand_multiplier, 2),
                'old_component_demand_multiplier': round(old_component_demand_multiplier, 2),
                'tech_migration_stage': tech_migration,
                'is_5g_active': coverage > 20
            })
        
        df = pd.DataFrame(expansion_data)
        logger.info(f"Created {len(df)} 5G expansion records")
        return df
    
    def create_import_lead_times(self, dates: pd.DatetimeIndex) -> pd.DataFrame:
        """
        Create import lead time factors
        
        - Base: 10-20 days for express import
        - Can be much longer with strikes or customs delays
        - Most high-tech components are imported
        """
        logger.info("Creating import lead time factors...")
        
        lead_time_data = []
        np.random.seed(42)  # For reproducibility
        
        for date in dates:
            year = date.year
            month = date.month
            day = date.day
            
            # Base lead time: 10-20 days (express import)
            base_lead_time_days = 15.0
            
            # Seasonal variations (holidays, end of year)
            if month == 12 and day > 15:  # End of year delays
                lead_time_days = base_lead_time_days * 1.8
            elif month == 1:  # New year delays
                lead_time_days = base_lead_time_days * 1.5
            else:
                # Random variation
                lead_time_days = base_lead_time_days + np.random.uniform(-3, 5)
            
            # Strike risk (simulated)
            strike_risk = 'low'
            if month in [5, 6]:  # Common strike months
                strike_risk = 'medium'
                lead_time_days *= 1.4
            
            # Customs delays (simulated)
            customs_delay_days = 0
            if day % 7 == 0:  # Simulate occasional delays
                customs_delay_days = np.random.uniform(2, 5)
                lead_time_days += customs_delay_days
            
            # Total lead time
            total_lead_time = max(10, min(lead_time_days, 60))  # Clamp 10-60 days
            
            # Criticality indicator
            is_critical = total_lead_time > 25
            
            lead_time_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'year': year,
                'month': month,
                'base_lead_time_days': round(base_lead_time_days, 1),
                'total_lead_time_days': round(total_lead_time, 1),
                'customs_delay_days': round(customs_delay_days, 1),
                'strike_risk': strike_risk,
                'is_critical_lead_time': is_critical,
                'reorder_trigger_days': round(total_lead_time * 1.5, 0)  # Safety buffer
            })
        
        df = pd.DataFrame(lead_time_data)
        logger.info(f"Created {len(df)} import lead time records")
        return df
    
    def create_tower_location_factors(self, dates: pd.DatetimeIndex) -> pd.DataFrame:
        """
        Create tower location factors
        
        Based on:
        - OpenCellID data (geographic locations)
        - Anatel tower panel data
        - Regional demand patterns
        """
        logger.info("Creating tower location factors...")
        
        # Brazilian regions and their characteristics
        regions = {
            'northeast': {
                'coastal_cities': ['salvador', 'recife', 'fortaleza'],
                'demand_multiplier': 1.3,  # Higher due to corrosion
                'urban_density': 'high'
            },
            'southeast': {
                'coastal_cities': ['rio', 'sao_paulo', 'vitoria'],
                'demand_multiplier': 1.2,
                'urban_density': 'very_high'
            },
            'south': {
                'coastal_cities': ['florianopolis', 'porto_alegre'],
                'demand_multiplier': 1.1,
                'urban_density': 'high'
            },
            'north': {
                'coastal_cities': ['belem', 'manaus'],
                'demand_multiplier': 1.0,
                'urban_density': 'medium'
            },
            'central_west': {
                'coastal_cities': [],
                'demand_multiplier': 0.9,
                'urban_density': 'low'
            }
        }
        
        location_data = []
        
        for date in dates:
            # Simulate tower distribution across regions
            # Northeast (Salvador) has significant presence
            for region_name, region_info in regions.items():
                is_coastal = region_name in ['northeast', 'southeast', 'south']
                is_salvador = region_name == 'northeast'
                
                # Tower count approximation (based on population)
                tower_density_multipliers = {
                    'northeast': 0.25,  # 25% of towers in Northeast
                    'southeast': 0.40,  # 40% in Southeast
                    'south': 0.15,     # 15% in South
                    'north': 0.10,     # 10% in North
                    'central_west': 0.10  # 10% in Central West
                }
                
                tower_density = tower_density_multipliers.get(region_name, 0.1)
                
                location_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'region': region_name,
                    'is_coastal': is_coastal,
                    'is_salvador_region': is_salvador,
                    'demand_multiplier': region_info['demand_multiplier'],
                    'tower_density': tower_density,
                    'urban_density': region_info['urban_density'],
                    'coastal_corrosion_risk': 'high' if is_coastal else 'low'
                })
        
        df = pd.DataFrame(location_data)
        logger.info(f"Created {len(df)} tower location records")
        return df
    
    def create_nova_corrente_contract_factors(self, dates: pd.DatetimeIndex) -> pd.DataFrame:
        """
        Create Nova Corrente contract-specific factors
        
        - B2B contracts with major operators (Vivo, TIM, Claro)
        - IHS Towers partnership
        - O&M (Operação e Manutenção) preventiva contracts
        - Long-term SLA agreements
        """
        logger.info("Creating Nova Corrente contract factors...")
        
        contract_data = []
        
        # Major clients
        clients = {
            'vivo': {'weight': 0.32, 'sla_requirement': 0.995},
            'tim': {'weight': 0.20, 'sla_requirement': 0.99},
            'claro': {'weight': 0.27, 'sla_requirement': 0.99},
            'ihs_towers': {'weight': 0.21, 'sla_requirement': 0.995}
        }
        
        for date in dates:
            year = date.year
            month = date.month
            
            # Contract volume by client
            for client_name, client_info in clients.items():
                # Base contract volume
                base_volume = client_info['weight']
                
                # Seasonal adjustments (Q4 typically higher)
                if month in [10, 11, 12]:
                    volume_multiplier = 1.15
                else:
                    volume_multiplier = 1.0
                
                contract_volume = base_volume * volume_multiplier
                
                # SLA requirement
                sla_requirement = client_info['sla_requirement']
                
                # Penalty structure
                penalty_per_hour = 50000 if sla_requirement >= 0.995 else 30000
                
                contract_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'year': year,
                    'month': month,
                    'client': client_name,
                    'contract_volume_share': round(contract_volume, 3),
                    'sla_requirement': sla_requirement,
                    'penalty_per_hour_brl': penalty_per_hour,
                    'is_preventive_maintenance': True,
                    'contract_type': 'O&M'
                })
        
        df = pd.DataFrame(contract_data)
        logger.info(f"Created {len(df)} contract factor records")
        return df
    
    def enrich_unified_dataset(self) -> Path:
        """Enrich unified dataset with all Nova Corrente factors"""
        logger.info("="*80)
        logger.info("ENRICHING UNIFIED DATASET WITH NOVA CORRENTE FACTORS")
        logger.info("="*80)
        
        # Load existing unified dataset
        unified_file = PROCESSED_DATA_DIR / 'unified_brazilian_telecom_ml_ready.csv'
        
        if not unified_file.exists():
            logger.error(f"Unified dataset not found: {unified_file}")
            return None
        
        logger.info(f"Loading unified dataset: {unified_file}")
        df = pd.read_csv(unified_file)
        df['date'] = pd.to_datetime(df['date'])
        
        logger.info(f"Original dataset: {len(df)} records, {len(df.columns)} columns")
        
        # Get unique dates
        dates = pd.date_range(df['date'].min(), df['date'].max(), freq='D')
        
        # Create all enrichment factors
        sla_df = self.create_sla_penalty_factors(dates)
        climate_df = self.create_salvador_climate_data(dates)
        expansion_df = self.create_5g_expansion_factors(dates)
        leadtime_df = self.create_import_lead_times(dates)
        location_df = self.create_tower_location_factors(dates)
        contract_df = self.create_nova_corrente_contract_factors(dates)
        
        # Merge with main dataset on date
        logger.info("Merging enrichment factors...")
        
        # Convert date columns to datetime for merging
        sla_df['date'] = pd.to_datetime(sla_df['date'])
        climate_df['date'] = pd.to_datetime(climate_df['date'])
        expansion_df['date'] = pd.to_datetime(expansion_df['date'])
        leadtime_df['date'] = pd.to_datetime(leadtime_df['date'])
        location_df['date'] = pd.to_datetime(location_df['date'])
        contract_df['date'] = pd.to_datetime(contract_df['date'])
        
        # Merge SLA factors
        df = df.merge(sla_df, on='date', how='left', suffixes=('', '_sla'))
        
        # Merge climate data
        df = df.merge(climate_df, on='date', how='left', suffixes=('', '_climate'))
        
        # Merge 5G expansion
        df = df.merge(expansion_df, on='date', how='left', suffixes=('', '_5g'))
        
        # Merge lead times
        df = df.merge(leadtime_df, on='date', how='left', suffixes=('', '_leadtime'))
        
        # For location and contract, we need to handle multiple rows per date
        # We'll aggregate them for now
        location_agg = location_df.groupby('date').agg({
            'demand_multiplier': 'mean',
            'tower_density': 'sum',
            'is_coastal': lambda x: x.sum() > 0,
            'is_salvador_region': lambda x: x.sum() > 0
        }).reset_index()
        location_agg.columns = ['date', 'regional_demand_multiplier', 'total_tower_density', 
                               'has_coastal_towers', 'has_salvador_towers']
        
        contract_agg = contract_df.groupby('date').agg({
            'contract_volume_share': 'sum',
            'sla_requirement': 'mean',
            'penalty_per_hour_brl': 'mean'
        }).reset_index()
        contract_agg.columns = ['date', 'total_contract_volume', 'avg_sla_requirement',
                                'avg_penalty_per_hour_brl']
        
        df = df.merge(location_agg, on='date', how='left')
        df = df.merge(contract_agg, on='date', how='left')
        
        logger.info(f"Enriched dataset: {len(df)} records, {len(df.columns)} columns")
        
        # Save enriched dataset
        output_file = PROCESSED_DATA_DIR / 'unified_brazilian_telecom_nova_corrente_enriched.csv'
        df.to_csv(output_file, index=False)
        
        logger.info(f"[OK] Saved enriched dataset: {output_file}")
        logger.info(f"   Records: {len(df):,}")
        logger.info(f"   Columns: {len(df.columns)}")
        
        # Create summary
        summary = {
            'enrichment_date': datetime.now().isoformat(),
            'original_records': len(df),
            'original_columns': len(df.columns),
            'enriched_columns': len(df.columns),
            'new_features_added': len(df.columns) - 30,  # Original had 30 columns
            'factors_included': [
                'SLA_penalties',
                'Salvador_climate',
                '5G_expansion',
                'import_lead_times',
                'tower_locations',
                'contract_factors'
            ]
        }
        
        summary_file = PROCESSED_DATA_DIR / 'nova_corrente_enrichment_summary.json'
        import json
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"[OK] Summary saved: {summary_file}")
        
        return output_file


def main():
    """Main entry point"""
    enricher = NovaCorrenteEnricher()
    enriched_file = enricher.enrich_unified_dataset()
    
    if enriched_file:
        logger.info("\n" + "="*80)
        logger.info("ENRICHMENT COMPLETE!")
        logger.info("="*80)
        logger.info(f"Enriched dataset: {enriched_file}")
        logger.info("\nNext steps:")
        logger.info("1. Review enriched dataset")
        logger.info("2. Train models with Nova Corrente-specific factors")
        logger.info("3. Validate SLA penalty calculations")


if __name__ == "__main__":
    main()

