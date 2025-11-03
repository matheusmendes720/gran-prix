"""
Model persistence utilities.
Save and load trained models.
"""
import pickle
import json
import joblib
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class ModelPersistence:
    """Save and load trained models."""
    
    def __init__(self, models_dir: str = 'models'):
        """
        Initialize model persistence.
        
        Args:
            models_dir: Directory to store models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(exist_ok=True)
    
    def save_model(self, model: Any, item_id: str, model_type: str,
                   metadata: Optional[Dict] = None) -> str:
        """
        Save trained model.
        
        Args:
            model: Trained model object
            item_id: Item identifier
            model_type: Type of model (e.g., 'arima', 'prophet', 'lstm', 'ensemble')
            metadata: Optional metadata dictionary
        
        Returns:
            Path to saved model file
        """
        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{item_id}_{model_type}_{timestamp}.pkl"
        model_path = self.models_dir / filename
        
        # Save model
        try:
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
        except Exception:
            # Fallback to joblib if pickle fails
            joblib.dump(model, model_path)
        
        # Save metadata if provided
        if metadata:
            metadata_path = model_path.with_suffix('.json')
            metadata['saved_at'] = datetime.now().isoformat()
            metadata['model_file'] = str(model_path)
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        return str(model_path)
    
    def load_model(self, item_id: str, model_type: str,
                   latest: bool = True) -> Optional[Any]:
        """
        Load trained model.
        
        Args:
            item_id: Item identifier
            model_type: Type of model
            latest: If True, load latest model; if False, load first found
        
        Returns:
            Loaded model object or None if not found
        """
        # Find model files
        pattern = f"{item_id}_{model_type}_*.pkl"
        model_files = list(self.models_dir.glob(pattern))
        
        if not model_files:
            return None
        
        # Select file (latest or first)
        if latest:
            model_file = max(model_files, key=lambda p: p.stat().st_mtime)
        else:
            model_file = model_files[0]
        
        # Load model
        try:
            with open(model_file, 'rb') as f:
                model = pickle.load(f)
        except Exception:
            # Fallback to joblib
            model = joblib.load(model_file)
        
        return model
    
    def list_models(self, item_id: Optional[str] = None,
                   model_type: Optional[str] = None) -> list:
        """
        List available models.
        
        Args:
            item_id: Filter by item ID (optional)
            model_type: Filter by model type (optional)
        
        Returns:
            List of model file paths
        """
        if item_id and model_type:
            pattern = f"{item_id}_{model_type}_*.pkl"
        elif item_id:
            pattern = f"{item_id}_*.pkl"
        elif model_type:
            pattern = f"*_{model_type}_*.pkl"
        else:
            pattern = "*.pkl"
        
        model_files = list(self.models_dir.glob(pattern))
        return [str(f) for f in sorted(model_files, key=lambda p: p.stat().st_mtime, reverse=True)]
    
    def load_metadata(self, model_path: str) -> Optional[Dict]:
        """Load metadata for a model."""
        metadata_path = Path(model_path).with_suffix('.json')
        
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                return json.load(f)
        
        return None
    
    def delete_model(self, model_path: str) -> bool:
        """
        Delete model and associated files.
        
        Args:
            model_path: Path to model file
        
        Returns:
            True if successful, False otherwise
        """
        model_file = Path(model_path)
        metadata_file = model_file.with_suffix('.json')
        
        try:
            if model_file.exists():
                model_file.unlink()
            if metadata_file.exists():
                metadata_file.unlink()
            return True
        except Exception:
            return False

