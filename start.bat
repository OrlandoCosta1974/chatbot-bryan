@echo off
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo Instalando dependências...
pip install -r requirements.txt

echo Iniciando o servidor Flask...
python app.py

pause
