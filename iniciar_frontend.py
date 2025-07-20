#!/usr/bin/env python3
"""
Script de inicialização para o DashBot Analytics Frontend
"""

import os
import sys
import subprocess
import webbrowser
import time

def main():
    print("🚀 DASHBOT ANALYTICS - INICIALIZANDO FRONTEND")
    print("=" * 60)
    
    # Verificar se está no diretório correto
    current_dir = os.getcwd()
    if not os.path.exists('frontend/server.py'):
        print("❌ Execute este script do diretório nps_automation")
        print(f"📁 Diretório atual: {current_dir}")
        print("💡 Execute: cd nps_automation && python iniciar_frontend.py")
        return
    
    # Verificar se o ambiente virtual está ativo
    if not os.path.exists('nps_env'):
        print("❌ Ambiente virtual 'nps_env' não encontrado")
        print("💡 Execute primeiro: python -m venv nps_env")
        return
    
    print("✅ Ambiente configurado corretamente")
    
    # Ativar ambiente virtual e executar servidor
    if os.name == 'nt':  # Windows
        activate_script = 'nps_env\\Scripts\\activate'
        python_exe = 'nps_env\\Scripts\\python.exe'
    else:  # Linux/Mac
        activate_script = 'source nps_env/bin/activate'
        python_exe = 'nps_env/bin/python'
    
    print("🔧 Ativando ambiente virtual...")
    print("🌐 Iniciando servidor frontend...")
    print()
    print("📡 Servidor será iniciado em: http://localhost:8080")
    print("🎯 O navegador abrirá automaticamente")
    print("⚠️  Para parar o servidor: Ctrl+C")
    print()
    print("=" * 60)
    
    try:
        # Executar servidor Flask (melhor que HTTP básico)
        os.system(f"{python_exe} frontend/server_flask.py")
    except KeyboardInterrupt:
        print("\n\n👋 Servidor parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {str(e)}")
        print("\n💡 Tente executar manualmente:")
        print("   cd frontend")
        print("   python server.py")

if __name__ == "__main__":
    main()