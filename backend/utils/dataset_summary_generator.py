"""
Gerador de resumos executivos para datasets
Cria documentos markdown com resumo completo de cada dataset
"""
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DatasetSummaryGenerator:
    """Gerador de resumos executivos para datasets"""
    
    def __init__(self, output_dir: str = 'data/processed/summaries'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_summary(self, dataset_id: str, dataset_info: Dict, 
                        quality_report: Optional[Dict] = None,
                        analysis_report: Optional[Dict] = None) -> Path:
        """Gerar resumo executivo completo"""
        logger.info(f"Generating summary for: {dataset_id}")
        
        # Carregar dados se disponíveis
        enriched_path = Path('data/processed/ml_ready') / f"{dataset_id}_enriched.csv"
        structured_path = Path('data/processed/ml_ready') / f"{dataset_id}_structured.csv"
        
        df_path = enriched_path if enriched_path.exists() else structured_path
        df = None
        
        if df_path.exists():
            try:
                df = pd.read_csv(df_path, low_memory=False)
            except Exception as e:
                logger.warning(f"Could not load data: {e}")
        
        # Gerar markdown
        md_content = self._generate_markdown(dataset_id, dataset_info, df, quality_report, analysis_report)
        
        # Salvar
        summary_path = self.output_dir / f"{dataset_id}_summary.md"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"✓ Summary saved: {summary_path}")
        
        return summary_path
    
    def _generate_markdown(self, dataset_id: str, dataset_info: Dict, 
                          df: Optional[pd.DataFrame],
                          quality_report: Optional[Dict],
                          analysis_report: Optional[Dict]) -> str:
        """Gerar conteúdo markdown"""
        lines = []
        
        # Cabeçalho
        lines.append(f"# 📊 Dataset Summary: {dataset_info.get('name', dataset_id)}")
        lines.append("")
        lines.append(f"**Dataset ID:** `{dataset_id}`  ")
        lines.append(f"**Source:** {dataset_info.get('source', 'unknown')}  ")
        lines.append(f"**Relevance:** {dataset_info.get('relevance', 'N/A')}  ")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Overview
        lines.append("## 📋 Overview")
        lines.append("")
        lines.append(f"**Description:** {dataset_info.get('description', 'N/A')}")
        lines.append("")
        
        # Dados básicos
        if df is not None:
            lines.append("### Data Statistics")
            lines.append("")
            lines.append(f"- **Rows:** {len(df):,}")
            lines.append(f"- **Columns:** {len(df.columns)}")
            lines.append(f"- **Date Range:** {self._get_date_range(df)}")
            lines.append("")
        
        # Quality Score
        if quality_report:
            quality_score = quality_report.get('quality_score', 0)
            lines.append("### Quality Score")
            lines.append("")
            lines.append(f"**Overall Quality:** {quality_score:.2%}")
            lines.append("")
            
            # Status por check
            checks = quality_report.get('checks', {})
            lines.append("#### Quality Checks:")
            for check_name, check_data in checks.items():
                status = check_data.get('status', 'unknown')
                status_emoji = '✅' if status == 'pass' else '⚠️' if status == 'warning' else '❌'
                lines.append(f"- {status_emoji} **{check_name.replace('_', ' ').title()}:** {status}")
            lines.append("")
        
        # Insights
        if analysis_report:
            insights = analysis_report.get('insights', [])
            if insights:
                lines.append("### Key Insights")
                lines.append("")
                for insight in insights[:10]:  # Limitar a 10
                    lines.append(f"- {insight}")
                lines.append("")
        
        # Preprocessing Notes
        if dataset_info.get('preprocessing_notes'):
            lines.append("## 🔧 Preprocessing Notes")
            lines.append("")
            lines.append(dataset_info.get('preprocessing_notes'))
            lines.append("")
        
        # Column Mapping
        if dataset_info.get('columns_mapping'):
            lines.append("## 📝 Column Mapping")
            lines.append("")
            lines.append("| Original Column | Mapped Column |")
            lines.append("|----------------|---------------|")
            for mapped, original in dataset_info.get('columns_mapping', {}).items():
                original_str = original if original else 'N/A'
                lines.append(f"| `{original_str}` | `{mapped}` |")
            lines.append("")
        
        # Recommended Models
        if analysis_report:
            temporal = analysis_report.get('temporal_analysis')
            if temporal and temporal.get('seasonality_detected'):
                lines.append("## 🤖 Recommended Models")
                lines.append("")
                lines.append("Based on analysis, the following models are recommended:")
                lines.append("")
                lines.append("1. **SARIMA/SARIMAX** - Seasonality detected")
                lines.append("2. **Prophet** - Handles seasonality and trends well")
                lines.append("3. **LSTM** - For complex non-linear patterns")
                lines.append("")
        
        # Links
        if dataset_info.get('url'):
            lines.append("## 🔗 Links")
            lines.append("")
            lines.append(f"- **Source URL:** [{dataset_info.get('url')}]({dataset_info.get('url')})")
            lines.append("")
        
        return "\n".join(lines)
    
    def _get_date_range(self, df: pd.DataFrame) -> str:
        """Obter range de datas"""
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        if not date_cols:
            return "N/A (no date column)"
        
        try:
            dates = pd.to_datetime(df[date_cols[0]], errors='coerce')
            valid_dates = dates.dropna()
            if len(valid_dates) > 0:
                min_date = valid_dates.min()
                max_date = valid_dates.max()
                days = (max_date - min_date).days
                return f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')} ({days} days)"
        except:
            pass
        
        return "N/A"

