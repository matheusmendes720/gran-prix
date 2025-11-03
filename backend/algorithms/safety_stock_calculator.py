"""
Safety stock calculator for Nova Corrente
SS = Z × σ × √LT
"""
from typing import Dict, Any, Optional
import numpy as np

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.algorithms.safety_stock')


class SafetyStockCalculator:
    """
    Calculate safety stock using service level, demand variability, and lead time
    """
    
    def calculate_simple(
        self,
        demand_std: float,
        lead_time_days: float,
        service_level: float = 0.95
    ) -> float:
        """
        Calculate safety stock: SS = Z × σ × √LT
        
        Args:
            demand_std: Standard deviation of demand
            lead_time_days: Lead time in days
            service_level: Desired service level (default 0.95)
        
        Returns:
            Safety stock (SS)
        """
        try:
            # Z-score for service level
            z_score = self._get_z_score(service_level)
            
            # Safety stock calculation
            safety_stock = z_score * demand_std * np.sqrt(lead_time_days)
            
            # Ensure non-negative
            safety_stock = max(0.0, safety_stock)
            
            logger.debug(
                f"Safety stock calculated: SS = {z_score:.2f} × {demand_std:.2f} × √{lead_time_days:.2f} = {safety_stock:.2f}"
            )
            
            return float(safety_stock)
        except Exception as e:
            logger.error(f"Error calculating safety stock: {e}")
            raise
    
    def calculate_with_lead_time_uncertainty(
        self,
        demand_mean: float,
        demand_std: float,
        lead_time_mean: float,
        lead_time_std: float,
        service_level: float = 0.95
    ) -> Dict[str, float]:
        """
        Calculate safety stock with both demand and lead time uncertainty
        
        Args:
            demand_mean: Mean daily demand
            demand_std: Standard deviation of daily demand
            lead_time_mean: Mean lead time in days
            lead_time_std: Standard deviation of lead time
            service_level: Desired service level
        
        Returns:
            Dictionary with safety stock and component values
        """
        try:
            # Z-score for service level
            z_score = self._get_z_score(service_level)
            
            # Safety stock with uncertainty in both demand and lead time
            # SS = Z × √(LT × σD² + D² × σLT²)
            variance_demand_lt = lead_time_mean * (demand_std ** 2)
            variance_lt_demand = (demand_mean ** 2) * (lead_time_std ** 2)
            total_variance = variance_demand_lt + variance_lt_demand
            
            safety_stock = z_score * np.sqrt(total_variance)
            
            return {
                'safety_stock': float(max(0.0, safety_stock)),
                'z_score': float(z_score),
                'service_level': float(service_level),
                'variance_components': {
                    'demand_variance': float(variance_demand_lt),
                    'lead_time_variance': float(variance_lt_demand),
                    'total_variance': float(total_variance),
                }
            }
        except Exception as e:
            logger.error(f"Error calculating safety stock with uncertainty: {e}")
            raise
    
    def calculate_with_historical_data(
        self,
        historical_demands: list,
        lead_time_days: float,
        service_level: float = 0.95
    ) -> float:
        """
        Calculate safety stock from historical demand data
        
        Args:
            historical_demands: List of historical demand values
            lead_time_days: Lead time in days
            service_level: Desired service level
        
        Returns:
            Safety stock (SS)
        """
        try:
            if not historical_demands or len(historical_demands) < 2:
                logger.warning("Insufficient historical data, returning 0")
                return 0.0
            
            # Calculate demand statistics
            demands_array = np.array(historical_demands)
            demand_std = float(np.std(demands_array))
            
            # Use simple calculation
            safety_stock = self.calculate_simple(
                demand_std=demand_std,
                lead_time_days=lead_time_days,
                service_level=service_level
            )
            
            return safety_stock
        except Exception as e:
            logger.error(f"Error calculating safety stock from historical data: {e}")
            raise
    
    def _get_z_score(self, service_level: float) -> float:
        """
        Get Z-score for given service level
        
        Args:
            service_level: Service level (0.0 to 1.0)
        
        Returns:
            Z-score
        """
        try:
            from scipy import stats
            return float(stats.norm.ppf(service_level))
        except ImportError:
            # Approximate Z-scores for common service levels
            z_map = {
                0.80: 0.84,
                0.85: 1.04,
                0.90: 1.28,
                0.95: 1.65,
                0.98: 2.05,
                0.99: 2.33,
            }
            
            # Find closest service level
            closest = min(z_map.keys(), key=lambda x: abs(x - service_level))
            z_score = z_map[closest]
            
            # Linear interpolation for intermediate values
            if closest < service_level:
                next_level = min([k for k in z_map.keys() if k > closest], default=None)
                if next_level:
                    next_z = z_map[next_level]
                    z_score = z_score + (service_level - closest) * (next_z - z_score) / (next_level - closest)
            
            logger.debug(f"Using approximate Z-score {z_score:.2f} for service level {service_level}")
            return z_score
        except Exception as e:
            logger.warning(f"Error calculating Z-score, using default 1.65: {e}")
            return 1.65  # Default for 95% service level


# Singleton instance
safety_stock_calculator = SafetyStockCalculator()

