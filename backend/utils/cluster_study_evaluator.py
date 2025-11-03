"""
Cluster Study Evaluator - Re-ranks and evaluates all datasets for telecom/logistics relevance
Scores datasets 0-100 based on business case fit (spare parts demand forecasting for Nova Corrente)
"""
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class ClusterStudyEvaluator:
    """
    Evaluates datasets for relevance to Nova Corrente's business case:
    - Spare parts demand forecasting
    - Telecom tower maintenance
    - Brazilian logistics market
    - SLA compliance (99%+ uptime)
    """
    
    # Keywords that indicate high relevance
    HIGH_RELEVANCE_KEYWORDS = {
        'telecom': ['telecom', 'tower', 'spare parts', 'infrastructure', 'network', 'base station', '5g', 'antenna', 'site'],
        'maintenance': ['maintenance', 'failure', 'repair', 'predictive', 'equipment', 'fault', 'downtime'],
        'logistics': ['logistics', 'warehouse', 'supply chain', 'inventory', 'lead time', 'delivery', 'shipment'],
        'brazil': ['brazil', 'brazilian', 'anatel', 'bahia', 'salvador', 'rio', 'são paulo'],
        'demand': ['demand', 'forecast', 'consumption', 'usage', 'quantity', 'orders']
    }
    
    # Keywords that indicate low relevance
    LOW_RELEVANCE_KEYWORDS = {
        'unrelated': ['ecommerce', 'retail', 'billing', 'consumer', 'social media', 'advertising']
    }
    
    def __init__(self, config_path: str = 'config/datasets_config.json'):
        """Initialize evaluator with datasets config"""
        self.config_path = Path(config_path)
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.datasets = self.config.get('datasets', {})
        
    def evaluate_dataset(self, dataset_id: str, dataset_info: Dict) -> Dict:
        """
        Evaluate a single dataset and return score + categories
        
        Scoring breakdown (0-100):
        - Direct relevance to spare parts demand (0-30 points)
        - Telecom industry fit (0-25 points)
        - Brazilian market relevance (0-15 points)
        - Data quality/completeness (0-15 points)
        - Lead time/cost information (0-10 points)
        - Research/validation value (0-5 points)
        """
        score = 0
        reasons = []
        categories = []
        
        # Combine all text fields for keyword search
        text_content = ' '.join([
            dataset_info.get('name', ''),
            dataset_info.get('description', ''),
            dataset_info.get('preprocessing_notes', ''),
            dataset_info.get('notes', ''),
            json.dumps(dataset_info.get('columns_mapping', {}))
        ]).lower()
        
        # 1. Direct relevance to spare parts demand (0-30)
        demand_score = 0
        if any(kw in text_content for kw in self.HIGH_RELEVANCE_KEYWORDS['demand']):
            demand_score += 10
            reasons.append("Contains demand/forecast data")
        if any(kw in text_content for kw in ['spare parts', 'part_id', 'part', 'sku', 'item_id']):
            demand_score += 15
            reasons.append("Direct spare parts/inventory focus")
        if 'lead_time' in text_content or 'lead time' in text_content:
            demand_score += 5
            reasons.append("Includes lead time data")
        score += demand_score
        if demand_score >= 20:
            categories.append('demand_forecasting')
            
        # 2. Telecom industry fit (0-25)
        telecom_score = 0
        if any(kw in text_content for kw in self.HIGH_RELEVANCE_KEYWORDS['telecom']):
            telecom_score += 15
            reasons.append("Telecom industry data")
        if any(kw in text_content for kw in self.HIGH_RELEVANCE_KEYWORDS['maintenance']):
            telecom_score += 10
            reasons.append("Maintenance/failure data")
        score += telecom_score
        if telecom_score >= 15:
            categories.append('telecom_industry')
            
        # 3. Brazilian market relevance (0-15)
        brazil_score = 0
        if any(kw in text_content for kw in self.HIGH_RELEVANCE_KEYWORDS['brazil']):
            brazil_score += 15
            reasons.append("Brazilian market data")
        elif dataset_info.get('source') in ['anatel', 'inmet', 'bacen', 'ibge']:
            brazil_score += 10
            reasons.append("Brazilian government source")
        score += brazil_score
        if brazil_score >= 10:
            categories.append('brazilian_market')
            
        # 4. Data quality/completeness (0-15)
        quality_score = 0
        has_date = dataset_info.get('columns_mapping', {}).get('date') is not None
        has_quantity = dataset_info.get('columns_mapping', {}).get('quantity') is not None
        has_item_id = dataset_info.get('columns_mapping', {}).get('item_id') is not None
        
        if has_date:
            quality_score += 5
            reasons.append("Time-series data available")
        if has_quantity:
            quality_score += 5
            reasons.append("Quantity/demand column present")
        if has_item_id:
            quality_score += 5
            reasons.append("Item/product identification available")
        score += quality_score
        if quality_score >= 10:
            categories.append('high_quality')
            
        # 5. Lead time/cost information (0-10)
        logistics_score = 0
        if 'lead_time' in text_content or 'lead time' in text_content:
            logistics_score += 5
            reasons.append("Lead time data included")
        if 'cost' in text_content or 'price' in text_content:
            logistics_score += 5
            reasons.append("Cost/price information available")
        score += logistics_score
        if logistics_score >= 5:
            categories.append('logistics_ready')
            
        # 6. Research/validation value (0-5)
        research_score = 0
        if dataset_info.get('source') in ['mit', 'ieee', 'zenodo']:
            research_score += 5
            reasons.append("Academic/research dataset")
            categories.append('research_reference')
        score += research_score
        
        # Special bonus for perfect fit datasets
        if 'mit_telecom' in dataset_id or 'mit_telecom_parts' in dataset_id:
            score = min(100, score + 20)
            reasons.append("BONUS: MIT telecom spare parts research (perfect match)")
            categories.append('perfect_match')
            
        # Penalties for low relevance
        if any(kw in text_content for kw in self.LOW_RELEVANCE_KEYWORDS['unrelated']):
            score = max(0, score - 20)
            reasons.append("PENALTY: Low relevance keywords detected")
            
        # Determine tier
        if score >= 80:
            tier = 'hell_yes'
            recommendation = 'CRITICAL - Perfect fit for business case'
        elif score >= 60:
            tier = 'high_priority'
            recommendation = 'HIGH - Strong relevance, recommended for pipeline'
        elif score >= 40:
            tier = 'medium_priority'
            recommendation = 'MEDIUM - Useful but may need adaptation'
        elif score >= 20:
            tier = 'low_priority'
            recommendation = 'LOW - Limited relevance, consider as external factor only'
        else:
            tier = 'skip'
            recommendation = 'SKIP - Not relevant for business case'
            
        return {
            'dataset_id': dataset_id,
            'score': min(100, max(0, score)),
            'tier': tier,
            'recommendation': recommendation,
            'categories': categories,
            'reasons': reasons,
            'breakdown': {
                'demand_relevance': demand_score,
                'telecom_fit': telecom_score,
                'brazil_market': brazil_score,
                'data_quality': quality_score,
                'logistics_info': logistics_score,
                'research_value': research_score
            }
        }
    
    def evaluate_all(self) -> Dict[str, Dict]:
        """Evaluate all datasets and return sorted results"""
        results = {}
        
        for dataset_id, dataset_info in self.datasets.items():
            evaluation = self.evaluate_dataset(dataset_id, dataset_info)
            results[dataset_id] = evaluation
            
        return results
    
    def get_tiered_datasets(self, results: Optional[Dict[str, Dict]] = None) -> Dict[str, List[Dict]]:
        """Group datasets by tier"""
        if results is None:
            results = self.evaluate_all()
            
        tiered = {
            'hell_yes': [],
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'skip': []
        }
        
        for dataset_id, eval_data in results.items():
            tier = eval_data['tier']
            tiered[tier].append({
                'dataset_id': dataset_id,
                'name': self.datasets[dataset_id].get('name', dataset_id),
                'score': eval_data['score'],
                'categories': eval_data['categories'],
                'recommendation': eval_data['recommendation']
            })
            
        # Sort each tier by score
        for tier in tiered:
            tiered[tier].sort(key=lambda x: x['score'], reverse=True)
            
        return tiered
    
    def generate_summary_report(self, output_path: Optional[Path] = None) -> Path:
        """Generate comprehensive evaluation report"""
        if output_path is None:
            output_path = Path('docs/documentation/cluster_study') / 'EVALUATION_SUMMARY.md'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        results = self.evaluate_all()
        tiered = self.get_tiered_datasets(results)
        
        lines = []
        lines.append("# 🎯 Cluster Study Evaluation Summary")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Total Datasets Evaluated:** {len(results)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📊 Evaluation Criteria")
        lines.append("")
        lines.append("Datasets are scored 0-100 based on:")
        lines.append("- **Direct Relevance to Spare Parts Demand (0-30):** Does it directly support demand forecasting?")
        lines.append("- **Telecom Industry Fit (0-25):** Is it from or relevant to telecom industry?")
        lines.append("- **Brazilian Market Relevance (0-15):** Does it cover Brazilian market/data?")
        lines.append("- **Data Quality/Completeness (0-15):** Has date, quantity, item_id columns?")
        lines.append("- **Lead Time/Cost Information (0-10):** Includes logistics data?")
        lines.append("- **Research/Validation Value (0-5):** Academic/research dataset?")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Summary stats
        lines.append("## 📈 Summary Statistics")
        lines.append("")
        for tier, datasets in tiered.items():
            if datasets:
                lines.append(f"- **{tier.replace('_', ' ').title()}:** {len(datasets)} datasets")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Hell Yes tier (most important)
        if tiered['hell_yes']:
            lines.append("## ✅ HELL YES - Critical Datasets (Score ≥ 80)")
            lines.append("")
            lines.append("**These datasets are perfect fit for Nova Corrente's business case.**")
            lines.append("")
            for ds in tiered['hell_yes']:
                lines.append(f"### {ds['name']}")
                lines.append("")
                lines.append(f"- **Score:** {ds['score']}/100")
                lines.append(f"- **ID:** `{ds['dataset_id']}`")
                lines.append(f"- **Categories:** {', '.join(ds['categories'])}")
                lines.append(f"- **Recommendation:** {ds['recommendation']}")
                lines.append("")
            lines.append("---")
            lines.append("")
            
        # High Priority
        if tiered['high_priority']:
            lines.append("## 🔥 High Priority Datasets (Score 60-79)")
            lines.append("")
            lines.append("**Strong relevance, recommended for pipeline.**")
            lines.append("")
            for ds in tiered['high_priority']:
                lines.append(f"### {ds['name']}")
                lines.append("")
                lines.append(f"- **Score:** {ds['score']}/100")
                lines.append(f"- **ID:** `{ds['dataset_id']}`")
                lines.append(f"- **Categories:** {', '.join(ds['categories'])}")
                lines.append("")
            lines.append("---")
            lines.append("")
            
        # Medium Priority
        if tiered['medium_priority']:
            lines.append("## ⚡ Medium Priority Datasets (Score 40-59)")
            lines.append("")
            for ds in tiered['medium_priority'][:10]:  # Top 10
                lines.append(f"- **{ds['name']}** (Score: {ds['score']}) - `{ds['dataset_id']}`")
            lines.append("")
            lines.append("---")
            lines.append("")
            
        # Low Priority and Skip (brief mention)
        if tiered['low_priority']:
            lines.append(f"## 📝 Low Priority Datasets (Score 20-39): {len(tiered['low_priority'])} datasets")
            lines.append("")
        if tiered['skip']:
            lines.append(f"## ⏭️ Skip Datasets (Score < 20): {len(tiered['skip'])} datasets")
            lines.append("")
            
        # Detailed evaluation for top datasets
        lines.append("---")
        lines.append("")
        lines.append("## 🔍 Detailed Evaluations (Top 20)")
        lines.append("")
        all_sorted = sorted(results.items(), key=lambda x: x[1]['score'], reverse=True)[:20]
        
        for dataset_id, eval_data in all_sorted:
            dataset_info = self.datasets[dataset_id]
            lines.append(f"### {dataset_info.get('name', dataset_id)}")
            lines.append("")
            lines.append(f"**Dataset ID:** `{dataset_id}`")
            lines.append(f"**Overall Score:** {eval_data['score']}/100")
            lines.append(f"**Tier:** {eval_data['tier'].replace('_', ' ').title()}")
            lines.append(f"**Recommendation:** {eval_data['recommendation']}")
            lines.append("")
            lines.append("**Score Breakdown:**")
            for key, value in eval_data['breakdown'].items():
                lines.append(f"- {key.replace('_', ' ').title()}: {value} points")
            lines.append("")
            lines.append("**Reasons:**")
            for reason in eval_data['reasons']:
                lines.append(f"- {reason}")
            lines.append("")
            lines.append("**Categories:** " + ', '.join(eval_data['categories']) if eval_data['categories'] else "None")
            lines.append("")
            lines.append("---")
            lines.append("")
            
        content = '\n'.join(lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        logger.info(f"✓ Evaluation summary saved: {output_path}")
        return output_path


