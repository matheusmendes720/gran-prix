"""Script para exibir dashboard de status do sistema."""
import sys
from pathlib import Path
import logging

# Adicionar projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.system_status_dashboard import SystemStatusDashboard

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Exibir dashboard de status"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Mostrar status do sistema')
    parser.add_argument('--save', action='store_true',
                       help='Salvar relatório em JSON')
    parser.add_argument('--output', default='data/registry/system_status.json',
                       help='Arquivo de saída para relatório')
    
    args = parser.parse_args()
    
    dashboard = SystemStatusDashboard()
    
    # Exibir dashboard
    dashboard.print_dashboard()
    
    # Salvar se solicitado
    if args.save:
        dashboard.save_report(Path(args.output))
        print(f"✅ Status report saved to: {args.output}")

if __name__ == "__main__":
    main()

