"""
Arquivo de Configuração da Aplicação RBCML
Edite este arquivo para configurar as credenciais de email e outras configurações
"""

import os

class Config:
    """Configurações da aplicação"""
    
    # Configurações do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'rbcml-secret-key-change-in-production')
    DEBUG = True
    
    # Configurações de Email
    # OPÇÃO 1: Usar variável de ambiente (mais seguro)
    EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'rbcmlproject@gmail.com')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', None)
    
    # OPÇÃO 2: Descomentar e preencher diretamente (menos seguro, mas mais fácil para testes)
    # EMAIL_ADDRESS = 'rbcmlproject@gmail.com'
    # EMAIL_PASSWORD = 'sua_senha_aqui'
    
    # Configurações do servidor SMTP
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    # Configurações do servidor
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Configurações SSL
    SSL_CERT = './ssl/cert.pem'
    SSL_KEY = './ssl/key.pem'
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações no app Flask"""
        pass

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    # Em produção, SEMPRE use variáveis de ambiente
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Configuração padrão
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

