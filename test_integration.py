#!/usr/bin/env python3
"""
Script de teste de integração para verificar se o backend está funcionando corretamente
"""

import sqlite3
import json
from pathlib import Path

def test_database_connection():
    """Testa conexão com o banco de dados"""
    print("🔍 Testando conexão com banco de dados...")
    try:
        db_path = Path("app/database/rbcml.db")
        if not db_path.exists():
            print("❌ Banco de dados não encontrado!")
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"✅ Tabelas encontradas: {[t[0] for t in tables]}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_models_in_database():
    """Verifica se existem modelos no banco"""
    print("\n🔍 Verificando modelos no banco...")
    try:
        db_path = Path("app/database/rbcml.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT Id, Name, Description FROM Model")
        models = cursor.fetchall()
        
        if models:
            print(f"✅ {len(models)} modelo(s) encontrado(s):")
            for model in models:
                print(f"   - ID: {model[0]}, Nome: {model[1]}")
        else:
            print("⚠️  Nenhum modelo encontrado. Você precisa criar modelos primeiro.")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_users_in_database():
    """Verifica se existem usuários no banco"""
    print("\n🔍 Verificando usuários no banco...")
    try:
        db_path = Path("app/database/rbcml.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT Tag, Name, Email FROM User")
        users = cursor.fetchall()
        
        if users:
            print(f"✅ {len(users)} usuário(s) encontrado(s):")
            for user in users:
                print(f"   - Tag: {user[0]}, Nome: {user[1]}, Email: {user[2]}")
        else:
            print("⚠️  Nenhum usuário encontrado. Você precisa criar uma conta primeiro.")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def test_static_files():
    """Verifica se os arquivos estáticos necessários existem"""
    print("\n🔍 Verificando arquivos estáticos...")
    
    required_files = [
        "app/static/scripts/start_call.js",
        "app/static/scripts/roles.js",
        "app/static/scripts/log_sing.js",
        "app/static/scripts/channel.js",
        "app/static/scripts/connections.js",
        "app/static/scripts/userMedia.js",
        "app/static/styles/home.css",
        "app/static/styles/log_sing.css",
        "app/static/styles/howtojson.css",
        "app/static/images/logo.png",
        "app/static/images/plus.png",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NÃO ENCONTRADO")
            all_exist = False
    
    return all_exist

def test_templates():
    """Verifica se os templates necessários existem"""
    print("\n🔍 Verificando templates...")
    
    required_templates = [
        "app/templates/home.html",
        "app/templates/createModel.html",
        "app/templates/createcall.html",
        "app/templates/session.html",
        "app/templates/howtojson.html",
        "app/templates/sessionsPage.html",
    ]
    
    all_exist = True
    for template_path in required_templates:
        path = Path(template_path)
        if path.exists():
            print(f"✅ {template_path}")
        else:
            print(f"❌ {template_path} - NÃO ENCONTRADO")
            all_exist = False
    
    return all_exist

def test_ssl_certificates():
    """Verifica se os certificados SSL existem"""
    print("\n🔍 Verificando certificados SSL...")
    
    cert_path = Path("ssl/cert.pem")
    key_path = Path("ssl/key.pem")
    
    if cert_path.exists() and key_path.exists():
        print("✅ Certificados SSL encontrados")
        return True
    else:
        print("⚠️  Certificados SSL não encontrados")
        print("   Execute: openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365")
        return False

def test_environment_variables():
    """Verifica variáveis de ambiente"""
    print("\n🔍 Verificando variáveis de ambiente...")
    
    import os
    
    email_password = os.getenv("EMAIL_PASSWORD")
    if email_password:
        print("✅ EMAIL_PASSWORD configurado")
        return True
    else:
        print("⚠️  EMAIL_PASSWORD não configurado")
        print("   Execute: export EMAIL_PASSWORD='sua_senha_app_gmail'")
        return False

def create_sample_model():
    """Cria um modelo de exemplo no banco de dados"""
    print("\n🔧 Criando modelo de exemplo...")
    
    try:
        db_path = Path("app/database/rbcml.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se já existe
        cursor.execute("SELECT * FROM Model WHERE Name='Sala de Aula Exemplo'")
        if cursor.fetchone():
            print("⚠️  Modelo de exemplo já existe")
            conn.close()
            return True
        
        # Criar modelo
        definition = {
            "roles": ["Professor", "Aluno"],
            "connections": {
                "Aluno-Professor": [
                    [True, True, True, True, True, True, False, False],
                    [True, True, True, True, True, True, False, False]
                ]
            }
        }
        
        cursor.execute("""
            INSERT INTO Model (Name, Description, Definition)
            VALUES (?, ?, ?)
        """, (
            "Sala de Aula Exemplo",
            "Modelo de exemplo para testes",
            json.dumps(definition)
        ))
        
        conn.commit()
        conn.close()
        
        print("✅ Modelo de exemplo criado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar modelo: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🧪 TESTE DE INTEGRAÇÃO - RBCML APPLICATION")
    print("=" * 60)
    
    results = []
    
    results.append(("Conexão com Banco de Dados", test_database_connection()))
    results.append(("Modelos no Banco", test_models_in_database()))
    results.append(("Usuários no Banco", test_users_in_database()))
    results.append(("Arquivos Estáticos", test_static_files()))
    results.append(("Templates", test_templates()))
    results.append(("Certificados SSL", test_ssl_certificates()))
    results.append(("Variáveis de Ambiente", test_environment_variables()))
    
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:.<40} {status}")
    
    print(f"\n{passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! O sistema está pronto para uso.")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")
    
    # Oferecer criar modelo de exemplo
    if passed >= 5:  # Se a maioria dos testes passou
        print("\n" + "=" * 60)
        response = input("Deseja criar um modelo de exemplo? (s/n): ")
        if response.lower() == 's':
            create_sample_model()
    
    print("\n" + "=" * 60)
    print("Para iniciar o servidor, execute: python run.py")
    print("=" * 60)

if __name__ == "__main__":
    main()

