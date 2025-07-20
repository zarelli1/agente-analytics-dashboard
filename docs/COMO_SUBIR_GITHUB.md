# 🚀 Como Subir o Projeto para o GitHub

## 📋 **Pré-requisitos**

- ✅ Conta no GitHub
- ✅ Git instalado no computador
- ✅ Terminal/Prompt de comando

## 🎯 **PASSO A PASSO COMPLETO**

### **1. Configurar Git (se não fez ainda)**
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### **2. Navegar para a Pasta do Projeto**
```bash
cd /caminho/para/seu/projeto
```

### **3. Inicializar Repositório Git**
```bash
git init
```

### **4. Adicionar Todos os Arquivos**
```bash
git add .
```

### **5. Fazer o Primeiro Commit**
```bash
git commit -m "🚀 Primeira versão do DashBot Analytics - Sistema NPS completo"
```

### **6. Criar Repositório no GitHub**

1. **Acesse**: https://github.com
2. **Clique**: "New repository" (botão verde)
3. **Nome**: `dashbot-nps-analytics` (ou outro nome)
4. **Descrição**: "Sistema completo de análise NPS com frontend moderno"
5. **Público ou Privado**: Escolha conforme preferência
6. **NÃO marque**: "Add a README file" (já temos)
7. **Clique**: "Create repository"

### **7. Conectar com o Repositório Remoto**
```bash
# Substitua SEU_USUARIO pelo seu nome de usuário do GitHub
git remote add origin https://github.com/SEU_USUARIO/dashbot-nps-analytics.git
```

### **8. Subir os Arquivos para o GitHub**
```bash
git branch -M main
git push -u origin main
```

## ⚡ **COMANDOS COMPLETOS (Copie e Cole)**

```bash
# Navegar para o projeto
cd /caminho/para/seu/projeto

# Inicializar git
git init

# Adicionar arquivos
git add .

# Primeiro commit
git commit -m "🚀 Primeira versão do DashBot Analytics - Sistema NPS completo"

# Conectar com GitHub (SUBSTITUA SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/dashbot-nps-analytics.git

# Subir para GitHub
git branch -M main
git push -u origin main
```

## 🔄 **Para Atualizações Futuras**

Depois de fazer mudanças no código:

```bash
# Adicionar mudanças
git add .

# Commit com descrição
git commit -m "📝 Descrição da sua mudança"

# Enviar para GitHub
git push
```

## 📁 **O que será enviado:**

- ✅ **Código Python** (backend completo)
- ✅ **Frontend web** (HTML/CSS/JS)
- ✅ **Documentação** (todos os .md)
- ✅ **Dependências** (requirements.txt)
- ❌ **Ambiente virtual** (nps_env/ - ignorado)
- ❌ **Credenciais** (credentials/ - ignorado)
- ❌ **Relatórios** (PDFs gerados - ignorado)

## 🏢 **Para Usar na Empresa**

1. **Clone o repositório**:
```bash
git clone https://github.com/SEU_USUARIO/dashbot-nps-analytics.git
cd dashbot-nps-analytics
```

2. **Configure o ambiente**:
```bash
python3 -m venv nps_env
source nps_env/bin/activate
pip install -r requirements.txt
```

3. **Execute**:
```bash
python frontend/server.py
```

## 🔐 **Dicas de Segurança**

- ✅ **Credenciais** estão no .gitignore (não serão enviadas)
- ✅ **Ambiente virtual** não é enviado (economiza espaço)
- ✅ **PDFs** não são enviados (arquivos grandes)

## 🚨 **Problemas Comuns**

### ❌ **"Permission denied"**
```bash
# Usar token de acesso pessoal em vez de senha
# GitHub > Settings > Developer settings > Personal access tokens
```

### ❌ **"Repository not found"**
```bash
# Verificar se o nome do repositório está correto
git remote -v
```

### ❌ **"Git not found"**
```bash
# Instalar git
sudo apt install git  # Linux
```

## 🎉 **Sucesso!**

Depois de seguir esses passos:
1. ✅ Projeto estará no GitHub
2. ✅ Poderá clonar em qualquer computador
3. ✅ Equipe poderá colaborar
4. ✅ Backup automático na nuvem

**Exemplo de URL final**: `https://github.com/seu-usuario/dashbot-nps-analytics`