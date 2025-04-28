@echo off
REM Tworzenie srodowiska wirtualnego
if not exist venv (
    python -m venv venv
    echo Utworzono nowe środowisko wirtualne.
)

REM Aktywacja i instalacja zalezności
call venv\Scripts\activate.bat
python -m pip install -r requirements.txt
pause