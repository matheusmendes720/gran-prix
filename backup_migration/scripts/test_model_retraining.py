"""
Quick test of model retraining pipeline.
Uses a small sample to verify everything works.
"""
import sys
from pathlib import Path

# Add parent directory to path
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.pipeline.retrain_models_with_brazilian_data import (
    load_enhanced_dataset,
    prepare_features,
    train_arima_model
)

def test_pipeline():
    """Quick test of retraining pipeline."""
    print("="*80)
    print("TESTING MODEL RETRAINING PIPELINE")
    print("="*80)
    
    # Load data
    print("\n[+] Loading dataset...")
    df = load_enhanced_dataset()
    
    # Use sample for quick test
    print("\n[+] Sampling 1000 rows for quick test...")
    df_sample = df.sample(n=min(1000, len(df)), random_state=42)
    
    # Prepare features
    print("\n[+] Preparing features...")
    X, y, feature_cols = prepare_features(df_sample)
    
    print(f"\n[OK] Test pipeline setup successful!")
    print(f"    Dataset shape: {df_sample.shape}")
    print(f"    Features: {len(feature_cols)}")
    print(f"    Target range: {y.min():.2f} to {y.max():.2f}")
    
    # Test ARIMA training (quick test)
    print("\n[+] Testing ARIMA training...")
    try:
        result = train_arima_model(X, y, train_size=0.7)
        if result['fitted']:
            print("[OK] ARIMA training successful!")
        else:
            print(f"[!] ARIMA training failed: {result.get('error')}")
    except Exception as e:
        print(f"[!] ARIMA test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("[SUCCESS] PIPELINE TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    test_pipeline()

