"""
Visualization module for demand forecasts.
Creates charts and plots for analysis.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict, List, Optional
try:
    import seaborn as sns
    sns.set_style("whitegrid")
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("Warning: seaborn not available. Using matplotlib default style.")
import warnings
warnings.filterwarnings('ignore')


class Visualization:
    """Create visualizations for demand forecasts and inventory metrics."""
    
    def __init__(self, figsize: tuple = (12, 6)):
        """
        Initialize visualization class.
        
        Args:
            figsize: Default figure size (width, height)
        """
        self.figsize = figsize
        if SEABORN_AVAILABLE:
            sns.set_style("whitegrid")
    
    def plot_forecast(self, historical: pd.Series, forecast: pd.Series,
                     actual: Optional[pd.Series] = None, item_id: str = '',
                     save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot historical data and forecast.
        
        Args:
            historical: Historical time series
            forecast: Forecasted values
            actual: Optional actual values for comparison
            item_id: Item identifier for title
            save_path: Optional path to save figure
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create date range for forecast
        if isinstance(historical.index, pd.DatetimeIndex):
            last_date = historical.index.max()
            forecast_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=len(forecast),
                freq='D'
            )
        else:
            # If not DatetimeIndex, use sequential dates
            forecast_dates = pd.date_range(
                start=pd.Timestamp.now(),
                periods=len(forecast),
                freq='D'
            )
        
        # Plot historical data
        if isinstance(historical.index, pd.DatetimeIndex):
            ax.plot(historical.index, historical.values, 
                   label='Historical', color='blue', linewidth=2)
        else:
            ax.plot(range(len(historical)), historical.values,
                   label='Historical', color='blue', linewidth=2)
        
        # Plot forecast
        ax.plot(forecast_dates, forecast.values,
               label='Forecast', color='green', linewidth=2, linestyle='--')
        
        # Plot actual if available
        if actual is not None:
            if isinstance(actual.index, pd.DatetimeIndex):
                ax.plot(actual.index, actual.values,
                       label='Actual', color='red', linewidth=2, marker='o', markersize=4)
            else:
                ax.plot(range(len(historical), len(historical) + len(actual)), 
                       actual.values, label='Actual', color='red', 
                       linewidth=2, marker='o', markersize=4)
        
        # Formatting
        ax.set_xlabel('Date')
        ax.set_ylabel('Demand')
        title = f'Demand Forecast - {item_id}' if item_id else 'Demand Forecast'
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        if isinstance(historical.index, pd.DatetimeIndex) or isinstance(forecast_dates, pd.DatetimeIndex):
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_inventory_metrics(self, pp_metrics: Dict, item_id: str = '',
                              save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot inventory metrics (stock levels, reorder point).
        
        Args:
            pp_metrics: Dictionary with inventory metrics
            item_id: Item identifier for title
            save_path: Optional path to save figure
        
        Returns:
            matplotlib Figure object
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Stock levels bar chart
        categories = ['Current\nStock', 'Reorder\nPoint', 'Safety\nStock']
        values = [
            pp_metrics.get('current_stock', 0),
            pp_metrics.get('reorder_point', 0),
            pp_metrics.get('safety_stock', 0)
        ]
        
        colors_bar = ['green' if pp_metrics.get('current_stock', 0) > 
                     pp_metrics.get('reorder_point', 0) else 'red',
                     'orange', 'yellow']
        
        ax1.bar(categories, values, color=colors_bar, alpha=0.7, edgecolor='black')
        ax1.set_ylabel('Units')
        ax1.set_title(f'Inventory Levels - {item_id}' if item_id else 'Inventory Levels')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, v in enumerate(values):
            ax1.text(i, v, f'{v:.0f}', ha='center', va='bottom')
        
        # Metrics pie chart
        avg_demand = pp_metrics.get('avg_daily_demand', 0)
        days_to_rupture = pp_metrics.get('days_to_rupture', 0)
        
        if days_to_rupture != float('inf') and days_to_rupture > 0:
            # Days remaining vs safety threshold
            safety_days = 7  # Threshold
            remaining_days = days_to_rupture
            
            labels = ['Days Remaining', 'Safety Buffer']
            sizes = [remaining_days, max(0, safety_days - remaining_days)]
            colors_pie = ['green' if remaining_days > safety_days else 'red', 'lightgray']
            
            if sizes[1] > 0:
                ax2.pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%',
                       startangle=90)
            else:
                ax2.text(0.5, 0.5, f'{remaining_days:.1f} days\nremaining',
                        ha='center', va='center', fontsize=14)
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
            
            ax2.set_title('Days to Rupture Status')
        else:
            ax2.text(0.5, 0.5, 'No rupture risk',
                    ha='center', va='center', fontsize=14)
            ax2.set_xlim(0, 1)
            ax2.set_ylim(0, 1)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_ensemble_components(self, forecasts: Dict[str, np.ndarray],
                                item_id: str = '',
                                save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot individual model forecasts and ensemble.
        
        Args:
            forecasts: Dictionary with model forecasts:
                {'ARIMA': array, 'Prophet': array, 'LSTM': array, 'Ensemble': array}
            item_id: Item identifier for title
            save_path: Optional path to save figure
        
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Create date range
        max_len = max(len(fc) for fc in forecasts.values())
        dates = pd.date_range(start=pd.Timestamp.now(), periods=max_len, freq='D')
        
        # Plot each model
        colors_map = {'ARIMA': 'blue', 'Prophet': 'green', 'LSTM': 'orange', 
                     'Ensemble': 'red'}
        linestyles = {'ARIMA': '-', 'Prophet': '--', 'LSTM': '-.', 'Ensemble': '-'}
        linewidths = {'ARIMA': 1.5, 'Prophet': 1.5, 'LSTM': 1.5, 'Ensemble': 2}
        
        for model_name, forecast in forecasts.items():
            if len(forecast) > 0:
                ax.plot(dates[:len(forecast)], forecast,
                       label=model_name,
                       color=colors_map.get(model_name, 'gray'),
                       linestyle=linestyles.get(model_name, '-'),
                       linewidth=linewidths.get(model_name, 1.5),
                       alpha=0.8 if model_name != 'Ensemble' else 1.0)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Forecasted Demand')
        title = f'Ensemble Forecast Components - {item_id}' if item_id else 'Ensemble Forecast Components'
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig

