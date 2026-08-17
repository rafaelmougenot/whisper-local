@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"

if not exist "WHISPER_LOCAL_PORTATIL.exe" (
    echo ERRO: O executável WHISPER_LOCAL_PORTATIL.exe não foi encontrado.
    echo Esta pasta é o modelo da distribuição. Gere a versão portátil com build.ps1.
    pause
    exit /b 1
)

"%~dp0WHISPER_LOCAL_PORTATIL.exe" %*
set "RESULTADO=%ERRORLEVEL%"

echo.
if "%RESULTADO%"=="0" (
    echo Finalizado. Veja os arquivos na pasta output.
) else if "%RESULTADO%"=="2" (
    echo Nenhum arquivo foi processado.
) else (
    echo A execução terminou com erro. Veja a mensagem acima.
)
pause
exit /b %RESULTADO%
