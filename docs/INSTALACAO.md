# 🛠️ Guia de Instalação - DashBot Analytics

## 📋 **Pré-requisitos**

- **Python 3.8+** instalado
- **Git** (para clonar do GitHub)
- **Navegador moderno** (Chrome, Firefox, Safari, Edge)

## ⚡ **Instalação Rápida**

### **1. Clonar o Repositório**
```bash
git clone https://github.com/SEU_USUARIO/dashbot-nps-analytics.git
cd dashbot-nps-analytics
```

### **2. Criar Ambiente Virtual**
```bash
# Linux/Mac
python3 -m venv nps_env
source nps_env/bin/activate

# Windows
python -m venv nps_env
nps_env\Scripts\activate
```

### **3. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **4. Testar Instalação**
```bash
python main.py
```

## 🚀 **Instalação Detalhada**

### **Passo 1: Verificar Python**
```bash
python3 --version
# Deve mostrar Python 3.8 ou superior
```

**Se não tiver Python:**
- **Ubuntu/Debian**: `sudo apt install python3 python3-pip`
- **Windows**: Baixar em https://python.org
- **Mac**: `brew install python3`

### **Passo 2: Clonar Projeto**
```bash
# Opção 1: HTTPS
git clone https://github.com/SEU_USUARIO/dashbot-nps-analytics.git

# Opção 2: SSH (se configurado)
git clone git@github.com:SEU_USUARIO/dashbot-nps-analytics.git

# Entrar na pasta
cd dashbot-nps-analytics
```

### **Passo 3: Ambiente Virtual**
```bash
# Criar ambiente
python3 -m venv nps_env

# Ativar (Linux/Mac)
source nps_env/bin/activate

# Ativar (Windows)
nps_env\Scripts\activate

# Verificar ativação - deve aparecer (nps_env) na linha
```

### **Passo 4: Dependências**
```bash
# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list
```

## 🔧 **Configuração Opcional**

### **Para Planilhas Privadas (OAuth2)**
```bash
python configurar.py
```

### **Variáveis de Ambiente**
Criar arquivo `.env` (opcional):
```env
GOOGLE_SHEETS_API_KEY=sua_chave_aqui
DEFAULT_LOJA_NAME=Nome_Padrao_Loja
```

## ✅ **Verificar Instalação**

### **Teste 1: Backend**
```bash
python main.py
# Deve mostrar menu interativo
```

### **Teste 2: Frontend**
```bash
python frontend/server.py
# Deve abrir navegador em localhost:8080
```

### **Teste 3: Análise Completa**
```bash
python teste_sistema_pdf.py
# Deve gerar PDF de teste
```

## 📁 **Estrutura Após Instalação**

```
dashbot-nps-analytics/
├── 📄 main.py
├── 🌐 frontend/
├── 📁 nps_env/          # Ambiente virtual criado
├── 📁 relatorios/       # PDFs gerados aqui
├── 📁 credentials/      # Credenciais OAuth (se configurar)
├── 📋 requirements.txt
└── 📚 docs/
```

## 🚨 **Problemas Comuns**

### ❌ **"python3: command not found"**
```bash
# Linux
sudo apt update && sudo apt install python3

# Mac
brew install python3

# Windows
# Baixar do site oficial python.org
```

### ❌ **"pip: command not found"**
```bash
# Linux
sudo apt install python3-pip

# Mac
curl https://bootstrap.pypa.io/get-pip.py | python3

# Windows
# Instalar junto com Python do site oficial
```

### ❌ **"Permission denied"**
```bash
# Linux/Mac - não usar sudo com pip
python3 -m pip install --user -r requirements.txt
```

### ❌ **"ModuleNotFoundError"**
```bash
# Verificar se ambiente virtual está ativo
source nps_env/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

### ❌ **"No module named 'pandas'"**
```bash
# Ativar ambiente virtual
source nps_env/bin/activate

# Instalar manualmente
pip install pandas reportlab matplotlib gspread
```

## 🔄 **Atualizações**

### **Atualizar do GitHub**
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### **Atualizar Dependências**
```bash
pip install --upgrade -r requirements.txt
```

## 🏢 **Instalação Empresarial**

### **Servidor Ubuntu/Debian**
```bash
# Dependências do sistema
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# Clonar e configurar
git clone https://github.com/SEU_USUARIO/dashbot-nps-analytics.git
cd dashbot-nps-analytics
python3 -m venv nps_env
source nps_env/bin/activate
pip install -r requirements.txt

# Testar
python main.py
```

### **Windows Server**
```powershell
# Baixar Python do site oficial
# Baixar Git do site oficial

# No PowerShell ou CMD
git clone https://github.com/SEU_USUARIO/dashbot-nps-analytics.git
cd dashbot-nps-analytics
python -m venv nps_env
nps_env\Scripts\activate
pip install -r requirements.txt
python main.py
```

## ✅ **Checklist de Instalação**

- [ ] Python 3.8+ instalado
- [ ] Git instalado
- [ ] Repositório clonado
- [ ] Ambiente virtual criado
- [ ] Ambiente virtual ativado `(nps_env)`
- [ ] Dependências instaladas
- [ ] Teste backend funcionou
- [ ] Teste frontend funcionou
- [ ] PDF de teste gerado

**🎉 Instalação concluída com sucesso!**