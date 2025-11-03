"""
Model registry for Nova Corrente ML models
Model versioning, persistence, and loading
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import pickle
import json
from pathlib import Path

from backend.services.database_service import db_service
from backend.config.ml_config import MODEL_STORAGE
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.ml_models.registry')


class ModelRegistry:
    """
    Manage ML model registry and persistence
    """
    
    def __init__(self):
        """Initialize model registry"""
        self.storage_path = Path(MODEL_STORAGE['base_path'])
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def register_model(
        self,
        model_name: str,
        model_type: str,
        model_version: str,
        algoritmo: str,
        metrics: Dict[str, float],
        hiperparametros: Dict[str, Any],
        model_path: str,
        familia_id: Optional[int] = None,
        description: Optional[str] = None
    ) -> int:
        """
        Register a new model in the database
        
        Args:
            model_name: Model name
            model_type: Model type (FORECASTING, CLASSIFICATION, etc.)
            model_version: Model version
            algoritmo: Algorithm name
            metrics: Evaluation metrics dictionary
            hiperparametros: Hyperparameters dictionary
            model_path: Path to saved model file
            familia_id: Optional family ID
            description: Optional description
        
        Returns:
            Model ID
        """
        try:
            query = """
                INSERT INTO MLModelRegistry (
                    model_name, model_type, model_version, algoritmo,
                    metricas_avaliacao, hiperparametros, caminho_modelo,
                    data_treinamento, status, descricao, familia_id
                ) VALUES (
                    :model_name, :model_type, :model_version, :algoritmo,
                    :metricas_avaliacao, :hiperparametros, :caminho_modelo,
                    NOW(), 'ATIVO', :descricao, :familia_id
                )
            """
            
            params = {
                'model_name': model_name,
                'model_type': model_type,
                'model_version': model_version,
                'algoritmo': algoritmo,
                'metricas_avaliacao': json.dumps(metrics),
                'hiperparametros': json.dumps(hiperparametros),
                'caminho_modelo': model_path,
                'descricao': description,
                'familia_id': familia_id,
            }
            
            db_service.execute_raw_sql(query, params=params)
            
            # Get inserted model ID
            query_id = """
                SELECT model_id FROM MLModelRegistry
                WHERE model_name = :model_name AND model_version = :model_version
                ORDER BY model_id DESC LIMIT 1
            """
            
            result = db_service.execute_query(
                query_id,
                params={'model_name': model_name, 'model_version': model_version},
                fetch_one=True
            )
            
            model_id = result['model_id'] if result else None
            
            logger.info(f"Registered model {model_name} v{model_version} with ID {model_id}")
            
            return model_id
        except Exception as e:
            logger.error(f"Error registering model: {e}")
            raise
    
    def get_model(self, model_id: int) -> Optional[Dict[str, Any]]:
        """
        Get model by ID
        
        Args:
            model_id: Model ID
        
        Returns:
            Model dictionary or None
        """
        try:
            query = """
                SELECT * FROM MLModelRegistry WHERE model_id = :model_id
            """
            
            result = db_service.execute_query(
                query,
                params={'model_id': model_id},
                fetch_one=True
            )
            
            if result:
                # Parse JSON fields
                if result.get('metricas_avaliacao'):
                    try:
                        result['metricas_avaliacao'] = json.loads(result['metricas_avaliacao'])
                    except:
                        result['metricas_avaliacao'] = {}
                
                if result.get('hiperparametros'):
                    try:
                        result['hiperparametros'] = json.loads(result['hiperparametros'])
                    except:
                        result['hiperparametros'] = {}
            
            return result
        except Exception as e:
            logger.error(f"Error getting model {model_id}: {e}")
            raise
    
    def get_active_models(
        self,
        model_type: Optional[str] = None,
        familia_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get active models with optional filters
        
        Args:
            model_type: Optional model type filter
            familia_id: Optional family ID filter
        
        Returns:
            List of model dictionaries
        """
        try:
            query = """
                SELECT * FROM MLModelRegistry
                WHERE status = 'ATIVO'
            """
            
            params = {}
            
            if model_type:
                query += " AND model_type = :model_type"
                params['model_type'] = model_type
            
            if familia_id:
                query += " AND (familia_id = :familia_id OR familia_id IS NULL)"
                params['familia_id'] = familia_id
            
            query += " ORDER BY data_treinamento DESC"
            
            results = db_service.execute_query(query, params=params)
            
            # Parse JSON fields
            for result in results:
                if result.get('metricas_avaliacao'):
                    try:
                        result['metricas_avaliacao'] = json.loads(result['metricas_avaliacao'])
                    except:
                        result['metricas_avaliacao'] = {}
                
                if result.get('hiperparametros'):
                    try:
                        result['hiperparametros'] = json.loads(result['hiperparametros'])
                    except:
                        result['hiperparametros'] = {}
            
            return results
        except Exception as e:
            logger.error(f"Error getting active models: {e}")
            raise
    
    def update_model_status(
        self,
        model_id: int,
        status: str
    ) -> bool:
        """
        Update model status
        
        Args:
            model_id: Model ID
            status: New status ('ATIVO', 'ARQUIVADO', 'DEPRECADO')
        
        Returns:
            True if successful
        """
        try:
            query = """
                UPDATE MLModelRegistry
                SET status = :status, data_atualizacao = NOW()
                WHERE model_id = :model_id
            """
            
            db_service.execute_raw_sql(
                query,
                params={'model_id': model_id, 'status': status}
            )
            
            logger.info(f"Updated model {model_id} status to {status}")
            return True
        except Exception as e:
            logger.error(f"Error updating model status: {e}")
            raise
    
    def save_model(
        self,
        model: Any,
        model_name: str,
        model_type: str,
        model_version: str
    ) -> str:
        """
        Save model to disk
        
        Args:
            model: Model object
            model_name: Model name
            model_type: Model type
            model_version: Model version
        
        Returns:
            Path to saved model file
        """
        try:
            # Create directory for model type
            model_dir = self.storage_path / model_type.lower()
            model_dir.mkdir(parents=True, exist_ok=True)
            
            # Create model filename
            model_filename = f"{model_name}_v{model_version}.pkl"
            model_path = model_dir / model_filename
            
            # Save model
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            
            logger.info(f"Saved model to {model_path}")
            
            return str(model_path)
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise
    
    def load_model(self, model_path: str) -> Any:
        """
        Load model from disk
        
        Args:
            model_path: Path to model file
        
        Returns:
            Loaded model object
        """
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            logger.info(f"Loaded model from {model_path}")
            
            return model
        except Exception as e:
            logger.error(f"Error loading model from {model_path}: {e}")
            raise


# Singleton instance
model_registry = ModelRegistry()

