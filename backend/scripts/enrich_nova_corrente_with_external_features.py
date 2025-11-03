"""
Enrich Nova Corrente data with external features
- Climate (Salvador/BA)
- Economic indicators (Brazil)
- 5G expansion data
- SLA and operational features
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
NOVA_CORRENTE_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_processed.csv"
ENRICHED_DATASET = PROJECT_ROOT / "data" / "processed" / "unified_brazilian_telecom_nova_corrente_enriched.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "nova_corrente"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_data():
    """Load Nova Corrente processed data and enriched dataset"""
    print("=" * 80)
    print("CARREGANDO DADOS PARA ENRIQUECIMENTO")
    print("=" * 80)
    
    # Load Nova Corrente processed data
    nova_corrente = pd.read_csv(NOVA_CORRENTE_FILE, parse_dates=['date'])
    print(f"\n[INFO] Nova Corrente: {len(nova_corrente):,} registros")
    print(f"[INFO] Período: {nova_corrente['date'].min()} a {nova_corrente['date'].max()}")
    
    # Load enriched dataset (sample for merging)
    enriched = pd.read_csv(ENRICHED_DATASET, parse_dates=['date'], nrows=10000)
    print(f"\n[INFO] Enriched dataset: {len(enriched):,} registros (sample)")
    print(f"[INFO] Features disponíveis: {len(enriched.columns)}")
    
    return nova_corrente, enriched

def merge_external_features(nova_corrente, enriched):
    """Merge Nova Corrente with external features"""
    print("\n" + "=" * 80)
    print("MESCLANDO FEATURES EXTERNAS")
    print("=" * 80)
    
    # Select relevant external features from enriched dataset
    external_features = [
        'date', 'year', 'month', 'day',
        # Climate
        'temperature_avg_c', 'precipitation_mm', 'humidity_percent',
        'is_intense_rain', 'is_high_humidity', 'corrosion_risk',
        # Economic
        'inflation_rate', 'exchange_rate_brl_usd', 'gdp_growth_rate',
        # 5G
        '5g_coverage_pct', '5g_investment_brl_billions', 'is_5g_milestone',
        # Operational
        'is_holiday', 'is_weekend', 'is_drought', 'is_flood_risk',
        # SLA
        'sla_penalty_brl', 'availability_target', 'downtime_hours_monthly',
        'sla_violation_risk',
        # Lead Time
        'base_lead_time_days', 'total_lead_time_days', 'customs_delay_days',
        'strike_risk', 'is_critical_lead_time'
    ]
    
    # Get available features
    available_features = [f for f in external_features if f in enriched.columns]
    
    # Create subset of enriched data
    enriched_subset = enriched[available_features].copy()
    
    # Remove duplicates by date (keep first)
    enriched_subset = enriched_subset.drop_duplicates(subset='date', keep='first')
    
    print(f"\n[INFO] Features externas disponíveis: {len(available_features)}")
    print(f"[INFO] Features selecionadas: {available_features[:10]}...")
    
    # Merge by date
    print(f"\n[INFO] Mesclando por data...")
    nova_corrente_enriched = nova_corrente.merge(
        enriched_subset,
        on='date',
        how='left',
        suffixes=('', '_external')
    )
    
    # Statistics
    merged_count = nova_corrente_enriched[available_features[1]].notna().sum()
    merge_rate = merged_count / len(nova_corrente_enriched) * 100
    
    print(f"\n[INFO] Merge completado:")
    print(f"  - Registros mesclados: {merged_count:,}/{len(nova_corrente_enriched):,} ({merge_rate:.1f}%)")
    print(f"  - Features adicionadas: {len(available_features) - 1}")  # -1 for date
    
    return nova_corrente_enriched, available_features

def add_calculated_features(df):
    """Add calculated features from external data"""
    print("\n" + "=" * 80)
    print("ADICIONANDO FEATURES CALCULADAS")
    print("=" * 80)
    
    # Temporal features (if not already present)
    if 'year' not in df.columns or df['year'].isna().any():
        df['year'] = df['date'].dt.year
    if 'month' not in df.columns or df['month'].isna().any():
        df['month'] = df['date'].dt.month
    if 'day' not in df.columns or df['day'].isna().any():
        df['day'] = df['date'].dt.day
    if 'weekday' not in df.columns:
        df['weekday'] = df['date'].dt.weekday
    if 'is_weekend' not in df.columns or df['is_weekend'].isna().any():
        df['is_weekend'] = (df['weekday'] >= 5).astype(int)
    if 'quarter' not in df.columns:
        df['quarter'] = df['date'].dt.quarter
    if 'day_of_year' not in df.columns:
        df['day_of_year'] = df['date'].dt.dayofyear
    
    # Cyclical encoding
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    df['day_of_year_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365.25)
    df['day_of_year_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365.25)
    
    # Climate impact features
    if 'temperature_avg_c' in df.columns:
        df['extreme_heat'] = (df['temperature_avg_c'] > 35).astype(int)
        df['cold_weather'] = (df['temperature_avg_c'] < 18).astype(int)
    
    if 'precipitation_mm' in df.columns:
        df['heavy_rain'] = (df['precipitation_mm'] > 50).astype(int)
        df['no_rain'] = (df['precipitation_mm'] == 0).astype(int)
    
    # Economic impact
    if 'inflation_rate' in df.columns:
        df['high_inflation'] = (df['inflation_rate'] > 5).astype(int)
        df['currency_devaluation'] = (df['exchange_rate_brl_usd'].diff() > 0.1).astype(int)
    
    # 5G impact
    if '5g_coverage_pct' in df.columns:
        df['5g_active'] = (df['5g_coverage_pct'] > 0).astype(int)
        df['5g_expansion_rate'] = df['5g_coverage_pct'].diff().fillna(0)
    
    # Lead time features (if not from external)
    if 'lead_time_days' in df.columns:
        df['lead_time_category'] = pd.cut(
            df['lead_time_days'].fillna(df['lead_time_days'].median()),
            bins=[0, 7, 14, 30, np.inf],
            labels=['fast', 'normal', 'slow', 'very_slow']
        )
        df['is_critical_lead_time_nc'] = (df['lead_time_days'] > 14).astype(int)
    
    # Family and site aggregations
    df['family_frequency'] = df.groupby('familia')['familia'].transform('count')
    df['site_frequency'] = df.groupby('site_id')['site_id'].transform('count')
    df['supplier_frequency'] = df.groupby('fornecedor')['fornecedor'].transform('count')
    
    print(f"\n[INFO] Features calculadas adicionadas:")
    print(f"  - Temporais: year, month, day, weekday, quarter, cyclical")
    print(f"  - Clima: extreme_heat, cold_weather, heavy_rain, no_rain")
    print(f"  - Econômicas: high_inflation, currency_devaluation")
    print(f"  - 5G: 5g_active, 5g_expansion_rate")
    print(f"  - Lead time: lead_time_category, is_critical_lead_time_nc")
    print(f"  - Agregações: family_frequency, site_frequency, supplier_frequency")
    
    return df

def add_hierarchical_features(df):
    """Add hierarchical features by family, site, region"""
    print("\n" + "=" * 80)
    print("ADICIONANDO FEATURES HIERÁRQUICAS")
    print("=" * 80)
    
    # Sort by date and family/site for rolling calculations
    df = df.sort_values(['date', 'familia', 'site_id'])
    
    # Family-level features
    for window in [7, 30]:
        family_rolling = df.groupby('familia')['quantidade'].transform(
            lambda x: x.rolling(window=window, min_periods=1).mean()
        )
        df[f'family_demand_ma_{window}'] = family_rolling
        
        family_std = df.groupby('familia')['quantidade'].transform(
            lambda x: x.rolling(window=window, min_periods=1).std()
        )
        df[f'family_demand_std_{window}'] = family_std.fillna(0)
    
    # Site-level features
    for window in [7, 30]:
        site_rolling = df.groupby('site_id')['quantidade'].transform(
            lambda x: x.rolling(window=window, min_periods=1).mean()
        )
        df[f'site_demand_ma_{window}'] = site_rolling
    
    # Supplier-level features
    supplier_lead_mean = df.groupby('fornecedor')['lead_time_days'].transform('mean')
    df['supplier_lead_time_mean'] = supplier_lead_mean
    
    supplier_lead_std = df.groupby('fornecedor')['lead_time_days'].transform('std')
    df['supplier_lead_time_std'] = supplier_lead_std.fillna(0)
    
    print(f"\n[INFO] Features hierárquicas adicionadas:")
    print(f"  - Por família: family_demand_ma_7/30, family_demand_std_7/30")
    print(f"  - Por site: site_demand_ma_7/30")
    print(f"  - Por fornecedor: supplier_lead_time_mean/std")
    
    return df

def save_enriched_dataset(df, available_features):
    """Save enriched dataset"""
    print("\n" + "=" * 80)
    print("SALVANDO DATASET ENRIQUECIDO")
    print("=" * 80)
    
    output_file = OUTPUT_DIR / "nova_corrente_enriched.csv"
    df.to_csv(output_file, index=False, encoding='utf-8')
    
    print(f"\n[SUCCESS] Dataset enriquecido salvo: {output_file}")
    print(f"[INFO] Total de features: {len(df.columns)}")
    print(f"[INFO] Total de registros: {len(df):,}")
    
    # Save summary
    summary = {
        'processing_date': datetime.now().isoformat(),
        'total_records': len(df),
        'total_features': len(df.columns),
        'external_features_added': len(available_features) - 1,
        'date_range': {
            'min': str(df['date'].min()),
            'max': str(df['date'].max()),
            'span_days': (df['date'].max() - df['date'].min()).days
        },
        'features_list': list(df.columns),
        'missing_data_stats': {
            col: {
                'missing_count': int(df[col].isna().sum()),
                'missing_pct': float(df[col].isna().sum() / len(df) * 100)
            }
            for col in df.columns if df[col].isna().sum() > 0
        }
    }
    
    summary_file = OUTPUT_DIR / "enrichment_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"[SUCCESS] Resumo: {summary_file}")
    
    return summary

def main():
    """Main enrichment pipeline"""
    print("\n" + "=" * 80)
    print("PIPELINE DE ENRIQUECIMENTO: NOVA CORRENTE")
    print("=" * 80 + "\n")
    
    # Step 1: Load data
    nova_corrente, enriched = load_data()
    
    # Step 2: Merge external features
    nova_corrente_enriched, available_features = merge_external_features(nova_corrente, enriched)
    
    # Step 3: Add calculated features
    nova_corrente_enriched = add_calculated_features(nova_corrente_enriched)
    
    # Step 4: Add hierarchical features
    nova_corrente_enriched = add_hierarchical_features(nova_corrente_enriched)
    
    # Step 5: Save enriched dataset
    summary = save_enriched_dataset(nova_corrente_enriched, available_features)
    
    print("\n" + "=" * 80)
    print("ENRIQUECIMENTO CONCLUÍDO!")
    print("=" * 80)
    print(f"\n[RESUMO]")
    print(f"  - Features totais: {summary['total_features']}")
    print(f"  - Features externas adicionadas: {summary['external_features_added']}")
    print(f"  - Registros enriquecidos: {summary['total_records']:,}")
    print(f"\n[PRÓXIMOS PASSOS]")
    print(f"  1. Combinar com datasets existentes")
    print(f"  2. Criar splits train/validation/test")
    print(f"  3. Treinar modelos com top 5 famílias")
    
    return nova_corrente_enriched, summary

if __name__ == "__main__":
    main()

