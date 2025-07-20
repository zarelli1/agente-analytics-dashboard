#!/usr/bin/env python3
"""
NPS Extractor - Conecta e extrai dados do Google Sheets
Autor: Claude Code
Data: 09/07/2025
"""

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import requests
from urllib.parse import urlparse
import re
from datetime import datetime
import io
import os
from service_account_config import ServiceAccountConfig
try:
    from auth_automatico import AuthAutomatico
except ImportError:
    AuthAutomatico = None


class NPSExtractor:
    """Classe para extrair dados NPS do Google Sheets"""
    
    def __init__(self, auth_method='auto'):
        """Inicializa o extrator
        
        Args:
            auth_method: 'auto', 'service_account', 'oauth2', 'public'
        """
        self.gc = None
        self.dados = None
        self.auth_method = auth_method
        self.method_used = None
        
        # Configura autenticação
        if auth_method == 'auto':
            self._setup_auto_auth()
        elif auth_method == 'service_account':
            self._setup_service_account()
        elif auth_method == 'oauth2':
            self._setup_oauth2()
        
    def conectar_sheets(self, url):
        """
        Conecta com o Google Sheets usando Service Account ou método público
        
        Args:
            url: URL do Google Sheets
            
        Returns:
            bool: True se conectado com sucesso
        """
        try:
            print(f"🔗 Conectando com: {url}")
            
            # Usa método disponível
            if self.gc and self.method_used in ['service_account', 'oauth2']:
                return self._conectar_com_auth(url)
            
            # Fallback: método público
            return self._conectar_publico(url)
            
        except Exception as e:
            print(f"❌ Erro na conexão: {str(e)}")
            return False
    
    def _setup_auto_auth(self):
        """Configura autenticação automática (prioridade: Auth Automático > Service Account > Público)"""
        # Tenta Auth Automático primeiro (suas credenciais OAuth2)
        if os.path.exists('credentials/token_automatico.json'):
            if self._setup_auth_automatico():
                return
        
        # Depois Service Account
        if os.path.exists('credentials/service-account.json'):
            if self._setup_service_account():
                return
        
        # Fallback: método público
        print("⚠️ Usando método público (apenas planilhas públicas)")
        self.method_used = 'public'
    
    def _setup_service_account(self):
        """Configura Service Account"""
        try:
            if os.path.exists('credentials/service-account.json'):
                print("🔐 Configurando Service Account...")
                config = ServiceAccountConfig()
                if config.setup_credentials():
                    self.gc = config.get_client()
                    self.method_used = 'service_account'
                    print("✅ Service Account configurado!")
                    return True
                else:
                    print("⚠️ Erro na configuração Service Account")
            else:
                print("⚠️ Service Account não encontrado")
                
        except Exception as e:
            print(f"⚠️ Erro Service Account: {str(e)}")
        
        return False
    
    def _setup_auth_automatico(self):
        """Configura Auth Automático (suas credenciais automáticas)"""
        try:
            if AuthAutomatico is None:
                print("⚠️ Auth Automático não disponível")
                return False
                
            print("🔑 Configurando Auth Automático (suas credenciais)...")
            config = AuthAutomatico()
            
            if config.conectar_automatico():
                self.gc = config.get_client()
                self.method_used = 'auth_automatico'
                print("✅ Auth Automático configurado!")
                return True
            else:
                print("⚠️ Auth Automático não configurado")
                
        except Exception as e:
            print(f"⚠️ Erro Auth Automático: {str(e)}")
        
        return False
    
    def _conectar_com_auth(self, url):
        """Conecta usando autenticação e extrai TODOS os dados disponíveis"""
        try:
            method_name = self._get_method_name()
            print(f"🔐 Conectando com {method_name}...")
            
            # Extrai ID da planilha
            sheet_id = self._extrair_sheet_id(url)
            if not sheet_id:
                print("❌ ID da planilha não encontrado")
                return False
            
            # Abre planilha
            spreadsheet = self.gc.open_by_key(sheet_id)
            
            # Lista todas as abas disponíveis
            worksheets = spreadsheet.worksheets()
            print(f"📋 Encontradas {len(worksheets)} abas: {[ws.title for ws in worksheets]}")
            
            # Prioriza primeira aba ou aba com mais dados
            worksheet = self._selecionar_melhor_aba(worksheets)
            print(f"📊 Usando aba: '{worksheet.title}'")
            
            # Extração completa com múltiplos métodos
            dados_completos = self._extrair_dados_completos(worksheet)
            
            if dados_completos is None or len(dados_completos) == 0:
                print("❌ Nenhum dado válido encontrado")
                return False
            
            self.dados = dados_completos
            print(f"✅ {len(self.dados)} registros extraídos com {len(self.dados.columns)} colunas")
            print(f"📋 Colunas: {list(self.dados.columns)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro {self._get_method_name()}: {str(e)}")
            print("🔄 Tentando método público...")
            return self._conectar_publico(url)
    
    def _get_method_name(self):
        """Retorna nome do método de autenticação"""
        if self.method_used == 'service_account':
            return "Service Account"
        elif self.method_used == 'auth_automatico':
            return "OAuth2 (suas credenciais)"
        else:
            return "OAuth2"
    
    def _selecionar_melhor_aba(self, worksheets):
        """Seleciona a aba com mais dados relevantes"""
        melhor_aba = worksheets[0]  # Padrão: primeira aba
        maior_linhas = 0
        
        for ws in worksheets:
            try:
                # Conta linhas com dados (evita contar linhas vazias)
                valores = ws.get_all_values()
                linhas_com_dados = len([linha for linha in valores if any(cel.strip() for cel in linha)])
                
                print(f"📊 Aba '{ws.title}': {linhas_com_dados} linhas com dados")
                
                if linhas_com_dados > maior_linhas:
                    maior_linhas = linhas_com_dados
                    melhor_aba = ws
                    
            except Exception as e:
                print(f"⚠️ Erro ao analisar aba '{ws.title}': {str(e)}")
                continue
        
        return melhor_aba
    
    def _extrair_dados_completos(self, worksheet):
        """Extrai TODOS os dados usando múltiplos métodos"""
        try:
            # Método 1: get_all_records (preserva tipos)
            print("🔍 Tentando extração com get_all_records...")
            try:
                records = worksheet.get_all_records(empty_value='', head=1)
                if records:
                    df = pd.DataFrame(records)
                    print(f"✅ Método 1: {len(df)} registros extraídos")
                    return self._limpar_dados_completos(df)
            except Exception as e:
                print(f"⚠️ Método 1 falhou: {str(e)}")
            
            # Método 2: get_all_values (matriz bruta)
            print("🔍 Tentando extração com get_all_values...")
            try:
                valores = worksheet.get_all_values()
                if valores and len(valores) > 1:
                    # Primeira linha como cabeçalho
                    cabecalho = valores[0]
                    dados = valores[1:]
                    
                    # Remove linhas completamente vazias
                    dados_filtrados = [linha for linha in dados if any(cel.strip() for cel in linha)]
                    
                    df = pd.DataFrame(dados_filtrados, columns=cabecalho)
                    print(f"✅ Método 2: {len(df)} registros extraídos")
                    return self._limpar_dados_completos(df)
            except Exception as e:
                print(f"⚠️ Método 2 falhou: {str(e)}")
            
            # Método 3: Range específico (última tentativa)
            print("🔍 Tentando extração por range...")
            try:
                # Detecta range de dados
                range_dados = worksheet.get_all_values()
                if range_dados:
                    df = pd.DataFrame(range_dados[1:], columns=range_dados[0])
                    df = df.dropna(how='all')  # Remove linhas completamente vazias
                    print(f"✅ Método 3: {len(df)} registros extraídos")
                    return self._limpar_dados_completos(df)
            except Exception as e:
                print(f"⚠️ Método 3 falhou: {str(e)}")
            
            return None
            
        except Exception as e:
            print(f"❌ Erro na extração completa: {str(e)}")
            return None
    
    def _limpar_dados_completos(self, df):
        """Limpeza avançada mantendo TODOS os dados relevantes"""
        try:
            print(f"🧹 Limpando dados: {len(df)} registros, {len(df.columns)} colunas")
            
            # Remove apenas linhas completamente vazias
            df = df.dropna(how='all')
            
            # Normaliza nomes de colunas (remove caracteres especiais)
            df.columns = df.columns.str.strip()
            df.columns = df.columns.str.replace('\n', ' ')
            df.columns = df.columns.str.replace('\r', ' ')
            
            # EXTRAÇÃO UNIVERSAL - Mantém TODAS as colunas de QUALQUER planilha
            colunas_corrigidas = {}
            for col in df.columns:
                col_limpa = col.strip()
                
                # Remove apenas caracteres que causam problemas técnicos
                col_limpa = col_limpa.replace('\n', ' ')
                col_limpa = col_limpa.replace('\r', ' ')
                col_limpa = col_limpa.replace('\t', ' ')
                
                # Corrige apenas encoding comum (mantém nomes originais)
                col_limpa = col_limpa.replace('AvaliaÃ§Ã£o', 'Avaliação')
                col_limpa = col_limpa.replace('ComentÃ¡rio', 'Comentário')
                col_limpa = col_limpa.replace('SituaÃ§Ã£o', 'Situação')
                col_limpa = col_limpa.replace('ResouÃ§Ã£o', 'Resolução')
                col_limpa = col_limpa.replace('InformaÃ§Ã£o', 'Informação')
                col_limpa = col_limpa.replace('DescriÃ§Ã£o', 'Descrição')
                
                # Remove espaços extras mas MANTÉM o nome original
                col_limpa = ' '.join(col_limpa.split())
                
                colunas_corrigidas[col] = col_limpa
            
            df = df.rename(columns=colunas_corrigidas)
            
            # Converte datas automaticamente
            for col in df.columns:
                if any(palavra in col.lower() for palavra in ['data', 'date', 'timestamp', 'hora']):
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    except:
                        pass
            
            # Limpa espaços em strings
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
                # Remove linhas onde a coluna principal está vazia
                if col.lower() in ['nome', 'cliente', 'vendedor']:
                    df = df[df[col] != '']
            
            print(f"✅ Dados limpos: {len(df)} registros válidos")
            return df
            
        except Exception as e:
            print(f"❌ Erro na limpeza: {str(e)}")
            return df  # Retorna dados originais se limpeza falhar
    
    def _conectar_publico(self, url):
        """Conecta usando método público com extração robusta"""
        try:
            print("🌐 Conectando com método público...")
            
            # Extrai ID da planilha
            sheet_id = self._extrair_sheet_id(url)
            if not sheet_id:
                print("❌ Erro: ID da planilha não encontrado")
                return False
            
            # Tenta múltiplos formatos de export
            formatos = [
                ('CSV', f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"),
                ('TSV', f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=tsv"),
                ('CSV com gid=0', f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0")
            ]
            
            for formato, export_url in formatos:
                try:
                    print(f"🔍 Tentando formato {formato}...")
                    
                    response = requests.get(export_url, timeout=30)
                    
                    if response.status_code == 200 and response.text.strip():
                        print(f"✅ Dados obtidos via {formato}")
                        
                        # Detecta separador
                        separador = ',' if formato.startswith('CSV') else '\t'
                        
                        # Múltiplos encodings
                        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                        
                        for encoding in encodings:
                            try:
                                # Decodifica com encoding específico
                                texto_decodificado = response.content.decode(encoding)
                                
                                # Carrega dados
                                self.dados = pd.read_csv(
                                    io.StringIO(texto_decodificado), 
                                    sep=separador,
                                    encoding=None,  # Já decodificado
                                    na_values=['', 'NA', 'N/A', 'null', 'NULL'],
                                    keep_default_na=True,
                                    dtype=str  # Mantém como string para preservar dados
                                )
                                
                                # Aplica limpeza robusta
                                self.dados = self._limpar_dados_completos(self.dados)
                                
                                if len(self.dados) > 0:
                                    print(f"✅ {len(self.dados)} registros extraídos via método público")
                                    print(f"📋 Colunas encontradas: {list(self.dados.columns)}")
                                    return True
                                    
                            except Exception as e:
                                print(f"⚠️ Encoding {encoding} falhou: {str(e)[:50]}...")
                                continue
                        
                    else:
                        print(f"⚠️ {formato} retornou código {response.status_code}")
                        
                except Exception as e:
                    print(f"⚠️ Erro em {formato}: {str(e)[:50]}...")
                    continue
            
            print("❌ Todos os métodos públicos falharam")
            print("💡 Verifique se a planilha está pública e tente OAuth2")
            return False
                
        except Exception as e:
            print(f"❌ Erro crítico na conexão pública: {str(e)}")
            return False
    
    def extrair_avaliacoes(self):
        """
        Extrai TODOS os dados para análise completa de pós-venda
        
        Returns:
            pandas.DataFrame: Todos os dados para análise IA
        """
        if self.dados is None:
            print("❌ Erro: Dados não carregados")
            return None
        
        try:
            print("🔍 Extraindo TODOS os dados para análise pós-venda...")
            
            # Retorna TODOS os dados sem filtros para análise completa
            dados_completos = self.dados.copy()
            
            # Apenas limpeza básica de dados
            dados_completos = self._limpar_dados_basicos(dados_completos)
            
            print(f"✅ {len(dados_completos)} registros completos extraídos")
            print(f"📋 Todas as colunas: {list(dados_completos.columns)}")
            
            return dados_completos
            
        except Exception as e:
            print(f"❌ Erro na extração: {str(e)}")
            return None
    
    def _limpar_dados_basicos(self, df):
        """Limpeza básica dos dados mantendo todas as informações"""
        try:
            # Remove linhas completamente vazias
            df = df.dropna(how='all')
            
            # Converte datas se existir coluna de data
            colunas_data = [col for col in df.columns if any(palavra in col.lower() for palavra in ['data', 'date', 'timestamp'])]
            for col in colunas_data:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except:
                    pass
            
            # Limpa espaços em branco
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str).str.strip()
            
            return df
            
        except Exception as e:
            print(f"⚠️ Erro na limpeza básica: {str(e)}")
            return df
    
    def _extrair_sheet_id(self, url):
        """Extrai ID da planilha da URL"""
        try:
            pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
            match = re.search(pattern, url)
            return match.group(1) if match else None
        except:
            return None
    
    def _detectar_colunas(self):
        """Detecta colunas automaticamente"""
        colunas = {}
        
        print("🔍 Detectando colunas automaticamente...")
        print(f"📋 Colunas disponíveis: {list(self.dados.columns)}")
        
        # Padrões para cada tipo de coluna
        padroes = {
            'data': ['data', 'date', 'timestamp', 'created', 'hora', 'time'],
            'nome': ['nome', 'name', 'client', 'customer', 'cliente'],
            'loja': ['loja', 'store', 'unidade', 'filial', 'shop'],
            'vendedor': ['vendedor', 'atendente', 'funcionario', 'staff', 'seller', 'funcionário'],
            'avaliacao': ['avaliacao', 'avaliação', 'nota', 'score', 'rating', 'nps', 'nota_nps', 'grade'],
            'classificacao': ['classificacao', 'classificação', 'category', 'tipo', 'class']
        }
        
        # Busca colunas
        for tipo, palavras in padroes.items():
            for coluna in self.dados.columns:
                coluna_lower = coluna.lower().strip()
                for palavra in palavras:
                    if palavra in coluna_lower:
                        colunas[tipo] = coluna
                        print(f"   ✅ {tipo.upper()}: {coluna}")
                        break
                if tipo in colunas:
                    break
            
            if tipo not in colunas:
                print(f"   ❌ {tipo.upper()}: Não encontrada")
        
        # Verifica se tem pelo menos avaliação
        if 'avaliacao' not in colunas:
            print("⚠️ ATENÇÃO: Coluna de avaliação não encontrada!")
            print("💡 Certifique-se que sua planilha tem uma coluna com notas (0-10)")
            print("📋 Nomes aceitos: avaliacao, avaliação, nota, score, rating, nps")
        
        return colunas
    
    def _limpar_dados(self, df):
        """Limpa e valida dados"""
        try:
            # Remove linhas vazias
            df = df.dropna(how='all')
            
            # Se tem coluna Avaliacao, converte para numérico
            if 'Avaliacao' in df.columns:
                df['Avaliacao'] = pd.to_numeric(df['Avaliacao'], errors='coerce')
                # Filtra apenas notas válidas (0-10)
                df = df[(df['Avaliacao'] >= 0) & (df['Avaliacao'] <= 10)]
            
            # Converte Data se existe
            if 'Data' in df.columns:
                df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            
            # Remove linhas com dados críticos faltando
            if 'Avaliacao' in df.columns:
                df = df.dropna(subset=['Avaliacao'])
            
            return df
            
        except Exception as e:
            print(f"⚠️ Erro na limpeza: {str(e)}")
            return df


def main():
    """Função principal para teste"""
    extractor = NPSExtractor()
    
    # URL de teste
    url = input("Digite a URL do Google Sheets: ")
    
    # Conecta
    if extractor.conectar_sheets(url):
        # Extrai dados
        dados = extractor.extrair_avaliacoes()
        
        if dados is not None:
            print(f"\n📊 RESUMO DOS DADOS:")
            print(f"Total de registros: {len(dados)}")
            print(f"Colunas disponíveis: {list(dados.columns)}")
            
            if 'Avaliacao' in dados.columns:
                print(f"Avaliações válidas: {dados['Avaliacao'].count()}")
                print(f"Nota média: {dados['Avaliacao'].mean():.2f}")
            
            # Salva amostra
            dados.head(10).to_csv('amostra_dados.csv', index=False)
            print(f"✅ Amostra salva em: amostra_dados.csv")
        else:
            print("❌ Falha ao extrair dados")
    else:
        print("❌ Falha na conexão")


if __name__ == "__main__":
    main()