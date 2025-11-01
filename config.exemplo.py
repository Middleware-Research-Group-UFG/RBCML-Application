"""
ARQUIVO DE EXEMPLO - COPIE ESTE ARQUIVO PARA app/config.py E EDITE

Como usar:
1. Copie este arquivo: cp config.exemplo.py app/config.py
2. Edite app/config.py
3. Preencha EMAIL_PASSWORD com sua senha
4. Salve e execute o servidor
"""

import os

class Config:
    """Configurações da aplicação"""
    
    # Configurações do Flask
    SECRET_KEY = 'rbcml-secret-key-change-in-production'
    DEBUG = True
    
    # ============================================
    # CONFIGURAÇÕES DE EMAIL
    # ============================================
    
    # Email remetente (Gmail)
    EMAIL_ADDRESS = 'rbcmlproject@gmail.com'
    
    # PREENCHA AQUI COM SUA SENHA DE APP DO GMAIL
    EMAIL_PASSWORD = 'COLOQUE_SUA_SENHA_AQUI'
    
    # Como obter a senha:
    # 1. Acesse: https://myaccount.google.com/apppasswords
    # 2. Faça login na sua conta Google
    # 3. Clique em "Gerar" para criar uma senha de app
    # 4. Copie a senha gerada (16 caracteres)
    # 5. Cole aqui substituindo 'COLOQUE_SUA_SENHA_AQUI'
    
    # ============================================
    
    # Configurações do servidor SMTP
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    # Configurações do servidor
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Configurações SSL
    SSL_CERT = './ssl/cert.pem'
    SSL_KEY = './ssl/key.pem'

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

