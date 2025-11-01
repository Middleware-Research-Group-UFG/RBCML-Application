@echo off
REM Script para iniciar o servidor RBCML no Windows
REM Autor: Sistema RBCML
REM Data: 2024

echo ========================================
echo    RBCML Application - Windows
echo ========================================
echo.

REM Verificar se está na pasta correta
if not exist "run.py" (
    echo [ERRO] Arquivo run.py nao encontrado!
    echo Execute este script na pasta RBCML-Application
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo [1/5] Ativando ambiente virtual...
if exist "environment\Scripts\activate.bat" (
    call environment\Scripts\activate.bat
    echo [OK] Ambiente virtual ativado!
) else (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute: python -m venv environment
    pause
    exit /b 1
)

echo.

REM Verificar se EMAIL_PASSWORD está configurado
echo [2/5] Verificando configuracao de email...
if "%EMAIL_PASSWORD%"=="" (
    echo [AVISO] EMAIL_PASSWORD nao configurado!
    echo Os emails de convite nao serao enviados.
    echo.
    echo Para configurar, execute:
    echo set EMAIL_PASSWORD=sua_senha_app_gmail
    echo.
    set /p continuar="Deseja continuar mesmo assim? (S/N): "
    if /i not "%continuar%"=="S" exit /b 1
) else (
    echo [OK] EMAIL_PASSWORD configurado!
)

echo.

REM Verificar certificados SSL
echo [3/5] Verificando certificados SSL...
if exist "ssl\cert.pem" (
    if exist "ssl\key.pem" (
        echo [OK] Certificados SSL encontrados!
    ) else (
        echo [AVISO] Certificado key.pem nao encontrado!
        goto :ssl_warning
    )
) else (
    :ssl_warning
    echo [AVISO] Certificados SSL nao encontrados!
    echo.
    echo Para gerar certificados, execute no Git Bash:
    echo openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365
    echo.
    set /p continuar="Deseja continuar sem SSL? (S/N): "
    if /i not "%continuar%"=="S" exit /b 1
)

echo.

REM Verificar banco de dados
echo [4/5] Verificando banco de dados...
if exist "app\database\rbcml.db" (
    echo [OK] Banco de dados encontrado!
) else (
    echo [AVISO] Banco de dados nao encontrado!
    echo Criando banco de dados...
    if exist "app\database\schema.sql" (
        sqlite3 app\database\rbcml.db < app\database\schema.sql
        echo [OK] Banco de dados criado!
    ) else (
        echo [ERRO] Arquivo schema.sql nao encontrado!
        pause
        exit /b 1
    )
)

echo.

REM Iniciar servidor
echo [5/5] Iniciando servidor...
echo.
echo ========================================
echo  Servidor iniciando em:
echo  https://localhost:5000
echo ========================================
echo.
echo Pressione Ctrl+C para parar o servidor
echo.

python run.py

pause

