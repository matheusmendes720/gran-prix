"""
Reorder Point (PP) Calculator and Alert System
Phase 3: PP Calculation, Alerts, and Reporting
"""
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Optional, Tuple, List
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class PPCalculator:
    """
    Calculate Reorder Points (PP) and generate alerts.
    """
    
    def __init__(self, service_level: float = 0.95):
        """
        Initialize PP Calculator.
        
        Parameters:
        -----------
        service_level : float
            Desired service level (e.g., 0.95 for 95%)
        """
        self.service_level = service_level
        self.z_score = stats.norm.ppf(service_level)
    
    def calculate_safety_stock(self, avg_demand: float, std_demand: float,
                              lead_time: int, std_lead_time: Optional[float] = None) -> float:
        """
        Calculate Safety Stock (SS).
        
        Formula: SS = Z_α × σ_D × √LT (simplified)
        Advanced: SS = Z_α × √(LT × σ_D² + D² × σ_LT²)
        
        Parameters:
        -----------
        avg_demand : float
            Average daily demand
        std_demand : float
            Standard deviation of daily demand
        lead_time : int
            Average lead time in days
        std_lead_time : Optional[float]
            Standard deviation of lead time (for advanced calculation)
        
        Returns:
        --------
        float
            Safety stock value
        """
        if std_lead_time is not None and std_lead_time > 0:
            # Advanced formula: account for lead time variability
            ss = self.z_score * np.sqrt(
                lead_time * std_demand ** 2 + avg_demand ** 2 * std_lead_time ** 2
            )
        else:
            # Simplified formula: assume constant lead time
            ss = self.z_score * std_demand * np.sqrt(lead_time)
        
        return max(0, ss)  # Ensure non-negative
    
    def calculate_reorder_point(self, forecast: pd.DataFrame,
                               lead_time: int,
                               current_stock: float,
                               std_demand: Optional[float] = None,
                               std_lead_time: Optional[float] = None) -> Dict:
        """
        Calculate Reorder Point (PP) and days to rupture.
        
        Formula: PP = (avg_daily_demand × lead_time) + safety_stock
        
        Parameters:
        -----------
        forecast : pd.DataFrame
            Forecast dataframe with 'forecast' column
        lead_time : int
            Lead time in days
        current_stock : float
            Current stock level
        std_demand : Optional[float]
            Standard deviation of demand (for SS calculation)
        std_lead_time : Optional[float]
            Standard deviation of lead time (for SS calculation)
        
        Returns:
        --------
        Dict
            Dictionary with PP, safety_stock, avg_demand, days_to_rupture
        """
        # Calculate average daily demand from forecast
        avg_demand = forecast['forecast'].mean()
        
        # Calculate safety stock
        if std_demand is None:
            # Use forecast standard deviation as proxy
            std_demand = forecast['forecast'].std()
        
        safety_stock = self.calculate_safety_stock(
            avg_demand=avg_demand,
            std_demand=std_demand,
            lead_time=lead_time,
            std_lead_time=std_lead_time
        )
        
        # Calculate Reorder Point
        pp = (avg_demand * lead_time) + safety_stock
        
        # Calculate days to rupture
        if avg_demand > 0:
            days_to_rupture = (current_stock - safety_stock) / avg_demand
        else:
            days_to_rupture = float('inf')
        
        return {
            'reorder_point': pp,
            'safety_stock': safety_stock,
            'avg_daily_demand': avg_demand,
            'lead_time': lead_time,
            'current_stock': current_stock,
            'days_to_rupture': days_to_rupture,
            'stock_status': 'critical' if days_to_rupture < lead_time else 'normal'
        }
    
    def check_alert(self, pp_info: Dict, alert_threshold: Optional[float] = None) -> Optional[str]:
        """
        Check if alert should be triggered.
        
        Parameters:
        -----------
        pp_info : Dict
            Output from calculate_reorder_point
        alert_threshold : Optional[float]
            Custom threshold for alert. If None, use PP as threshold.
        
        Returns:
        --------
        Optional[str]
            Alert message if threshold exceeded, None otherwise
        """
        current_stock = pp_info['current_stock']
        pp = pp_info['reorder_point']
        days_to_rupture = pp_info['days_to_rupture']
        
        threshold = alert_threshold if alert_threshold is not None else pp
        
        if current_stock <= threshold:
            # Calculate reorder quantity
            reorder_qty = int(pp - current_stock + pp_info['safety_stock'])
            
            alert = (
                f"🚨 ALERTA: Reordenar agora!\n"
                f"  Estoque atual: {current_stock:.1f} unidades\n"
                f"  Ponto de Reposição (PP): {pp:.1f} unidades\n"
                f"  Quantidade a reordenar: {reorder_qty} unidades\n"
                f"  Dias até ruptura: {days_to_rupture:.1f} dias\n"
                f"  Lead Time: {pp_info['lead_time']} dias\n"
                f"  Status: {pp_info['stock_status'].upper()}"
            )
            
            return alert
        
        return None
    
    def calculate_for_multiple_items(self, forecasts: Dict[str, pd.DataFrame],
                                    lead_times: Dict[str, int],
                                    current_stocks: Dict[str, float],
                                    std_demands: Optional[Dict[str, float]] = None,
                                    std_lead_times: Optional[Dict[str, float]] = None) -> Dict[str, Dict]:
        """
        Calculate PP for multiple items.
        
        Parameters:
        -----------
        forecasts : Dict[str, pd.DataFrame]
            Dictionary of {item_id: forecast_dataframe}
        lead_times : Dict[str, int]
            Dictionary of {item_id: lead_time}
        current_stocks : Dict[str, float]
            Dictionary of {item_id: current_stock}
        std_demands : Optional[Dict[str, float]]
            Dictionary of {item_id: std_demand}
        std_lead_times : Optional[Dict[str, float]]
            Dictionary of {item_id: std_lead_time}
        
        Returns:
        --------
        Dict[str, Dict]
            Dictionary of {item_id: pp_info}
        """
        results = {}
        
        std_demands = std_demands or {}
        std_lead_times = std_lead_times or {}
        
        for item_id in forecasts.keys():
            try:
                pp_info = self.calculate_reorder_point(
                    forecast=forecasts[item_id],
                    lead_time=lead_times.get(item_id, 14),
                    current_stock=current_stocks.get(item_id, 0),
                    std_demand=std_demands.get(item_id),
                    std_lead_time=std_lead_times.get(item_id)
                )
                results[item_id] = pp_info
            except Exception as e:
                print(f"Error calculating PP for {item_id}: {e}")
                results[item_id] = {'error': str(e)}
        
        return results
    
    def generate_weekly_report(self, pp_results: Dict[str, Dict],
                              output_path: str = 'weekly_pp_report.csv') -> pd.DataFrame:
        """
        Generate weekly PP report.
        
        Parameters:
        -----------
        pp_results : Dict[str, Dict]
            Output from calculate_for_multiple_items
        output_path : str
            Path to save report CSV
        
        Returns:
        --------
        pd.DataFrame
            Report dataframe
        """
        report_data = []
        
        for item_id, pp_info in pp_results.items():
            if 'error' in pp_info:
                continue
            
            report_data.append({
                'Item_ID': item_id,
                'Current_Stock': pp_info['current_stock'],
                'Reorder_Point': pp_info['reorder_point'],
                'Safety_Stock': pp_info['safety_stock'],
                'Avg_Daily_Demand': pp_info['avg_daily_demand'],
                'Lead_Time': pp_info['lead_time'],
                'Days_to_Rupture': pp_info['days_to_rupture'],
                'Stock_Status': pp_info['stock_status'],
                'Alert_Triggered': 'YES' if pp_info['current_stock'] <= pp_info['reorder_point'] else 'NO'
            })
        
        report_df = pd.DataFrame(report_data)
        report_df.to_csv(output_path, index=False)
        
        return report_df


# Example usage
if __name__ == "__main__":
    import pandas as pd
    import numpy as np
    
    # Create sample forecast
    forecast = pd.DataFrame({
        'forecast': np.random.poisson(8, 30),
        'lower': np.random.poisson(6, 30),
        'upper': np.random.poisson(10, 30)
    })
    
    # Initialize calculator
    calculator = PPCalculator(service_level=0.95)
    
    # Calculate PP
    pp_info = calculator.calculate_reorder_point(
        forecast=forecast,
        lead_time=14,
        current_stock=100,
        std_demand=2.5
    )
    
    print("Reorder Point Calculation:")
    print(f"  Reorder Point (PP): {pp_info['reorder_point']:.2f}")
    print(f"  Safety Stock: {pp_info['safety_stock']:.2f}")
    print(f"  Avg Daily Demand: {pp_info['avg_daily_demand']:.2f}")
    print(f"  Days to Rupture: {pp_info['days_to_rupture']:.2f}")
    print(f"  Status: {pp_info['stock_status']}")
    
    # Check alert
    alert = calculator.check_alert(pp_info)
    if alert:
        print(f"\n{alert}")

