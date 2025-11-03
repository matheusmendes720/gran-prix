"""
Reorder point calculator for Nova Corrente
PP = (D × LT) + SS
"""
from typing import Dict, Any, Optional
from datetime import date, timedelta
import numpy as np

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.algorithms.reorder_point')


class ReorderPointCalculator:
    """
    Calculate reorder point (PP) using demand, lead time, and safety stock
    """
    
    def calculate(
        self,
        demand: float,
        lead_time_days: float,
        safety_stock: float = 0.0
    ) -> float:
        """
        Calculate reorder point: PP = (D × LT) + SS
        
        Args:
            demand: Average daily demand
            lead_time_days: Lead time in days
            safety_stock: Safety stock quantity
        
        Returns:
            Reorder point (PP)
        """
        try:
            reorder_point = (demand * lead_time_days) + safety_stock
            
            # Ensure non-negative
            reorder_point = max(0.0, reorder_point)
            
            logger.debug(
                f"Reorder point calculated: PP = ({demand} × {lead_time_days}) + {safety_stock} = {reorder_point}"
            )
            
            return float(reorder_point)
        except Exception as e:
            logger.error(f"Error calculating reorder point: {e}")
            raise
    
    def calculate_with_uncertainty(
        self,
        demand_mean: float,
        demand_std: float,
        lead_time_mean: float,
        lead_time_std: float,
        service_level: float = 0.95,
        safety_stock: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Calculate reorder point with demand and lead time uncertainty
        
        Args:
            demand_mean: Mean daily demand
            demand_std: Standard deviation of daily demand
            lead_time_mean: Mean lead time in days
            lead_time_std: Standard deviation of lead time
            service_level: Desired service level (default 0.95)
            safety_stock: Optional pre-calculated safety stock
        
        Returns:
            Dictionary with PP and component values
        """
        try:
            from scipy import stats
            
            # Calculate Z-score for service level
            z_score = stats.norm.ppf(service_level)
            
            # Calculate safety stock if not provided
            if safety_stock is None:
                # Safety stock with demand and lead time uncertainty
                # SS = Z × √(LT × σD² + D² × σLT²)
                variance_demand_lt = lead_time_mean * (demand_std ** 2)
                variance_lt_demand = (demand_mean ** 2) * (lead_time_std ** 2)
                total_variance = variance_demand_lt + variance_lt_demand
                
                safety_stock = z_score * np.sqrt(total_variance)
            
            # Expected demand during lead time
            expected_demand_lt = demand_mean * lead_time_mean
            
            # Reorder point
            reorder_point = expected_demand_lt + safety_stock
            
            return {
                'reorder_point': float(reorder_point),
                'expected_demand_lt': float(expected_demand_lt),
                'safety_stock': float(safety_stock),
                'z_score': float(z_score),
                'service_level': float(service_level),
            }
        except ImportError:
            logger.warning("scipy not available, using simplified calculation")
            # Fallback to simple calculation
            safety_stock_val = safety_stock or (1.65 * demand_std * np.sqrt(lead_time_mean))  # Z≈1.65 for 95%
            reorder_point = (demand_mean * lead_time_mean) + safety_stock_val
            
            return {
                'reorder_point': float(reorder_point),
                'expected_demand_lt': float(demand_mean * lead_time_mean),
                'safety_stock': float(safety_stock_val),
                'z_score': 1.65,
                'service_level': 0.95,
            }
        except Exception as e:
            logger.error(f"Error calculating reorder point with uncertainty: {e}")
            raise
    
    def calculate_with_forecast(
        self,
        forecasted_demand: Dict[date, float],
        lead_time_days: float,
        safety_stock: float = 0.0,
        start_date: Optional[date] = None
    ) -> float:
        """
        Calculate reorder point using forecasted demand
        
        Args:
            forecasted_demand: Dictionary of date -> forecasted demand
            lead_time_days: Lead time in days
            safety_stock: Safety stock quantity
            start_date: Start date for calculation (default: earliest date in forecast)
        
        Returns:
            Reorder point (PP)
        """
        try:
            if not forecasted_demand:
                logger.warning("Empty forecast, returning 0")
                return 0.0
            
            if start_date is None:
                start_date = min(forecasted_demand.keys())
            
            # Calculate average daily demand from forecast
            forecast_dates = sorted([d for d in forecasted_demand.keys() if d >= start_date])
            
            if not forecast_dates:
                return 0.0
            
            # Calculate demand over lead time period
            lead_time_end = start_date + timedelta(days=int(lead_time_days))
            
            total_demand = sum(
                forecasted_demand.get(d, 0.0)
                for d in forecast_dates
                if d <= lead_time_end
            )
            
            # Average daily demand
            days_in_period = len([d for d in forecast_dates if d <= lead_time_end])
            if days_in_period == 0:
                days_in_period = int(lead_time_days)
            
            avg_daily_demand = total_demand / days_in_period if days_in_period > 0 else 0.0
            
            # Calculate reorder point
            reorder_point = (avg_daily_demand * lead_time_days) + safety_stock
            
            return float(max(0.0, reorder_point))
        except Exception as e:
            logger.error(f"Error calculating reorder point with forecast: {e}")
            raise


# Singleton instance
reorder_point_calculator = ReorderPointCalculator()

