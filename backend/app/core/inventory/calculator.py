"""
Reorder Point (PP) calculation module.
Implements safety stock and reorder point calculations based on forecasts.
"""
import numpy as np
import pandas as pd
from typing import Dict, Optional
from scipy import stats


class ReorderPointCalculator:
    """Calculate reorder points (PP) based on forecasts and inventory parameters."""
    
    def __init__(self, service_level: float = 0.95):
        """
        Initialize reorder point calculator.
        
        Args:
            service_level: Target service level (default 0.95 = 95%)
        """
        if not 0 < service_level < 1:
            raise ValueError("Service level must be between 0 and 1")
        
        self.service_level = service_level
        self.z_score = stats.norm.ppf(service_level)  # z-score for service level
    
    def calculate_safety_stock(self, forecast: pd.Series, lead_time: int,
                              demand_std: Optional[float] = None) -> float:
        """
        Calculate safety stock using standard formula.
        
        Safety Stock = z * σ_demand * √(lead_time)
        
        Args:
            forecast: Forecasted demand series
            lead_time: Lead time in days
            demand_std: Optional standard deviation (calculated from forecast if not provided)
        
        Returns:
            Safety stock quantity
        """
        if demand_std is None:
            demand_std = forecast.std()
        
        # Handle zero or negative std
        if demand_std <= 0:
            # Use coefficient of variation if available, or default
            mean_demand = forecast.mean()
            if mean_demand > 0:
                demand_std = mean_demand * 0.1  # Default 10% CV
            else:
                demand_std = 1.0
        
        safety_stock = self.z_score * demand_std * np.sqrt(lead_time)
        return max(0, safety_stock)
    
    def calculate_reorder_point(self, forecast: pd.Series, lead_time: int,
                               safety_stock: Optional[float] = None) -> float:
        """
        Calculate reorder point (PP).
        
        PP = (Average Daily Demand × Lead Time) + Safety Stock
        
        Args:
            forecast: Forecasted demand series
            lead_time: Lead time in days
            safety_stock: Optional safety stock (calculated if not provided)
        
        Returns:
            Reorder point quantity
        """
        avg_daily_demand = forecast.mean()
        
        if avg_daily_demand < 0:
            avg_daily_demand = 0
        
        if safety_stock is None:
            safety_stock = self.calculate_safety_stock(forecast, lead_time)
        
        reorder_point = (avg_daily_demand * lead_time) + safety_stock
        return max(0, reorder_point)
    
    def calculate_days_to_rupture(self, current_stock: float, forecast: pd.Series,
                                  safety_stock: float) -> float:
        """
        Calculate days until stock rupture.
        
        Args:
            current_stock: Current inventory level
            forecast: Forecasted demand series
            safety_stock: Safety stock level
        
        Returns:
            Days to rupture (infinity if demand is zero)
        """
        avg_daily_demand = forecast.mean()
        
        if avg_daily_demand <= 0:
            return float('inf')
        
        days_to_rupture = (current_stock - safety_stock) / avg_daily_demand
        return max(0, days_to_rupture)
    
    def compute_all(self, forecast: pd.Series, lead_time: int,
                   current_stock: float) -> Dict:
        """
        Compute all inventory metrics.
        
        Args:
            forecast: Forecasted demand series
            lead_time: Lead time in days
            current_stock: Current inventory level
        
        Returns:
            Dictionary with all inventory metrics
        """
        safety_stock = self.calculate_safety_stock(forecast, lead_time)
        reorder_point = self.calculate_reorder_point(forecast, lead_time, safety_stock)
        days_to_rupture = self.calculate_days_to_rupture(current_stock, forecast, safety_stock)
        
        return {
            'avg_daily_demand': forecast.mean(),
            'demand_std': forecast.std(),
            'safety_stock': safety_stock,
            'reorder_point': reorder_point,
            'current_stock': current_stock,
            'days_to_rupture': days_to_rupture,
            'service_level': self.service_level,
            'lead_time': lead_time
        }

