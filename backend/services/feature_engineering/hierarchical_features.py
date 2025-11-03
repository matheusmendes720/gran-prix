"""
Hierarchical feature engineering for Nova Corrente
Family, site, supplier aggregations
"""
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from backend.services.database_service import db_service
from backend.config.feature_config import HIERARCHICAL_FEATURES
from backend.config.logging_config import get_logger

logger = get_logger('nova_corrente.features.hierarchical')


class HierarchicalFeatureExtractor:
    """
    Extract hierarchical features (family, site, supplier aggregations)
    """
    
    def extract_family_features(
        self,
        material_id: int,
        aggregation_metrics: List[str] = None
    ) -> Dict[str, float]:
        """
        Extract features aggregated at family level
        
        Args:
            material_id: Material ID
            aggregation_metrics: List of aggregation methods (default from config)
        
        Returns:
            Dictionary of family feature name -> value
        """
        if aggregation_metrics is None:
            aggregation_metrics = HIERARCHICAL_FEATURES.get(
                'aggregation_metrics',
                ['mean', 'sum', 'count', 'std']
            )
        
        features = {}
        
        try:
            # Get material's family ID
            query = """
                SELECT familia_id FROM Material WHERE material_id = :material_id
            """
            result = db_service.execute_query(
                query,
                params={'material_id': material_id},
                fetch_one=True
            )
            
            if not result or not result.get('familia_id'):
                return {}
            
            familia_id = result['familia_id']
            
            # Get family-level aggregations
            query = """
                SELECT 
                    COUNT(DISTINCT m.material_id) as total_materiais,
                    AVG(m.quantidade_atual) as media_estoque,
                    SUM(m.quantidade_atual) as total_estoque,
                    STDDEV(m.quantidade_atual) as std_estoque,
                    AVG(m.reorder_point) as media_reorder_point,
                    SUM(CASE WHEN me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada ELSE 0 END) as total_saidas,
                    COUNT(me.movimentacao_id) as total_movimentacoes
                FROM Material m
                LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id
                WHERE m.familia_id = :familia_id
                AND DATE(me.data_movimentacao) >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                GROUP BY m.familia_id
            """
            
            result = db_service.execute_query(
                query,
                params={'familia_id': familia_id},
                fetch_one=True
            )
            
            if result:
                features['familia_total_materiais'] = float(result.get('total_materiais', 0) or 0)
                features['familia_media_estoque'] = float(result.get('media_estoque', 0) or 0)
                features['familia_total_estoque'] = float(result.get('total_estoque', 0) or 0)
                features['familia_std_estoque'] = float(result.get('std_estoque', 0) or 0)
                features['familia_media_reorder_point'] = float(result.get('media_reorder_point', 0) or 0)
                features['familia_total_saidas'] = float(result.get('total_saidas', 0) or 0)
                features['familia_total_movimentacoes'] = float(result.get('total_movimentacoes', 0) or 0)
                
                # Calculate ratios if material's stock is available
                material_query = """
                    SELECT quantidade_atual FROM Material WHERE material_id = :material_id
                """
                material_result = db_service.execute_query(
                    material_query,
                    params={'material_id': material_id},
                    fetch_one=True
                )
                
                if material_result and HIERARCHICAL_FEATURES.get('include_ratios', True):
                    material_stock = float(material_result.get('quantidade_atual', 0) or 0)
                    if features['familia_media_estoque'] > 0:
                        features['material_familia_ratio'] = material_stock / features['familia_media_estoque']
                    else:
                        features['material_familia_ratio'] = 0.0
        except Exception as e:
            logger.warning(f"Error extracting family features for material {material_id}: {e}")
        
        return features
    
    def extract_site_features(
        self,
        material_id: int,
        site_id: Optional[str] = None
    ) -> Dict[str, float]:
        """
        Extract features aggregated at site level
        
        Args:
            material_id: Material ID
            site_id: Optional specific site ID
        
        Returns:
            Dictionary of site feature name -> value
        """
        features = {}
        
        try:
            # Get site aggregations for this material
            if site_id:
                query = """
                    SELECT 
                        COUNT(DISTINCT me.movimentacao_id) as movimentacoes_site,
                        SUM(CASE WHEN me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada ELSE 0 END) as saidas_site,
                        AVG(CASE WHEN me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada ELSE 0 END) as media_saidas_site,
                        MAX(me.data_movimentacao) as ultima_movimentacao_site
                    FROM MovimentacaoEstoque me
                    WHERE me.material_id = :material_id
                    AND me.site_id = :site_id
                    AND DATE(me.data_movimentacao) >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                """
                params = {'material_id': material_id, 'site_id': site_id}
            else:
                # Aggregate across all sites
                query = """
                    SELECT 
                        COUNT(DISTINCT me.site_id) as total_sites,
                        COUNT(DISTINCT me.movimentacao_id) as movimentacoes_total,
                        SUM(CASE WHEN me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada ELSE 0 END) as saidas_total,
                        AVG(CASE WHEN me.tipo_movimentacao = 'SAIDA' THEN me.quantidade_movimentada ELSE 0 END) as media_saidas
                    FROM MovimentacaoEstoque me
                    WHERE me.material_id = :material_id
                    AND DATE(me.data_movimentacao) >= DATE_SUB(NOW(), INTERVAL 30 DAY)
                """
                params = {'material_id': material_id}
            
            result = db_service.execute_query(query, params=params, fetch_one=True)
            
            if result:
                if site_id:
                    features['site_movimentacoes'] = float(result.get('movimentacoes_site', 0) or 0)
                    features['site_saidas'] = float(result.get('saidas_site', 0) or 0)
                    features['site_media_saidas'] = float(result.get('media_saidas_site', 0) or 0)
                else:
                    features['total_sites'] = float(result.get('total_sites', 0) or 0)
                    features['site_movimentacoes_total'] = float(result.get('movimentacoes_total', 0) or 0)
                    features['site_saidas_total'] = float(result.get('saidas_total', 0) or 0)
                    features['site_media_saidas'] = float(result.get('media_saidas', 0) or 0)
        except Exception as e:
            logger.warning(f"Error extracting site features for material {material_id}: {e}")
        
        return features
    
    def extract_supplier_features(
        self,
        material_id: int
    ) -> Dict[str, float]:
        """
        Extract features aggregated at supplier level
        
        Args:
            material_id: Material ID
        
        Returns:
            Dictionary of supplier feature name -> value
        """
        features = {}
        
        try:
            # Get supplier aggregations
            query = """
                SELECT 
                    COUNT(DISTINCT fm.fornecedor_id) as total_fornecedores,
                    AVG(fm.lead_time_padrao) as media_lead_time,
                    MIN(fm.lead_time_padrao) as min_lead_time,
                    MAX(fm.lead_time_padrao) as max_lead_time,
                    AVG(f.score_performance) as media_score_performance,
                    AVG(f.lead_time_medio) as media_lead_time_fornecedor,
                    COUNT(CASE WHEN me.tipo_movimentacao = 'ENTRADA' THEN 1 END) as total_entradas_fornecedores
                FROM Material m
                LEFT JOIN Fornecedor_Material fm ON m.material_id = fm.material_id
                LEFT JOIN Fornecedor f ON fm.fornecedor_id = f.fornecedor_id
                LEFT JOIN MovimentacaoEstoque me ON m.material_id = me.material_id AND me.fornecedor_id = f.fornecedor_id
                WHERE m.material_id = :material_id
                AND DATE(me.data_movimentacao) >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            """
            
            result = db_service.execute_query(
                query,
                params={'material_id': material_id},
                fetch_one=True
            )
            
            if result:
                features['total_fornecedores'] = float(result.get('total_fornecedores', 0) or 0)
                features['media_lead_time'] = float(result.get('media_lead_time', 0) or 0)
                features['min_lead_time'] = float(result.get('min_lead_time', 0) or 0)
                features['max_lead_time'] = float(result.get('max_lead_time', 0) or 0)
                features['media_score_performance'] = float(result.get('media_score_performance', 0) or 0)
                features['media_lead_time_fornecedor'] = float(result.get('media_lead_time_fornecedor', 0) or 0)
                features['total_entradas_fornecedores'] = float(result.get('total_entradas_fornecedores', 0) or 0)
        except Exception as e:
            logger.warning(f"Error extracting supplier features for material {material_id}: {e}")
        
        return features
    
    def extract_all_hierarchical_features(
        self,
        material_id: int,
        include_family: bool = True,
        include_site: bool = True,
        include_supplier: bool = True
    ) -> Dict[str, float]:
        """
        Extract all hierarchical features
        
        Args:
            material_id: Material ID
            include_family: Include family features
            include_site: Include site features
            include_supplier: Include supplier features
        
        Returns:
            Dictionary of all hierarchical feature name -> value
        """
        features = {}
        
        if include_family:
            features.update(self.extract_family_features(material_id))
        
        if include_site:
            features.update(self.extract_site_features(material_id))
        
        if include_supplier:
            features.update(self.extract_supplier_features(material_id))
        
        return features


# Singleton instance
hierarchical_feature_extractor = HierarchicalFeatureExtractor()

