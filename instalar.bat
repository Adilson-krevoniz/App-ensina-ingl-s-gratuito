@echo off
color 0A
echo ===============================================
echo    INSTALACAO DO BOT DE WHATSAPP ALEX
echo ===============================================
echo.
echo Este script vai iniciar o assistente de instalacao
echo do bot de WhatsApp para ensino de ingles.
echo.
echo Pressione qualquer tecla para continuar...
pause > nul

REM Verificar se o Python esta instalado
where python > nul 2>&1
if %ERRORLEVEL% neq 0 (
    color 0C
    echo.
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.8 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo Certifique-se de marcar a opcao "Add Python to PATH"
    echo durante a instalacao.
    echo.
    echo Pressione qualquer tecla para abrir o site de download...
    pause > nul
    start https://www.python.org/downloads/
    echo.
    echo Apos instalar o Python, execute este script novamente.
    pause
    exit /b 1
)

REM Executar o script de instalacao Python
echo.
echo Iniciando o assistente de instalacao...
echo.
python instalar.py

REM Se o script Python falhar
if %ERRORLEVEL% neq 0 (
    color 0C
    echo.
    echo Ocorreu um erro durante a instalacao.
    echo Por favor, verifique as mensagens acima.
    echo.
    pause
    exit /b 1
)

exit /b 0