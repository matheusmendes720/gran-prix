"""Brazilian calendar ETL - Generate holidays calendar"""
from typing import Dict, Any
from datetime import date, datetime, timedelta
import pandas as pd
from dateutil.relativedelta import relativedelta

from backend.services.database_service import db_service
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.etl.calendar')


class BrazilianCalendarETL:
    """ETL for Brazilian holidays calendar"""
    
    def generate_holidays(self, start_year: int, end_year: int) -> pd.DataFrame:
        """Generate Brazilian holidays calendar"""
        try:
            holidays = []
            current_date = date(start_year, 1, 1)
            end_date = date(end_year, 12, 31)
            
            while current_date <= end_date:
                row = {
                    'data_referencia': current_date,
                    'dia_semana': current_date.weekday() + 1,  # 1=Monday
                    'is_feriado': False,
                    'is_weekend': current_date.weekday() >= 5,
                }
                
                # National holidays (fixed dates)
                national_holidays = {
                    (1, 1): 'Ano Novo',
                    (4, 21): 'Tiradentes',
                    (5, 1): 'Dia do Trabalhador',
                    (9, 7): 'Independência',
                    (10, 12): 'Nossa Senhora Aparecida',
                    (11, 2): 'Finados',
                    (11, 15): 'Proclamação da República',
                    (12, 25): 'Natal',
                }
                
                if (current_date.month, current_date.day) in national_holidays:
                    row['is_feriado'] = True
                    row['nome_feriado'] = national_holidays[(current_date.month, current_date.day)]
                    row['tipo_feriado'] = 'NACIONAL'
                
                # Carnival (approximate - 47 days before Easter)
                # Easter calculation (simplified)
                # Summer (Dec-Feb)
                if current_date.month in [12, 1, 2]:
                    row['is_verao'] = True
                
                # Rainy season in Salvador (May-Aug)
                if current_date.month in range(5, 9):
                    row['is_chuva_sazonal'] = True
                
                # Christmas period
                if current_date.month == 12 and current_date.day >= 24:
                    row['is_natal'] = True
                
                # Default impact
                row['impact_demanda'] = 1.0
                if row.get('is_feriado'):
                    row['impact_demanda'] = 0.7  # Reduced demand on holidays
                
                holidays.append(row)
                current_date += timedelta(days=1)
            
            df = pd.DataFrame(holidays)
            
            # Fill missing values
            df['is_feriado'] = df['is_feriado'].fillna(False)
            df['is_weekend'] = df['is_weekend'].fillna(False)
            df['is_verao'] = df.get('is_verao', False).fillna(False)
            df['is_chuva_sazonal'] = df.get('is_chuva_sazonal', False).fillna(False)
            df['is_natal'] = df.get('is_natal', False).fillna(False)
            df['impact_demanda'] = df['impact_demanda'].fillna(1.0)
            
            logger.info(f"Generated {len(df)} calendar entries")
            return df
        except Exception as e:
            logger.error(f"Error generating holidays: {e}")
            raise
    
    def load(self, calendar_data: pd.DataFrame) -> int:
        """Load calendar data into database"""
        try:
            if calendar_data.empty:
                return 0
            
            rows_inserted = db_service.insert_dataframe(
                'CalendarioBrasil',
                calendar_data,
                if_exists='replace'
            )
            
            logger.info(f"Loaded {rows_inserted} calendar records")
            return rows_inserted
        except Exception as e:
            logger.error(f"Error loading calendar data: {e}")
            raise
    
    def run(self, start_year: int = 2020, end_year: int = 2030) -> int:
        """Run complete ETL pipeline"""
        try:
            calendar_data = self.generate_holidays(start_year, end_year)
            rows_inserted = self.load(calendar_data)
            return rows_inserted
        except Exception as e:
            logger.error(f"Error running calendar ETL: {e}")
            raise


brazilian_calendar_etl = BrazilianCalendarETL()

