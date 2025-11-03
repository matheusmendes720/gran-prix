"""
Quick setup and run script.
Checks dependencies and runs the system.
"""
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    required = [
        'pandas',
        'numpy',
        'statsmodels',
        'prophet',
        'scikit-learn',
        'holidays',
        'pyyaml'
    ]
    
    optional = {
        'pmdarima': 'Auto ARIMA (recommended)',
        'tensorflow': 'LSTM model (optional)',
        'reportlab': 'PDF reports (optional)',
        'streamlit': 'Interactive dashboard (optional)',
        'flask': 'API server (optional)'
    }
    
    missing_required = []
    missing_optional = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing_required.append(package)
    
    for package, description in optional.items():
        try:
            __import__(package)
        except ImportError:
            missing_optional.append((package, description))
    
    if missing_required:
        print("\n[ERROR] Missing required dependencies:")
        for pkg in missing_required:
            print(f"   - {pkg}")
        print("\nInstall with: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print("\n[WARNING] Missing optional dependencies:")
        for pkg, desc in missing_optional:
            print(f"   - {pkg}: {desc}")
        print("\nThese features will be disabled, but system will run.")
    
    return True

def main():
    """Main setup and run."""
    print("\n" + "="*80)
    print(" "*25 + "DEMAND FORECASTING SYSTEM")
    print(" "*30 + "Setup & Run")
    print("="*80 + "\n")
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("\n[ERROR] Please install required dependencies first:")
        print("   pip install -r requirements.txt\n")
        return 1
    
    print("[OK] All required dependencies installed\n")
    
    # Run main script
    print("="*80)
    print("Starting forecast system...")
    print("="*80 + "\n")
    
    run_script = Path(__file__).parent / "scripts" / "run_all.py"
    
    try:
        result = subprocess.run([sys.executable, str(run_script)] + sys.argv[1:], 
                               check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\n\n[WARNING] Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())

