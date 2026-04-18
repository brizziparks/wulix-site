@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Lancement AISATOU texte...
python aisatou.py
pause
