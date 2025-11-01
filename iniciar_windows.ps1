# Script PowerShell para iniciar o servidor RBCML no Windows
# Autor: Sistema RBCML
# Data: 2024

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   RBCML Application - Windows" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se está na pasta correta
if (-not (Test-Path "run.py")) {
    Write-Host "[ERRO] Arquivo run.py não encontrado!" -ForegroundColor Red
    Write-Host "Execute este script na pasta RBCML-Application" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Ativar ambiente virtual
Write-Host "[1/5] Ativando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "environment\Scripts\Activate.ps1") {
    & ".\environment\Scripts\Activate.ps1"
    Write-Host "[OK] Ambiente virtual ativado!" -ForegroundColor Green
} else {
    Write-Host "[ERRO] Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "Execute: python -m venv environment" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# Verificar se EMAIL_PASSWORD está configurado
Write-Host "[2/5] Verificando configuração de email..." -ForegroundColor Yellow
if (-not $env:EMAIL_PASSWORD) {
    Write-Host "[AVISO] EMAIL_PASSWORD não configurado!" -ForegroundColor Yellow
    Write-Host "Os emails de convite não serão enviados." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para configurar, execute:" -ForegroundColor Cyan
    Write-Host '$env:EMAIL_PASSWORD="sua_senha_app_gmail"' -ForegroundColor Cyan
    Write-Host ""
    $continuar = Read-Host "Deseja continuar mesmo assim? (S/N)"
    if ($continuar -ne "S" -and $continuar -ne "s") {
        exit 1
    }
} else {
    Write-Host "[OK] EMAIL_PASSWORD configurado!" -ForegroundColor Green
}

Write-Host ""

# Verificar certificados SSL
Write-Host "[3/5] Verificando certificados SSL..." -ForegroundColor Yellow
if ((Test-Path "ssl\cert.pem") -and (Test-Path "ssl\key.pem")) {
    Write-Host "[OK] Certificados SSL encontrados!" -ForegroundColor Green
} else {
    Write-Host "[AVISO] Certificados SSL não encontrados!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para gerar certificados, execute no Git Bash:" -ForegroundColor Cyan
    Write-Host "openssl req -x509 -newkey rsa:4096 -nodes -out ssl/cert.pem -keyout ssl/key.pem -days 365" -ForegroundColor Cyan
    Write-Host ""
    $continuar = Read-Host "Deseja continuar sem SSL? (S/N)"
    if ($continuar -ne "S" -and $continuar -ne "s") {
        exit 1
    }
}

Write-Host ""

# Verificar banco de dados
Write-Host "[4/5] Verificando banco de dados..." -ForegroundColor Yellow
if (Test-Path "app\database\rbcml.db") {
    Write-Host "[OK] Banco de dados encontrado!" -ForegroundColor Green
} else {
    Write-Host "[AVISO] Banco de dados não encontrado!" -ForegroundColor Yellow
    Write-Host "Criando banco de dados..." -ForegroundColor Yellow
    if (Test-Path "app\database\schema.sql") {
        # Criar banco de dados usando Python
        python -c "import sqlite3; conn = sqlite3.connect('app/database/rbcml.db'); conn.close()"
        Write-Host "[OK] Banco de dados criado!" -ForegroundColor Green
    } else {
        Write-Host "[ERRO] Arquivo schema.sql não encontrado!" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

Write-Host ""

# Executar testes
Write-Host "[OPCIONAL] Deseja executar os testes de integração? (S/N)" -ForegroundColor Cyan
$executarTestes = Read-Host
if ($executarTestes -eq "S" -or $executarTestes -eq "s") {
    Write-Host ""
    Write-Host "Executando testes..." -ForegroundColor Yellow
    python test_integration.py
    Write-Host ""
    Read-Host "Pressione Enter para continuar"
}

Write-Host ""

# Iniciar servidor
Write-Host "[5/5] Iniciando servidor..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Servidor iniciando em:" -ForegroundColor Cyan
Write-Host " https://localhost:5000" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

# Aguardar 2 segundos e abrir navegador
Start-Sleep -Seconds 2
Start-Process "https://localhost:5000"

# Iniciar servidor
python run.py

