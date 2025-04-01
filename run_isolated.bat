@echo off
echo ==========================================
echo NYC Dogs Map - Isolated Environment Runner
echo ==========================================

REM Check if virtual environment exists, if not create it
if not exist dogs_env\ (
    echo Creating virtual environment...
    python -m venv dogs_env
)

REM Activate the virtual environment
echo Activating virtual environment...
call dogs_env\Scripts\activate.bat

REM Install dependencies
echo Installing required packages...
pip install -r requirements.txt

REM Check data files
if not exist nycdogs.csv (
    echo Error: nycdogs.csv file not found!
    echo Please make sure the dataset is in the current directory.
    call dogs_env\Scripts\deactivate.bat
    exit /b 1
)

if not exist ZCTA.gpkg (
    echo Error: ZCTA.gpkg file not found!
    echo Please make sure the shapefile is in the current directory.
    call dogs_env\Scripts\deactivate.bat
    exit /b 1
)

REM Create necessary directories
mkdir data 2>nul
mkdir maps\breeds 2>nul
mkdir maps\names 2>nul
mkdir templates 2>nul
mkdir static 2>nul

echo Starting Flask app...
python app.py

REM Deactivate the virtual environment when done
call dogs_env\Scripts\deactivate.bat 