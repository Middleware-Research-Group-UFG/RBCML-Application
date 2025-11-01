# Adaptações do Backend para o Novo Frontend

## 📋 Resumo das Mudanças

Este documento descreve todas as adaptações feitas no backend da aplicação RBCML para integrar com o novo frontend e implementar funcionalidades de videochamada e envio de emails.

---

## 🔧 Mudanças Implementadas

### 1. **Rotas Corrigidas e Otimizadas (`app/routes.py`)**

#### Rotas Removidas/Consolidadas:
- ❌ Removidas rotas duplicadas de `/login`
- ❌ Removidas rotas antigas: `/welcome`, `/createRole`, `/user/<user>`
- ✅ Consolidadas rotas de autenticação

#### Novas Rotas Adicionadas:

##### **Autenticação:**
```python
POST /login          # Login de usuário (retorna cookie JWT)
POST /cadastro       # Cadastro de novo usuário
GET  /logout         # Logout (remove cookie JWT)
```

##### **Páginas:**
```python
GET  /home           # Página inicial
GET  /createModel    # Página para criar novo modelo
GET  /createcall     # Página para criar sessão (requer model_id)
GET  /sessionsPage   # Página listando sessões do usuário
GET  /howtojson      # Tutorial de como criar JSON
```

##### **Sessões e Convites:**
```python
GET  /session/<session_id>    # Página da videochamada
GET  /invite                  # Link de convite para participantes
POST /createsession           # Criar nova sessão (envia emails)
```

##### **API REST:**
```python
GET  /api/models              # Lista todos os modelos disponíveis
GET  /api/sessions            # Lista sessões do usuário logado
GET  /api/model/<model_id>    # Detalhes de um modelo específico
```

---

### 2. **Sistema de Envio de Emails (`app/email.py`)**

**Funcionalidade:** Envia convites automáticos para participantes quando uma sessão é criada.

**Configuração necessária:**
```bash
# Definir variável de ambiente
export EMAIL_PASSWORD="sua_senha_de_app_do_gmail"
```

**Fluxo:**
1. Usuário cria uma sessão em `/createsession`
2. Sistema insere sessão no banco de dados
3. Sistema busca emails dos participantes
4. Envia email com link de convite para cada participante
5. Link inclui: `https://[host]/invite?session=[id]&user=[tag]`

**Exemplo de Email Enviado:**
```
Assunto: Invitation

[Creator] invited you to participate in session [ID]
as [Role]

You can access the session using the link:
https://localhost:5000/invite?session=1&user=joao

Valid from: 2024-01-01 10:00:00
      to: 2024-01-01 12:00:00
```

---

### 3. **Banco de Dados (`app/database/db.py`)**

**Nova Função Adicionada:**
```python
def search_all(table, db=db_path):
    """Busca todos os registros de uma tabela"""
    # Retorna lista de tuplas com todos os registros
```

**Uso:**
```python
models = db.search_all('Model')
sessions = db.search_all('Session')
```

---

### 4. **Frontend JavaScript Adaptado**

#### **`start_call.js`** (Carregamento de Modelos)
**Antes:**
```javascript
fetch('/static/model.json')  // Arquivo estático
```

**Depois:**
```javascript
fetch('/api/models')  // API dinâmica do banco
```

**Mudanças:**
- ✅ Busca modelos do banco de dados via API
- ✅ Adiciona card "Crie um Room" automaticamente
- ✅ Links corretos: `/createModel` ou `/createcall?model_id=X`

#### **`roles.js`** (Seleção de Roles)
**Antes:**
```javascript
const modelId = urlParams.get('nome');
fetch('../../model.json')
```

**Depois:**
```javascript
const modelId = urlParams.get('model_id');
fetch(`/api/model/${modelId}`)
```

**Mudanças:**
- ✅ Busca modelo específico por ID
- ✅ Acessa roles via `model.definition.roles`
- ✅ Inclui campos hidden no formulário (role, model_id)

#### **`log_sing.js`** (Sistema de Login)
**Mudanças:**
- ✅ Popup centralizado com overlay
- ✅ Fecha com ESC, clique fora ou botão X
- ✅ Formulários de login e cadastro funcionais
- ✅ Mensagens de erro/sucesso

---

### 5. **Templates Atualizados**

#### **`createModel.html`**
**Adicionado:**
```html
<input type="text" name="name" required>
<textarea name="description" required></textarea>
<input type="file" name="jsonModel" required>
```

#### **`howtojson.html`**
- ✅ Novo template criado
- ✅ Tutorial completo de JSON
- ✅ Link para documentação Oracle
- ✅ Integrado com o sistema de rotas Flask

#### **`home.html`**
**Adicionado:**
```html
<div class="login-popup" id="popUp">
    <!-- Popup de login/cadastro -->
</div>
```

---

## 🎯 Fluxo Completo de Uso

### **1. Criar Modelo**
```
1. Usuário acessa /home
2. Clica em "Login" e faz login
3. Clica em "Crie um Room"
4. Preenche: Nome, Descrição, Upload JSON
5. Sistema salva no banco de dados
6. Modelo aparece na home automaticamente
```

### **2. Criar Sessão e Videochamada**
```
1. Usuário clica em um modelo na home
2. Sistema redireciona para /createcall?model_id=X
3. Página carrega roles do modelo
4. Usuário insere emails para cada role
5. Sistema cria sessão no banco
6. Sistema envia emails automáticos
7. Participantes clicam no link do email
8. Sistema autentica e redireciona para /session/[id]
9. WebRTC estabelece conexões de vídeo/áudio
```

### **3. Videochamada (WebRTC)**
```
1. Usuário entra em /session/[id]
2. JavaScript conecta via Socket.IO
3. Backend usa eventos do events.py:
   - 'join': Usuário entra na sessão
   - 'setup_connections': Define conexões permitidas
   - 'setup_channel': Estabelece canais WebRTC
4. Frontend (channel.js) cria RTCPeerConnection
5. Streams de vídeo/áudio são trocados
6. Chat em tempo real via DataChannel
```

---

## 📦 Estrutura de Dados

### **Modelo JSON (Definition)**
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

**Capabilities:** `[sendVideo, recvVideo, sendAudio, recvAudio, sendString, recvString, ?, ?]`

### **Sessão (Participants JSON)**
```json
{
  "joao": ["Aluno"],
  "maria": ["Professor"]
}
```

---

## 🔐 Autenticação JWT

**Payload:**
```python
{
    'tag': 'usuario123',
    'iat': datetime.now(),      # Issued at
    'nbf': datetime.now(),      # Not before
    'exp': datetime.now() + timedelta(days=1)  # Expiration
}
```

**Cookie:**
- Nome: `jwt`
- HttpOnly: `True`
- Secure: `True` (HTTPS)
- SameSite: `Strict`

---

## 🚀 Como Testar

### **1. Configurar Ambiente**
```bash
cd RBCML-Application
source environment/bin/activate  # Linux/Mac
# ou
environment\Scripts\activate  # Windows

# Configurar email
export EMAIL_PASSWORD="sua_senha_app_gmail"

# Instalar dependências
pip install -r requirements.txt
```

### **2. Iniciar Servidor**
```bash
python run.py
```

Acesse: `https://localhost:5000`

### **3. Testar Fluxo Completo**
1. ✅ Criar conta (Cadastro)
2. ✅ Fazer login
3. ✅ Criar modelo personalizado
4. ✅ Criar sessão com participantes
5. ✅ Verificar emails enviados
6. ✅ Entrar na videochamada
7. ✅ Testar vídeo, áudio e chat

---

## ⚠️ Requisitos

### **Certificados SSL**
```bash
# Gerar certificados para desenvolvimento
openssl req -x509 -newkey rsa:4096 -nodes \
  -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

### **Variáveis de Ambiente**
```bash
EMAIL_PASSWORD=senha_do_app_gmail
```

### **Banco de Dados**
- SQLite: `app/database/rbcml.db`
- Schema: `app/database/schema.sql`

---

## 📝 Notas Importantes

1. **CORS:** Não configurado - frontend e backend devem estar no mesmo domínio
2. **HTTPS:** Obrigatório para WebRTC funcionar
3. **Socket.IO:** Versão 4.7.5 no frontend
4. **STUN Server:** Usando Google STUN para NAT traversal

---

## 🐛 Troubleshooting

### Email não enviado?
```python
# Verificar senha de app do Gmail
# Habilitar "Acesso a apps menos seguros"
# Ou usar senha de aplicativo
```

### WebRTC não conecta?
```javascript
// Verificar HTTPS está habilitado
// Verificar permissões de câmera/microfone
// Verificar console do navegador
```

### Modelo não aparece na home?
```python
# Verificar se foi salvo no banco:
import sqlite3
conn = sqlite3.connect('app/database/rbcml.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Model")
print(cursor.fetchall())
```

---

## ✅ Checklist de Funcionalidades

- [x] Login/Cadastro com popup
- [x] Criar modelos personalizados
- [x] Listar modelos dinamicamente
- [x] Criar sessões com participantes
- [x] Enviar emails de convite
- [x] Link de convite funcional
- [x] Videochamada WebRTC
- [x] Chat em tempo real
- [x] Controles de áudio/vídeo
- [x] Tutorial JSON
- [ ] Testes completos (pendente)

---

## 📚 Próximos Passos

1. Implementar página de sessões (`/sessionsPage`)
2. Adicionar validação de datas de sessão
3. Implementar gravação de sessões
4. Adicionar compartilhamento de tela
5. Melhorar UI/UX da videochamada
6. Adicionar testes unitários
7. Documentar API REST completa

---

**Data:** Novembro 2024  
**Versão:** 2.0  
**Status:** ✅ Pronto para testes

