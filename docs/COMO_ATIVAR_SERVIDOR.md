# 🚀 Como Ativar o Servidor Frontend - Guia Simples

## 📍 **PASSO A PASSO**

### **1. Abrir Terminal**
- Pressione `Ctrl + Alt + T` (Linux)
- Ou abra o terminal do VS Code

### **2. Navegar para a Pasta**
```bash
cd /caminho/para/seu/projeto
```

### **3. Ativar Ambiente Virtual**
```bash
source nps_env/bin/activate
```

**✅ Você verá `(nps_env)` no início da linha do terminal**

### **4. Iniciar o Servidor**
```bash
python frontend/server.py
```

## 🌐 **Resultado Esperado**

Você verá algo assim:
```
🚀 DASHBOT ANALYTICS - SERVIDOR FRONTEND
============================================================
📡 Servidor rodando em: http://localhost:8080
📁 Diretório: /caminho/para/seu/projeto/frontend
🌐 Abrindo navegador...
============================================================
💡 Para parar o servidor: Ctrl+C
```

## 🎯 **Comandos Completos (Copie e Cole)**

```bash
cd /caminho/para/seu/projeto
source nps_env/bin/activate
python frontend/server.py
```

## 📱 **Acessar o Frontend**

1. **Automático**: O navegador abre sozinho
2. **Manual**: Vá para `http://localhost:8080`

## 🛑 **Parar o Servidor**

Pressione `Ctrl + C` no terminal

## 🔧 **Se Der Erro**

### ❌ **"No such file or directory"**
```bash
# Verifique se está na pasta certa
pwd
# Deve mostrar: /caminho/para/seu/projeto
```

### ❌ **"nps_env not found"**
```bash
# Criar ambiente virtual
python3 -m venv nps_env
source nps_env/bin/activate
pip install -r requirements.txt
```

### ❌ **"Module not found"**
```bash
# Instalar dependências
source nps_env/bin/activate
pip install -r requirements.txt
```

## ⚡ **Versão Super Rápida**

**APENAS 3 COMANDOS:**
```bash
cd /caminho/para/seu/projeto && source nps_env/bin/activate && python frontend/server.py
```

## 📋 **Checklist**

- [ ] Abri o terminal
- [ ] Naveguei para `/caminho/para/seu/projeto`
- [ ] Ativei o ambiente virtual `(nps_env)`
- [ ] Executei `python frontend/server.py`
- [ ] Vi a mensagem de servidor rodando
- [ ] Acessei `http://localhost:8080`

**🎉 Frontend funcionando!**