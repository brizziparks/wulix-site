@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Lancement AISATOU HUD...
python aisatou_hud.py
pause
