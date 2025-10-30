@echo off

REM Remove existing virtual environments
if exist .venv rmdir /s /q .venv
if exist .venv_clean rmdir /s /q .venv_clean

REM Create a new virtual environment
py -m venv .venv

REM Activate and install requirements
call .venv\Scripts\activate.bat
pip install --upgrade pip
pip install torch transformers

REM Create a requirements.txt file
echo torch>=2.0.0 > requirements.txt
echo transformers>=4.30.0 >> requirements.txt

echo.
echo Environment setup complete!
echo Use the following commands to activate the environment:
echo .venv\Scripts\activate.bat
