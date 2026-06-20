@echo off
chcp 65001 >nul
title Agent IA Strategique OPA/EFA - Mode Local (Edge Computing)

echo.
echo ============================================================
echo  Agent IA Strategique OPA/EFA - Mode Edge (Ollama + Local)
echo ============================================================
echo.

:: Vérifier si Ollama est lancé
echo [1/3] Verification d'Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo      Ollama non detecte. Lancement d'Ollama...
    start "" "ollama" serve
    timeout /t 5 /nobreak >nul
    echo      Ollama lance.
) else (
    echo      Ollama deja actif.
)

:: Vérifier si le modèle est disponible
echo [2/3] Verification du modele llama3...
ollama list 2>nul | findstr "llama3" >nul
if %errorlevel% neq 0 (
    echo      Telechargement du modele llama3 (peut prendre quelques minutes)...
    ollama pull llama3
) else (
    echo      Modele llama3 disponible.
)

:: Lancer l'application
echo [3/3] Lancement de l'Agent IA...
echo.
echo  Ouvrez votre navigateur sur : http://localhost:8501
echo  Dans la barre laterale, selectionnez : Ollama (local / Edge)
echo.
echo  Appuyez sur Ctrl+C pour arreter l'agent.
echo.

streamlit run strategic_agent.py --server.port 8501 --server.headless false

pause
