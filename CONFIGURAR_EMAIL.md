# 📧 Como Configurar o Email (Forma Fácil)

## ✅ **Método Recomendado: Arquivo de Configuração**

### **Passo 1: Editar o arquivo config.py**

Abra o arquivo `app/config.py` e procure por esta seção:

```python
# OPÇÃO 2: Descomentar e preencher diretamente (menos seguro, mas mais fácil para testes)
# EMAIL_ADDRESS = 'rbcmlproject@gmail.com'
# EMAIL_PASSWORD = 'sua_senha_aqui'
```

### **Passo 2: Descomentar e preencher**

Remova o `#` e preencha com suas credenciais:

```python
# OPÇÃO 2: Descomentar e preencher diretamente (menos seguro, mas mais fácil para testes)
EMAIL_ADDRESS = 'seuemail@gmail.com'
EMAIL_PASSWORD = 'sua_senha_de_app_aqui'
```

### **Passo 3: Comentar a Opção 1**

Comente as linhas da Opção 1 para não usar variáveis de ambiente:

```python
# OPÇÃO 1: Usar variável de ambiente (mais seguro)
# EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'rbcmlproject@gmail.com')
# EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', None)
```

### **Passo 4: Salvar e pronto!**

Agora você não precisa mais configurar variáveis de ambiente! 🎉

---

## 🔑 **Como Obter a Senha de App do Gmail**

### **Passo 1: Ativar Verificação em 2 Etapas**
1. Acesse: https://myaccount.google.com/security
2. Clique em "Verificação em duas etapas"
3. Ative se ainda não estiver ativo

### **Passo 2: Gerar Senha de App**
1. Acesse: https://myaccount.google.com/apppasswords
2. Faça login se necessário
3. Em "Selecionar app", escolha "Outro (nome personalizado)"
4. Digite: "RBCML Application"
5. Clique em "Gerar"

### **Passo 3: Copiar a Senha**
1. Uma senha de 16 caracteres será gerada
2. Exemplo: `abcd efgh ijkl mnop`
3. Copie essa senha (sem espaços)
4. Cole no arquivo `app/config.py`

---

## 📝 **Exemplo Completo**

Seu arquivo `app/config.py` deve ficar assim:

```python
import os

class Config:
    """Configurações da aplicação"""
    
    SECRET_KEY = 'rbcml-secret-key-change-in-production'
    DEBUG = True
    
    # Configurações de Email
    # OPÇÃO 1: Usar variável de ambiente (comentado)
    # EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'rbcmlproject@gmail.com')
    # EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', None)
    
    # OPÇÃO 2: Direto no código (ATIVO)
    EMAIL_ADDRESS = 'seuemail@gmail.com'
    EMAIL_PASSWORD = 'abcdefghijklmnop'  # Senha de app de 16 caracteres
    
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    HOST = '0.0.0.0'
    PORT = 5000
    
    SSL_CERT = './ssl/cert.pem'
    SSL_KEY = './ssl/key.pem'
```

---

## ⚠️ **IMPORTANTE: Segurança**

### **Para Desenvolvimento (Testes):**
✅ Pode colocar a senha direto no código  
✅ Mais fácil e rápido

### **Para Produção (Deploy):**
❌ NUNCA coloque senhas no código  
✅ Use variáveis de ambiente  
✅ Use a Opção 1 (comentada no exemplo acima)

### **Proteger o Arquivo:**

Adicione ao `.gitignore` para não subir para o GitHub:

```
# .gitignore
app/config.py
*.pyc
__pycache__/
```

---

## 🚀 **Testando**

Depois de configurar, teste:

```bash
python test_integration.py
```

Se aparecer:
```
✅ EMAIL_PASSWORD configurado!
```

Está tudo certo! 🎉

---

## 🔄 **Alternativa: Usar Outro Email**

Se não quiser usar Gmail, você pode usar outros serviços:

### **Outlook/Hotmail:**
```python
EMAIL_ADDRESS = 'seuemail@outlook.com'
EMAIL_PASSWORD = 'sua_senha'
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587
```

### **Yahoo:**
```python
EMAIL_ADDRESS = 'seuemail@yahoo.com'
EMAIL_PASSWORD = 'sua_senha'
SMTP_SERVER = 'smtp.mail.yahoo.com'
SMTP_PORT = 587
```

### **Email Corporativo:**
Consulte as configurações SMTP da sua empresa.

---

## ❓ **Perguntas Frequentes**

### **P: Posso usar minha senha normal do Gmail?**
R: Não! Você precisa gerar uma "senha de app" específica.

### **P: A senha de app tem espaços?**
R: Quando você copia, pode ter espaços. Remova-os ao colar no código.

### **P: Preciso fazer isso toda vez?**
R: Não! Configure uma vez e pronto.

### **P: E se eu não quiser enviar emails?**
R: Deixe `EMAIL_PASSWORD = None`. O sistema vai funcionar, mas não enviará emails.

### **P: É seguro colocar senha no código?**
R: Para testes locais, sim. Para produção, use variáveis de ambiente.

---

## ✅ **Checklist**

- [ ] Abri o arquivo `app/config.py`
- [ ] Descomentei a Opção 2
- [ ] Comentei a Opção 1
- [ ] Gerei senha de app no Gmail
- [ ] Copiei a senha (sem espaços)
- [ ] Colei no `EMAIL_PASSWORD`
- [ ] Salvei o arquivo
- [ ] Testei com `python test_integration.py`
- [ ] Funcionou! 🎉

---

**Pronto! Agora você não precisa mais configurar variáveis de ambiente!** 🚀

