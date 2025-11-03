"""
Configuration management module.
Handles configuration loading from YAML files.
"""
import yaml
import os
from typing import Dict, Optional
from pathlib import Path


class Config:
    """Configuration management class."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path or self._default_config_path()
        self.config: Dict = {}
        self.load()
    
    def _default_config_path(self) -> str:
        """Get default configuration file path."""
        # Look for config.yaml in project root
        current_dir = Path(__file__).parent.parent.parent
        config_path = current_dir / 'config.yaml'
        return str(config_path)
    
    def load(self, config_path: Optional[str] = None) -> Dict:
        """
        Load configuration from YAML file.
        
        Args:
            config_path: Optional path to config file
        
        Returns:
            Configuration dictionary
        """
        if config_path:
            self.config_path = config_path
        
        if not os.path.exists(self.config_path):
            # Use default configuration
            self.config = self._default_config()
            return self.config
        
        try:
            with open(self.config_path, 'r') as f:
                self.config = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
            self.config = self._default_config()
        
        return self.config
    
    def _default_config(self) -> Dict:
        """Get default configuration."""
        return {
            'forecasting': {
                'forecast_steps': 30,
                'service_level': 0.95,
                'lead_time': 14,
                'safety_stock_default': 20,
                'min_years_data': 2
            },
            'models': {
                'arima': {
                    'seasonal': True,
                    'm': 7
                },
                'prophet': {
                    'country': 'BR',
                    'daily_seasonality': True,
                    'yearly_seasonality': True,
                    'weekly_seasonality': True
                },
                'lstm': {
                    'look_back': 30,
                    'units': 50,
                    'epochs': 50,
                    'batch_size': 32
                },
                'ensemble': {
                    'weights': {
                        'ARIMA': 0.4,
                        'Prophet': 0.3,
                        'LSTM': 0.3
                    },
                    'use_lstm': True
                }
            },
            'data': {
                'external_features': True,
                'min_years': 2
            },
            'alerts': {
                'enabled': False,
                'urgency_thresholds': {
                    'critical': 7,
                    'high': 14,
                    'medium': 30
                }
            },
            'reporting': {
                'output_dir': 'reports',
                'format': ['csv', 'pdf'],
                'visualizations': True
            }
        }
    
    def get(self, key: str, default=None):
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'models.arima.seasonal')
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
                if value is default and k != keys[-1]:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def save(self, config_path: Optional[str] = None):
        """
        Save configuration to YAML file.
        
        Args:
            config_path: Optional path to save config file
        """
        if config_path:
            self.config_path = config_path
        
        # Create directory if needed
        os.makedirs(os.path.dirname(self.config_path) if os.path.dirname(self.config_path) else '.', 
                   exist_ok=True)
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

