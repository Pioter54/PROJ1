@echo off
REM Tworzenie środowiska wirtualnego (jeśli nie istnieje)
if not exist venv (
    python -m venv venv
    echo Utworzono nowe środowisko wirtualne.
)

REM Aktywacja i instalacja zależności
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt
pause