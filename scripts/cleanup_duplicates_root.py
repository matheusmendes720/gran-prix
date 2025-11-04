#!/usr/bin/env python3
"""
Script para Remover Arquivos Duplicados da Raiz
Remove arquivos que já existem no destino organizado
"""

import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent

# Mapeamento de arquivos na raiz que devem ser removidos se já existem no destino
DUPLICATES_TO_REMOVE = {
    # Fix Reports
    "ALL_ERRORS_FIXED.md": "docs/reports/fixes/ALL_ERRORS_FIXED.md",
    "ALL_FIXES_AND_TESTING.md": "docs/reports/fixes/ALL_FIXES_AND_TESTING.md",
    "ALL_FIXES_COMPLETE.md": "docs/reports/fixes/ALL_FIXES_COMPLETE.md",
    "ALL_FIXES_SUMMARY.md": "docs/reports/fixes/ALL_FIXES_SUMMARY.md",
    "BACKEND_FIXES_COMPLETE.md": "docs/reports/fixes/BACKEND_FIXES_COMPLETE.md",
    "ENV_AND_PORT_FIXED.md": "docs/reports/fixes/ENV_AND_PORT_FIXED.md",
    "ERRORS_FIXED_SUMMARY.md": "docs/reports/fixes/ERRORS_FIXED_SUMMARY.md",
    "EXTERNAL_FEATURES_FIX.md": "docs/reports/fixes/EXTERNAL_FEATURES_FIX.md",
    "FEATURES_FIX_SUMMARY.md": "docs/reports/fixes/FEATURES_FIX_SUMMARY.md",
    "FRONTEND_ERRORS_FIXED.md": "docs/reports/fixes/FRONTEND_ERRORS_FIXED.md",
    "KEEPING_IT_UP.md": "docs/reports/fixes/KEEPING_IT_UP.md",
    "STARTUP_FIX_APPLIED.md": "docs/reports/fixes/STARTUP_FIX_APPLIED.md",
    
    # Monitoring Reports
    "APP_BEHAVIOR_MONITORING.md": "docs/reports/monitoring/APP_BEHAVIOR_MONITORING.md",
    "AUTO_MONITORING_SETUP.md": "docs/reports/monitoring/AUTO_MONITORING_SETUP.md",
    "CONTINUOUS_MONITORING.md": "docs/reports/monitoring/CONTINUOUS_MONITORING.md",
    "CONTINUOUS_TESTING.md": "docs/reports/monitoring/CONTINUOUS_TESTING.md",
    "LIVE_LOGS_MONITORING.md": "docs/reports/monitoring/LIVE_LOGS_MONITORING.md",
    "LIVE_MONITORING_ACTIVE.md": "docs/reports/monitoring/LIVE_MONITORING_ACTIVE.md",
    "LIVE_MONITORING_RUNNING.md": "docs/reports/monitoring/LIVE_MONITORING_RUNNING.md",
    "LIVE_TESTING_STATUS.md": "docs/reports/monitoring/LIVE_TESTING_STATUS.md",
    "MONITORING_LIVE.md": "docs/reports/monitoring/MONITORING_LIVE.md",
    "MONITORING_LOG.md": "docs/reports/monitoring/MONITORING_LOG.md",
    "MONITORING_LOG_CONTINUED.md": "docs/reports/monitoring/MONITORING_LOG_CONTINUED.md",
    "MONITORING_SETUP.md": "docs/reports/monitoring/MONITORING_SETUP.md",
    "MONITORING_STATUS.md": "docs/reports/monitoring/MONITORING_STATUS.md",
    
    # Screenshot Reports
    "RESTART_AND_SCREENSHOTS.md": "docs/reports/screenshots/RESTART_AND_SCREENSHOTS.md",
    "SCREENSHOTS_CAPTURED.md": "docs/reports/screenshots/SCREENSHOTS_CAPTURED.md",
    "SCREENSHOTS_READY.md": "docs/reports/screenshots/SCREENSHOTS_READY.md",
    "SCREENSHOTS_STATUS.md": "docs/reports/screenshots/SCREENSHOTS_STATUS.md",
    
    # System Status
    "BACKEND_RUNNING.md": "docs/reports/system-status/BACKEND_RUNNING.md",
    "SYSTEM_LAUNCH_STATUS.md": "docs/reports/system-status/SYSTEM_LAUNCH_STATUS.md",
    "SYSTEM_LAUNCHED.md": "docs/reports/system-status/SYSTEM_LAUNCHED.md",
    "SYSTEM_RESTARTED.md": "docs/reports/system-status/SYSTEM_RESTARTED.md",
    "SYSTEM_STATUS_FINAL.md": "docs/reports/system-status/SYSTEM_STATUS_FINAL.md",
    
    # Quick Guides
    "QUICK_START_GUIDE.md": "docs/guides/QUICK_START_GUIDE.md",
    "NEXT_STEPS.md": "docs/guides/NEXT_STEPS.md",
    
    # README files (mover para docs/guides/)
    "README_BACKEND_FIXED.md": "docs/guides/README_BACKEND_FIXED.md",
    "README_BACKEND_START.md": "docs/guides/README_BACKEND_START.md",
    "README_FINAL_BACKEND_START.md": "docs/guides/README_FINAL_BACKEND_START.md",
    "README_STARTUP.md": "docs/guides/README_STARTUP.md",
}

def main():
    """Remove arquivos duplicados da raiz"""
    import sys
    import io
    
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("[*] Removendo arquivos duplicados da raiz...\n")
    
    removed = []
    not_found_dest = []
    not_found_root = []
    
    for root_file, dest_file in DUPLICATES_TO_REMOVE.items():
        root_path = ROOT_DIR / root_file
        dest_path = ROOT_DIR / dest_file
        
        if not root_path.exists():
            not_found_root.append(root_file)
            continue
        
        if dest_path.exists():
            # Arquivo existe no destino, remover da raiz
            try:
                root_path.unlink()
                removed.append(root_file)
                print(f"[OK] Removido: {root_file} (existe em {dest_file})")
            except Exception as e:
                print(f"[ERROR] Erro ao remover {root_file}: {str(e)}")
        else:
            # Arquivo não existe no destino, mover
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                import shutil
                shutil.move(str(root_path), str(dest_path))
                removed.append(root_file)
                print(f"[OK] Movido: {root_file} -> {dest_file}")
            except Exception as e:
                print(f"[ERROR] Erro ao mover {root_file}: {str(e)}")
    
    print("\n" + "="*60)
    print("[*] RESUMO DA LIMPEZA")
    print("="*60)
    print(f"[OK] Arquivos removidos/movidos: {len(removed)}")
    
    if removed:
        print("\n[OK] Arquivos processados:")
        for file in removed:
            print(f"   - {file}")
    
    # Verificar arquivos restantes na raiz
    print("\n[*] Arquivos .md restantes na raiz:")
    root_files = [f for f in ROOT_DIR.glob("*.md") if f.name not in ["README.md", "CHANGELOG.md"]]
    if root_files:
        print(f"   Total: {len(root_files)} arquivos")
        for file in sorted(root_files):
            print(f"   - {file.name}")
    else:
        print("   (nenhum arquivo .md alem dos essenciais - perfeito!)")
    
    print("\n" + "="*60)
    print("[*] Limpeza completa!")
    print("="*60)

if __name__ == "__main__":
    main()

