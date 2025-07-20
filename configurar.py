#!/usr/bin/env python3
"""
Script de configuração rápida do sistema NPS
Autor: Claude Code
Data: 12/07/2025
"""

from auth_automatico import AuthAutomatico

def configurar_sistema():
    """Configura sistema de forma simplificada"""
    print("🚀 CONFIGURAÇÃO RÁPIDA - SISTEMA NPS")
    print("=" * 50)
    
    auth = AuthAutomatico()
    
    print(f"✅ Client ID: {auth.client_id}")
    print(f"✅ Client Secret: {auth.client_secret[:15]}...")
    print()
    
    # Verifica se já configurado
    if auth.conectar_automatico():
        print("🎉 Sistema já configurado e funcionando!")
        
        # Testa planilha
        print("🧪 Testando acesso à sua planilha...")
        if auth.testar_planilha():
            print("✅ Tudo funcionando perfeitamente!")
            print("🚀 Execute 'python main.py' para usar o sistema")
        else:
            print("❌ Problema no acesso à planilha")
    else:
        print("⚙️ Sistema precisa ser configurado uma vez")
        print()
        print("📋 PASSOS:")
        print("1. Abra este link no navegador:")
        print(f"🔗 {auth.get_auth_url()}")
        print()
        print("2. Faça login e autorize")
        print("3. Copie o código")
        print("4. Execute:")
        print("   python -c \"")
        print("   from auth_automatico import AuthAutomatico")
        print("   auth = AuthAutomatico()")
        print("   auth.configurar_token_inicial('SEU_CODIGO_AQUI')\"")
        print()
        print("🎯 Depois disso, sistema funcionará automaticamente!")

if __name__ == "__main__":
    configurar_sistema()