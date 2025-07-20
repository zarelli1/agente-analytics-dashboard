#!/usr/bin/env python3
"""
Servidor simples para o frontend DashBot Analytics
"""

import http.server
import socketserver
import webbrowser
import os
import json
from urllib.parse import urlparse, parse_qs
import subprocess
import sys

# Configurações
PORT = 8080
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))

class DashBotHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)
    
    def do_GET(self):
        """Processa requisições GET"""
        if self.path.startswith('/relatorios/'):
            # Servir PDFs da pasta relatorios - MELHORADO
            pdf_name = self.path[12:]  # Remove '/relatorios/'
            relatorios_dir = os.path.join(os.path.dirname(FRONTEND_DIR), 'relatorios')
            pdf_path = os.path.join(relatorios_dir, pdf_name)
            
            print(f"📁 Solicitação PDF: {pdf_name}")
            print(f"📂 Caminho: {pdf_path}")
            print(f"📋 Existe: {os.path.exists(pdf_path)}")
            
            if os.path.exists(pdf_path) and pdf_name.endswith('.pdf'):
                try:
                    # Obter tamanho do arquivo
                    file_size = os.path.getsize(pdf_path)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/pdf')
                    self.send_header('Content-Disposition', f'attachment; filename="{pdf_name}"')
                    self.send_header('Content-Length', str(file_size))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Cache-Control', 'no-cache')
                    self.end_headers()
                    
                    # Ler e enviar arquivo
                    with open(pdf_path, 'rb') as f:
                        self.wfile.write(f.read())
                    
                    print(f"✅ PDF enviado: {pdf_name} ({file_size} bytes)")
                    return
                    
                except Exception as e:
                    print(f"❌ Erro ao enviar PDF: {e}")
                    self.send_error(500, f'Erro ao enviar PDF: {str(e)}')
                    return
            else:
                print(f"❌ PDF não encontrado: {pdf_path}")
                self.send_error(404, 'PDF não encontrado')
                return
        else:
            # Requisições normais para arquivos estáticos
            super().do_GET()
    
    def do_POST(self):
        """Processa requisições POST para análise NPS"""
        if self.path == '/api/analyze':
            try:
                print("📨 REQUISIÇÃO RECEBIDA")
                
                # Ler dados da requisição
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                sheets_url = data.get('sheets_url', '')
                loja_nome = data.get('loja_nome', 'Sistema')
                
                print(f"📋 Dados recebidos: {data}")
                
                # Headers CORS
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                # Executar análise real
                print("🚀 Iniciando análise...")
                result = self.run_nps_analysis(sheets_url, loja_nome)
                
                # Retornar resultado
                response = json.dumps(result, ensure_ascii=False, indent=2)
                self.wfile.write(response.encode('utf-8'))
                self.wfile.flush()
                
                print("📤 RESPOSTA ENVIADA")
                
            except Exception as e:
                print(f"❌ ERRO NO SERVIDOR: {str(e)}")
                import traceback
                traceback.print_exc()
                
                try:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    error_response = json.dumps({
                        'success': False,
                        'error': f'Erro no servidor: {str(e)}'
                    })
                    self.wfile.write(error_response.encode('utf-8'))
                except:
                    pass
        
        elif self.path == '/api/analyze-multi':
            try:
                print("📨 REQUISIÇÃO MULTI-ABAS RECEBIDA")
                
                # Ler dados da requisição
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                sheets_url = data.get('sheets_url', '')
                loja_nome = data.get('loja_nome', 'Sistema')
                
                print(f"📋 Dados recebidos: {data}")
                
                # Headers CORS
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                # Executar análise multi-abas
                print("🚀 Iniciando análise multi-abas...")
                result = self.run_multi_sheet_analysis(sheets_url, loja_nome)
                
                # Retornar resultado
                response = json.dumps(result, ensure_ascii=False, indent=2)
                self.wfile.write(response.encode('utf-8'))
                self.wfile.flush()
                
                print("📤 RESPOSTA MULTI-ABAS ENVIADA")
                
            except Exception as e:
                print(f"❌ ERRO NO SERVIDOR MULTI-ABAS: {str(e)}")
                import traceback
                traceback.print_exc()
                
                try:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    
                    error_response = json.dumps({
                        'success': False,
                        'error': f'Erro no servidor: {str(e)}'
                    })
                    self.wfile.write(error_response.encode('utf-8'))
                except:
                    pass
        
        else:
            self.send_error(404, 'Endpoint não encontrado')
    
    def do_OPTIONS(self):
        """Permitir CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def run_nps_analysis(self, sheets_url, loja_nome):
        """Executa a análise NPS real usando o backend Python"""
        try:
            print(f"🚀 INICIANDO ANÁLISE NPS")
            print(f"🔗 URL: {sheets_url}")
            print(f"🏪 Loja: {loja_nome}")
            
            # Importar módulos do sistema NPS
            sys.path.append(os.path.dirname(FRONTEND_DIR))
            
            from nps_extractor import NPSExtractor
            from calculadora_metricas import CalculadoraMetricas
            from gerador_relatorio_pdf import GeradorRelatorioPDF
            from datetime import datetime
            
            # 1. Extrair dados
            print(f"🔍 PASSO 1: Conectando com planilha...")
            extractor = NPSExtractor()
            
            if not extractor.conectar_sheets(sheets_url):
                print("❌ Falha na conexão")
                return {
                    'success': False,
                    'error': 'Falha na conexão com a planilha. Verifique se está pública.'
                }
            
            print("✅ Conexão estabelecida!")
            dados = extractor.extrair_avaliacoes()
            
            if dados is None or len(dados) == 0:
                print("❌ Nenhum dado encontrado")
                return {
                    'success': False,
                    'error': 'Nenhum dado válido encontrado na planilha.'
                }
            
            print(f"✅ {len(dados)} registros extraídos")
            
            # 2. Calcular métricas
            print("📊 PASSO 2: Calculando métricas...")
            calculadora = CalculadoraMetricas(dados)
            metricas = calculadora.calcular_todas_metricas()
            
            if not metricas:
                print("❌ Erro no cálculo de métricas")
                return {
                    'success': False,
                    'error': 'Erro ao calcular métricas NPS.'
                }
            
            print("✅ Métricas calculadas!")
            
            # 3. Gerar PDF
            print("📄 PASSO 3: Gerando relatório PDF...")
            gerador = GeradorRelatorioPDF(metricas)
            sucesso = gerador.gerar_relatorio_completo(loja_nome)
            
            if not sucesso:
                print("❌ Erro na geração do PDF")
                return {
                    'success': False,
                    'error': 'Erro ao gerar relatório PDF.'
                }
            
            print("✅ PDF gerado!")
            
            # 4. Salvar arquivo
            print("💾 PASSO 4: Salvando arquivo...")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nome_arquivo = f"relatorio_nps_{loja_nome.replace(' ', '_')}_{timestamp}.pdf"
            caminho_arquivo = gerador.salvar_pdf(nome_arquivo)
            
            if not caminho_arquivo:
                print("❌ Erro ao salvar PDF")
                return {
                    'success': False,
                    'error': 'Erro ao salvar arquivo PDF.'
                }
            
            print(f"✅ Arquivo salvo: {nome_arquivo}")
            
            # 5. Preparar resposta
            resumo = calculadora.obter_resumo()
            nps_geral = metricas.get('percentuais_nps', {}).get('nps_score', 0)
            
            result = {
                'success': True,
                'metrics': {
                    'nps_score': round(nps_geral, 1),
                    'total_responses': resumo['avaliacoes'],
                    'avg_rating': round(resumo['nota_media'], 1),
                    'vendedores': resumo['vendedores']
                },
                'file_path': caminho_arquivo,
                'file_name': nome_arquivo,
                'rankings': {
                    'lojas': metricas.get('ranking_lojas', [])[:3],
                    'vendedores': metricas.get('ranking_vendedores', [])[:3]
                }
            }
            
            print("🎉 ANÁLISE CONCLUÍDA COM SUCESSO!")
            print(f"📊 NPS: {result['metrics']['nps_score']}")
            print(f"📋 Respostas: {result['metrics']['total_responses']}")
            print(f"⭐ Nota: {result['metrics']['avg_rating']}")
            
            return result
            
        except Exception as e:
            print(f"❌ ERRO CRÍTICO: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Erro interno: {str(e)}'
            }
    
    def run_multi_sheet_analysis(self, sheets_url, loja_nome):
        """Executa análise de múltiplas abas"""
        try:
            print(f"🚀 ANÁLISE MULTI-ABAS")
            print(f"🔗 URL: {sheets_url}")
            print(f"🏪 Loja: {loja_nome}")
            
            # Importar módulos necessários
            sys.path.append(os.path.dirname(FRONTEND_DIR))
            import re
            import pandas as pd
            import requests
            from calculadora_metricas import CalculadoraMetricas
            from gerador_relatorio_pdf import GeradorRelatorioPDF
            from datetime import datetime
            
            # Extrair ID da planilha
            sheet_id_match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheets_url)
            if not sheet_id_match:
                return {
                    'success': False,
                    'error': 'URL inválida da planilha'
                }
            
            sheet_id = sheet_id_match.group(1)
            print(f"📋 ID da planilha: {sheet_id}")
            
            # Listar abas disponíveis
            print("🔍 Procurando abas disponíveis...")
            abas_encontradas = []
            
            # Testa alguns GIDs comuns
            gids_teste = [0, 1202595829, 1, 2, 3, 4, 5]
            
            for gid in gids_teste:
                try:
                    url_teste = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"
                    response = requests.get(url_teste, timeout=10)
                    
                    if response.status_code == 200 and len(response.text) > 50:
                        dados = pd.read_csv(url_teste)
                        if not dados.empty:
                            abas_encontradas.append({
                                'gid': gid,
                                'url': url_teste,
                                'registros': len(dados),
                                'colunas': list(dados.columns)
                            })
                except:
                    continue
            
            if not abas_encontradas:
                return {
                    'success': False,
                    'error': 'Nenhuma aba encontrada ou planilha não pública'
                }
            
            print(f"✅ {len(abas_encontradas)} aba(s) encontrada(s)")
            
            # Processar cada aba
            resultados = []
            arquivos_gerados = []
            
            for aba in abas_encontradas:
                try:
                    print(f"📊 Processando aba GID {aba['gid']} - {aba['registros']} registros")
                    
                    # Lê dados da aba
                    dados = pd.read_csv(aba['url'])
                    
                    # Calcula métricas
                    calculadora = CalculadoraMetricas(dados)
                    metricas = calculadora.calcular_todas_metricas()
                    
                    # Gera relatório
                    gerador = GeradorRelatorioPDF(metricas)
                    sucesso = gerador.gerar_relatorio_completo(f"{loja_nome} - Aba {aba['gid']}")
                    
                    if sucesso:
                        # Salva PDF
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        nome_arquivo = f"relatorio_aba_{aba['gid']}_{timestamp}.pdf"
                        caminho_pdf = gerador.salvar_pdf(nome_arquivo)
                        
                        if caminho_pdf:
                            resumo = calculadora.obter_resumo()
                            nps_geral = metricas.get('percentuais_nps', {}).get('nps_score', 0)
                            
                            resultado_aba = {
                                'gid': aba['gid'],
                                'registros': len(dados),
                                'file_path': caminho_pdf,
                                'file_name': nome_arquivo,
                                'nps_score': round(nps_geral, 1),
                                'total_responses': resumo['avaliacoes'],
                                'avg_rating': round(resumo['nota_media'], 1)
                            }
                            
                            resultados.append(resultado_aba)
                            arquivos_gerados.append(nome_arquivo)
                            
                            print(f"✅ Aba {aba['gid']}: NPS {nps_geral:.1f}, {len(dados)} registros")
                        
                except Exception as e:
                    print(f"❌ Erro na aba {aba['gid']}: {e}")
                    continue
            
            if not resultados:
                return {
                    'success': False,
                    'error': 'Nenhuma aba pôde ser processada'
                }
            
            # Resultado final
            total_registros = sum(r['registros'] for r in resultados)
            nps_medio = sum(r['nps_score'] for r in resultados) / len(resultados)
            
            return {
                'success': True,
                'multi_sheet': True,
                'total_sheets': len(resultados),
                'total_records': total_registros,
                'avg_nps': round(nps_medio, 1),
                'sheets': resultados,
                'files': arquivos_gerados,
                'message': f'Análise concluída: {len(resultados)} abas processadas com {total_registros} registros'
            }
            
        except Exception as e:
            print(f"❌ ERRO CRÍTICO MULTI-ABAS: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': f'Erro interno: {str(e)}'
            }

def start_server():
    """Inicia o servidor web universal"""
    try:
        # Permite reutilizar a porta
        socketserver.TCPServer.allow_reuse_address = True
        
        with socketserver.TCPServer(("", PORT), DashBotHandler) as httpd:
            print("🚀 ANALYTICS UNIVERSAL - IA GPT-4o")
            print("=" * 60)
            print(f"📡 Servidor: http://localhost:{PORT}")
            print(f"🧠 IA: GPT-4o para análise universal")
            print(f"📊 Suporte: Qualquer planilha")
            print(f"🔗 API: /api/analyze")
            print("=" * 60)
            print("💡 Ctrl+C para parar")
            print()
            
            # Abrir navegador automaticamente
            try:
                webbrowser.open(f'http://localhost:{PORT}')
            except:
                print("🌐 Abra manualmente: http://localhost:8080")
            
            # Iniciar servidor
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n👋 Servidor parado")
    except OSError as e:
        if e.errno == 98:
            print(f"❌ Porta {PORT} ocupada. Execute:")
            print(f"   sudo lsof -ti:{PORT} | xargs kill -9")
        else:
            print(f"❌ Erro: {e}")
    except Exception as e:
        print(f"❌ Erro no servidor: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server()