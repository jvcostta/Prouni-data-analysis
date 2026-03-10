@echo off
echo =====================================
echo Iniciando Dashboard ProUni
echo =====================================
echo.

cd /d "%~dp0"

:: Ativar ambiente virtual
call venv\Scripts\activate.bat

:: Executar dashboard
python app.py

pause
