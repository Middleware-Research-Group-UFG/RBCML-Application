# 📞 Sistema de Chamadas RBCML - Instruções de Uso

## 🎯 Visão Geral

O sistema foi remodelado para permitir a criação de videochamadas de forma simples e flexível:

- ✅ **Modelos carregados do `model.json`** (não precisa cadastrar no banco)
- ✅ **Links genéricos compartilháveis** (qualquer pessoa com o link pode entrar)
- ✅ **Usuários não precisam estar pré-cadastrados** (guests são bem-vindos)
- ✅ **Convites automáticos por email**
- ✅ **Chamadas expiram automaticamente** em 24 horas

---

## 🚀 Como Usar

### 1. Login (Apenas Criador da Chamada)

Apenas o **criador** precisa estar logado. Participantes podem entrar via link genérico.

```
1. Acesse https://localhost:5000/home
2. Faça login com suas credenciais
```

### 2. Escolher Modelo de Sala

Na página home, clique em um dos modelos disponíveis:
- **Sala de Aula** (Professor, Aluno)
- **Auditório** (Palestrante, Plateia)
- **Tribunal** (Juiz, Advogado, Réu)

### 3. Adicionar Participantes (Opcional)

Na tela de criação:

```
1. Digite o EMAIL do participante
2. Escolha a ROLE (Professor, Aluno, etc)
3. Clique na seta → para adicionar
4. Repita para cada participante
5. Para remover, clique na tag azul do email
```

**⚠️ Participantes NÃO precisam estar cadastrados no sistema!**

### 4. Iniciar Chamada

```
1. Clique no botão "Iniciar Sessão"
2. Um link será gerado automaticamente
3. Convites serão enviados por email (se configurado)
4. Você será redirecionado para a sala
```

### 5. Compartilhar Link

O link gerado tem este formato:

```
https://seu-servidor.com/call/abc123def
```

**Qualquer pessoa com este link pode entrar!**

---

## 📧 Sistema de Convites por Email

### Configuração (Primeira Vez)

1. Configure o email no arquivo `app/config.py` ou variáveis de ambiente
2. Veja o arquivo `CONFIGURAR_EMAIL.md` para detalhes

### Como Funciona

Quando você adiciona participantes e clica em "Iniciar Sessão":

1. ✉️ Um email é enviado automaticamente para cada participante
2. 📨 O email contém:
   - Nome do criador da chamada
   - Modelo da sala
   - Role atribuída
   - Link direto para entrar
   - Data de expiração

### Exemplo de Email

```
Olá!

joao_silva convidou você para participar de uma videochamada.

Modelo: Sala de Aula
Sua role: Aluno

Clique no link abaixo para entrar:
https://localhost:5000/call/abc123def

A chamada expira em: 2025-11-08T14:30:00-03:00

---
RBCML Application
```

---

## 🔗 Link Genérico - Como Funciona

### Características

- ✅ Não requer login
- ✅ Não requer cadastro prévio
- ✅ Atribui automaticamente uma role
- ✅ Gera username automático para guests (`guest_abc123`)

### Fluxo de Acesso

**Cenário 1: Participante Convidado**
```
1. Recebe email com link
2. Clica no link
3. Entra automaticamente com a role atribuída
```

**Cenário 2: Visitante Desconhecido**
```
1. Recebe link de alguém
2. Clica no link
3. Entra como guest com primeira role disponível
4. Username: guest_abc123
```

---

## 📊 Estrutura das Chamadas

### Armazenamento

As chamadas ativas são armazenadas **em memória** no servidor.

**⚠️ Importante:** Ao reiniciar o servidor, todas as chamadas ativas são perdidas.

**Para Produção:** Use Redis ou banco de dados:

```python
# Em routes.py, substitua:
active_calls = {}

# Por:
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
```

### Expiração

- **Padrão:** 24 horas após criação
- **Automática:** Chamadas expiradas são removidas ao tentar acessá-las

### Dados Armazenados

```json
{
  "call_id": "abc123de",
  "model_name": "Sala de Aula",
  "model": {
    "name": "Sala de Aula",
    "roles": ["Professor", "Aluno"],
    "description": "..."
  },
  "creator": "joao_silva",
  "participants": {
    "maria@example.com": {
      "email": "maria@example.com",
      "roles": ["Aluno"]
    }
  },
  "created_at": "2025-11-07T10:00:00-03:00",
  "expires_at": "2025-11-08T10:00:00-03:00"
}
```

---

## 🔌 API Endpoints

### 1. POST `/api/create-call`

Cria uma nova chamada.

**Requer:** JWT token (cookie)

**Body:**
```json
{
  "model_name": "Sala de Aula",
  "participants": {
    "maria@example.com": {
      "email": "maria@example.com",
      "roles": ["Aluno"]
    }
  }
}
```

**Resposta:**
```json
{
  "success": true,
  "call_id": "abc123de",
  "call_url": "/call/abc123de",
  "share_url": "https://localhost:5000/call/abc123de"
}
```

### 2. GET `/call/<call_id>`

Acessa uma chamada ativa.

**Não requer autenticação**

**Resposta:** Página HTML da videochamada

### 3. POST `/api/send-invites`

Envia convites por email.

**Requer:** JWT token (cookie)

**Body:**
```json
{
  "call_id": "abc123de",
  "invites": [
    {"email": "maria@example.com", "role": "Aluno"},
    {"email": "pedro@example.com", "role": "Professor"}
  ]
}
```

### 4. GET `/api/active-calls`

Lista chamadas ativas do usuário.

**Requer:** JWT token (cookie)

**Resposta:**
```json
{
  "calls": [
    {
      "call_id": "abc123de",
      "model_name": "Sala de Aula",
      "created_at": "2025-11-07T10:00:00-03:00",
      "call_url": "/call/abc123de",
      "is_creator": true
    }
  ]
}
```

### 5. GET `/api/models/<model_name>`

Retorna dados de um modelo do `model.json`.

**Resposta:**
```json
{
  "name": "Sala de Aula",
  "description": "Modelo para salas de aula",
  "roles": ["Professor", "Aluno"],
  "imagem": {
    "src": "images/SalaDeAula.jpg",
    "alt": "Sala de Aula"
  }
}
```

---

## 🛠️ Testes Rápidos

### Teste 1: Chamada Simples

```
1. Login no sistema
2. Escolha "Sala de Aula"
3. NÃO adicione participantes
4. Clique "Iniciar Sessão"
5. Você entra sozinho na sala
```

### Teste 2: Chamada com Participantes

```
1. Login no sistema
2. Escolha "Auditório"
3. Adicione email: test@example.com, Role: Plateia
4. Clique "Iniciar Sessão"
5. Copie o link mostrado
6. Abra em aba anônima
7. Cole o link
8. Veja que entrou sem login!
```

### Teste 3: Email de Convite

```
1. Configure email (veja CONFIGURAR_EMAIL.md)
2. Login no sistema
3. Escolha "Tribunal"
4. Adicione seu próprio email
5. Clique "Iniciar Sessão"
6. Verifique sua caixa de entrada
7. Clique no link do email
```

---

## ⚠️ Limitações Atuais

### 1. Armazenamento em Memória

**Problema:** Chamadas são perdidas ao reiniciar servidor

**Solução para Produção:**
- Use Redis para persistência
- Ou migre para banco de dados

### 2. Sem Controle de Acesso Rígido

**Comportamento:** Qualquer pessoa com o link pode entrar

**Solução (se necessário):**
- Adicionar senha para chamadas
- Validar participantes por email
- Limitar número de participantes

### 3. Email Requer Configuração

**Problema:** Convites não funcionam sem SMTP configurado

**Solução:**
- Configure SMTP no `config.py`
- Ou use serviço como SendGrid, Mailgun

### 4. Roles Automáticas para Guests

**Comportamento:** Guests recebem a primeira role disponível

**Customização possível em:** `app/routes.py`, função `view_call()`

---

## 🔒 Segurança

### Recomendações para Produção

1. **IDs de Chamada Longos**
```python
# Em routes.py:
call_id = str(uuid.uuid4())  # ID completo
# Em vez de:
call_id = str(uuid.uuid4())[:8]  # ID curto
```

2. **Expiração Configurável**
```python
# Permitir criador definir tempo de expiração
expiration_hours = data.get('expiration_hours', 24)
```

3. **Limite de Participantes**
```python
# Verificar número de participantes
if len(active_participants) >= MAX_PARTICIPANTS:
    return error("Chamada cheia")
```

4. **Logs de Acesso**
```python
# Registrar quem entra
log_access(call_id, user_tag, ip_address)
```

---

## 📝 Exemplos de Uso

### Exemplo 1: Aula Online

```
Professor:
1. Login como "prof_joao"
2. Escolhe "Sala de Aula"
3. Adiciona emails dos 30 alunos como "Aluno"
4. Clica "Iniciar Sessão"
5. Alunos recebem email
6. Alunos clicam no link e entram

Resultado:
- Professor tem controle total
- Alunos entram facilmente
- Ninguém precisou cadastrar senha
```

### Exemplo 2: Reunião Rápida

```
Gerente:
1. Login como "gerente_maria"
2. Escolhe "Auditório"
3. NÃO adiciona participantes
4. Clica "Iniciar Sessão"
5. Copia link gerado
6. Cola no WhatsApp da equipe
7. Equipe clica e entra

Resultado:
- Reunião criada em 10 segundos
- Sem burocracia
- Todos entram como "Plateia"
```

---

## 🆘 Solução de Problemas

### "Chamada não encontrada"

**Causas:**
- Servidor foi reiniciado
- Chamada expirou (>24h)
- ID incorreto no link

**Solução:** Criar nova chamada

### "Erro ao enviar convites"

**Causas:**
- SMTP não configurado
- Email inválido
- Servidor de email offline

**Solução:** 
- Verifique `CONFIGURAR_EMAIL.md`
- Use link genérico em vez de email

### "Unauthorized"

**Causas:**
- Não está logado
- JWT expirou

**Solução:** Faça login novamente

### Participantes não aparecem na lista

**Causa:** Bug no WebRTC/Socket.IO

**Solução:** 
- Recarregue a página
- Verifique console (F12)
- Veja logs do servidor

---

## 🎓 Tutoriais em Vídeo (Sugeridos)

1. **Criando Sua Primeira Chamada** (2 min)
2. **Adicionando Participantes** (3 min)
3. **Compartilhando Links** (2 min)
4. **Configurando Email** (5 min)
5. **Personalizando Modelos** (10 min)

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique logs do servidor: `python3 run.py`
2. Console do navegador (F12)
3. Arquivo de issues no GitHub

---

## 🚀 Próximos Passos

Possíveis melhorias futuras:

1. ✨ Persistência em Redis
2. 🔐 Senha opcional para chamadas
3. 👥 Sala de espera (host aprova entrada)
4. 📊 Estatísticas de uso
5. 🎨 Temas personalizáveis
6. 📱 App mobile
7. 🔗 Integração com calendário
8. 🎥 Gravação de chamadas

---

**Versão:** 1.0  
**Última atualização:** Novembro 2025  
**Autor:** Sistema RBCML

