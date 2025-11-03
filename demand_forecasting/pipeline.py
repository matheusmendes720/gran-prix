"""
Main Pipeline for Nova Corrente Demand Forecasting System
Integrates all components: Data → Models → PP → Alerts → Reports
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

from .data_loader import DataLoader
from .models.arima_model import ARIMAForecaster
from .models.prophet_model import ProphetForecaster
from .models.lstm_model import LSTMForecaster
from .models.ensemble_model import EnsembleForecaster
from .pp_calculator import PPCalculator


class DemandForecastingPipeline:
    """
    Complete pipeline for demand forecasting.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize pipeline with configuration.
        
        Parameters:
        -----------
        config : Optional[Dict]
            Configuration dictionary with:
            - service_level: float (default: 0.95)
            - ensemble_weights: Dict (default: {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3})
            - forecast_horizon: int (default: 30)
            - use_ensemble: bool (default: True)
        """
        if config is None:
            config = {}
        
        self.config = {
            'service_level': config.get('service_level', 0.95),
            'ensemble_weights': config.get('ensemble_weights', 
                                         {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3}),
            'forecast_horizon': config.get('forecast_horizon', 30),
            'use_ensemble': config.get('use_ensemble', True),
            'external_features': config.get('external_features', True)
        }
        
        # Initialize components
        self.data_loader = DataLoader(external_features=self.config['external_features'])
        self.pp_calculator = PPCalculator(service_level=self.config['service_level'])
        self.models = {}
        self.ensemble = None
        
        # Results storage
        self.forecasts = {}
        self.pp_results = {}
        self.alerts = []
    
    def load_and_preprocess(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """
        Load and preprocess data.
        
        Parameters:
        -----------
        file_path : str
            Path to data file
        
        Returns:
        --------
        Dict[str, pd.DataFrame]
            Dictionary of {item_id: processed_dataframe}
        """
        print("Loading and preprocessing data...")
        data_dict = self.data_loader.load_and_preprocess(file_path)
        print(f"Loaded {len(data_dict)} items")
        return data_dict
    
    def prepare_models(self, data_dict: Dict[str, pd.DataFrame],
                      target_col: str = 'Quantity_Consumed'):
        """
        Prepare and initialize models.
        
        Parameters:
        -----------
        data_dict : Dict[str, pd.DataFrame]
            Dictionary of processed dataframes
        target_col : str
            Name of target column
        """
        print("\nPreparing models...")
        
        if self.config['use_ensemble']:
            # Create ensemble
            self.ensemble = EnsembleForecaster(weights=self.config['ensemble_weights'])
            
            # Add individual models
            self.ensemble.add_model('ARIMA', ARIMAForecaster(seasonal=True, m=7))
            self.ensemble.add_model('Prophet', ProphetForecaster())
            
            # Add LSTM if TensorFlow available
            try:
                self.ensemble.add_model('LSTM', LSTMForecaster(look_back=30))
            except ImportError:
                print("Warning: TensorFlow not available. Skipping LSTM.")
                # Adjust weights
                total_weight = sum(self.config['ensemble_weights'].values())
                arima_weight = self.config['ensemble_weights'].get('ARIMA', 0.4) / total_weight
                prophet_weight = self.config['ensemble_weights'].get('Prophet', 0.3) / total_weight
                self.ensemble.weights = {'ARIMA': arima_weight, 'Prophet': prophet_weight}
        else:
            # Individual models only
            self.models['ARIMA'] = ARIMAForecaster(seasonal=True, m=7)
            self.models['Prophet'] = ProphetForecaster()
            try:
                self.models['LSTM'] = LSTMForecaster(look_back=30)
            except ImportError:
                print("Warning: TensorFlow not available. Skipping LSTM.")
        
        print("Models prepared")
    
    def train_models(self, data_dict: Dict[str, pd.DataFrame],
                    target_col: str = 'Quantity_Consumed',
                    test_size: float = 0.2) -> Dict[str, pd.DataFrame]:
        """
        Train models on data.
        
        Parameters:
        -----------
        data_dict : Dict[str, pd.DataFrame]
            Dictionary of processed dataframes
        target_col : str
            Name of target column
        test_size : float
            Proportion of data for testing
        
        Returns:
        --------
        Dict[str, pd.DataFrame]
            Dictionary of {item_id: test_dataframe}
        """
        print("\nTraining models...")
        test_dict = {}
        
        for item_id, df in data_dict.items():
            print(f"\nProcessing {item_id}...")
            
            # Split train/test
            train_df, test_df = self.data_loader.split_train_test(df, test_size=test_size)
            test_dict[item_id] = test_df
            
            # Prepare target series
            if target_col in train_df.columns:
                series = train_df[target_col]
            else:
                raise ValueError(f"Target column '{target_col}' not found in data")
            
            # Train ensemble or individual models
            if self.ensemble:
                # Train ensemble
                self.ensemble.fit(train_df, target_col=target_col)
            else:
                # Train individual models
                if 'ARIMA' in self.models:
                    print(f"  Training ARIMA for {item_id}...")
                    self.models['ARIMA'].fit(series)
                
                if 'Prophet' in self.models:
                    print(f"  Training Prophet for {item_id}...")
                    self.models['Prophet'].fit(train_df, target_col=target_col)
                
                if 'LSTM' in self.models:
                    print(f"  Training LSTM for {item_id}...")
                    self.models['LSTM'].fit(series)
        
        print("\nTraining completed")
        return test_dict
    
    def generate_forecasts(self, data_dict: Dict[str, pd.DataFrame],
                          target_col: str = 'Quantity_Consumed') -> Dict[str, pd.DataFrame]:
        """
        Generate forecasts for all items.
        
        Parameters:
        -----------
        data_dict : Dict[str, pd.DataFrame]
            Dictionary of processed dataframes
        target_col : str
            Name of target column
        
        Returns:
        --------
        Dict[str, pd.DataFrame]
            Dictionary of {item_id: forecast_dataframe}
        """
        print("\nGenerating forecasts...")
        forecasts = {}
        
        for item_id, df in data_dict.items():
            print(f"  Forecasting {item_id}...")
            
            # Prepare target series
            if target_col in df.columns:
                series = df[target_col]
            else:
                raise ValueError(f"Target column '{target_col}' not found in data")
            
            # Generate ensemble or individual forecasts
            if self.ensemble:
                forecast_df = self.ensemble.forecast(steps=self.config['forecast_horizon'])
            else:
                # Combine individual forecasts (simple average)
                forecast_list = []
                
                if 'ARIMA' in self.models:
                    arima_fc = self.models['ARIMA'].forecast(steps=self.config['forecast_horizon'])
                    forecast_list.append(arima_fc['forecast'])
                
                if 'Prophet' in self.models:
                    prophet_fc = self.models['Prophet'].forecast(periods=self.config['forecast_horizon'])
                    forecast_list.append(prophet_fc['forecast'].values)
                
                if 'LSTM' in self.models:
                    lstm_fc = self.models['LSTM'].forecast(series, steps=self.config['forecast_horizon'])
                    forecast_list.append(lstm_fc)
                
                if len(forecast_list) > 0:
                    # Average forecasts
                    avg_forecast = np.mean(forecast_list, axis=0)
                    forecast_df = pd.DataFrame({
                        'forecast': avg_forecast,
                        'lower': avg_forecast * 0.9,  # Simplified
                        'upper': avg_forecast * 1.1    # Simplified
                    })
                else:
                    raise ValueError("No models available for forecasting")
            
            forecasts[item_id] = forecast_df
        
        self.forecasts = forecasts
        print(f"\nGenerated forecasts for {len(forecasts)} items")
        return forecasts
    
    def calculate_reorder_points(self, forecasts: Dict[str, pd.DataFrame],
                                lead_times: Dict[str, int],
                                current_stocks: Dict[str, float],
                                std_demands: Optional[Dict[str, float]] = None) -> Dict[str, Dict]:
        """
        Calculate Reorder Points for all items.
        
        Parameters:
        -----------
        forecasts : Dict[str, pd.DataFrame]
            Dictionary of forecasts
        lead_times : Dict[str, int]
            Dictionary of {item_id: lead_time}
        current_stocks : Dict[str, float]
            Dictionary of {item_id: current_stock}
        std_demands : Optional[Dict[str, float]]
            Dictionary of {item_id: std_demand}
        
        Returns:
        --------
        Dict[str, Dict]
            Dictionary of {item_id: pp_info}
        """
        print("\nCalculating Reorder Points...")
        
        pp_results = self.pp_calculator.calculate_for_multiple_items(
            forecasts=forecasts,
            lead_times=lead_times,
            current_stocks=current_stocks,
            std_demands=std_demands
        )
        
        self.pp_results = pp_results
        
        # Generate alerts
        self.alerts = []
        for item_id, pp_info in pp_results.items():
            if 'error' not in pp_info:
                alert = self.pp_calculator.check_alert(pp_info)
                if alert:
                    self.alerts.append({
                        'item_id': item_id,
                        'alert': alert,
                        'pp_info': pp_info
                    })
        
        print(f"Calculated PP for {len(pp_results)} items")
        print(f"Generated {len(self.alerts)} alerts")
        
        return pp_results
    
    def generate_reports(self, output_dir: str = 'output') -> Dict[str, str]:
        """
        Generate weekly reports.
        
        Parameters:
        -----------
        output_dir : str
            Output directory
        
        Returns:
        --------
        Dict[str, str]
            Dictionary of {report_type: file_path}
        """
        print(f"\nGenerating reports in {output_dir}...")
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        report_files = {}
        
        # PP Report
        if self.pp_results:
            pp_report_path = Path(output_dir) / 'weekly_pp_report.csv'
            pp_report = self.pp_calculator.generate_weekly_report(
                self.pp_results,
                output_path=str(pp_report_path)
            )
            report_files['pp_report'] = str(pp_report_path)
            print(f"  PP Report: {pp_report_path}")
        
        # Forecasts Report
        if self.forecasts:
            forecasts_list = []
            for item_id, forecast_df in self.forecasts.items():
                forecast_df['item_id'] = item_id
                forecast_df = forecast_df.reset_index()
                forecasts_list.append(forecast_df)
            
            if forecasts_list:
                forecasts_report = pd.concat(forecasts_list, ignore_index=True)
                forecasts_path = Path(output_dir) / 'forecasts_report.csv'
                forecasts_report.to_csv(forecasts_path, index=False)
                report_files['forecasts'] = str(forecasts_path)
                print(f"  Forecasts Report: {forecasts_path}")
        
        # Alerts Report
        if self.alerts:
            alerts_list = []
            for alert_info in self.alerts:
                alerts_list.append({
                    'item_id': alert_info['item_id'],
                    'alert_message': alert_info['alert'],
                    'current_stock': alert_info['pp_info']['current_stock'],
                    'reorder_point': alert_info['pp_info']['reorder_point'],
                    'days_to_rupture': alert_info['pp_info']['days_to_rupture']
                })
            
            alerts_df = pd.DataFrame(alerts_list)
            alerts_path = Path(output_dir) / 'alerts_report.csv'
            alerts_df.to_csv(alerts_path, index=False)
            report_files['alerts'] = str(alerts_path)
            print(f"  Alerts Report: {alerts_path}")
        
        print(f"\nReports generated in {output_dir}")
        return report_files
    
    def run(self, data_file: str,
            lead_times: Dict[str, int],
            current_stocks: Dict[str, float],
            target_col: str = 'Quantity_Consumed',
            output_dir: str = 'output') -> Dict:
        """
        Run complete pipeline.
        
        Parameters:
        -----------
        data_file : str
            Path to data file
        lead_times : Dict[str, int]
            Dictionary of {item_id: lead_time}
        current_stocks : Dict[str, float]
            Dictionary of {item_id: current_stock}
        target_col : str
            Name of target column
        output_dir : str
            Output directory
        
        Returns:
        --------
        Dict
            Complete results
        """
        print("=" * 60)
        print("Nova Corrente Demand Forecasting Pipeline")
        print("=" * 60)
        
        # Step 1: Load and preprocess
        data_dict = self.load_and_preprocess(data_file)
        
        # Step 2: Prepare models
        self.prepare_models(data_dict, target_col=target_col)
        
        # Step 3: Train models
        test_dict = self.train_models(data_dict, target_col=target_col)
        
        # Step 4: Generate forecasts
        forecasts = self.generate_forecasts(data_dict, target_col=target_col)
        
        # Step 5: Calculate Reorder Points
        pp_results = self.calculate_reorder_points(
            forecasts=forecasts,
            lead_times=lead_times,
            current_stocks=current_stocks
        )
        
        # Step 6: Generate reports
        report_files = self.generate_reports(output_dir=output_dir)
        
        # Summary
        print("\n" + "=" * 60)
        print("Pipeline Execution Complete")
        print("=" * 60)
        print(f"Items processed: {len(data_dict)}")
        print(f"Forecasts generated: {len(forecasts)}")
        print(f"PP calculations: {len(pp_results)}")
        print(f"Alerts generated: {len(self.alerts)}")
        print(f"Reports: {len(report_files)}")
        
        return {
            'data': data_dict,
            'forecasts': forecasts,
            'pp_results': pp_results,
            'alerts': self.alerts,
            'reports': report_files
        }


# Example usage
if __name__ == "__main__":
    # Configuration
    config = {
        'service_level': 0.95,
        'ensemble_weights': {'ARIMA': 0.4, 'Prophet': 0.3, 'LSTM': 0.3},
        'forecast_horizon': 30,
        'use_ensemble': True,
        'external_features': True
    }
    
    # Initialize pipeline
    pipeline = DemandForecastingPipeline(config=config)
    
    # Example data file (create sample if needed)
    data_file = 'sample_demand_data.csv'
    
    # Lead times and current stocks (example)
    lead_times = {
        'CONN-001': 14,
        'CONN-002': 10,
    }
    
    current_stocks = {
        'CONN-001': 100,
        'CONN-002': 50,
    }
    
    # Run pipeline
    results = pipeline.run(
        data_file=data_file,
        lead_times=lead_times,
        current_stocks=current_stocks,
        output_dir='output'
    )
    
    print("\nPipeline execution completed successfully!")

