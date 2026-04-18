@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Lancement AISATOU vocal...
python aisatou.py --voice
pause
