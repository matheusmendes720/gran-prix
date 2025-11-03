#!/usr/bin/env python3
"""
Main entry point for Nova Corrente Dashboard
Run this script to start the interactive visualization dashboard
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.visualization.dash_app import NovaCorrenteDashboard

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🚀 Nova Corrente Telecom Demand Forecasting Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_dashboard.py                    # Run on default port 8050
  python run_dashboard.py --port 8080       # Run on custom port
  python run_dashboard.py --host 0.0.0.0    # Allow external access
  
For D3.js interactive map:
  Open src/visualization/d3_map.html in a web browser
        """
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8050,
        help='Port to run dashboard (default: 8050)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Host to run dashboard (default: 127.0.0.1, use 0.0.0.0 for external access)'
    )
    
    parser.add_argument(
        '--no-debug',
        action='store_true',
        help='Disable debug mode'
    )
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*70)
        print("🇧🇷 NOVA CORRENTE TELECOM DEMAND FORECASTING")
        print("="*70)
        print("📊 Starting interactive dashboard...")
        print(f"🌐 Dashboard URL: http://{args.host}:{args.port}")
        print("📁 D3.js Map: Open src/visualization/d3_map.html in browser")
        print("="*70 + "\n")
        
        dashboard = NovaCorrenteDashboard()
        dashboard.run(host=args.host, port=args.port, debug=not args.no_debug)
        
    except KeyboardInterrupt:
        print("\n\n✓ Dashboard stopped by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error running dashboard: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you have installed all dependencies:")
        print("   pip install -r requirements.txt")
        print("2. Ensure training data exists in data/training/")
        print("3. Check that metadata.json and training_summary.json exist")
        import traceback
        traceback.print_exc()
        sys.exit(1)

