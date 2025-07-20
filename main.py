#!/usr/bin/env python3
"""
Interface Final - Sistema NPS Simplificado
Autor: Claude Code
Data: 09/07/2025
"""

import sys
import os
from datetime import datetime
from nps_extractor import NPSExtractor
from calculadora_metricas import CalculadoraMetricas
from gerador_relatorio_pdf import GeradorRelatorioPDF


def exibir_menu():
    """Exibe o menu principal"""
    print("\n🚀 AGENTE ANALISTA DE DASHBOARD NPS")
    print("=" * 60)
    print("1. 📊 Gerar Relatório NPS")
    print("2. 📋 Instruções de Uso")
    print("3. 🔧 Testar Sistema")
    print("4. 🔐 Configurar Autenticação")
    print("5. 🔍 Testar Planilha Específica")
    print("6. 🚪 Sair")
    print("=" * 60)

def mostrar_instrucoes():
    """Mostra instruções de uso"""
    print("\n📋 INSTRUÇÕES DE USO")
    print("=" * 60)
    print("1. 🔗 Preparar planilha no Google Sheets:")
    print("   - Abra sua planilha no Google Sheets")
    print("   - Clique em 'Compartilhar' (botão azul)")
    print("   - Altere para 'Qualquer pessoa com o link'")
    print("   - Permissão: 'Visualizador'")
    print("   - Clique em 'Concluído'")
    print()
    print("2. 📊 Estrutura da planilha:")
    print("   - Data: Datas das avaliações")
    print("   - Nome: Nome do cliente")
    print("   - Loja: Nome da loja")
    print("   - Vendedor: Nome do vendedor")
    print("   - Avaliação: Nota de 0 a 10")
    print()
    print("3. 🎯 O sistema irá:")
    print("   - Conectar com a planilha")
    print("   - Extrair e processar os dados")
    print("   - Calcular métricas NPS")
    print("   - Gerar relatório PDF")
    print()
    print("4. 📄 Relatório gerado:")
    print("   - Arquivo: relatorio_nps_[LOJA]_[DATA].pdf")
    print("   - Local: pasta 'relatorios/'")
    print()
    input("Pressione Enter para voltar ao menu...")

def processar_relatorio():
    """Processa geração de relatório"""
    print("\n📊 GERAÇÃO DE RELATÓRIO NPS")
    print("=" * 60)
    
    try:
        # 1. Coleta informações
        print("\n📋 INFORMAÇÕES DA ANÁLISE")
        print("-" * 40)
        
        nome_loja = input("Nome da loja (ex: MDO Colombo): ").strip()
        if not nome_loja:
            nome_loja = "Sistema"
        
        url = input("URL do Google Sheets: ").strip()
        if not url:
            print("❌ URL não fornecida!")
            return False
        
        # 2. EXTRAIR DADOS
        print(f"\n🔍 PASSO 1: Extraindo dados de '{nome_loja}'...")
        extractor = NPSExtractor()
        
        if not extractor.conectar_sheets(url):
            print("❌ Falha na conexão com a planilha!")
            print("💡 Verifique se a planilha está pública (opção 2 do menu)")
            return False
        
        dados = extractor.extrair_avaliacoes()
        
        if dados is None or len(dados) == 0:
            print("❌ Nenhum dado válido encontrado!")
            print("💡 Verifique se a planilha tem as colunas corretas")
            print("📋 Colunas necessárias: Data, Nome, Loja, Vendedor, Avaliacao")
            return False
        
        print(f"✅ Dados extraídos: {len(dados)} registros")
        print(f"📋 Colunas encontradas: {list(dados.columns)}")
        
        # Verifica se tem coluna de avaliação
        if 'Avaliacao' not in dados.columns:
            print("⚠️ ATENÇÃO: Sem coluna de avaliação - relatório será limitado!")
            print("💡 Para relatório completo, adicione coluna 'Avaliacao' com notas 0-10")
        
        # Mostra amostra dos dados
        print("📊 Amostra dos dados:")
        print(dados.head(3).to_string())
        print()
        
        # 3. CALCULAR MÉTRICAS
        print(f"\n📊 PASSO 2: Calculando métricas para '{nome_loja}'...")
        calculadora = CalculadoraMetricas(dados)
        metricas = calculadora.calcular_todas_metricas()
        
        if not metricas:
            print("❌ Erro ao calcular métricas!")
            return False
        
        print("✅ Métricas calculadas com sucesso!")
        
        # 4. GERAR RELATÓRIO
        print(f"\n📄 PASSO 3: Gerando relatório para '{nome_loja}'...")
        
        gerador = GeradorRelatorioPDF(metricas)
        sucesso = gerador.gerar_relatorio_completo(nome_loja)
        
        if not sucesso:
            print("❌ Erro ao gerar relatório!")
            return False
        
        # 5. SALVAR ARQUIVO
        print(f"\n💾 PASSO 4: Salvando arquivo...")
        
        # Nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo = f"relatorio_nps_{nome_loja.replace(' ', '_')}_{timestamp}.pdf"
        
        caminho_arquivo = gerador.salvar_pdf(nome_arquivo)
        
        if caminho_arquivo:
            print(f"✅ Relatório salvo em: {caminho_arquivo}")
            
            # Exibe resumo
            resumo = calculadora.obter_resumo()
            print(f"\n🎯 RESUMO - {nome_loja}:")
            print(f"📊 {resumo['vendedores']} VENDEDORES | {resumo['avaliacoes']} AVALIAÇÕES | NOTA {resumo['nota_media']:.1f}")
            
            # Top 3 lojas
            if 'ranking_lojas' in metricas and metricas['ranking_lojas']:
                print(f"\n🏆 TOP 3 LOJAS:")
                for i, loja in enumerate(metricas['ranking_lojas'][:3], 1):
                    print(f"  {i}. {loja['loja']}: NPS {loja['nps_score']:.1f}")
            
            # Top 3 vendedores
            if 'ranking_vendedores' in metricas and metricas['ranking_vendedores']:
                print(f"\n👤 TOP 3 VENDEDORES:")
                for i, vendedor in enumerate(metricas['ranking_vendedores'][:3], 1):
                    print(f"  {i}. {vendedor['vendedor']}: NPS {vendedor['nps_score']:.1f}")
            
            # NPS Geral
            if 'percentuais_nps' in metricas:
                nps_geral = metricas['percentuais_nps'].get('nps_score', 0)
                print(f"\n📊 NPS GERAL: {nps_geral:.1f}")
            
            print(f"\n🎉 RELATÓRIO DE '{nome_loja}' CONCLUÍDO!")
            print(f"👆 Abra o arquivo {nome_arquivo} para ver o relatório PDF")
            
            return True
        else:
            print("❌ Erro ao salvar arquivo!")
            return False
            
    except KeyboardInterrupt:
        print("\n\n👋 Operação cancelada pelo usuário")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        return False

def executar_teste():
    """Executa teste do sistema"""
    print("\n🔧 TESTE DO SISTEMA")
    print("=" * 60)
    
    try:
        from teste_sistema_pdf import teste_sistema_pdf
        print("Executando teste com dados de exemplo...")
        sucesso = teste_sistema_pdf()
        
        if sucesso:
            print("\n✅ TESTE PASSOU!")
            print("💡 Sistema funcionando corretamente")
        else:
            print("\n❌ TESTE FALHOU!")
            print("💡 Verifique as dependências")
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
    
    # Verificar se é ambiente interativo antes de pedir entrada
    import sys
    if sys.stdin.isatty():
        input("\nPressione Enter para voltar ao menu...")

def configurar_autenticacao():
    """Menu de configuração de autenticação"""
    print("\n🔐 CONFIGURAÇÃO DE AUTENTICAÇÃO")
    print("=" * 60)
    print("1. 🔑 Configurar OAuth2 (Recomendado)")
    print("2. 🔐 Configurar Service Account")
    print("3. 📊 Verificar Status")
    print("4. 🔙 Voltar")
    print("=" * 60)
    
    opcao = input("\nEscolha uma opção (1-4): ").strip()
    
    if opcao == '1':
        configurar_oauth2()
    elif opcao == '2':
        configurar_service_account()
    elif opcao == '3':
        verificar_status_auth()
    elif opcao == '4':
        return
    else:
        print("❌ Opção inválida!")
    
    input("\nPressione Enter para continuar...")

def configurar_oauth2():
    """Configura OAuth2"""
    print("\n🔑 CONFIGURANDO OAUTH2")
    print("=" * 40)
    
    try:
        from oauth2_working import setup_oauth2_working
        print("📋 CONFIGURANDO COM SUAS CREDENCIAIS:")
        print("1. Usarei suas credenciais OAuth2 fornecidas")
        print("2. Você precisará autorizar uma única vez")
        print("3. Depois funcionará automaticamente")
        print()
        
        resposta = input("Configurar OAuth2 agora? (s/n): ").strip().lower()
        
        if resposta in ['s', 'sim', 'y', 'yes', '']:
            config = setup_oauth2_working()
            
            if config:
                print("✅ OAuth2 configurado com sucesso!")
                print("💡 Agora você pode acessar planilhas privadas!")
                print("🔄 Teste gerando um relatório!")
            else:
                print("❌ Erro na configuração OAuth2")
        else:
            print("⏭️ Configuração OAuth2 cancelada")
            print("💡 Configure quando precisar acessar planilhas privadas")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print("💡 Use Service Account como alternativa")

def configurar_service_account():
    """Configura Service Account"""
    print("\n🔐 CONFIGURANDO SERVICE ACCOUNT")
    print("=" * 40)
    
    try:
        from service_account_config import setup_service_account
        config = setup_service_account()
        
        if config:
            print("✅ Service Account configurado com sucesso!")
            print("💡 Agora você pode acessar planilhas privadas!")
        else:
            print("❌ Erro na configuração Service Account")
            print("💡 Veja as instruções em INSTRUCOES_SERVICE_ACCOUNT.md")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

def verificar_status_auth():
    """Verifica status da autenticação"""
    print("\n📊 STATUS DA AUTENTICAÇÃO")
    print("=" * 40)
    
    import os
    
    # Verifica OAuth2 Working (suas credenciais)
    if os.path.exists('credentials/oauth2_token_working.json'):
        print("✅ OAuth2 (suas credenciais): Configurado")
        print("  💡 Token salvo localmente")
        try:
            from oauth2_working import OAuth2Working
            config = OAuth2Working()
            creds = config.load_token()
            if creds and creds.valid:
                print("  ✅ Teste: Funcionando")
            else:
                print("  ⚠️ Teste: Token expirado ou inválido")
        except Exception as e:
            print(f"  ❌ Teste: Erro - {str(e)[:50]}...")
    else:
        print("❌ OAuth2 (suas credenciais): Não configurado")
    
    print()
    
    # Verifica OAuth2 padrão
    if os.path.exists('credentials/oauth2_token.pickle'):
        print("✅ OAuth2 padrão: Configurado")
        print("  💡 Token salvo localmente")
    else:
        print("❌ OAuth2 padrão: Não configurado")
    
    print()
    
    # Verifica Service Account
    if os.path.exists('credentials/service-account.json'):
        print("✅ Service Account: Configurado")
        try:
            from service_account_config import ServiceAccountConfig
            config = ServiceAccountConfig()
            if config.setup_credentials():
                print("  ✅ Teste: Funcionando")
            else:
                print("  ❌ Teste: Com problemas")
        except Exception as e:
            print(f"  ⚠️ Teste: Erro - {str(e)[:50]}...")
    else:
        print("❌ Service Account: Não configurado")
    
    print()
    
    # Teste de método público
    print("🌐 Método Público: Sempre disponível")
    print("  💡 Funciona apenas com planilhas públicas")
    
    print()
    print("💡 PRIORIDADE DE USO:")
    if os.path.exists('credentials/oauth2_token_working.json'):
        print("  1️⃣ OAuth2 (suas credenciais) - PRIORITÁRIO")
    if os.path.exists('credentials/oauth2_token.pickle'):
        print("  2️⃣ OAuth2 padrão")
    if os.path.exists('credentials/service-account.json'):
        print("  3️⃣ Service Account")
    print("  4️⃣ Método público (fallback)")
    
    print()
    print("🎯 RECOMENDAÇÃO:")
    if os.path.exists('credentials/oauth2_token_working.json'):
        print("  ✅ OAuth2 com suas credenciais está configurado!")
        print("  🚀 Sistema acessará planilhas privadas automaticamente")
    else:
        print("  💡 Configure OAuth2 com suas credenciais:")
        print("     → Opção 4 → Opção 1 (Configurar OAuth2)")
        print("     → Autorize uma única vez no navegador")
        print("     → Depois funcionará automaticamente")

def testar_planilha_especifica():
    """Testa uma planilha específica"""
    print("\n🔍 TESTAR PLANILHA ESPECÍFICA")
    print("=" * 60)
    
    # URL de exemplo para demonstração
    url_exemplo = "https://docs.google.com/spreadsheets/d/EXAMPLE_SHEET_ID/edit"
    
    print(f"URL de teste: {url_exemplo}")
    print()
    opcao = input("Usar esta URL? (s/n) ou cole uma nova URL: ").strip()
    
    if opcao.lower() in ['s', 'sim', 'yes', '']:
        url = url_exemplo
    elif opcao.startswith('http'):
        url = opcao
    else:
        url = input("Cole a URL da planilha: ").strip()
    
    if not url:
        print("❌ URL não fornecida!")
        return
    
    try:
        from testar_planilha import testar_planilha
        testar_planilha(url)
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
    
    input("\nPressione Enter para voltar ao menu...")

def main():
    """Interface principal do sistema"""
    print("🚀 AGENTE ANALISTA DE DASHBOARD NPS")
    print("Autor: Leonardo | Data: 2025")
    
    # Verificar se é ambiente não-interativo
    import sys
    if not sys.stdin.isatty():
        print("\n🔧 MODO AUTOMÁTICO DETECTADO - Executando teste do sistema...")
        try:
            executar_teste()
        except Exception as e:
            print(f"❌ Erro no teste automático: {str(e)}")
        return
    
    while True:
        try:
            exibir_menu()
            
            opcao = input("\nEscolha uma opção (1-6): ").strip()
            
            if opcao == '1':
                processar_relatorio()
                input("\nPressione Enter para voltar ao menu...")
            elif opcao == '2':
                mostrar_instrucoes()
            elif opcao == '3':
                executar_teste()
            elif opcao == '4':
                configurar_autenticacao()
            elif opcao == '5':
                testar_planilha_especifica()
            elif opcao == '6':
                print("\n👋 Saindo do sistema...")
                break
            else:
                print("❌ Opção inválida! Escolha 1, 2, 3, 4, 5 ou 6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saindo do sistema...")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")
            try:
                input("Pressione Enter para continuar...")
            except EOFError:
                print("\n👋 Saindo do sistema...")
                break


if __name__ == "__main__":
    main()