#!/usr/bin/env python3
"""
Configuração Service Account para Google Sheets
Autor: Claude Code
Data: 11/07/2025
"""

import gspread
from google.oauth2.service_account import Credentials
import os
import json

class ServiceAccountConfig:
    """Classe para configurar autenticação com Service Account"""
    
    def __init__(self, service_account_path=None):
        """
        Inicializa configuração do Service Account
        
        Args:
            service_account_path: Caminho para arquivo JSON do service account
        """
        self.service_account_path = service_account_path or 'credentials/service-account.json'
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        self.gc = None
    
    def setup_credentials(self):
        """Configura credenciais do Service Account"""
        try:
            # Verifica se arquivo existe
            if not os.path.exists(self.service_account_path):
                print(f"❌ Arquivo de credenciais não encontrado: {self.service_account_path}")
                print("💡 Instruções:")
                print("   1. Baixe o arquivo JSON do Service Account do Google Cloud Console")
                print("   2. Salve como 'credentials/service-account.json'")
                print("   3. Ou especifique o caminho correto")
                return False
            
            # Carrega credenciais
            credentials = Credentials.from_service_account_file(
                self.service_account_path, 
                scopes=self.scopes
            )
            
            # Autoriza gspread
            self.gc = gspread.authorize(credentials)
            
            print("✅ Service Account configurado com sucesso!")
            return True
            
        except json.JSONDecodeError:
            print("❌ Erro: Arquivo JSON inválido")
            return False
        except Exception as e:
            print(f"❌ Erro ao configurar Service Account: {str(e)}")
            return False
    
    def test_connection(self):
        """Testa conexão com Google Sheets"""
        try:
            if not self.gc:
                print("❌ Service Account não configurado")
                return False
            
            # Lista planilhas disponíveis (teste básico)
            sheets = self.gc.list_permissions()
            print(f"✅ Conexão testada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro no teste de conexão: {str(e)}")
            return False
    
    def get_client(self):
        """Retorna cliente gspread autorizado"""
        if not self.gc:
            if not self.setup_credentials():
                return None
        return self.gc

def setup_service_account():
    """Função auxiliar para configurar Service Account"""
    print("🔐 CONFIGURAÇÃO SERVICE ACCOUNT")
    print("=" * 50)
    
    # Cria diretório de credenciais se não existir
    os.makedirs('credentials', exist_ok=True)
    
    # Verifica se arquivo já existe
    if os.path.exists('credentials/service-account.json'):
        print("✅ Arquivo de credenciais encontrado!")
        
        # Testa configuração
        config = ServiceAccountConfig()
        if config.setup_credentials():
            return config
    else:
        print("📋 INSTRUÇÕES PARA CONFIGURAR SERVICE ACCOUNT:")
        print()
        print("1. 🌐 Acesse Google Cloud Console:")
        print("   https://console.cloud.google.com")
        print()
        print("2. 🔧 Crie/Configure Service Account:")
        print("   • IAM & Admin > Service Accounts")
        print("   • Create Service Account")
        print("   • Nome: nps-automation-service")
        print("   • Role: Editor")
        print()
        print("3. 🔑 Gere chave JSON:")
        print("   • Clique no Service Account criado")
        print("   • Keys > Add Key > Create new key")
        print("   • Tipo: JSON")
        print()
        print("4. 📁 Salve o arquivo:")
        print("   • Salve como: credentials/service-account.json")
        print("   • Neste diretório: /caminho/para/seu/projeto/")
        print()
        print("5. 🔌 Ative APIs necessárias:")
        print("   • APIs & Services > Library")
        print("   • Google Sheets API")
        print("   • Google Drive API")
        print()
        
    return None

if __name__ == "__main__":
    setup_service_account()