#!/usr/bin/env python3
"""
Servidor Flask eficiente para automação universal
Solução robusta com melhor tratamento de erros
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
import threading
import webbrowser
from datetime import datetime

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)  # Permite CORS para todas as rotas

# Configurações
PORT = 8080
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(FRONTEND_DIR)

@app.route('/')
def index():
    """Serve a página principal"""
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """Serve arquivos estáticos"""
    return send_from_directory(FRONTEND_DIR, filename)

@app.route('/relatorios/<path:filename>')
def serve_reports(filename):
    """Serve relatórios PDF"""
    relatorios_dir = os.path.join(BASE_DIR, 'relatorios')
    return send_from_directory(relatorios_dir, filename)

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze_data():
    """Endpoint principal para análise universal - Suporte para upload e URLs"""
    
    if request.method == 'OPTIONS':
        # Resposta para preflight CORS
        return '', 200
    
    try:
        print("📨 NOVA REQUISIÇÃO DE ANÁLISE")
        
        # Verifica se é upload de arquivo ou URL
        if 'file' in request.files:
            # Upload de arquivo CSV
            result = handle_file_upload()
        else:
            # URL do Google Sheets (método original)
            result = handle_sheets_url()
        
        print("✅ ANÁLISE CONCLUÍDA")
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ ERRO NA API: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

def handle_file_upload():
    """Processa upload de arquivo CSV"""
    print("📤 Processando upload de arquivo...")
    
    file = request.files['file']
    if not file or file.filename == '':
        return {
            'success': False,
            'error': 'Nenhum arquivo selecionado'
        }
    
    # Parâmetros do formulário
    loja_nome = request.form.get('nome_loja', 'Upload Teste')
    usar_looker = request.form.get('usar_looker', 'false').lower() == 'true'
    gerar_ia = request.form.get('gerar_ia', 'false').lower() == 'true'
    estilo_pdf = request.form.get('estilo_pdf', 'moderno')  # NOVO: Estilo do PDF
    
    print(f"🏢 Loja: {loja_nome}")
    print(f"📊 Usar Looker: {usar_looker}")
    print(f"🤖 Gerar IA: {gerar_ia}")
    print(f"🎨 Estilo PDF: {estilo_pdf}")
    
    # Salva arquivo temporário
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+b', suffix='.csv', delete=False) as tmp:
        file.save(tmp.name)
        csv_path = tmp.name
    
    try:
        # Carrega dados do CSV
        import pandas as pd
        dados = pd.read_csv(csv_path, encoding='utf-8')
        print(f"✅ {len(dados)} registros carregados do CSV")
        print(f"📋 Colunas: {list(dados.columns)}")
        
        # Executar análise direta com PDF executivo simples
        from calculadora_metricas import CalculadoraMetricas
        from gerador_pdf_executivo_simples import GeradorPDFExecutivoSimples
        
        print("🧠 Calculando métricas dos dados...")
        calculadora = CalculadoraMetricas(dados)
        metricas = calculadora.calcular_todas_metricas()
        
        if not metricas:
            return {
                'success': False,
                'error': 'Erro ao calcular métricas dos dados.'
            }
        
        # Preparar dados para PDF executivo simples
        dados_pdf = {
            'nps_final': metricas.get('percentuais_nps', {}).get('nps_score', 0),
            'promotores_count': metricas.get('percentuais_nps', {}).get('promotores', 0),
            'neutros_count': metricas.get('percentuais_nps', {}).get('neutros', 0),
            'detratores_count': metricas.get('percentuais_nps', {}).get('detratores', 0),
            'total_avaliacoes': len(dados),
            'vendedores': metricas.get('analise_vendedores', [])
        }
        
        # Gerar PDF executivo simples
        gerador = GeradorPDFExecutivoSimples()
        caminho_arquivo = gerador.gerar_pdf_executivo_simples(dados_pdf, loja_nome)
        
        if not caminho_arquivo:
            return {
                'success': False,
                'error': 'Erro ao gerar relatório PDF.'
            }
        
        import os
        nome_arquivo = os.path.basename(caminho_arquivo)
        
        result = {
            'success': True,
            'message': 'Dashboard executivo concluído com sucesso!',
            'arquivo': nome_arquivo,
            'download_url': f'/relatorios/{nome_arquivo}',
            'dados': {
                'nps_score': dados_pdf['nps_final'],
                'total_registros': dados_pdf['total_avaliacoes']
            },
            'tipo_relatorio': 'PDF Executivo Simples'
        }
        
        # Remove arquivo temporário
        os.unlink(csv_path)
        
        return result
        
    except Exception as e:
        # Remove arquivo temporário em caso de erro
        if os.path.exists(csv_path):
            os.unlink(csv_path)
        raise e

def handle_sheets_url():
    """Processa URL do Google Sheets (método original)"""
    print("🔗 Processando URL do Google Sheets...")
    
    data = request.get_json()
    if not data:
        return {
            'success': False,
            'error': 'Dados não fornecidos'
        }
    
    sheets_url = data.get('sheets_url', '')
    loja_nome = data.get('loja_nome', 'Análise Universal')
    estilo_pdf = data.get('estilo_pdf', 'executivo_simples')  # Novo parâmetro
    
    print(f"🔗 URL: {sheets_url}")
    print(f"🏢 Projeto: {loja_nome}")
    print(f"🎨 Estilo PDF: {estilo_pdf}")
    
    if not sheets_url:
        return {
            'success': False,
            'error': 'URL da planilha é obrigatória'
        }
    
    # Executa análise original
    return run_analysis(sheets_url, loja_nome, estilo_pdf)

def run_analysis(sheets_url, loja_nome, estilo_pdf='executivo_simples'):
    """Executa análise e gera PDF executivo simples"""
    try:
        print(f"📊 INICIANDO DASHBOARD EXECUTIVO para: {loja_nome}")
        
        # Importa apenas o necessário
        from nps_extractor import NPSExtractor
        from calculadora_metricas import CalculadoraMetricas
        from gerador_pdf_executivo_simples import GeradorPDFExecutivoSimples
        
        # 1. EXTRAÇÃO DOS DADOS
        print("🔍 PASSO 1: Extraindo dados da planilha...")
        extractor = NPSExtractor()
        
        if not extractor.conectar_sheets(sheets_url):
            return {
                'success': False,
                'error': 'Não foi possível conectar com a planilha. Verifique se está pública.'
            }
        
        dados = extractor.extrair_avaliacoes()
        
        if dados is None or len(dados) == 0:
            return {
                'success': False,
                'error': 'Nenhum dado encontrado na planilha. Verifique se há dados válidos.'
            }
        
        print(f"✅ {len(dados)} registros extraídos")
        
        # 2. ANÁLISE DAS MÉTRICAS
        print("🧠 PASSO 2: Calculando métricas NPS...")
        calculadora = CalculadoraMetricas(dados)
        metricas = calculadora.calcular_todas_metricas()
        
        if not metricas:
            return {
                'success': False,
                'error': 'Erro ao calcular métricas dos dados.'
            }
        
        # 3. GERAÇÃO DO PDF EXECUTIVO SIMPLES
        print("📄 PASSO 3: Gerando relatório PDF executivo...")
        
        gerador = GeradorPDFExecutivoSimples()
        
        # Preparar dados para o PDF
        dados_pdf = {
            'nps_final': metricas.get('percentuais_nps', {}).get('nps_score', 0),
            'promotores_count': metricas.get('percentuais_nps', {}).get('promotores', 0),
            'neutros_count': metricas.get('percentuais_nps', {}).get('neutros', 0),
            'detratores_count': metricas.get('percentuais_nps', {}).get('detratores', 0),
            'total_avaliacoes': len(dados),
            'vendedores': metricas.get('analise_vendedores', [])
        }
        
        print(f"🎯 Métricas: NPS {dados_pdf['nps_final']}, {dados_pdf['total_avaliacoes']} avaliações")
        
        # Gerar PDF executivo simples
        caminho_arquivo = gerador.gerar_pdf_executivo_simples(dados_pdf, loja_nome)
        
        if not caminho_arquivo:
            return {
                'success': False,
                'error': 'Erro ao gerar relatório PDF.'
            }
        
        # Extrair apenas o nome do arquivo
        import os
        nome_arquivo = os.path.basename(caminho_arquivo)
        
        print(f"✅ PDF executivo gerado: {nome_arquivo}")
        
        # Retornar estrutura compatível com frontend
        return {
            'success': True,
            'message': 'Dashboard executivo concluído com sucesso!',
            'arquivo': nome_arquivo,
            'download_url': f'/relatorios/{nome_arquivo}',
            'dados': {
                'nps_score': dados_pdf['nps_final'],
                'total_registros': dados_pdf['total_avaliacoes'],
                'promotores_count': dados_pdf['promotores_count'],
                'neutros_count': dados_pdf['neutros_count'],
                'detratores_count': dados_pdf['detratores_count']
            },
            'tipo_relatorio': 'PDF Executivo Simples'
        }
        
    except Exception as e:
        print(f"❌ ERRO NO DASHBOARD: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'success': False,
            'error': f'Erro ao gerar dashboard: {str(e)}'
        }


def start_server():
    """Inicia o servidor Flask"""
    print("🚀 ANALYTICS UNIVERSAL - SERVIDOR FLASK")
    print("=" * 60)
    print(f"📡 Rodando em: http://localhost:{PORT}")
    print(f"🧠 IA: GPT-4o integrada")
    print(f"📊 Suporte: Qualquer planilha")
    print(f"🔗 API: /api/analyze")
    print("=" * 60)
    print("💡 Ctrl+C para parar")
    print()
    
    # Abre navegador em thread separada
    def open_browser():
        import time
        time.sleep(1)  # Aguarda servidor iniciar
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            print("🌐 Abra manualmente: http://localhost:8080")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Inicia servidor Flask
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)

if __name__ == "__main__":
    start_server()