# 🚀 RBCML Application - Início Rápido

## 📖 Documentação

- **`GUIA_TESTE_WINDOWS.md`** - Guia completo de como testar no Windows
- **`ADAPTACOES_BACKEND.md`** - Documentação técnica das mudanças
- **`README.md`** - Documentação original do projeto

---

## ⚡ Início Rápido (Windows)

### **Método 1: Script Automático (Recomendado)**

#### PowerShell:
```powershell
.\iniciar_windows.ps1
```

#### CMD:
```cmd
iniciar_windows.bat
```

### **Método 2: Manual**

```bash
# 1. Ativar ambiente virtual
.\environment\Scripts\Activate.ps1  # PowerShell
# ou
environment\Scripts\activate.bat    # CMD

# 2. Configurar email (opcional)
$env:EMAIL_PASSWORD="sua_senha"     # PowerShell
# ou
set EMAIL_PASSWORD=sua_senha        # CMD

# 3. Iniciar servidor
python run.py
```

### **Método 3: Testar Primeiro**

```bash
# Executar testes de integração
python test_integration.py

# Se tudo passar, iniciar servidor
python run.py
```

---

## 🌐 Acessar

Abra seu navegador em:
```
https://localhost:5000
```

**⚠️ Aceite o certificado SSL no navegador**

---

## 📋 Pré-requisitos

- ✅ Python 3.8+
- ✅ Ambiente virtual criado
- ✅ Dependências instaladas (`pip install -r requirements.txt`)
- ⚠️ Certificados SSL (opcional, mas recomendado)
- ⚠️ EMAIL_PASSWORD configurado (opcional, para envio de emails)

---

## 🎯 Funcionalidades

- ✅ **Autenticação** - Login e cadastro de usuários
- ✅ **Modelos Personalizados** - Crie seus próprios modelos de sala
- ✅ **Sessões** - Crie sessões com participantes
- ✅ **Convites por Email** - Sistema automático de envio
- ✅ **Videochamada WebRTC** - Vídeo, áudio e chat em tempo real
- ✅ **Controle de Permissões** - Sistema baseado em roles (RBCML)

---

## 🔧 Configuração Inicial

### **1. Criar Ambiente Virtual (se não existir)**
```bash
python -m venv environment
```

### **2. Instalar Dependências**
```bash
pip install -r requirements.txt
```

### **3. Gerar Certificados SSL**
```bash
# Git Bash
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -nodes \
  -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

### **4. Configurar Email (Gmail)**
```bash
# PowerShell
$env:EMAIL_PASSWORD="sua_senha_app_gmail"

# CMD
set EMAIL_PASSWORD=sua_senha_app_gmail
```

**Como obter senha de app do Gmail:**
1. Acesse: https://myaccount.google.com/apppasswords
2. Gere uma senha de app
3. Use essa senha (não sua senha normal)

---

## 🧪 Testar

```bash
# Executar todos os testes
python test_integration.py

# Criar modelo de exemplo
python test_integration.py
# Responda 's' quando perguntado
```

---

## 📱 Uso Básico

### **1. Criar Conta**
1. Acesse https://localhost:5000
2. Clique em "Login"
3. Clique em "Cadastro"
4. Preencha os dados
5. Faça login

### **2. Criar Modelo**
1. Clique em "Crie um Room"
2. Preencha nome e descrição
3. Faça upload de um arquivo JSON com o modelo
4. Exemplo de JSON:
```json
{
  "roles": ["Professor", "Aluno"],
  "connections": {
    "Aluno-Professor": [
      [true, true, true, true, true, true, false, false],
      [true, true, true, true, true, true, false, false]
    ]
  }
}
```

### **3. Criar Sessão**
1. Clique em um modelo na home
2. Insira emails para cada role
3. Clique nas setas para enviar
4. Participantes receberão emails com link

### **4. Entrar na Videochamada**
1. Clique no link do email (ou acesse direto)
2. Permita acesso à câmera e microfone
3. Conecte com outros participantes!

---

## 🐛 Problemas Comuns

### **"Não é possível executar scripts"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **"Port 5000 already in use"**
```bash
# Encontrar processo
netstat -ano | findstr :5000

# Matar processo
taskkill /PID <PID> /F
```

### **"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

### **"Email não enviado"**
- Verifique se EMAIL_PASSWORD está configurado
- Use senha de app do Gmail (não senha normal)
- Verifique logs no terminal

### **"WebRTC não conecta"**
- Use HTTPS (certificado SSL)
- Permita câmera/microfone no navegador
- Teste em localhost primeiro

---

## 📚 Estrutura do Projeto

```
RBCML-Application/
├── app/
│   ├── __init__.py           # Inicialização Flask
│   ├── routes.py             # Rotas da aplicação
│   ├── events.py             # Eventos Socket.IO
│   ├── email.py              # Sistema de emails
│   ├── database/
│   │   ├── db.py             # Funções do banco
│   │   ├── rbcml.db          # Banco SQLite
│   │   └── schema.sql        # Schema do banco
│   ├── static/
│   │   ├── scripts/          # JavaScript
│   │   ├── styles/           # CSS
│   │   └── images/           # Imagens
│   └── templates/            # HTML
├── ssl/
│   ├── cert.pem              # Certificado SSL
│   └── key.pem               # Chave privada
├── environment/              # Ambiente virtual
├── run.py                    # Iniciar servidor
├── requirements.txt          # Dependências
├── test_integration.py       # Testes
├── iniciar_windows.bat       # Script CMD
├── iniciar_windows.ps1       # Script PowerShell
├── GUIA_TESTE_WINDOWS.md     # Guia completo
└── ADAPTACOES_BACKEND.md     # Documentação técnica
```

---

## 🔐 Segurança

- ✅ Autenticação JWT
- ✅ Cookies HttpOnly
- ✅ HTTPS (SSL/TLS)
- ✅ Validação de entrada
- ✅ Senhas hasheadas (se implementado)

---

## 🚀 Tecnologias

- **Backend:** Python, Flask, Socket.IO
- **Frontend:** HTML, CSS, JavaScript
- **Banco de Dados:** SQLite
- **WebRTC:** Peer-to-peer video/audio
- **Email:** SMTP (Gmail)

---

## 📞 Suporte

Se encontrar problemas:

1. Leia o **GUIA_TESTE_WINDOWS.md**
2. Execute `python test_integration.py`
3. Verifique os logs no terminal
4. Verifique o console do navegador (F12)

---

## 📝 Licença

Ver arquivo LICENSE

---

## 👥 Contribuindo

Este é um projeto acadêmico (TCC). Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um Pull Request

---

## ✅ Status

- [x] Backend adaptado ao novo frontend
- [x] Sistema de autenticação funcionando
- [x] Criação de modelos implementada
- [x] Sistema de emails funcionando
- [x] Videochamada WebRTC funcionando
- [x] Chat em tempo real funcionando
- [x] Documentação completa
- [ ] Testes unitários (em desenvolvimento)
- [ ] Deploy em produção (futuro)

---

**Desenvolvido para TCC - 2024**

🎓 **Universidade:** [Sua Universidade]  
👨‍💻 **Autor:** Lucas  
📅 **Data:** Novembro 2024  
🔖 **Versão:** 2.0

