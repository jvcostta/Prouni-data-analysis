@echo off
echo =====================================
echo Processando Dados do ProUni
echo =====================================
echo.

cd /d "%~dp0"

:: Ativar ambiente virtual
call venv\Scripts\activate.bat

:: Executar script de processamento
python src\data_processing\clean_data.py

echo.
echo =====================================
echo Processamento concluido!
echo =====================================
pause
