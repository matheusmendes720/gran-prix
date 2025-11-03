"""
Run Cluster Study Evaluation - Evaluates all datasets for telecom/logistics relevance
Creates organized folder structure with categorized datasets and deep documentation
"""
import sys
from pathlib import Path
import json
import logging
from datetime import datetime
from typing import Dict

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.utils.cluster_study_evaluator import ClusterStudyEvaluator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_cluster_study_structure():
    """Create organized folder structure for cluster study"""
    base_dir = project_root / 'docs' / 'documentation' / 'cluster_study'
    
    directories = [
        base_dir,
        base_dir / 'hell_yes',
        base_dir / 'high_priority',
        base_dir / 'medium_priority',
        base_dir / 'low_priority',
        base_dir / 'evaluations',
        base_dir / 'datasets_config',
        base_dir / 'download_scripts',
    ]
    
    for dir_path in directories:
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Created directory: {dir_path}")
        
    return base_dir


def generate_tier_configs(evaluator: ClusterStudyEvaluator, base_dir: Path):
    """Generate separate config files for each tier"""
    results = evaluator.evaluate_all()
    tiered = evaluator.get_tiered_datasets(results)
    
    config_base = base_dir / 'datasets_config'
    
    for tier, datasets in tiered.items():
        if not datasets:
            continue
            
        # Create config for this tier
        tier_config = {
            'tier': tier,
            'description': {
                'hell_yes': 'Critical datasets - Perfect fit for business case',
                'high_priority': 'High priority datasets - Strong relevance',
                'medium_priority': 'Medium priority datasets - Useful with adaptation',
                'low_priority': 'Low priority datasets - Limited relevance',
                'skip': 'Skip datasets - Not relevant for business case'
            }.get(tier, ''),
            'datasets': {}
        }
        
        # Add full dataset configs
        for ds in datasets:
            dataset_id = ds['dataset_id']
            if dataset_id in evaluator.datasets:
                tier_config['datasets'][dataset_id] = evaluator.datasets[dataset_id]
                tier_config['datasets'][dataset_id]['_evaluation'] = results[dataset_id]
        
        # Save tier config
        tier_config_path = config_base / f'{tier}_config.json'
        with open(tier_config_path, 'w', encoding='utf-8') as f:
            json.dump(tier_config, f, indent=2, ensure_ascii=False)
        logger.info(f"✓ Created tier config: {tier_config_path} ({len(datasets)} datasets)")
        
        # Also save individual dataset docs for hell_yes and high_priority
        if tier in ['hell_yes', 'high_priority']:
            tier_docs_dir = base_dir / tier
            for ds in datasets:
                dataset_id = ds['dataset_id']
                dataset_info = evaluator.datasets[dataset_id]
                eval_data = results[dataset_id]
                
                # Generate deep documentation
                doc_content = generate_deep_documentation(dataset_id, dataset_info, eval_data)
                doc_path = tier_docs_dir / f'{dataset_id}_deep_docs.md'
                with open(doc_path, 'w', encoding='utf-8') as f:
                    f.write(doc_content)
                logger.info(f"✓ Generated deep docs: {doc_path}")


def generate_deep_documentation(dataset_id: str, dataset_info: Dict, eval_data: Dict) -> str:
    """Generate comprehensive deep documentation for a dataset"""
    lines = []
    
    lines.append(f"# 📊 Deep Technical Documentation: {dataset_info.get('name', dataset_id)}")
    lines.append("")
    lines.append(f"**Dataset ID:** `{dataset_id}`")
    lines.append(f"**Source:** {dataset_info.get('source', 'unknown')}")
    lines.append(f"**Evaluation Score:** {eval_data['score']}/100")
    lines.append(f"**Tier:** {eval_data['tier'].replace('_', ' ').title()}")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Business Case Relevance
    lines.append("## 🎯 Business Case Relevance")
    lines.append("")
    lines.append("### Nova Corrente Use Case")
    lines.append("")
    lines.append("**Primary Problem:** Spare parts demand forecasting for 18,000+ telecom towers")
    lines.append("")
    lines.append("**Key Requirements:**")
    lines.append("- Predict future consumption of spare parts/services")
    lines.append("- Support inventory optimization and reorder point calculation")
    lines.append("- Maintain SLA compliance (99%+ uptime)")
    lines.append("- Account for lead times, seasonality, and external factors")
    lines.append("")
    lines.append(f"**This Dataset's Fit:** {eval_data['recommendation']}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Detailed Evaluation
    lines.append("## 📊 Detailed Evaluation")
    lines.append("")
    lines.append("### Score Breakdown")
    lines.append("")
    for key, value in eval_data['breakdown'].items():
        lines.append(f"- **{key.replace('_', ' ').title()}:** {value} points")
    lines.append("")
    lines.append("### Evaluation Reasons")
    lines.append("")
    for reason in eval_data['reasons']:
        lines.append(f"- {reason}")
    lines.append("")
    lines.append("### Categories")
    lines.append("")
    for category in eval_data['categories']:
        lines.append(f"- `{category}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Dataset Information
    lines.append("## 📋 Dataset Information")
    lines.append("")
    lines.append(f"**Name:** {dataset_info.get('name', 'N/A')}")
    lines.append(f"**Description:** {dataset_info.get('description', 'N/A')}")
    lines.append("")
    
    if dataset_info.get('url'):
        lines.append(f"**URL:** [{dataset_info.get('url')}]({dataset_info.get('url')})")
        lines.append("")
        
    if dataset_info.get('columns_mapping'):
        lines.append("### Column Mapping")
        lines.append("")
        lines.append("| Mapped Column | Original Column | Notes |")
        lines.append("|--------------|----------------|-------|")
        for mapped, original in dataset_info.get('columns_mapping', {}).items():
            original_str = original if original else 'N/A'
            lines.append(f"| `{mapped}` | `{original_str}` | - |")
        lines.append("")
        
    if dataset_info.get('preprocessing_notes'):
        lines.append("### Preprocessing Notes")
        lines.append("")
        lines.append(dataset_info.get('preprocessing_notes'))
        lines.append("")
        
    if dataset_info.get('notes'):
        lines.append("### Additional Notes")
        lines.append("")
        lines.append(dataset_info.get('notes'))
        lines.append("")
        
    lines.append("---")
    lines.append("")
    
    # ML Algorithm Recommendations
    lines.append("## 🤖 Recommended ML Algorithms")
    lines.append("")
    
    if 'demand_forecasting' in eval_data['categories']:
        lines.append("### Time-Series Forecasting")
        lines.append("")
        lines.append("1. **ARIMA/SARIMA:** For univariate time-series with trend and seasonality")
        lines.append("2. **Prophet:** Facebook's forecasting tool, handles holidays and seasonality well")
        lines.append("3. **LSTM:** Deep learning for complex non-linear patterns")
        lines.append("4. **XGBoost:** Gradient boosting with feature engineering")
        lines.append("")
        
    if 'telecom_industry' in eval_data['categories']:
        lines.append("### Predictive Maintenance")
        lines.append("")
        lines.append("1. **Random Forest:** For classification of failure types")
        lines.append("2. **XGBoost:** For failure prediction with feature importance")
        lines.append("3. **LSTM:** For sequential failure pattern detection")
        lines.append("")
        
    lines.append("---")
    lines.append("")
    
    # Integration Guide
    lines.append("## 🔗 Integration Guide")
    lines.append("")
    lines.append("### How to Use This Dataset")
    lines.append("")
    lines.append("1. **Download:** Use the download script in `cluster_study/download_scripts/`")
    lines.append("2. **Structure:** Run through ML data structuring pipeline")
    lines.append("3. **Enrich:** Integrate with external factors (climate, economy)")
    lines.append("4. **Validate:** Run quality validation checks")
    lines.append("5. **Model:** Train forecasting models (ARIMA, Prophet, LSTM)")
    lines.append("")
    
    lines.append("### Pipeline Integration")
    lines.append("")
    lines.append("```bash")
    lines.append(f"# Download dataset")
    lines.append(f"python backend/scripts/fetch_all_ml_datasets.py --dataset {dataset_id}")
    lines.append("")
    lines.append(f"# Structure for ML")
    lines.append(f"python backend/scripts/structure_ml_datasets.py --dataset {dataset_id}")
    lines.append("")
    lines.append(f"# Enrich with external factors")
    lines.append(f"python backend/scripts/comprehensive_dataset_pipeline.py --dataset {dataset_id}")
    lines.append("```")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Business Impact
    lines.append("## 💼 Business Impact")
    lines.append("")
    lines.append("### Expected Benefits")
    lines.append("")
    if eval_data['score'] >= 80:
        lines.append("- **CRITICAL:** This dataset directly addresses the core business problem")
        lines.append("- High accuracy demand forecasts expected")
        lines.append("- Can significantly reduce inventory stockouts")
        lines.append("- Supports SLA compliance (99%+ uptime)")
    elif eval_data['score'] >= 60:
        lines.append("- **HIGH VALUE:** Strong relevance to business case")
        lines.append("- Good accuracy for demand forecasting")
        lines.append("- Helps optimize inventory levels")
    else:
        lines.append("- **SUPPORTING:** Provides context or external factors")
        lines.append("- Enhances model performance when combined with core datasets")
    lines.append("")
    
    lines.append("### ROI Potential")
    lines.append("")
    lines.append("Based on Internet Aberta ROI analysis (internet_aberta_roi_brazil dataset):")
    lines.append("- B2B telecom solutions typically show ROI >100%")
    lines.append("- Predictive maintenance can reduce costs by 20-30%")
    lines.append("- Inventory optimization can free 15-20% of capital")
    lines.append("")
    
    return '\n'.join(lines)


def main():
    """Main execution"""
    logger.info("="*80)
    logger.info("CLUSTER STUDY EVALUATION")
    logger.info("="*80)
    logger.info(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create folder structure
    base_dir = create_cluster_study_structure()
    
    # Initialize evaluator
    evaluator = ClusterStudyEvaluator()
    
    # Evaluate all datasets
    logger.info("\nEvaluating all datasets...")
    results = evaluator.evaluate_all()
    
    # Generate summary report
    logger.info("\nGenerating evaluation summary...")
    summary_path = evaluator.generate_summary_report()
    
    # Generate tier configs and deep docs
    logger.info("\nGenerating tier configurations...")
    generate_tier_configs(evaluator, base_dir)
    
    # Save full results JSON
    results_path = base_dir / 'evaluations' / 'full_evaluation_results.json'
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    logger.info(f"✓ Saved full results: {results_path}")
    
    # Summary
    tiered = evaluator.get_tiered_datasets(results)
    logger.info("\n" + "="*80)
    logger.info("EVALUATION COMPLETE")
    logger.info("="*80)
    logger.info(f"Total datasets evaluated: {len(results)}")
    logger.info(f"\nTier Distribution:")
    for tier, datasets in tiered.items():
        if datasets:
            logger.info(f"  - {tier.replace('_', ' ').title()}: {len(datasets)} datasets")
    logger.info(f"\n✓ Summary report: {summary_path}")
    logger.info(f"✓ Full results: {results_path}")
    logger.info(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()

