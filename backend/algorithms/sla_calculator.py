"""
SLA calculator for Nova Corrente
SLA penalty calculations
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.algorithms.sla')


class SLACalculator:
    """
    Calculate SLA penalties and metrics
    """
    
    def calculate_availability(
        self,
        total_time: float,
        downtime: float
    ) -> Dict[str, float]:
        """
        Calculate availability percentage
        
        Args:
            total_time: Total time period (hours)
            downtime: Downtime period (hours)
        
        Returns:
            Dictionary with availability metrics
        """
        try:
            uptime = total_time - downtime
            availability = (uptime / total_time) * 100 if total_time > 0 else 100.0
            
            return {
                'availability_percent': float(availability),
                'uptime_hours': float(uptime),
                'downtime_hours': float(downtime),
                'total_time_hours': float(total_time),
            }
        except Exception as e:
            logger.error(f"Error calculating availability: {e}")
            raise
    
    def calculate_penalty(
        self,
        availability_percent: float,
        target_availability: float,
        penalty_per_hour: float,
        total_time_hours: float
    ) -> Dict[str, float]:
        """
        Calculate SLA penalty
        
        Args:
            availability_percent: Actual availability percentage
            target_availability: Target availability percentage
            penalty_per_hour: Penalty per hour of downtime (BRL)
            total_time_hours: Total time period (hours)
        
        Returns:
            Dictionary with penalty information
        """
        try:
            if availability_percent >= target_availability:
                return {
                    'penalty_brl': 0.0,
                    'downtime_hours': 0.0,
                    'availability_percent': float(availability_percent),
                    'target_availability': float(target_availability),
                    'meets_sla': True,
                }
            
            # Calculate downtime
            expected_uptime = (target_availability / 100.0) * total_time_hours
            actual_uptime = (availability_percent / 100.0) * total_time_hours
            downtime_hours = expected_uptime - actual_uptime
            
            # Calculate penalty
            penalty = downtime_hours * penalty_per_hour
            
            return {
                'penalty_brl': float(max(0.0, penalty)),
                'downtime_hours': float(max(0.0, downtime_hours)),
                'availability_percent': float(availability_percent),
                'target_availability': float(target_availability),
                'meets_sla': False,
            }
        except Exception as e:
            logger.error(f"Error calculating penalty: {e}")
            raise
    
    def calculate_stockout_penalty(
        self,
        stockout_hours: float,
        penalty_per_hour: float,
        material_value: float = 0.0
    ) -> Dict[str, float]:
        """
        Calculate penalty for stockout events
        
        Args:
            stockout_hours: Total stockout hours
            penalty_per_hour: Penalty per hour (BRL)
            material_value: Material value (BRL)
        
        Returns:
            Dictionary with stockout penalty information
        """
        try:
            base_penalty = stockout_hours * penalty_per_hour
            
            # Additional penalty based on material value (optional)
            value_penalty = material_value * 0.01 * stockout_hours  # 1% of value per hour
            
            total_penalty = base_penalty + value_penalty
            
            return {
                'penalty_brl': float(total_penalty),
                'stockout_hours': float(stockout_hours),
                'base_penalty': float(base_penalty),
                'value_penalty': float(value_penalty),
            }
        except Exception as e:
            logger.error(f"Error calculating stockout penalty: {e}")
            raise
    
    def calculate_lead_time_penalty(
        self,
        actual_lead_time: float,
        target_lead_time: float,
        penalty_per_day: float
    ) -> Dict[str, float]:
        """
        Calculate penalty for lead time violations
        
        Args:
            actual_lead_time: Actual lead time (days)
            target_lead_time: Target lead time (days)
            penalty_per_day: Penalty per day of delay (BRL)
        
        Returns:
            Dictionary with lead time penalty information
        """
        try:
            delay_days = max(0.0, actual_lead_time - target_lead_time)
            penalty = delay_days * penalty_per_day
            
            return {
                'penalty_brl': float(penalty),
                'delay_days': float(delay_days),
                'actual_lead_time': float(actual_lead_time),
                'target_lead_time': float(target_lead_time),
                'meets_target': actual_lead_time <= target_lead_time,
            }
        except Exception as e:
            logger.error(f"Error calculating lead time penalty: {e}")
            raise


# Singleton instance
sla_calculator = SLACalculator()

