#!/usr/bin/env python3
"""
Autenticação automática usando suas credenciais
Autor: Claude Code
Data: 11/07/2025
"""

import gspread
import json
import os
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class AuthAutomatico:
    """Classe para autenticação automática com suas credenciais"""
    
    def __init__(self):
        """Inicializa com credenciais do ambiente"""
        # IMPORTANTE: Configure essas variáveis no arquivo .env ou como variáveis de ambiente
        self.client_id = os.environ.get('GOOGLE_CLIENT_ID', 'YOUR_CLIENT_ID_HERE')
        self.client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', 'YOUR_CLIENT_SECRET_HERE')
        self.project_id = os.environ.get('GOOGLE_PROJECT_ID', 'YOUR_PROJECT_ID_HERE')
        
        # Token de refresh pré-configurado (você precisa gerar uma vez)
        self.refresh_token = None
        
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        self.token_file = 'credentials/token_automatico.json'
        self.gc = None
    
    def gerar_access_token(self):
        """Gera access token automaticamente"""
        try:
            # Se já temos um token salvo, tenta usar
            if os.path.exists(self.token_file):
                with open(self.token_file, 'r') as f:
                    token_data = json.load(f)
                
                if 'refresh_token' in token_data:
                    # Usa refresh token para gerar novo access token
                    data = {
                        'client_id': self.client_id,
                        'client_secret': self.client_secret,
                        'refresh_token': token_data['refresh_token'],
                        'grant_type': 'refresh_token'
                    }
                    
                    response = requests.post('https://oauth2.googleapis.com/token', data=data)
                    
                    if response.status_code == 200:
                        new_token = response.json()
                        # Mantém refresh token
                        new_token['refresh_token'] = token_data['refresh_token']
                        
                        # Salva token atualizado
                        with open(self.token_file, 'w') as f:
                            json.dump(new_token, f, indent=2)
                        
                        print("✅ Token renovado automaticamente!")
                        return True
            
            # Se não tem token, precisa configurar uma vez
            print("❌ Token não encontrado")
            return False
            
        except Exception as e:
            print(f"❌ Erro ao gerar token: {str(e)}")
            return False
    
    def configurar_token_inicial(self, codigo_auth):
        """Configura token inicial com código de autorização"""
        try:
            print("🔄 Configurando token inicial...")
            
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': codigo_auth,
                'grant_type': 'authorization_code',
                'redirect_uri': 'http://localhost:8080'
            }
            
            response = requests.post('https://oauth2.googleapis.com/token', data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                
                # Salva token
                os.makedirs('credentials', exist_ok=True)
                with open(self.token_file, 'w') as f:
                    json.dump(token_data, f, indent=2)
                
                print("✅ Token inicial configurado!")
                print("🚀 Agora o sistema funcionará automaticamente!")
                return True
            else:
                print(f"❌ Erro ao configurar token: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            return False
    
    def conectar_automatico(self):
        """Conecta automaticamente usando token"""
        try:
            # Tenta gerar/renovar token
            if not self.gerar_access_token():
                return False
            
            # Carrega token
            with open(self.token_file, 'r') as f:
                token_data = json.load(f)
            
            # Cria credenciais
            creds = Credentials(
                token=token_data.get('access_token'),
                refresh_token=token_data.get('refresh_token'),
                token_uri='https://oauth2.googleapis.com/token',
                client_id=self.client_id,
                client_secret=self.client_secret,
                scopes=self.scopes
            )
            
            # Autoriza gspread
            self.gc = gspread.authorize(creds)
            print("✅ Conectado automaticamente!")
            return True
            
        except Exception as e:
            print(f"❌ Erro na conexão automática: {str(e)}")
            return False
    
    def testar_planilha(self, sheet_id="EXAMPLE_SHEET_ID"):
        """Testa acesso à planilha"""
        try:
            if not self.gc:
                print("❌ Não conectado")
                return False
            
            print(f"🧪 Testando planilha: {sheet_id}")
            
            # Abre planilha
            sheet = self.gc.open_by_key(sheet_id)
            worksheet = sheet.sheet1
            
            # Obtém dados
            records = worksheet.get_all_records()
            
            print(f"✅ Sucesso! {len(records)} registros encontrados")
            if records:
                print(f"📋 Colunas: {list(records[0].keys())}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no teste: {str(e)}")
            return False
    
    def get_client(self):
        """Retorna cliente gspread"""
        return self.gc
    
    def get_auth_url(self):
        """Retorna URL de autorização para configuração inicial"""
        url = (
            f"https://accounts.google.com/o/oauth2/auth?"
            f"client_id={self.client_id}&"
            f"redirect_uri=http://localhost:8080&"
            f"scope={'%20'.join(self.scopes)}&"
            f"response_type=code&"
            f"access_type=offline&"
            f"prompt=consent"
        )
        return url

def configurar_sistema():
    """Configura sistema automaticamente"""
    print("🔑 CONFIGURAÇÃO AUTOMÁTICA - SUAS CREDENCIAIS")
    print("=" * 60)
    print("📋 Client ID:", "*** Configure no arquivo .env ***")
    print("📋 Client Secret:", "*** Configure no arquivo .env ***")
    print()
    
    auth = AuthAutomatico()
    
    # Verifica se já está configurado
    if auth.conectar_automatico():
        print("🎉 Sistema já configurado!")
        
        # Testa planilha
        if auth.testar_planilha():
            print("✅ Planilha acessível!")
            print("🚀 Sistema pronto para uso!")
            return auth
        else:
            print("❌ Problema no acesso à planilha")
    else:
        print("❌ Sistema não configurado")
        print()
        print("📋 PARA CONFIGURAR (UMA VEZ APENAS):")
        print("1. Abra este link:")
        print(f"🔗 {auth.get_auth_url()}")
        print()
        print("2. Faça login e autorize")
        print("3. Copie o código")
        print("4. Execute:")
        print("   python -c \"")
        print("   from auth_automatico import AuthAutomatico")
        print("   auth = AuthAutomatico()")
        print("   auth.configurar_token_inicial('SEU_CODIGO_AQUI')\"")
    
    return None

if __name__ == "__main__":
    configurar_sistema()