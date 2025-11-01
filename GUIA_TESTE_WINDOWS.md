# 🪟 Guia de Teste no Windows

## 📋 Pré-requisitos

- ✅ Python 3.8+ instalado
- ✅ Git Bash ou PowerShell
- ✅ Navegador moderno (Chrome, Edge, Firefox)

---

## 🚀 Passo a Passo

### **1. Ativar o Ambiente Virtual**

#### Opção A: PowerShell
```powershell
cd "C:\Users\lucas\OneDrive\Área de Trabalho\cursor\projetos\TCC\RBCML-Application"
.\environment\Scripts\Activate.ps1
```

**Se der erro de execução de scripts:**
```powershell
# Execute como Administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Depois tente novamente
.\environment\Scripts\Activate.ps1
```

#### Opção B: CMD
```cmd
cd "C:\Users\lucas\OneDrive\Área de Trabalho\cursor\projetos\TCC\RBCML-Application"
environment\Scripts\activate.bat
```

#### Opção C: Git Bash
```bash
cd "/c/Users/lucas/OneDrive/Área de Trabalho/cursor/projetos/TCC/RBCML-Application"
source environment/Scripts/activate
```

**Você saberá que funcionou quando aparecer `(environment)` no início da linha.**

---

### **2. Instalar Dependências**

```bash
pip install -r requirements.txt
```

**Dependências principais:**
- Flask
- Flask-SocketIO
- python-socketio
- PyJWT
- bcrypt (se usar hash de senhas)

---

### **3. Configurar Variável de Ambiente para Email**

#### PowerShell:
```powershell
$env:EMAIL_PASSWORD="sua_senha_app_gmail"
```

#### CMD:
```cmd
set EMAIL_PASSWORD=sua_senha_app_gmail
```

#### Git Bash:
```bash
export EMAIL_PASSWORD="sua_senha_app_gmail"
```

**⚠️ IMPORTANTE:** Esta variável só vale para a sessão atual do terminal!

**Para tornar permanente (PowerShell como Admin):**
```powershell
[System.Environment]::SetEnvironmentVariable('EMAIL_PASSWORD', 'sua_senha', 'User')
```

---

### **4. Gerar Certificados SSL**

#### Opção A: Com OpenSSL (Git Bash)
```bash
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -nodes \
  -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

**Durante o processo, preencha:**
- Country Name: BR
- State: Seu Estado
- City: Sua Cidade
- Organization: RBCML
- Common Name: localhost
- Email: seu@email.com

#### Opção B: Sem OpenSSL (PowerShell)
```powershell
# Instalar OpenSSL via Chocolatey
choco install openssl

# Ou baixar de: https://slproweb.com/products/Win32OpenSSL.html
```

#### Opção C: Usar certificados de desenvolvimento
```bash
# Se não conseguir gerar, pode usar sem SSL temporariamente
# Edite run.py e remova o ssl_context
```

---

### **5. Verificar Banco de Dados**

```bash
# Verificar se o banco existe
ls app/database/rbcml.db

# Se não existir, criar as tabelas
python -c "from app.database import db; print('DB OK')"
```

**Criar banco manualmente (se necessário):**
```bash
cd app/database
sqlite3 rbcml.db < schema.sql
cd ../..
```

---

### **6. Executar Script de Teste**

```bash
python test_integration.py
```

**Saída esperada:**
```
🧪 TESTE DE INTEGRAÇÃO - RBCML APPLICATION
============================================================
🔍 Testando conexão com banco de dados...
✅ Tabelas encontradas: ['User', 'Model', 'Session']

🔍 Verificando modelos no banco...
⚠️  Nenhum modelo encontrado. Você precisa criar modelos primeiro.

🔍 Verificando usuários no banco...
⚠️  Nenhum usuário encontrado. Você precisa criar uma conta primeiro.

...

📊 RESUMO DOS TESTES
============================================================
Conexão com Banco de Dados.................. ✅ PASSOU
Modelos no Banco............................ ✅ PASSOU
Usuários no Banco........................... ✅ PASSOU
Arquivos Estáticos.......................... ✅ PASSOU
Templates................................... ✅ PASSOU
Certificados SSL............................ ✅ PASSOU
Variáveis de Ambiente....................... ✅ PASSOU

7/7 testes passaram

🎉 Todos os testes passaram! O sistema está pronto para uso.
```

---

### **7. Iniciar o Servidor**

```bash
python run.py
```

**Saída esperada:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on https://0.0.0.0:5000
Press CTRL+C to quit
```

---

### **8. Acessar no Navegador**

Abra seu navegador e acesse:
```
https://localhost:5000
```

**⚠️ Aviso de Segurança:**
O navegador vai mostrar um aviso sobre certificado não confiável. Isso é normal!

#### Chrome/Edge:
1. Clique em "Avançado"
2. Clique em "Continuar para localhost (não seguro)"

#### Firefox:
1. Clique em "Avançado"
2. Clique em "Aceitar o Risco e Continuar"

---

## 🧪 Testando as Funcionalidades

### **Teste 1: Criar Conta**
1. Na home, clique em **"Login"**
2. Clique em **"Cadastro"**
3. Preencha:
   - Tag: `teste123`
   - Nome: `Usuário Teste`
   - Email: `teste@email.com`
   - Senha: `senha123`
4. Clique em **"Cadastrar"**
5. ✅ Deve mostrar "Cadastro realizado com sucesso!"

### **Teste 2: Fazer Login**
1. Clique em **"Login"** novamente
2. Preencha:
   - Tag: `teste123`
   - Senha: `senha123`
3. Clique em **"Entrar"**
4. ✅ Deve mostrar "Login realizado com sucesso!"

### **Teste 3: Criar Modelo**
1. Na home, clique em **"Crie um Room"**
2. Preencha:
   - Nome: `Sala de Teste`
   - Descrição: `Modelo para testes`
3. Crie um arquivo JSON (`modelo.json`):
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
4. Faça upload do arquivo
5. Clique em **"Criar Modelo"**
6. ✅ Deve voltar para home com o novo modelo aparecendo

### **Teste 4: Criar Sessão**
1. Clique no modelo criado
2. Você verá os roles: **Professor** e **Aluno**
3. Insira emails para cada role
4. Clique nas setas para enviar
5. ✅ Sistema deve criar sessão e enviar emails

### **Teste 5: Videochamada**
1. Abra o link de convite (do email ou direto)
2. Permita acesso à câmera e microfone
3. ✅ Deve ver sua própria imagem
4. Abra em outra aba/navegador
5. ✅ Deve conectar e ver o outro participante

---

## 🐛 Resolução de Problemas

### **Problema: "Não é possível executar scripts"**
**Solução:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Problema: "ModuleNotFoundError: No module named 'flask'"**
**Solução:**
```bash
# Certifique-se de que o ambiente está ativado
pip install -r requirements.txt
```

### **Problema: "sqlite3.OperationalError: no such table"**
**Solução:**
```bash
cd app/database
sqlite3 rbcml.db < schema.sql
```

### **Problema: "Port 5000 already in use"**
**Solução:**
```bash
# Encontrar processo usando a porta
netstat -ano | findstr :5000

# Matar o processo (substitua PID pelo número encontrado)
taskkill /PID <PID> /F

# Ou mudar a porta em run.py
```

### **Problema: "Email não enviado"**
**Soluções:**
1. Verificar se EMAIL_PASSWORD está configurado:
   ```bash
   echo $env:EMAIL_PASSWORD  # PowerShell
   echo %EMAIL_PASSWORD%     # CMD
   ```

2. Gerar senha de app do Gmail:
   - Acesse: https://myaccount.google.com/apppasswords
   - Gere uma senha de app
   - Use essa senha (não sua senha normal)

3. Verificar logs no terminal

### **Problema: "WebRTC não conecta"**
**Soluções:**
1. Usar HTTPS (certificado SSL)
2. Permitir câmera/microfone no navegador
3. Verificar firewall do Windows
4. Testar em localhost primeiro

### **Problema: "Certificado SSL inválido"**
**Solução:**
```bash
# No navegador, aceite o certificado
# Ou gere um novo certificado
openssl req -x509 -newkey rsa:4096 -nodes \
  -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

---

## 📊 Verificar Logs

### **Ver logs do servidor:**
Os logs aparecem no terminal onde você executou `python run.py`

### **Ver logs do navegador:**
1. Pressione `F12`
2. Vá na aba **Console**
3. Veja erros JavaScript

### **Ver banco de dados:**
```bash
# Abrir SQLite
sqlite3 app/database/rbcml.db

# Comandos úteis
.tables                    # Listar tabelas
SELECT * FROM User;        # Ver usuários
SELECT * FROM Model;       # Ver modelos
SELECT * FROM Session;     # Ver sessões
.quit                      # Sair
```

---

## 🔥 Comandos Úteis

### **Limpar cache do Python:**
```bash
# PowerShell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force

# CMD
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
del /s /q *.pyc
```

### **Reiniciar servidor rapidamente:**
```bash
# No terminal do servidor, pressione:
Ctrl + C  # Para o servidor
python run.py  # Inicia novamente
```

### **Ver processos Python rodando:**
```bash
tasklist | findstr python
```

### **Matar todos os processos Python:**
```bash
taskkill /F /IM python.exe
```

---

## 📝 Checklist de Teste Completo

- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] EMAIL_PASSWORD configurado
- [ ] Certificados SSL gerados
- [ ] Banco de dados criado
- [ ] Script de teste executado (7/7 passou)
- [ ] Servidor iniciado sem erros
- [ ] Navegador acessa https://localhost:5000
- [ ] Consegue criar conta
- [ ] Consegue fazer login
- [ ] Consegue criar modelo
- [ ] Modelo aparece na home
- [ ] Consegue criar sessão
- [ ] Consegue acessar videochamada
- [ ] Câmera e microfone funcionam
- [ ] Chat funciona

---

## 🎯 Atalhos do Windows

```bash
# Abrir PowerShell rapidamente
Win + X → A (como Admin)
Win + X → I (normal)

# Copiar caminho de arquivo
Shift + Botão Direito → "Copiar como caminho"

# Abrir terminal na pasta
Shift + Botão Direito → "Abrir janela do PowerShell aqui"
```

---

## 📞 Suporte

Se encontrar problemas:

1. **Verifique os logs** no terminal
2. **Verifique o console** do navegador (F12)
3. **Execute o script de teste** novamente
4. **Verifique o banco de dados** com SQLite

---

## 🎉 Pronto!

Agora você pode testar toda a aplicação no Windows! 

**Próximos passos:**
1. Criar alguns modelos de teste
2. Convidar amigos para testar a videochamada
3. Testar com múltiplos participantes
4. Experimentar diferentes configurações de roles

**Divirta-se testando! 🚀**

