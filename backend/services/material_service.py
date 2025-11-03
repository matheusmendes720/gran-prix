"""
Material service for Nova Corrente
Provides CRUD operations and feature retrieval
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import pandas as pd

from backend.services.database_service import db_service
from backend.data_structures.time_series import TimeSeries
from backend.data_structures.material_context import MaterialContext
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.services.material')


class MaterialService:
    """
    Service for material operations
    """
    
    def get_material(self, material_id: int) -> Optional[Dict[str, Any]]:
        """
        Get material by ID
        
        Args:
            material_id: Material ID
        
        Returns:
            Material dictionary or None
        """
        try:
            query = """
                SELECT m.*, f.nome_familia, f.categoria_criticidade as familia_criticidade
                FROM Material m
                LEFT JOIN Familia f ON m.familia_id = f.familia_id
                WHERE m.material_id = :material_id
            """
            result = db_service.execute_query(
                query,
                params={'material_id': material_id},
                fetch_one=True
            )
            
            if result:
                logger.info(f"Retrieved material {material_id}")
            else:
                logger.warning(f"Material {material_id} not found")
            
            return result
        except Exception as e:
            logger.error(f"Error getting material {material_id}: {e}")
            raise
    
    def get_materials(
        self,
        familia_id: Optional[int] = None,
        tier_nivel: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get list of materials with filters
        
        Args:
            familia_id: Optional family ID filter
            tier_nivel: Optional tier level filter
            limit: Maximum results
            offset: Offset for pagination
        
        Returns:
            List of material dictionaries
        """
        try:
            query = """
                SELECT m.*, f.nome_familia, f.categoria_criticidade as familia_criticidade
                FROM Material m
                LEFT JOIN Familia f ON m.familia_id = f.familia_id
                WHERE 1=1
            """
            params = {}
            
            if familia_id:
                query += " AND m.familia_id = :familia_id"
                params['familia_id'] = familia_id
            
            if tier_nivel:
                query += " AND m.tier_nivel = :tier_nivel"
                params['tier_nivel'] = tier_nivel
            
            query += " LIMIT :limit OFFSET :offset"
            params['limit'] = limit
            params['offset'] = offset
            
            results = db_service.execute_query(query, params=params)
            logger.info(f"Retrieved {len(results)} materials")
            return results
        except Exception as e:
            logger.error(f"Error getting materials: {e}")
            raise
    
    def get_material_historical(
        self,
        material_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        aggregation: str = 'daily'
    ) -> TimeSeries:
        """
        Get historical data for material
        
        Args:
            material_id: Material ID
            start_date: Optional start date
            end_date: Optional end date
            aggregation: Aggregation level ('daily', 'weekly', 'monthly')
        
        Returns:
            TimeSeries object
        """
        try:
            # Determine table based on aggregation
            table_map = {
                'daily': 'MaterialHistoricoDiario',
                'weekly': 'MaterialHistoricoSemanal',
                'monthly': 'MaterialHistoricoMensal'
            }
            
            table = table_map.get(aggregation, 'MaterialHistoricoDiario')
            
            query = f"""
                SELECT data_referencia, quantidade_final, entrada_total, saida_total,
                       numero_movimentacoes, movimentacao_media, is_feriado, is_weekend
                FROM {table}
                WHERE material_id = :material_id
            """
            
            params = {'material_id': material_id}
            
            if start_date:
                query += " AND data_referencia >= :start_date"
                params['start_date'] = start_date
            
            if end_date:
                query += " AND data_referencia <= :end_date"
                params['end_date'] = end_date
            
            query += " ORDER BY data_referencia"
            
            df = db_service.get_dataframe(query, params=params)
            
            if df.empty:
                logger.warning(f"No historical data found for material {material_id}")
                return TimeSeries(pd.DataFrame(), material_id=material_id)
            
            time_series = TimeSeries(
                df,
                date_column='data_referencia',
                value_column='quantidade_final',
                material_id=material_id
            )
            
            logger.info(
                f"Retrieved {len(df)} historical records for material {material_id}"
            )
            return time_series
        except Exception as e:
            logger.error(f"Error getting historical data for material {material_id}: {e}")
            raise
    
    def get_material_movements(
        self,
        material_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        tipo_movimentacao: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get stock movements for material
        
        Args:
            material_id: Material ID
            start_date: Optional start date
            end_date: Optional end date
            tipo_movimentacao: Optional movement type ('ENTRADA', 'SAIDA')
        
        Returns:
            DataFrame with movements
        """
        try:
            query = """
                SELECT me.*, u.nome_usuario, f.nome_fornecedor
                FROM MovimentacaoEstoque me
                LEFT JOIN Usuario u ON me.usuario_id = u.usuario_id
                LEFT JOIN Fornecedor f ON me.fornecedor_id = f.fornecedor_id
                WHERE me.material_id = :material_id
            """
            
            params = {'material_id': material_id}
            
            if start_date:
                query += " AND DATE(me.data_movimentacao) >= :start_date"
                params['start_date'] = start_date
            
            if end_date:
                query += " AND DATE(me.data_movimentacao) <= :end_date"
                params['end_date'] = end_date
            
            if tipo_movimentacao:
                query += " AND me.tipo_movimentacao = :tipo_movimentacao"
                params['tipo_movimentacao'] = tipo_movimentacao
            
            query += " ORDER BY me.data_movimentacao DESC"
            
            df = db_service.get_dataframe(query, params=params)
            logger.info(f"Retrieved {len(df)} movements for material {material_id}")
            return df
        except Exception as e:
            logger.error(f"Error getting movements for material {material_id}: {e}")
            raise
    
    def get_material_context(self, material_id: int) -> MaterialContext:
        """
        Get complete material context with features and time series
        
        Args:
            material_id: Material ID
        
        Returns:
            MaterialContext object
        """
        try:
            # Get material info
            material = self.get_material(material_id)
            if not material:
                raise ValueError(f"Material {material_id} not found")
            
            # Get time series
            time_series = self.get_material_historical(material_id)
            
            # Get metadata
            metadata = {
                'familia_id': material.get('familia_id'),
                'familia_nome': material.get('nome_familia'),
                'tier_nivel': material.get('tier_nivel'),
                'categoria_abc': material.get('categoria_abc'),
                'reorder_point': material.get('reorder_point'),
                'safety_stock': material.get('safety_stock'),
            }
            
            context = MaterialContext(
                material_id=material_id,
                material_name=material.get('nome_material', ''),
                time_series=time_series,
                metadata=metadata
            )
            
            logger.info(f"Created material context for material {material_id}")
            return context
        except Exception as e:
            logger.error(f"Error getting material context for {material_id}: {e}")
            raise
    
    def update_material_ml_fields(
        self,
        material_id: int,
        reorder_point: Optional[int] = None,
        safety_stock: Optional[int] = None,
        categoria_abc: Optional[str] = None,
        score_importancia: Optional[float] = None
    ) -> bool:
        """
        Update ML-calculated fields for material
        
        Args:
            material_id: Material ID
            reorder_point: New reorder point
            safety_stock: New safety stock
            categoria_abc: New ABC category
            score_importancia: New importance score
        
        Returns:
            True if successful
        """
        try:
            updates = []
            params = {'material_id': material_id}
            
            if reorder_point is not None:
                updates.append("reorder_point = :reorder_point")
                params['reorder_point'] = reorder_point
            
            if safety_stock is not None:
                updates.append("safety_stock = :safety_stock")
                params['safety_stock'] = safety_stock
            
            if categoria_abc is not None:
                updates.append("categoria_abc = :categoria_abc")
                params['categoria_abc'] = categoria_abc
            
            if score_importancia is not None:
                updates.append("score_importancia = :score_importancia")
                params['score_importancia'] = score_importancia
            
            if not updates:
                return True
            
            updates.append("ultima_atualizacao_ml = NOW()")
            
            query = f"""
                UPDATE Material
                SET {', '.join(updates)}
                WHERE material_id = :material_id
            """
            
            db_service.execute_raw_sql(query, params=params)
            logger.info(f"Updated ML fields for material {material_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating ML fields for material {material_id}: {e}")
            raise


# Singleton instance
material_service = MaterialService()

