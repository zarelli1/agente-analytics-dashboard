# 🚀 DashBot Analytics - Sistema NPS Completo

Sistema completo de automação para análise de NPS (Net Promoter Score) com frontend moderno e backend Python.

## 📊 **Funcionalidades**

- ✅ **Extração automática** de dados do Google Sheets
- ✅ **Cálculo de métricas NPS** avançadas
- ✅ **Geração de relatórios PDF** profissionais
- ✅ **Frontend moderno** com interface intuitiva
- ✅ **Análise em tempo real** via web
- ✅ **Rankings de vendedores e lojas**
- ✅ **Insights automáticos** e alertas

## 🎯 **Demonstração**

![DashBot Interface](https://via.placeholder.com/800x400/0f0f0f/FBBF24?text=DashBot+Analytics+Interface)

## 🛠️ **Tecnologias**

### Backend
- **Python 3.x**
- **Pandas** - Manipulação de dados
- **ReportLab** - Geração de PDFs
- **GSpread** - Integração Google Sheets
- **Matplotlib** - Gráficos e visualizações

### Frontend
- **HTML5 + CSS3 + JavaScript**
- **Font Awesome** - Ícones
- **Servidor HTTP Python** - Backend integrado

## ⚡ **Instalação Rápida**

```bash
# 1. Clonar repositório
git clone https://github.com/SEU_USUARIO/dashbot-nps.git
cd dashbot-nps

# 2. Criar ambiente virtual
python3 -m venv nps_env
source nps_env/bin/activate  # Linux/Mac
# ou
nps_env\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar sistema
python main.py  # Para backend
# ou
python frontend/server.py  # Para frontend web
```

## 🚀 **Como Usar**

### **Opção 1: Interface Terminal**
```bash
source nps_env/bin/activate
python main.py
```

### **Opção 2: Interface Web (RECOMENDADO)**
```bash
source nps_env/bin/activate
python frontend/server.py
```
Acesse: `http://localhost:8080`

## 📋 **Estrutura do Projeto**

```
dashbot-nps/
├── 📄 main.py                    # Interface principal terminal
├── 📊 nps_extractor.py          # Extração de dados
├── 📈 calculadora_metricas.py   # Cálculos NPS
├── 📑 gerador_relatorio_pdf.py  # Geração de PDFs
├── 🌐 frontend/                 # Interface web
│   ├── index.html               # Interface principal
│   ├── style.css                # Estilos modernos
│   ├── script.js                # Lógica frontend
│   ├── api.js                   # Integração backend
│   └── server.py                # Servidor web
├── 📁 relatorios/               # PDFs gerados
├── 🔐 credentials/              # Credenciais OAuth (não commitado)
├── 📋 requirements.txt          # Dependências Python
└── 📚 docs/                     # Documentação
```

## 📊 **Exemplo de Uso**

1. **Preparar planilha** no Google Sheets com colunas:
   - Data, Nome, Loja, Vendedor, Avaliacao

2. **Tornar planilha pública** ou configurar OAuth2

3. **Executar análise**:
   - Via web: Acessar frontend e inserir URL
   - Via terminal: Seguir menu interativo

4. **Obter resultados**:
   - PDF completo com gráficos e insights
   - Métricas calculadas automaticamente

## 🎨 **Features do Frontend**

- 🎨 **Design moderno** dark/yellow
- 📱 **Responsivo** mobile/desktop
- ⚡ **Loading realista** com progresso
- 🔍 **Validação de URL** em tempo real
- 📊 **Métricas animadas** 
- 📄 **Download direto** de PDFs

## 🔧 **Configuração Avançada**

### **Para planilhas privadas:**
```bash
python configurar.py
```

### **Autenticação OAuth2:**
1. Criar projeto no Google Cloud Console
2. Ativar Google Sheets API
3. Baixar credenciais
4. Executar configuração

## 📈 **Métricas Calculadas**

- **NPS Score** geral e por segmento
- **Rankings** de vendedores e lojas
- **Distribuição** de notas (0-10)
- **Evolução temporal** das avaliações
- **Insights automáticos** e alertas
- **Top performers** e áreas de melhoria

## 🚨 **Suporte**

- 📖 [Documentação Completa](./docs/)
- 🚀 [Guia de Instalação](./COMO_ATIVAR_SERVIDOR.md)
- ⚡ [Quick Start](./FRONTEND_QUICKSTART.md)
- 📊 [Como Usar](./Como_usar.md)

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 **Autor**

**Developer** - Sistema NPS DashBot Analytics

---

⭐ **Se este projeto te ajudou, considere dar uma estrela!**

📞 **Suporte**: Para dúvidas ou suporte, abra uma issue no GitHub.