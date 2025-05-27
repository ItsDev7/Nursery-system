@echo off
echo Building ELNADA Application...

:: Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

:: Install/Upgrade required packages
pip install -r requirements.txt

:: Build the application
pyinstaller --clean ELNADA.spec

echo Build completed!
echo The executable can be found in the 'dist' folder.
pause 