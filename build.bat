@echo off
echo Building Application...

:: Create virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install/Upgrade required packages
pip install -r requirements.txt

:: Build the application
pyinstaller --clean --name "نظام_الحضانة" --icon "images/Nursery-icon.ico" --noconsole main.py

echo Build completed!
echo The executable can be found in the 'dist' folder.
pause 