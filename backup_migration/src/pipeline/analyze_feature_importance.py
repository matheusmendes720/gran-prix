"""
Analyze feature importance for enhanced Brazilian dataset.

Identifies which Brazilian features contribute most to forecasting accuracy.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    """Load enhanced dataset."""
    file_path = DATA_DIR / "unified_dataset_with_brazilian_factors.csv"
    df = pd.read_csv(file_path, low_memory=False)
    
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='ISO8601', errors='coerce')
    
    return df


def prepare_data(df: pd.DataFrame, target_col: str = 'quantity', sample_size: Optional[int] = None):
    """Prepare data for feature importance analysis."""
    # Sample if needed
    if sample_size and len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=42)
    
    # Identify target
    if target_col not in df.columns:
        alternatives = ['Quantity_Consumed', 'order_demand', 'Order_Demand', 'demand']
        for alt in alternatives:
            if alt in df.columns:
                target_col = alt
                break
    
    if target_col not in df.columns:
        raise ValueError(f"Target column not found")
    
    # Get target
    y = df[target_col].copy()
    
    # Exclude target and metadata
    exclude_cols = [
        target_col, 'item_id', 'item_name', 'site_id', 'dataset_source',
        'date', 'timestamp', 'id', 'UID', 'Product ID', 'SKU_ID'
    ]
    
    # Get features
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    X = df[feature_cols].copy()
    
    # Select only numerical features
    numerical_features = X.select_dtypes(include=[np.number]).columns.tolist()
    X = X[numerical_features].copy()
    feature_cols = numerical_features
    
    # Handle missing values
    X = X.fillna(0).replace([np.inf, -np.inf], 0)
    
    # Remove constant features
    constant_features = [col for col in X.columns if X[col].nunique() <= 1]
    if constant_features:
        print(f"[+] Removing {len(constant_features)} constant features")
        X = X.drop(columns=constant_features)
        feature_cols = [c for c in feature_cols if c not in constant_features]
    
    return X, y, feature_cols


def calculate_feature_importance(X: pd.DataFrame, y: pd.Series, 
                                 feature_cols: List[str],
                                 n_estimators: int = 100) -> Dict:
    """Calculate feature importance using Random Forest."""
    print("[+] Calculating feature importance with Random Forest...")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train Random Forest
    print(f"[+] Training Random Forest ({n_estimators} trees)...")
    rf = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=10,
        random_state=42,
        n_jobs=1,  # Use single thread on Windows
        verbose=0
    )
    
    rf.fit(X_train, y_train)
    
    # Get feature importances
    importances = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Permutation importance (reduced repeats for faster processing)
    print("[+] Calculating permutation importance...")
    perm_importance = permutation_importance(
        rf, X_test, y_test, n_repeats=5, random_state=42, n_jobs=1  # Use single thread on Windows
    )
    
    perm_df = pd.DataFrame({
        'feature': feature_cols,
        'perm_importance_mean': perm_importance.importances_mean,
        'perm_importance_std': perm_importance.importances_std
    }).sort_values('perm_importance_mean', ascending=False)
    
    # Combine results
    importance_df = importances.merge(perm_df, on='feature', how='inner')
    importance_df = importance_df.sort_values('perm_importance_mean', ascending=False)
    
    # Calculate score
    test_score = rf.score(X_test, y_test)
    
    return {
        'importance_df': importance_df,
        'model_score': test_score,
        'top_features': importance_df.head(20).to_dict('records')
    }


def categorize_features(feature_cols: List[str]) -> Dict[str, List[str]]:
    """Categorize features by type."""
    categories = {
        'Climate': [],
        'Economic': [],
        'IoT': [],
        'Fiber': [],
        'Operators': [],
        'Temporal': [],
        'Other': []
    }
    
    for feat in feature_cols:
        feat_lower = feat.lower()
        
        if any(k in feat_lower for k in ['temp', 'precip', 'humid', 'climate']):
            categories['Climate'].append(feat)
        elif any(k in feat_lower for k in ['inflation', 'exchange', 'economic']):
            categories['Economic'].append(feat)
        elif 'iot' in feat_lower:
            categories['IoT'].append(feat)
        elif 'fiber' in feat_lower:
            categories['Fiber'].append(feat)
        elif any(k in feat_lower for k in ['market', 'operator', '5g', 'vivo', 'claro', 'tim']):
            categories['Operators'].append(feat)
        elif any(k in feat_lower for k in ['month', 'year', 'holiday', 'weekend', 'carnival', 'vacation']):
            categories['Temporal'].append(feat)
        else:
            categories['Other'].append(feat)
    
    return categories


def analyze_brazilian_features(results: Dict) -> Dict:
    """Analyze Brazilian feature contributions."""
    importance_df = results['importance_df']
    
    # Identify Brazilian features
    brazilian_keywords = ['iot', 'fiber', 'vivo', 'claro', 'tim', 'market', '5g', 'operator']
    
    brazilian_features = []
    non_brazilian_features = []
    
    for _, row in importance_df.iterrows():
        feat = row['feature'].lower()
        if any(kw in feat for kw in brazilian_keywords):
            brazilian_features.append(row.to_dict())
        else:
            non_brazilian_features.append(row.to_dict())
    
    # Calculate contributions
    brazilian_importance = sum(f['perm_importance_mean'] for f in brazilian_features)
    total_importance = importance_df['perm_importance_mean'].sum()
    brazilian_contribution = (brazilian_importance / total_importance) * 100 if total_importance > 0 else 0
    
    # Top Brazilian features
    top_brazilian = sorted(brazilian_features, 
                          key=lambda x: x['perm_importance_mean'], 
                          reverse=True)[:10]
    
    return {
        'brazilian_contribution_pct': brazilian_contribution,
        'total_brazilian_features': len(brazilian_features),
        'top_brazilian_features': top_brazilian,
        'brazilian_importance_total': brazilian_importance,
        'non_brazilian_features': len(non_brazilian_features)
    }


def generate_report(results: Dict, brazilian_analysis: Dict, 
                   categories: Dict[str, List[str]]):
    """Generate feature importance report."""
    print("\n" + "="*80)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("="*80)
    
    print(f"\n[+] Model R² Score: {results['model_score']:.4f}")
    print(f"[+] Total Features Analyzed: {len(results['importance_df'])}")
    print(f"[+] Brazilian Feature Contribution: {brazilian_analysis['brazilian_contribution_pct']:.2f}%")
    
    print("\n[+] Top 10 Features:")
    top_10 = results['importance_df'].head(10)
    for idx, row in top_10.iterrows():
        print(f"    {row['feature']:30s} {row['perm_importance_mean']:8.4f} ± {row['perm_importance_std']:.4f}")
    
    print("\n[+] Top 5 Brazilian Features:")
    for feat in brazilian_analysis['top_brazilian_features'][:5]:
        print(f"    {feat['feature']:30s} {feat['perm_importance_mean']:8.4f} ± {feat['perm_importance_std']:.4f}")
    
    # Save report
    report = {
        'timestamp': datetime.now().isoformat(),
        'model_score': float(results['model_score']),
        'total_features': len(results['importance_df']),
        'brazilian_analysis': brazilian_analysis,
        'top_features': results['importance_df'].head(20).to_dict('records'),
        'feature_categories': {
            cat: len(feats) for cat, feats in categories.items()
        }
    }
    
    report_file = RESULTS_DIR / f"feature_importance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Save CSV
    csv_file = RESULTS_DIR / f"feature_importance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    results['importance_df'].to_csv(csv_file, index=False)
    
    print(f"\n[OK] Report saved to: {report_file}")
    print(f"[OK] CSV saved to: {csv_file}")
    
    return report_file, csv_file


def main():
    """Main feature importance analysis."""
    print("="*80)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("Brazilian Dataset Enhancement")
    print("="*80)
    
    # Load data
    print("\n[+] Loading dataset...")
    df = load_dataset()
    print(f"[OK] Loaded {len(df):,} rows × {len(df.columns)} columns")
    
    # Sample for faster processing
    sample_size = min(50000, len(df))
    print(f"[+] Sampling {sample_size:,} rows for analysis...")
    
    # Prepare data
    X, y, feature_cols = prepare_data(df, sample_size=sample_size)
    
    # Categorize features
    categories = categorize_features(feature_cols)
    print("\n[+] Feature Categories:")
    for cat, feats in categories.items():
        if feats:
            print(f"    {cat:15s}: {len(feats):3d} features")
    
    # Calculate importance
    results = calculate_feature_importance(X, y, feature_cols, n_estimators=100)
    
    # Analyze Brazilian features
    brazilian_analysis = analyze_brazilian_features(results)
    
    # Generate report
    report_file, csv_file = generate_report(results, brazilian_analysis, categories)
    
    print("\n" + "="*80)
    print("[SUCCESS] FEATURE IMPORTANCE ANALYSIS COMPLETE")
    print("="*80)
    
    return results, brazilian_analysis, report_file, csv_file


if __name__ == "__main__":
    main()

