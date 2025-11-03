"""
Demand forecaster algorithm for Nova Corrente
Multi-horizon demand forecasting utilities
"""
from typing import Dict, Any, List, Optional
from datetime import date, timedelta
import pandas as pd
import numpy as np

from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.algorithms.demand_forecaster')


class DemandForecaster:
    """
    Utility functions for demand forecasting
    """
    
    def calculate_average_demand(
        self,
        historical_demands: List[float],
        window_size: int = 30
    ) -> float:
        """
        Calculate average demand from historical data
        
        Args:
            historical_demands: List of historical demand values
            window_size: Window size for averaging (default 30 days)
        
        Returns:
            Average daily demand
        """
        try:
            if not historical_demands:
                return 0.0
            
            # Use last N values
            recent_demands = historical_demands[-window_size:]
            avg_demand = np.mean(recent_demands)
            
            return float(max(0.0, avg_demand))
        except Exception as e:
            logger.error(f"Error calculating average demand: {e}")
            return 0.0
    
    def calculate_trend(
        self,
        historical_demands: List[float],
        window_size: int = 30
    ) -> Dict[str, float]:
        """
        Calculate demand trend
        
        Args:
            historical_demands: List of historical demand values
            window_size: Window size for trend calculation
        
        Returns:
            Dictionary with trend information
        """
        try:
            if len(historical_demands) < 2:
                return {
                    'trend': 0.0,
                    'direction': 'stable',
                    'slope': 0.0,
                }
            
            # Use last N values
            recent_demands = historical_demands[-window_size:]
            
            # Simple linear trend
            x = np.arange(len(recent_demands))
            y = np.array(recent_demands)
            
            # Linear regression
            slope = np.polyfit(x, y, 1)[0]
            
            # Determine direction
            if slope > 0.1:
                direction = 'increasing'
            elif slope < -0.1:
                direction = 'decreasing'
            else:
                direction = 'stable'
            
            return {
                'trend': float(slope),
                'direction': direction,
                'slope': float(slope),
            }
        except Exception as e:
            logger.error(f"Error calculating trend: {e}")
            return {
                'trend': 0.0,
                'direction': 'stable',
                'slope': 0.0,
            }
    
    def forecast_simple_average(
        self,
        historical_demands: List[float],
        horizon: int = 30,
        window_size: int = 30
    ) -> List[float]:
        """
        Simple moving average forecast
        
        Args:
            historical_demands: List of historical demand values
            horizon: Forecast horizon in days
            window_size: Window size for averaging
        
        Returns:
            List of forecasted demands
        """
        try:
            if not historical_demands:
                return [0.0] * horizon
            
            avg_demand = self.calculate_average_demand(historical_demands, window_size)
            
            # Forecast is constant average
            forecast = [avg_demand] * horizon
            
            return [float(max(0.0, f)) for f in forecast]
        except Exception as e:
            logger.error(f"Error in simple average forecast: {e}")
            return [0.0] * horizon
    
    def forecast_with_trend(
        self,
        historical_demands: List[float],
        horizon: int = 30,
        window_size: int = 30
    ) -> List[float]:
        """
        Forecast with trend adjustment
        
        Args:
            historical_demands: List of historical demand values
            horizon: Forecast horizon in days
            window_size: Window size for calculations
        
        Returns:
            List of forecasted demands
        """
        try:
            if not historical_demands:
                return [0.0] * horizon
            
            # Calculate average and trend
            avg_demand = self.calculate_average_demand(historical_demands, window_size)
            trend_info = self.calculate_trend(historical_demands, window_size)
            trend = trend_info['trend']
            
            # Forecast with trend
            forecast = []
            for i in range(horizon):
                forecasted = avg_demand + (trend * (i + 1))
                forecast.append(float(max(0.0, forecasted)))
            
            return forecast
        except Exception as e:
            logger.error(f"Error in trend forecast: {e}")
            return [0.0] * horizon
    
    def calculate_demand_variability(
        self,
        historical_demands: List[float],
        window_size: int = 30
    ) -> Dict[str, float]:
        """
        Calculate demand variability metrics
        
        Args:
            historical_demands: List of historical demand values
            window_size: Window size for calculation
        
        Returns:
            Dictionary with variability metrics
        """
        try:
            if len(historical_demands) < 2:
                return {
                    'std': 0.0,
                    'cv': 0.0,  # Coefficient of variation
                    'min': 0.0,
                    'max': 0.0,
                    'range': 0.0,
                }
            
            recent_demands = historical_demands[-window_size:]
            demands_array = np.array(recent_demands)
            
            std = float(np.std(demands_array))
            mean = float(np.mean(demands_array))
            cv = (std / mean) if mean > 0 else 0.0
            
            return {
                'std': std,
                'cv': float(cv),
                'min': float(np.min(demands_array)),
                'max': float(np.max(demands_array)),
                'range': float(np.max(demands_array) - np.min(demands_array)),
            }
        except Exception as e:
            logger.error(f"Error calculating demand variability: {e}")
            return {
                'std': 0.0,
                'cv': 0.0,
                'min': 0.0,
                'max': 0.0,
                'range': 0.0,
            }


# Singleton instance
demand_forecaster = DemandForecaster()

