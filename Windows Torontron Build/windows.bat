@echo off
REM Arcade Launcher Setup & Run Script (WINDOWS VER)

SET DIR=%cd%
SET VENV_PATH=%DIR%\venv

REM Check if venv exists
IF NOT EXIST "%VENV_PATH%" (
    echo First-time setup: Creating Virtual Environment...
    py -m venv "%VENV_PATH%"
    call "%VENV_PATH%\Scripts\activate.bat"
    echo Installing requirements...
    python -m pip install --upgrade pip setuptools wheel
    pip install py5
    pip install pynput
) ELSE (
    echo Environment detected - launching instantly ...
    call "%VENV_PATH%\Scripts\activate.bat"
)

REM Launch the game launcher
python "%DIR%\launcherWindows.py"
