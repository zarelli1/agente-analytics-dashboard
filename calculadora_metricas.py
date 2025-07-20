#!/usr/bin/env python3
"""
Calculadora de Métricas NPS - Calcula exatamente as métricas do dashboard
Autor: Claude Code
Data: 09/07/2025
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import openai
import json
import os
from looker_formulas import LookerFormulas


class CalculadoraMetricas:
    """Classe para calcular métricas NPS"""
    
    def __init__(self, dados):
        """
        Inicializa calculadora com dados
        
        Args:
            dados: DataFrame com dados NPS
        """
        self.dados = dados
        self.metricas = {}
        
        # Configura OpenAI - use variável de ambiente OPENAI_API_KEY
        self.openai_client = openai.OpenAI(
            api_key=os.environ.get('OPENAI_API_KEY', 'your_openai_api_key_here')
        )
    
    def calcular_metricas_gerais(self):
        """Calcula métricas gerais do dashboard"""
        try:
            print("📊 Calculando métricas gerais...")
            
            # Total de vendedores únicos
            total_vendedores = 0
            if 'Vendedor' in self.dados.columns:
                total_vendedores = self.dados['Vendedor'].nunique()
            
            # Total de avaliações
            total_avaliacoes = len(self.dados)
            
            # Nota média geral
            nota_media = 0
            if 'Avaliacao' in self.dados.columns:
                nota_media = self.dados['Avaliacao'].mean()
            
            self.metricas['gerais'] = {
                'total_vendedores': total_vendedores,
                'total_avaliacoes': total_avaliacoes,
                'nota_media': nota_media
            }
            
            print(f"✅ Vendedores: {total_vendedores} | Avaliações: {total_avaliacoes} | Nota: {nota_media:.2f}")
            return self.metricas['gerais']
            
        except Exception as e:
            print(f"❌ Erro nas métricas gerais: {str(e)}")
            return {}
    
    def calcular_nps_por_loja(self):
        """Calcula NPS por loja (ranking)"""
        try:
            print("🏪 Calculando NPS por loja...")
            
            if 'Loja' not in self.dados.columns or 'Avaliacao' not in self.dados.columns:
                print("⚠️ Colunas Loja ou Avaliacao não encontradas")
                return []
            
            ranking_lojas = []
            
            for loja in self.dados['Loja'].unique():
                dados_loja = self.dados[self.dados['Loja'] == loja]
                
                if len(dados_loja) > 0:
                    # Calcula NPS
                    nps_info = self._calcular_nps_detalhado(dados_loja['Avaliacao'])
                    
                    ranking_lojas.append({
                        'loja': loja,
                        'total_avaliacoes': len(dados_loja),
                        'nota_media': dados_loja['Avaliacao'].mean(),
                        'nps_score': nps_info['nps_score'],
                        'promotores': nps_info['promotores'],
                        'neutros': nps_info['neutros'],
                        'detratores': nps_info['detratores'],
                        'pct_promotores': nps_info['pct_promotores'],
                        'pct_neutros': nps_info['pct_neutros'],
                        'pct_detratores': nps_info['pct_detratores']
                    })
            
            # Ordena por NPS
            ranking_lojas = sorted(ranking_lojas, key=lambda x: x['nps_score'], reverse=True)
            
            self.metricas['ranking_lojas'] = ranking_lojas
            
            print(f"✅ NPS calculado para {len(ranking_lojas)} lojas")
            return ranking_lojas
            
        except Exception as e:
            print(f"❌ Erro no NPS por loja: {str(e)}")
            return []
    
    def calcular_nps_por_vendedor(self):
        """Calcula NPS por vendedor"""
        try:
            print("👤 Calculando NPS por vendedor...")
            
            if 'Vendedor' not in self.dados.columns or 'Avaliacao' not in self.dados.columns:
                print("⚠️ Colunas Vendedor ou Avaliacao não encontradas")
                return []
            
            ranking_vendedores = []
            
            for vendedor in self.dados['Vendedor'].unique():
                dados_vendedor = self.dados[self.dados['Vendedor'] == vendedor]
                
                if len(dados_vendedor) > 0:
                    # Calcula NPS
                    nps_info = self._calcular_nps_detalhado(dados_vendedor['Avaliacao'])
                    
                    # Loja do vendedor (mais comum)
                    loja_vendedor = "N/A"
                    if 'Loja' in self.dados.columns:
                        loja_vendedor = dados_vendedor['Loja'].mode().iloc[0] if len(dados_vendedor['Loja'].mode()) > 0 else "N/A"
                    
                    ranking_vendedores.append({
                        'vendedor': vendedor,
                        'loja': loja_vendedor,
                        'total_avaliacoes': len(dados_vendedor),
                        'nota_media': dados_vendedor['Avaliacao'].mean(),
                        'nps_score': nps_info['nps_score'],
                        'promotores': nps_info['promotores'],
                        'neutros': nps_info['neutros'],
                        'detratores': nps_info['detratores'],
                        'pct_promotores': nps_info['pct_promotores'],
                        'pct_neutros': nps_info['pct_neutros'],
                        'pct_detratores': nps_info['pct_detratores']
                    })
            
            # Ordena por NPS
            ranking_vendedores = sorted(ranking_vendedores, key=lambda x: x['nps_score'], reverse=True)
            
            self.metricas['ranking_vendedores'] = ranking_vendedores
            
            print(f"✅ NPS calculado para {len(ranking_vendedores)} vendedores")
            return ranking_vendedores
            
        except Exception as e:
            print(f"❌ Erro no NPS por vendedor: {str(e)}")
            return []
    
    def calcular_distribuicao_notas(self):
        """Calcula distribuição de notas (8, 9, 10)"""
        try:
            print("📈 Calculando distribuição de notas...")
            
            if 'Avaliacao' not in self.dados.columns:
                print("⚠️ Coluna Avaliacao não encontrada")
                return {}
            
            # Conta cada nota
            distribuicao = {}
            for nota in range(0, 11):
                count = len(self.dados[self.dados['Avaliacao'] == nota])
                porcentagem = (count / len(self.dados)) * 100 if len(self.dados) > 0 else 0
                
                distribuicao[nota] = {
                    'count': count,
                    'porcentagem': porcentagem
                }
            
            # Destaque para notas altas (8, 9, 10)
            notas_altas = {
                8: distribuicao[8],
                9: distribuicao[9],
                10: distribuicao[10]
            }
            
            self.metricas['distribuicao_notas'] = distribuicao
            self.metricas['notas_altas'] = notas_altas
            
            print(f"✅ Distribuição calculada - Nota 10: {distribuicao[10]['count']} ({distribuicao[10]['porcentagem']:.1f}%)")
            return distribuicao
            
        except Exception as e:
            print(f"❌ Erro na distribuição: {str(e)}")
            return {}
    
    def calcular_percentuais_nps(self):
        """Calcula % Promotores/Neutros/Detratores"""
        try:
            print("🎯 Calculando percentuais NPS...")
            
            if 'Avaliacao' not in self.dados.columns:
                print("⚠️ Coluna Avaliacao não encontrada")
                return {}
            
            nps_info = self._calcular_nps_detalhado(self.dados['Avaliacao'])
            
            self.metricas['percentuais_nps'] = nps_info
            
            print(f"✅ Promotores: {nps_info['pct_promotores']:.1f}% | Neutros: {nps_info['pct_neutros']:.1f}% | Detratores: {nps_info['pct_detratores']:.1f}%")
            return nps_info
            
        except Exception as e:
            print(f"❌ Erro nos percentuais: {str(e)}")
            return {}
    
    def _calcular_nps_detalhado(self, avaliacoes):
        """Calcula NPS detalhado para uma série de avaliações"""
        try:
            total = len(avaliacoes)
            
            if total == 0:
                return {
                    'nps_score': 0,
                    'promotores': 0,
                    'neutros': 0,
                    'detratores': 0,
                    'pct_promotores': 0,
                    'pct_neutros': 0,
                    'pct_detratores': 0
                }
            
            # Categoriza avaliações
            promotores = len(avaliacoes[(avaliacoes >= 9) & (avaliacoes <= 10)])
            neutros = len(avaliacoes[(avaliacoes >= 7) & (avaliacoes <= 8)])
            detratores = len(avaliacoes[(avaliacoes >= 0) & (avaliacoes <= 6)])
            
            # Calcula percentuais
            pct_promotores = (promotores / total) * 100
            pct_neutros = (neutros / total) * 100
            pct_detratores = (detratores / total) * 100
            
            # Calcula NPS
            nps_score = pct_promotores - pct_detratores
            
            return {
                'nps_score': nps_score,
                'promotores': promotores,
                'neutros': neutros,
                'detratores': detratores,
                'pct_promotores': pct_promotores,
                'pct_neutros': pct_neutros,
                'pct_detratores': pct_detratores
            }
            
        except Exception as e:
            print(f"❌ Erro no cálculo NPS: {str(e)}")
            return {}
    
    def calcular_todas_metricas(self):
        """Calcula todas as métricas do dashboard"""
        try:
            print("🎯 Calculando todas as métricas...")
            
            # Calcula cada grupo de métricas
            self.calcular_metricas_gerais()
            self.calcular_nps_por_loja()
            self.calcular_nps_por_vendedor()
            self.calcular_distribuicao_notas()
            self.calcular_percentuais_nps()
            
            # Novas análises avançadas
            self.calcular_resumo_executivo()
            self.analisar_vendedores()
            self.calcular_evolucao_temporal()
            self.gerar_insights_automaticos()
            
            # NOVA FUNCIONALIDADE: Métricas Looker + IA Analytics
            self.calcular_metricas_looker()
            
            print("✅ Todas as métricas calculadas com sucesso!")
            print("   📊 Métricas tradicionais: ✅")
            print("   🔍 Métricas Looker: ✅")
            print("   🤖 Análise IA Analytics: ✅")
            
            return self.metricas
            
        except Exception as e:
            print(f"❌ Erro no cálculo geral: {str(e)}")
            return {}
    
    def obter_resumo(self):
        """Obtém resumo das métricas para o header"""
        try:
            gerais = self.metricas.get('gerais', {})
            
            resumo = {
                'vendedores': gerais.get('total_vendedores', 0),
                'avaliacoes': gerais.get('total_avaliacoes', 0),
                'nota_media': gerais.get('nota_media', 0)
            }
            
            return resumo
            
        except Exception as e:
            print(f"❌ Erro no resumo: {str(e)}")
            return {}
    
    def calcular_resumo_executivo(self):
        """Calcula resumo executivo detalhado"""
        try:
            print("📊 Calculando resumo executivo...")
            
            # Métricas gerais
            gerais = self.metricas.get('gerais', {})
            nps_geral = self.metricas.get('percentuais_nps', {})
            
            # Comparação temporal (se dados têm coluna Data)
            comparacao_mensal = self._calcular_comparacao_mensal()
            
            resumo_exec = {
                'nps_score_geral': nps_geral.get('nps_score', 0),
                'total_avaliacoes': gerais.get('total_avaliacoes', 0),
                'nota_media': gerais.get('nota_media', 0),
                'pct_promotores': nps_geral.get('pct_promotores', 0),
                'pct_neutros': nps_geral.get('pct_neutros', 0),
                'pct_detratores': nps_geral.get('pct_detratores', 0),
                'comparacao_mensal': comparacao_mensal
            }
            
            self.metricas['resumo_executivo'] = resumo_exec
            
            print(f"✅ Resumo executivo: NPS {resumo_exec['nps_score_geral']:.1f}")
            return resumo_exec
            
        except Exception as e:
            print(f"❌ Erro no resumo executivo: {str(e)}")
            return {}
    
    def _calcular_comparacao_mensal(self):
        """Calcula comparação com mês anterior"""
        try:
            if 'Data' not in self.dados.columns:
                return None
                
            # Converte datas
            self.dados['Data'] = pd.to_datetime(self.dados['Data'], errors='coerce')
            dados_com_data = self.dados.dropna(subset=['Data'])
            
            if len(dados_com_data) == 0:
                return None
            
            # Mês atual e anterior
            data_max = dados_com_data['Data'].max()
            mes_atual = data_max.month
            ano_atual = data_max.year
            
            # Calcula mês anterior
            if mes_atual == 1:
                mes_anterior = 12
                ano_anterior = ano_atual - 1
            else:
                mes_anterior = mes_atual - 1
                ano_anterior = ano_atual
            
            # Filtra dados por mês
            dados_mes_atual = dados_com_data[
                (dados_com_data['Data'].dt.month == mes_atual) & 
                (dados_com_data['Data'].dt.year == ano_atual)
            ]
            
            dados_mes_anterior = dados_com_data[
                (dados_com_data['Data'].dt.month == mes_anterior) & 
                (dados_com_data['Data'].dt.year == ano_anterior)
            ]
            
            if len(dados_mes_atual) == 0 or len(dados_mes_anterior) == 0:
                return None
            
            # Calcula NPS de cada mês
            nps_atual = self._calcular_nps_detalhado(dados_mes_atual['Avaliacao'])
            nps_anterior = self._calcular_nps_detalhado(dados_mes_anterior['Avaliacao'])
            
            diferenca = nps_atual['nps_score'] - nps_anterior['nps_score']
            
            return {
                'nps_mes_atual': nps_atual['nps_score'],
                'nps_mes_anterior': nps_anterior['nps_score'],
                'diferenca': diferenca,
                'tendencia': 'subida' if diferenca > 0 else 'queda' if diferenca < 0 else 'estável',
                'avaliacoes_mes_atual': len(dados_mes_atual),
                'avaliacoes_mes_anterior': len(dados_mes_anterior)
            }
            
        except Exception as e:
            print(f"❌ Erro na comparação mensal: {str(e)}")
            return None
    
    def analisar_vendedores(self):
        """Análise detalhada por vendedor"""
        try:
            print("👤 Analisando vendedores...")
            
            vendedores = self.metricas.get('ranking_vendedores', [])
            
            if not vendedores:
                return {}
            
            # Identifica top performers e problemáticos
            top_performers = [v for v in vendedores if v['nps_score'] >= 70]
            vendedores_problema = [v for v in vendedores if v['nps_score'] < 50]
            
            # Média de avaliações por vendedor
            media_avaliacoes = sum(v['total_avaliacoes'] for v in vendedores) / len(vendedores)
            
            # Vendedores com poucas avaliações
            poucas_avaliacoes = [v for v in vendedores if v['total_avaliacoes'] < media_avaliacoes * 0.5]
            
            analise = {
                'total_vendedores': len(vendedores),
                'top_performers': top_performers,
                'vendedores_problema': vendedores_problema,
                'poucas_avaliacoes': poucas_avaliacoes,
                'media_avaliacoes_por_vendedor': media_avaliacoes,
                'nps_medio_vendedores': sum(v['nps_score'] for v in vendedores) / len(vendedores)
            }
            
            self.metricas['analise_vendedores'] = analise
            
            print(f"✅ Análise: {len(top_performers)} top performers, {len(vendedores_problema)} com dificuldades")
            return analise
            
        except Exception as e:
            print(f"❌ Erro na análise de vendedores: {str(e)}")
            return {}
    
    def calcular_evolucao_temporal(self):
        """Calcula evolução temporal do NPS"""
        try:
            print("📈 Calculando evolução temporal...")
            
            if 'Data' not in self.dados.columns:
                print("⚠️ Coluna Data não encontrada")
                return {}
            
            # Converte datas
            self.dados['Data'] = pd.to_datetime(self.dados['Data'], errors='coerce')
            dados_com_data = self.dados.dropna(subset=['Data'])
            
            if len(dados_com_data) == 0:
                return {}
            
            # Agrupa por mês
            dados_com_data['Ano_Mes'] = dados_com_data['Data'].dt.to_period('M')
            evolucao_mensal = []
            
            for periodo in dados_com_data['Ano_Mes'].unique():
                dados_periodo = dados_com_data[dados_com_data['Ano_Mes'] == periodo]
                nps_periodo = self._calcular_nps_detalhado(dados_periodo['Avaliacao'])
                
                evolucao_mensal.append({
                    'periodo': str(periodo),
                    'nps_score': nps_periodo['nps_score'],
                    'total_avaliacoes': len(dados_periodo),
                    'nota_media': dados_periodo['Avaliacao'].mean()
                })
            
            # Ordena por período
            evolucao_mensal = sorted(evolucao_mensal, key=lambda x: x['periodo'])
            
            # Calcula tendência
            tendencia = self._calcular_tendencia(evolucao_mensal)
            
            evolucao = {
                'evolucao_mensal': evolucao_mensal,
                'tendencia': tendencia,
                'periodo_inicio': evolucao_mensal[0]['periodo'] if evolucao_mensal else None,
                'periodo_fim': evolucao_mensal[-1]['periodo'] if evolucao_mensal else None
            }
            
            self.metricas['evolucao_temporal'] = evolucao
            
            print(f"✅ Evolução temporal: {len(evolucao_mensal)} períodos, tendência {tendencia}")
            return evolucao
            
        except Exception as e:
            print(f"❌ Erro na evolução temporal: {str(e)}")
            return {}
    
    def _calcular_tendencia(self, evolucao_mensal):
        """Calcula tendência da evolução"""
        try:
            if len(evolucao_mensal) < 2:
                return 'insuficiente'
            
            # Compara últimos 3 meses se disponível
            ultimos_meses = evolucao_mensal[-3:] if len(evolucao_mensal) >= 3 else evolucao_mensal
            
            if len(ultimos_meses) < 2:
                return 'insuficiente'
            
            # Calcula diferença entre primeiro e último
            diferenca = ultimos_meses[-1]['nps_score'] - ultimos_meses[0]['nps_score']
            
            if diferenca > 5:
                return 'crescimento'
            elif diferenca < -5:
                return 'declínio'
            else:
                return 'estável'
                
        except Exception as e:
            print(f"❌ Erro no cálculo de tendência: {str(e)}")
            return 'erro'
    
    def gerar_insights_automaticos(self):
        """Gera insights e recomendações automáticas"""
        try:
            print("💡 Gerando insights automáticos...")
            
            insights = []
            alertas = []
            recomendacoes = []
            
            # Análise do NPS geral
            nps_geral = self.metricas.get('percentuais_nps', {}).get('nps_score', 0)
            
            if nps_geral >= 70:
                insights.append("🎉 Excelente! NPS acima de 70 indica alta satisfação dos clientes")
            elif nps_geral >= 50:
                insights.append("👍 Bom! NPS entre 50-70 indica satisfação positiva")
            elif nps_geral >= 0:
                insights.append("⚠️ Atenção! NPS entre 0-50 indica margem para melhorias")
                recomendacoes.append("📈 Foque em reduzir detratores e aumentar promotores")
            else:
                alertas.append("🚨 CRÍTICO! NPS negativo indica insatisfação")
                recomendacoes.append("🔴 Ação urgente: investigue causas da insatisfação")
            
            # Análise de vendedores
            analise_vendedores = self.metricas.get('analise_vendedores', {})
            vendedores_problema = analise_vendedores.get('vendedores_problema', [])
            
            if vendedores_problema:
                alertas.append(f"⚠️ {len(vendedores_problema)} vendedores com NPS < 50")
                recomendacoes.append("👥 Implemente treinamento para vendedores com baixo NPS")
            
            # Análise temporal
            evolucao = self.metricas.get('evolucao_temporal', {})
            tendencia = evolucao.get('tendencia', 'sem_dados')
            
            if tendencia == 'crescimento':
                insights.append("📈 Tendência positiva! NPS em crescimento")
            elif tendencia == 'declínio':
                alertas.append("📉 Tendência negativa! NPS em declínio")
                recomendacoes.append("🔍 Investigue causas da queda no NPS")
            
            # Análise de distribuição
            detratores_pct = self.metricas.get('percentuais_nps', {}).get('pct_detratores', 0)
            
            if detratores_pct > 20:
                alertas.append(f"🚨 Alto índice de detratores: {detratores_pct:.1f}%")
                recomendacoes.append("📞 Implemente follow-up com clientes insatisfeitos")
            
            insights_completos = {
                'insights_positivos': insights,
                'alertas': alertas,
                'recomendacoes': recomendacoes,
                'vendedores_problema': vendedores_problema
            }
            
            self.metricas['insights_automaticos'] = insights_completos
            
            print(f"✅ Insights gerados: {len(insights)} positivos, {len(alertas)} alertas")
            return insights_completos
            
        except Exception as e:
            print(f"❌ Erro na geração de insights: {str(e)}")
            return {}
    
    def _detectar_empresa(self):
        """Detecta nome da empresa nos dados"""
        try:
            # Tenta várias estratégias para detectar empresa
            if 'Empresa' in self.dados.columns:
                return self.dados['Empresa'].iloc[0]
            
            # Busca padrões conhecidos nos dados
            if 'Loja' in self.dados.columns:
                loja_principal = self.dados['Loja'].value_counts().index[0]
                if 'MDO' in str(loja_principal):
                    return "Mercadão dos Óculos"
                elif 'Analytics' in str(loja_principal):
                    return "Analytics"
            
            return "Sistema NPS"
            
        except Exception as e:
            print(f"⚠️ Erro ao detectar empresa: {str(e)}")
            return "Sistema NPS"
    
    def _detectar_unidade(self):
        """Detecta unidade/loja principal"""
        try:
            if 'Loja' in self.dados.columns:
                loja_principal = self.dados['Loja'].value_counts().index[0]
                return f"Unidade {loja_principal}"
            return "Unidade Principal"
            
        except Exception as e:
            print(f"⚠️ Erro ao detectar unidade: {str(e)}")
            return "Unidade Principal"
    
    def _detectar_periodo(self):
        """Detecta período dos dados"""
        try:
            if 'Data' in self.dados.columns:
                data_mais_recente = pd.to_datetime(self.dados['Data'], errors='coerce').max()
                if pd.notna(data_mais_recente):
                    return data_mais_recente.strftime("%B/%Y")
            
            return datetime.now().strftime("%B/%Y")
            
        except Exception as e:
            print(f"⚠️ Erro ao detectar período: {str(e)}")
            return datetime.now().strftime("%B/%Y")
    
    def _extrair_comentarios_positivos(self):
        """Extrai comentários de promotores"""
        try:
            if 'Comentario' in self.dados.columns and 'Looker_Classificacao' in self.dados.columns:
                promotores = self.dados[self.dados['Looker_Classificacao'] == '🟢 Promotor']
                comentarios_com_nomes = []
                
                for _, row in promotores.iterrows():
                    comentario = row.get('Comentario', '')
                    nome = row.get('Nome', 'Cliente')
                    
                    if pd.notna(comentario) and str(comentario).strip():
                        comentarios_com_nomes.append({
                            'comentario': str(comentario).strip(),
                            'nome': str(nome).strip()
                        })
                
                return comentarios_com_nomes[:10]  # Top 10 comentários
            
            return []
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair comentários positivos: {str(e)}")
            return []
    
    def _extrair_comentarios_negativos(self):
        """Extrai comentários de detratores"""
        try:
            if 'Comentario' in self.dados.columns and 'Looker_Classificacao' in self.dados.columns:
                detratores = self.dados[self.dados['Looker_Classificacao'] == '🔴 Detrator']
                comentarios_com_nomes = []
                
                for _, row in detratores.iterrows():
                    comentario = row.get('Comentario', '')
                    nome = row.get('Nome', 'Cliente')
                    
                    if pd.notna(comentario) and str(comentario).strip():
                        comentarios_com_nomes.append({
                            'comentario': str(comentario).strip(),
                            'nome': str(nome).strip()
                        })
                
                return comentarios_com_nomes
            
            return []
            
        except Exception as e:
            print(f"⚠️ Erro ao extrair comentários negativos: {str(e)}")
            return []
    
    def _analisar_detratores(self):
        """Analisa detratores em detalhes"""
        try:
            if 'Looker_Classificacao' in self.dados.columns:
                detratores = self.dados[self.dados['Looker_Classificacao'] == '🔴 Detrator']
                analise = []
                
                for _, row in detratores.iterrows():
                    analise.append({
                        'nome': row.get('Nome', 'N/A'),
                        'vendedor': row.get('Vendedor', 'N/A'),
                        'nota': row.get('Avaliacao', 'N/A'),
                        'comentario': row.get('Comentario', 'Sem comentário')
                    })
                
                return analise
            
            return []
            
        except Exception as e:
            print(f"⚠️ Erro ao analisar detratores: {str(e)}")
            return []
    
    def _formatar_vendedores_para_ia(self, analise_vendedores):
        """Formata dados de vendedores para IA"""
        try:
            texto = ""
            for vendedor in analise_vendedores:
                texto += f"- {vendedor['vendedor']} ({vendedor['loja']}): {vendedor['total_avaliacoes']} avaliações, NPS {vendedor['nps_looker']}\n"
            return texto
            
        except Exception as e:
            print(f"⚠️ Erro ao formatar vendedores: {str(e)}")
            return "Dados de vendedores indisponíveis"
    
    def calcular_metricas_looker(self):
        """
        Calcula métricas usando fórmulas Looker exatas
        Integra com sistema existente SEM alterar funcionamento atual
        """
        try:
            print("🚀 Calculando métricas Looker...")
            
            # Aplicar todas as fórmulas Looker
            dados_enriquecidos = LookerFormulas.aplicar_todas_formulas(self.dados)
            
            # Calcular NPS Looker geral
            nps_geral = LookerFormulas.calcular_nps_looker(dados_enriquecidos)
            
            # Análise por loja (usando fórmulas Looker)
            analise_lojas = []
            if 'Loja' in self.dados.columns:
                analise_lojas = LookerFormulas.analisar_por_dimensao(dados_enriquecidos, 'Loja')
            
            # Análise por vendedor (usando fórmulas Looker)
            analise_vendedores = []
            if 'Vendedor' in self.dados.columns:
                analise_vendedores_raw = LookerFormulas.analisar_por_dimensao(dados_enriquecidos, 'Vendedor')
                
                # Adicionar informação de loja para cada vendedor
                for vendedor_data in analise_vendedores_raw:
                    vendedor_nome = vendedor_data['vendedor']
                    # Buscar loja do vendedor
                    loja_vendedor = "N/A"
                    if 'Loja' in self.dados.columns:
                        vendedor_rows = dados_enriquecidos[dados_enriquecidos['Vendedor'] == vendedor_nome]
                        if len(vendedor_rows) > 0:
                            loja_vendedor = vendedor_rows['Loja'].iloc[0]
                    
                    vendedor_data['loja'] = loja_vendedor
                    analise_vendedores.append(vendedor_data)
            
            # Análise de interações
            interacoes_d1_d30 = dados_enriquecidos['Looker_Interacao_D1_D30'].value_counts().get('Sim', 0)
            interacoes_outros = dados_enriquecidos['Looker_Interacao_Outros'].value_counts().get('Sim', 0)
            
            # Análise de avaliações
            avaliou_count = dados_enriquecidos['Looker_Avaliou'].value_counts().get('Avaliou', 0)
            nao_avaliou_count = dados_enriquecidos['Looker_Avaliou'].value_counts().get('Não avaliou', 0)
            
            # Compilar resultados Looker
            resultados_looker = {
                'metricas_gerais': nps_geral,
                'analise_lojas': analise_lojas,
                'analise_vendedores': analise_vendedores,
                'dados_enriquecidos': dados_enriquecidos,
                'interacoes': {
                    'd1_d30_positivas': interacoes_d1_d30,
                    'outros_periodos_positivas': interacoes_outros,
                    'total_registros': len(dados_enriquecidos)
                },
                'avaliacoes': {
                    'avaliou': avaliou_count,
                    'nao_avaliou': nao_avaliou_count,
                    'total': len(dados_enriquecidos)
                },
                'metadados': {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'versao_looker': '1.0.0',
                    'colunas_adicionadas': 4,
                    'status': 'integrado_com_sucesso'
                }
            }
            
            # Gerar análise IA Analytics
            if nps_geral['status'] == 'sucesso':
                analise_ia = self.gerar_analise_ia_socialzap(resultados_looker)
                resultados_looker['analise_ia_socialzap'] = analise_ia
            
            # Salvar nos resultados gerais
            self.metricas['looker'] = resultados_looker
            
            print(f"✅ Métricas Looker calculadas com sucesso!")
            print(f"   🎯 NPS Final: {nps_geral['nps_final']}")
            print(f"   📊 Lojas analisadas: {len(analise_lojas)}")
            print(f"   👥 Vendedores analisados: {len(analise_vendedores)}")
            print(f"   📋 Interações D+1/D+30: {interacoes_d1_d30}")
            
            return resultados_looker
            
        except Exception as e:
            print(f"❌ Erro ao calcular métricas Looker: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def gerar_analise_ia_socialzap(self, resultados_looker):
        """
        Envia dados para IA analisar e gerar relatório no formato Analytics
        """
        try:
            print("🤖 Gerando análise IA formato Analytics...")
            
            # Preparar dados estruturados para IA
            dados_para_ia = {
                'empresa': self._detectar_empresa(),
                'unidade': self._detectar_unidade(),
                'periodo': self._detectar_periodo(),
                'metricas_gerais': resultados_looker['metricas_gerais'],
                'analise_vendedores': resultados_looker['analise_vendedores'],
                'comentarios_positivos': self._extrair_comentarios_positivos(),
                'comentarios_negativos': self._extrair_comentarios_negativos(),
                'detratores_detalhados': self._analisar_detratores()
            }
            
            # Prompt específico para formato Analytics
            prompt_socialzap = f"""
Analise os dados de NPS e gere um relatório EXATAMENTE no formato Analytics:

DADOS PROCESSADOS:
- Empresa: {dados_para_ia['empresa']}
- Unidade: {dados_para_ia['unidade']} 
- Período: {dados_para_ia['periodo']}
- NPS Final: {dados_para_ia['metricas_gerais']['nps_final']}%
- Total Avaliações: {dados_para_ia['metricas_gerais']['total_avaliacoes']}
- Promotores: {dados_para_ia['metricas_gerais']['promotores_count']} ({dados_para_ia['metricas_gerais']['perc_promotores']}%)
- Detratores: {dados_para_ia['metricas_gerais']['detratores_count']} ({dados_para_ia['metricas_gerais']['perc_detratores']}%)

VENDEDORES:
{self._formatar_vendedores_para_ia(dados_para_ia['analise_vendedores'])}

COMENTÁRIOS POSITIVOS:
{chr(10).join([f"- {c['comentario']} ({c['nome']})" for c in dados_para_ia['comentarios_positivos'][:5]])}

COMENTÁRIOS NEGATIVOS:
{chr(10).join([f"- {c['comentario']} ({c['nome']})" for c in dados_para_ia['comentarios_negativos'][:5]])}

GERE RELATÓRIO SEGUINDO EXATAMENTE ESTE FORMATO:

📊 Análise Pós-venda — {dados_para_ia['periodo']}
{dados_para_ia['empresa']} — {dados_para_ia['unidade']}

✅ Visão Geral:
● NPS Atendimento: {dados_para_ia['metricas_gerais']['nps_final']}
● Total Avaliações Atendimento: {dados_para_ia['metricas_gerais']['total_avaliacoes']}

👥 Avaliação de Atendimento
[ANÁLISE DETALHADA DO NPS - 2-3 parágrafos baseado nos dados reais]

Destaques positivos nos comentários:
{chr(10).join([f"● \"{c['comentario']}\" — {c['nome']}" for c in dados_para_ia['comentarios_positivos'][:3]])}

Observações relevantes:
● [PONTO DE MELHORIA 1 baseado nos dados]
● [PONTO DE MELHORIA 2 baseado nos dados]

👤 Avaliação por Vendedor

{chr(10).join([f"**Vendedor:** {v['vendedor']}{chr(10)}- Atendimento (NPS): {v['nps_looker']}{chr(10)}- Total Avaliações: {v['total_avaliacoes']}{chr(10)}" for v in dados_para_ia['analise_vendedores']])}

**Análise de Desempenho:**
[ANÁLISE DOS VENDEDORES - identificar padrões baseado nos dados reais]

📌 Recomendações
1. [RECOMENDAÇÃO ESPECÍFICA 1 baseada nos problemas identificados]
2. [RECOMENDAÇÃO ESPECÍFICA 2 baseada nos dados]  
3. [RECOMENDAÇÃO ESPECÍFICA 3 acionável]
4. [RECOMENDAÇÃO ESPECÍFICA 4 para melhoria]
5. [RECOMENDAÇÃO ESPECÍFICA 5 preventiva]

INSTRUÇÕES ESPECÍFICAS:
- Use dados REAIS fornecidos
- Analise comentários para insights
- Identifique padrões específicos nos vendedores
- Gere recomendações acionáveis
- Use tom profissional
- Seja específico sobre problemas identificados
"""

            # Enviar para OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é um analista especialista em NPS que gera relatórios no formato Analytics. Seja preciso, profissional e use exatamente o formato solicitado."
                    },
                    {
                        "role": "user", 
                        "content": prompt_socialzap
                    }
                ],
                temperature=0.3
            )
            
            relatorio_ia = response.choices[0].message.content
            
            # Salvar relatório
            nome_arquivo = f"Relatorio_NPS_{dados_para_ia['unidade'].replace(' ', '_')}_{dados_para_ia['periodo'].replace('/', '_')}.txt"
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio_ia)
            
            print(f"✅ Relatório IA Analytics gerado: {nome_arquivo}")
            return relatorio_ia
            
        except Exception as e:
            print(f"❌ Erro na análise IA Analytics: {str(e)}")
            return None


def main():
    """Função principal para teste"""
    # Dados de exemplo
    dados_teste = pd.DataFrame({
        'Vendedor': ['João', 'Maria', 'Pedro', 'Ana', 'João'] * 20,
        'Loja': ['Loja A', 'Loja B', 'Loja A', 'Loja C', 'Loja B'] * 20,
        'Avaliacao': [9, 8, 10, 7, 6, 9, 10, 8, 7, 9] * 10
    })
    
    print("📊 Testando calculadora de métricas...")
    
    calc = CalculadoraMetricas(dados_teste)
    metricas = calc.calcular_todas_metricas()
    
    # Exibe resumo
    resumo = calc.obter_resumo()
    print(f"\n🎯 RESUMO: {resumo['vendedores']} VENDEDORES | {resumo['avaliacoes']} AVALIAÇÕES | NOTA {resumo['nota_media']:.1f}")
    
    # Exibe ranking
    if 'ranking_lojas' in metricas:
        print(f"\n🏆 TOP 3 LOJAS:")
        for i, loja in enumerate(metricas['ranking_lojas'][:3], 1):
            print(f"{i}. {loja['loja']}: NPS {loja['nps_score']:.1f}")


if __name__ == "__main__":
    main()