@echo off
SET PYTHONIOENCODING=utf-8
cd /d "C:\Users\USER\.claude\projects\projet jarvis"
python run_agents.py daily >> agents\logs\daily_run.log 2>&1
