#!/usr/bin/env python3
"""
Script de Reorganização do Root Workspace
Move arquivos da raiz para subpastas temáticas organizadas
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

# Configuração do projeto
ROOT_DIR = Path(__file__).parent.parent
DOCS_DIR = ROOT_DIR / "docs"
REPORTS_DIR = DOCS_DIR / "reports"

# Mapeamento de arquivos para mover
FILE_MOVEMENTS: Dict[str, str] = {
    # Fix Reports → docs/reports/fixes/
    "ALL_ERRORS_FIXED.md": "docs/reports/fixes/",
    "ALL_FIXES_AND_TESTING.md": "docs/reports/fixes/",
    "ALL_FIXES_COMPLETE.md": "docs/reports/fixes/",
    "ALL_FIXES_SUMMARY.md": "docs/reports/fixes/",
    "BACKEND_FIXES_COMPLETE.md": "docs/reports/fixes/",
    "ENV_AND_PORT_FIXED.md": "docs/reports/fixes/",
    "ERRORS_FIXED_SUMMARY.md": "docs/reports/fixes/",
    "EXTERNAL_FEATURES_FIX.md": "docs/reports/fixes/",
    "FEATURES_FIX_SUMMARY.md": "docs/reports/fixes/",
    "FRONTEND_ERRORS_FIXED.md": "docs/reports/fixes/",
    "KEEPING_IT_UP.md": "docs/reports/fixes/",
    "STARTUP_FIX_APPLIED.md": "docs/reports/fixes/",
    
    # Backend Fix Reports → docs/reports/fixes/
    "backend/FIXED_START.md": "docs/reports/fixes/",
    "backend/FIXES_APPLIED.md": "docs/reports/fixes/",
    
    # Monitoring Reports → docs/reports/monitoring/
    "APP_BEHAVIOR_MONITORING.md": "docs/reports/monitoring/",
    "AUTO_MONITORING_SETUP.md": "docs/reports/monitoring/",
    "CONTINUOUS_MONITORING.md": "docs/reports/monitoring/",
    "CONTINUOUS_TESTING.md": "docs/reports/monitoring/",
    "LIVE_LOGS_MONITORING.md": "docs/reports/monitoring/",
    "LIVE_MONITORING_ACTIVE.md": "docs/reports/monitoring/",
    "LIVE_MONITORING_RUNNING.md": "docs/reports/monitoring/",
    "LIVE_TESTING_STATUS.md": "docs/reports/monitoring/",
    "MONITORING_LIVE.md": "docs/reports/monitoring/",
    "MONITORING_LOG.md": "docs/reports/monitoring/",
    "MONITORING_LOG_CONTINUED.md": "docs/reports/monitoring/",
    "MONITORING_SETUP.md": "docs/reports/monitoring/",
    "MONITORING_STATUS.md": "docs/reports/monitoring/",
    
    # Screenshot Reports → docs/reports/screenshots/
    "RESTART_AND_SCREENSHOTS.md": "docs/reports/screenshots/",
    "SCREENSHOTS_CAPTURED.md": "docs/reports/screenshots/",
    "SCREENSHOTS_READY.md": "docs/reports/screenshots/",
    "SCREENSHOTS_STATUS.md": "docs/reports/screenshots/",
    
    # System Status → docs/reports/system-status/
    "BACKEND_RUNNING.md": "docs/reports/system-status/",
    "SYSTEM_LAUNCH_STATUS.md": "docs/reports/system-status/",
    "SYSTEM_LAUNCHED.md": "docs/reports/system-status/",
    "SYSTEM_RESTARTED.md": "docs/reports/system-status/",
    "SYSTEM_STATUS_FINAL.md": "docs/reports/system-status/",
    
    # Git Docs → docs/development/
    "COMMIT_MESSAGE.md": "docs/development/",
    "GIT_TAGS_REFERENCE.md": "docs/development/",
    
    # Quick Guides → docs/guides/
    "QUICK_START_GUIDE.md": "docs/guides/",
    "NEXT_STEPS.md": "docs/guides/",
    
    # Outros docs → docs/development/
    "CLAUDE.md": "docs/development/",
}


def create_directories():
    """Cria todos os diretórios necessários"""
    directories = set()
    for dest in FILE_MOVEMENTS.values():
        directories.add(ROOT_DIR / dest)
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Diretorio criado/verificado: {directory.relative_to(ROOT_DIR)}")


def move_file_with_git(source: Path, dest_dir: Path) -> Tuple[bool, str]:
    """
    Move arquivo usando git mv para manter histórico
    Retorna (sucesso, mensagem)
    """
    if not source.exists():
        return False, f"[SKIP] Arquivo nao encontrado: {source}"
    
    dest_file = dest_dir / source.name
    
    # Se arquivo já existe no destino, não sobrescrever
    if dest_file.exists():
        return False, f"[SKIP] Arquivo ja existe no destino: {dest_file}"
    
    try:
        # Tentar usar git mv primeiro
        result = subprocess.run(
            ["git", "mv", str(source), str(dest_file)],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return True, f"[OK] Movido (git mv): {source.name} -> {dest_dir.relative_to(ROOT_DIR)}"
        else:
            # Se git mv falhar, usar shutil.move
            shutil.move(str(source), str(dest_file))
            return True, f"[OK] Movido (shutil): {source.name} -> {dest_dir.relative_to(ROOT_DIR)}"
    
    except Exception as e:
        return False, f"[ERROR] Erro ao mover {source.name}: {str(e)}"


def main():
    """Executa a reorganização completa"""
    import sys
    import io
    
    # Configurar stdout para UTF-8 no Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("[*] Iniciando reorganizacao do root workspace...\n")
    
    # Criar diretórios
    print("[*] Criando diretorios necessarios...")
    create_directories()
    print()
    
    # Mover arquivos
    print("[*] Movendo arquivos...")
    moved = []
    skipped = []
    errors = []
    
    for source_rel, dest_rel in FILE_MOVEMENTS.items():
        source = ROOT_DIR / source_rel
        dest_dir = ROOT_DIR / dest_rel
        
        success, message = move_file_with_git(source, dest_dir)
        print(message)
        
        if success:
            moved.append(source_rel)
        elif "nao encontrado" in message or "nao existe" in message:
            skipped.append(source_rel)
        else:
            errors.append((source_rel, message))
    
    # Resumo
    print("\n" + "="*60)
    print("[*] RESUMO DA REORGANIZACAO")
    print("="*60)
    print(f"[OK] Arquivos movidos: {len(moved)}")
    print(f"[SKIP] Arquivos nao encontrados (pulados): {len(skipped)}")
    print(f"[ERROR] Erros: {len(errors)}")
    
    if moved:
        print("\n[OK] Arquivos movidos com sucesso:")
        for file in moved:
            print(f"   - {file}")
    
    if skipped:
        print("\n[SKIP] Arquivos nao encontrados (ja movidos ou nao existem):")
        for file in skipped:
            print(f"   - {file}")
    
    if errors:
        print("\n[ERROR] Erros encontrados:")
        for file, error in errors:
            print(f"   - {file}: {error}")
    
    print("\n" + "="*60)
    print("[*] Reorganizacao completa!")
    print("="*60)
    
    # Verificar arquivos restantes na raiz
    print("\n[*] Arquivos .md restantes na raiz:")
    root_files = list(ROOT_DIR.glob("*.md"))
    if root_files:
        for file in root_files:
            print(f"   - {file.name}")
    else:
        print("   (nenhum arquivo .md na raiz - perfeito!)")
    
    # Arquivos essenciais que devem permanecer
    essential_files = [
        "README.md",
        "CHANGELOG.md"
    ]
    
    print("\n[OK] Arquivos essenciais que devem permanecer na raiz:")
    for file in essential_files:
        if (ROOT_DIR / file).exists():
            print(f"   [OK] {file}")
        else:
            print(f"   [WARN] {file} (nao encontrado)")


if __name__ == "__main__":
    main()

