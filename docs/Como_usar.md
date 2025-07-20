# 🚀 Como Usar o Sistema NPS Analytics

## ⚡ **Início Rápido (3 Passos)**

### **1. Ativação**
```bash
cd /caminho/para/seu/projeto
source nps_env/bin/activate
python main.py
```

### **2. Gerar Relatório**
- Digite **1** (Gerar Relatório NPS)
- Nome da loja: `mdo maria izabel`
- URL: `https://docs.google.com/spreadsheets/d/[SEU_SHEET_ID]/edit`

### **3. Resultado**
Relatório PDF gerado em `relatorios/`

---

## 🔧 **Para Planilhas Privadas**

Se aparecer erro 401:
```bash
python configurar.py
```
Siga as instruções na tela.

---

## 📋 **Formato da Planilha**

Colunas necessárias:
- **Data** - Data da avaliação  
- **Nome** - Nome do cliente
- **Loja** - Nome da loja
- **Vendedor** - Nome do vendedor
- **Avaliacao** - Nota NPS (0-10)

---

## 🎯 **Relatório Completo**

O PDF inclui:
- **Resumo Executivo** - NPS geral e distribuição
- **Análise por Vendedor** - Ranking e performance  
- **Evolução Temporal** - Gráficos de tendência
- **Insights** - Recomendações automáticas
- **Alertas** - Vendedores com NPS < 50

---

## 🚨 **Problemas Comuns**

- **Erro 401**: `python configurar.py`
- **Sem dados**: Verifique URL e colunas
- **Módulos**: `pip install -r requirements.txt`

🎉 **Sistema funcional e pronto para uso!**