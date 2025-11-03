"""
Optimize Data Preprocessing for Nova Corrente
- Impute external features (climate, economy, 5G)
- Normalize and scale data
- Feature selection
- Improve data quality
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer, KNNImputer
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = Path(__file__).parent.parent.parent
TRAIN_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_train.csv"
VAL_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_validation.csv"
TEST_FILE = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "nova_corrente_top5_test.csv"
ENRICHED_DATASET = PROJECT_ROOT / "data" / "processed" / "unified_brazilian_telecom_nova_corrente_enriched.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "nova_corrente" / "optimized"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_datasets():
    """Load train/validation/test datasets"""
    print("=" * 80)
    print("CARREGANDO DATASETS PARA OTIMIZAÇÃO")
    print("=" * 80)
    
    train_df = pd.read_csv(TRAIN_FILE, parse_dates=['date'])
    val_df = pd.read_csv(VAL_FILE, parse_dates=['date'])
    test_df = pd.read_csv(TEST_FILE, parse_dates=['date'])
    
    print(f"\n[INFO] Train: {len(train_df):,} registros")
    print(f"[INFO] Validation: {len(val_df):,} registros")
    print(f"[INFO] Test: {len(test_df):,} registros")
    
    return train_df, val_df, test_df

def impute_external_features(df, enriched_dataset=None):
    """Impute missing external features"""
    print("\n[IMPUTATION] Imputando features externas")
    
    # External feature columns
    climate_features = [
        'temperature_avg_c', 'precipitation_mm', 'humidity_percent',
        'is_intense_rain', 'is_high_humidity', 'corrosion_risk',
        'extreme_heat', 'cold_weather', 'heavy_rain', 'no_rain'
    ]
    
    economic_features = [
        'inflation_rate', 'exchange_rate_brl_usd', 'gdp_growth_rate',
        'high_inflation', 'currency_devaluation'
    ]
    
    g5_features = [
        '5g_coverage_pct', '5g_investment_brl_billions', 'is_5g_milestone',
        '5g_active', '5g_expansion_rate'
    ]
    
    sla_features = [
        'sla_penalty_brl', 'availability_target', 'downtime_hours_monthly',
        'sla_violation_risk'
    ]
    
    leadtime_features = [
        'base_lead_time_days', 'total_lead_time_days', 'customs_delay_days',
        'strike_risk', 'is_critical_lead_time'
    ]
    
    all_external = climate_features + economic_features + g5_features + sla_features + leadtime_features
    
    # Get available external features
    available_external = [f for f in all_external if f in df.columns]
    
    print(f"\n[INFO] Features externas disponíveis: {len(available_external)}")
    
    # Strategy 1: Use enriched dataset to fill if available
    if enriched_dataset is not None and Path(enriched_dataset).exists():
        try:
            enriched = pd.read_csv(enriched_dataset, parse_dates=['date'], nrows=10000)
            enriched_dates = enriched['date'].unique()
            
            for feature in available_external:
                if feature in enriched.columns:
                    # Merge by date
                    feature_data = enriched[['date', feature]].drop_duplicates(subset='date')
                    feature_data = feature_data[feature_data[feature].notna()]
                    
                    if len(feature_data) > 0:
                        df = df.merge(feature_data, on='date', how='left', suffixes=('', '_enriched'))
                        if f'{feature}_enriched' in df.columns:
                            # Fill missing with enriched data
                            mask = df[feature].isna() & df[f'{feature}_enriched'].notna()
                            df.loc[mask, feature] = df.loc[mask, f'{feature}_enriched']
                            df = df.drop(columns=[f'{feature}_enriched'])
            
            print(f"[INFO] Features preenchidas com enriched dataset")
        except Exception as e:
            print(f"[WARNING] Erro ao usar enriched dataset: {e}")
    
    # Strategy 2: Impute based on date patterns
    for feature in available_external:
        if df[feature].isna().sum() > 0:
            missing_pct = df[feature].isna().sum() / len(df) * 100
            
            # For temporal features, use forward fill + backward fill
            if missing_pct < 50:  # Only if not too many missing
                if df[feature].dtype in [np.float64, np.int64]:
                    # Forward fill then backward fill
                    df[feature] = df.groupby('familia')[feature].transform(
                        lambda x: x.fillna(method='ffill').fillna(method='bfill')
                    )
                    
                    # If still missing, fill with median by family
                    if df[feature].isna().sum() > 0:
                        median_by_family = df.groupby('familia')[feature].transform('median')
                        df[feature] = df[feature].fillna(median_by_family)
                    
                    # If still missing, fill with overall median
                    if df[feature].isna().sum() > 0:
                        overall_median = df[feature].median()
                        df[feature] = df[feature].fillna(overall_median)
    
    # Strategy 3: Impute based on domain knowledge
    # Climate features - use Salvador/BA averages
    if 'temperature_avg_c' in df.columns:
        df['temperature_avg_c'] = df['temperature_avg_c'].fillna(26.5)  # Salvador average
    if 'precipitation_mm' in df.columns:
        df['precipitation_mm'] = df['precipitation_mm'].fillna(130.0)  # Salvador average monthly
    if 'humidity_percent' in df.columns:
        df['humidity_percent'] = df['humidity_percent'].fillna(85.0)  # Salvador average
    
    # Economic features - use recent Brazilian averages
    if 'inflation_rate' in df.columns:
        df['inflation_rate'] = df['inflation_rate'].fillna(4.5)  # Recent Brazilian average
    if 'exchange_rate_brl_usd' in df.columns:
        df['exchange_rate_brl_usd'] = df['exchange_rate_brl_usd'].fillna(5.0)  # Recent average
    if 'gdp_growth_rate' in df.columns:
        df['gdp_growth_rate'] = df['gdp_growth_rate'].fillna(2.0)  # Recent average
    
    # 5G features
    if '5g_coverage_pct' in df.columns:
        df['5g_coverage_pct'] = df['5g_coverage_pct'].fillna(60.0)  # Recent Brazilian average
    if '5g_investment_brl_billions' in df.columns:
        df['5g_investment_brl_billions'] = df['5g_investment_brl_billions'].fillna(15.0)
    
    # SLA features
    if 'sla_penalty_brl' in df.columns:
        df['sla_penalty_brl'] = df['sla_penalty_brl'].fillna(360000.0)  # Typical B2B penalty
    if 'availability_target' in df.columns:
        df['availability_target'] = df['availability_target'].fillna(0.99)  # 99% SLA
    
    # Lead time features
    if 'base_lead_time_days' in df.columns:
        df['base_lead_time_days'] = df['base_lead_time_days'].fillna(14.0)  # Typical lead time
    if 'total_lead_time_days' in df.columns:
        df['total_lead_time_days'] = df['total_lead_time_days'].fillna(22.5)  # Typical with delays
    
    print(f"\n[INFO] Imputação concluída")
    
    # Report imputation success
    for feature in available_external:
        missing_after = df[feature].isna().sum() if feature in df.columns else len(df)
        if missing_after < len(df):
            pct_imputed = (1 - missing_after / len(df)) * 100
            print(f"  {feature}: {pct_imputed:.1f}% cobertura")
    
    return df

def normalize_data(df, numeric_cols, scaler_type='robust'):
    """Normalize numeric data"""
    print("\n[NORMALIZATION] Normalizando dados numéricos")
    
    # Select scaler
    if scaler_type == 'standard':
        scaler = StandardScaler()
    elif scaler_type == 'minmax':
        scaler = MinMaxScaler()
    else:  # robust
        scaler = RobustScaler()
    
    # Get available numeric columns
    available_numeric = [col for col in numeric_cols if col in df.columns]
    
    # Exclude target and ID columns
    exclude_cols = ['quantidade', 'target', 'item_id', 'site_id', 'solicitacao']
    numeric_to_scale = [col for col in available_numeric if col not in exclude_cols]
    
    print(f"\n[INFO] Colunas para normalizar: {len(numeric_to_scale)}")
    
    # Create scaled dataframe
    df_scaled = df.copy()
    
    # Scale numeric columns
    for col in numeric_to_scale:
        if df[col].dtype in [np.float64, np.int64]:
            # Fit scaler on non-null values
            non_null_values = df[col].dropna()
            if len(non_null_values) > 0:
                scaler.fit(non_null_values.values.reshape(-1, 1))
                # Transform all values (including nulls will be handled separately)
                df_scaled[f'{col}_scaled'] = df[col].copy()
                mask = df_scaled[f'{col}_scaled'].notna()
                if mask.sum() > 0:
                    df_scaled.loc[mask, f'{col}_scaled'] = scaler.transform(
                        df_scaled.loc[mask, f'{col}_scaled'].values.reshape(-1, 1)
                    ).flatten()
    
    print(f"[INFO] Normalização concluída")
    
    return df_scaled, scaler

def feature_selection(df, target_col='quantidade', top_n=30):
    """Select top features by importance"""
    print("\n[FEATURE_SELECTION] Selecionando features importantes")
    
    try:
        from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
        
        # Get numeric features
        numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Exclude target and ID columns
        exclude_cols = [target_col, 'target', 'item_id', 'site_id', 'solicitacao', 'familia_encoded']
        features = [f for f in numeric_features if f not in exclude_cols and not f.endswith('_scaled')]
        
        # Prepare data
        X = df[features].fillna(0)
        y = df[target_col].fillna(0)
        
        # Select top features using f_regression
        selector = SelectKBest(score_func=f_regression, k=min(top_n, len(features)))
        selector.fit(X, y)
        
        # Get selected features
        selected_features = [features[i] for i in selector.get_support(indices=True)]
        
        print(f"\n[INFO] Features selecionadas: {len(selected_features)}/{len(features)}")
        print(f"[INFO] Top 10 features:")
        feature_scores = list(zip(selected_features, selector.scores_[selector.get_support()]))
        feature_scores.sort(key=lambda x: x[1], reverse=True)
        
        for i, (feature, score) in enumerate(feature_scores[:10], 1):
            print(f"  {i}. {feature}: {score:.2f}")
        
        return selected_features
        
    except Exception as e:
        print(f"[WARNING] Feature selection failed: {e}")
        print(f"[INFO] Usando todas as features numéricas")
        # Return all numeric features
        numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
        exclude_cols = [target_col, 'target', 'item_id', 'site_id', 'solicitacao']
        return [f for f in numeric_features if f not in exclude_cols]

def optimize_preprocessing(train_df, val_df, test_df):
    """Complete preprocessing optimization"""
    print("\n" + "=" * 80)
    print("OTIMIZANDO PRE-PROCESSAMENTO")
    print("=" * 80)
    
    # Step 1: Impute external features
    print("\n[STEP 1] Imputando features externas...")
    train_imputed = impute_external_features(train_df.copy(), ENRICHED_DATASET)
    val_imputed = impute_external_features(val_df.copy(), ENRICHED_DATASET)
    test_imputed = impute_external_features(test_df.copy(), ENRICHED_DATASET)
    
    # Step 2: Feature selection
    print("\n[STEP 2] Selecionando features importantes...")
    numeric_cols = train_imputed.select_dtypes(include=[np.number]).columns.tolist()
    selected_features = feature_selection(train_imputed, top_n=30)
    
    # Step 3: Normalize selected features
    print("\n[STEP 3] Normalizando features...")
    train_normalized, scaler = normalize_data(train_imputed, selected_features, scaler_type='robust')
    val_normalized, _ = normalize_data(val_imputed, selected_features, scaler_type='robust')
    test_normalized, _ = normalize_data(test_imputed, selected_features, scaler_type='robust')
    
    # Step 4: Create final optimized datasets
    print("\n[STEP 4] Criando datasets otimizados...")
    
    # Select final columns (original + scaled)
    final_cols = [
        'date', 'item_id', 'material', 'familia', 'category',
        'quantidade', 'target', 'deposito', 'site_id', 'fornecedor',
        'lead_time_days', 'solicitacao', 'data_solicitado', 'data_compra'
    ]
    
    # Add temporal features
    temporal_cols = ['year', 'month', 'day', 'weekday', 'quarter', 'day_of_year',
                     'month_sin', 'month_cos', 'day_of_year_sin', 'day_of_year_cos',
                     'is_weekend', 'is_holiday']
    
    # Add selected features
    all_final_cols = final_cols + temporal_cols + selected_features
    
    # Add scaled versions
    scaled_features = [f'{f}_scaled' for f in selected_features if f'{f}_scaled' in train_normalized.columns]
    all_final_cols = all_final_cols + scaled_features
    
    # Keep only available columns
    train_final = train_normalized[[col for col in all_final_cols if col in train_normalized.columns]].copy()
    val_final = val_normalized[[col for col in all_final_cols if col in val_normalized.columns]].copy()
    test_final = test_normalized[[col for col in all_final_cols if col in test_normalized.columns]].copy()
    
    print(f"\n[INFO] Datasets otimizados criados:")
    print(f"  Train: {len(train_final)} registros, {len(train_final.columns)} features")
    print(f"  Validation: {len(val_final)} registros, {len(val_final.columns)} features")
    print(f"  Test: {len(test_final)} registros, {len(test_final.columns)} features")
    
    return train_final, val_final, test_final, selected_features

def save_optimized_datasets(train_final, val_final, test_final, selected_features):
    """Save optimized datasets"""
    print("\n" + "=" * 80)
    print("SALVANDO DATASETS OTIMIZADOS")
    print("=" * 80)
    
    # Save datasets
    train_file = OUTPUT_DIR / "nova_corrente_top5_train_optimized.csv"
    train_final.to_csv(train_file, index=False, encoding='utf-8')
    print(f"\n[SUCCESS] Train otimizado: {train_file}")
    
    val_file = OUTPUT_DIR / "nova_corrente_top5_validation_optimized.csv"
    val_final.to_csv(val_file, index=False, encoding='utf-8')
    print(f"[SUCCESS] Validation otimizado: {val_file}")
    
    test_file = OUTPUT_DIR / "nova_corrente_top5_test_optimized.csv"
    test_final.to_csv(test_file, index=False, encoding='utf-8')
    print(f"[SUCCESS] Test otimizado: {test_file}")
    
    # Save selected features
    features_file = OUTPUT_DIR / "selected_features.json"
    with open(features_file, 'w', encoding='utf-8') as f:
        json.dump({'selected_features': selected_features}, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Features selecionadas: {features_file}")
    
    # Save summary
    summary = {
        'optimization_date': datetime.now().isoformat(),
        'train_records': len(train_final),
        'val_records': len(val_final),
        'test_records': len(test_final),
        'total_features': len(train_final.columns),
        'selected_features_count': len(selected_features),
        'selected_features': selected_features,
        'improvements': {
            'imputation': 'Features externas imputadas com domain knowledge',
            'normalization': 'Features normalizadas com RobustScaler',
            'feature_selection': f'Top {len(selected_features)} features selecionadas'
        }
    }
    
    summary_file = OUTPUT_DIR / "optimization_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
    print(f"[SUCCESS] Resumo: {summary_file}")
    
    return summary

def main():
    """Main optimization pipeline"""
    print("\n" + "=" * 80)
    print("PIPELINE DE OTIMIZAÇÃO DE PRE-PROCESSAMENTO")
    print("=" * 80 + "\n")
    
    # Step 1: Load datasets
    train_df, val_df, test_df = load_datasets()
    
    # Step 2: Optimize preprocessing
    train_optimized, val_optimized, test_optimized, selected_features = optimize_preprocessing(
        train_df, val_df, test_df
    )
    
    # Step 3: Save optimized datasets
    summary = save_optimized_datasets(train_optimized, val_optimized, test_optimized, selected_features)
    
    print("\n" + "=" * 80)
    print("OTIMIZAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print(f"\n[RESUMO]")
    print(f"  - Train: {summary['train_records']:,} registros, {summary['total_features']} features")
    print(f"  - Validation: {summary['val_records']:,} registros")
    print(f"  - Test: {summary['test_records']:,} registros")
    print(f"  - Features selecionadas: {summary['selected_features_count']}")
    print(f"\n[MELHORIAS]")
    print(f"  1. Imputação: Features externas preenchidas")
    print(f"  2. Normalização: Features normalizadas (RobustScaler)")
    print(f"  3. Feature Selection: Top {summary['selected_features_count']} features")
    print(f"\n[PRÓXIMOS PASSOS]")
    print(f"  1. Treinar modelos com dados otimizados")
    print(f"  2. Avaliar performance melhorada")
    print(f"  3. Criar ensemble model")
    
    return train_optimized, val_optimized, test_optimized, summary

if __name__ == "__main__":
    main()

