@echo off
pip install mysql-connector-python -q
python "%~dp0bank_mysql.py"
pause
