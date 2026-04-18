@echo off
echo ============================================
echo   Installation de AISATOU
echo   Agente Intelligente pour la Supervision,
echo   l'Automatisation des Taches et
echo   l'Organisation Universelle
echo ============================================
echo.

:: Vérifie que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo Telecharge Python sur https://python.org
    pause
    exit /b 1
)

echo [1/4] Creation de l'environnement virtuel...
python -m venv .venv
call .venv\Scripts\activate.bat

echo [2/4] Mise a jour de pip...
python -m pip install --upgrade pip --quiet

echo [3/4] Installation des dependances...
pip install -r requirements.txt

echo [4/4] Configuration...
if not exist .env (
    copy .env.example .env
    echo.
    echo [IMPORTANT] Le fichier .env a ete cree.
    echo Ouvre-le et ajoute ta cle API Anthropic ^(ANTHROPIC_API_KEY^).
    echo Obtiens-la sur : https://console.anthropic.com/
    echo.
    notepad .env
)

echo.
echo ============================================
echo   Installation terminee !
echo ============================================
echo.
echo Pour lancer AISATOU :
echo   Mode texte  : python aisatou.py
echo   Mode vocal  : python aisatou.py --voice
echo.
pause
