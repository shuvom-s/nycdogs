@echo off
echo ==========================================
echo NYC Dogs Map - Local Development Launcher
echo ==========================================

REM Install specific Flask and Werkzeug versions
echo Installing compatible Flask and Werkzeug versions...
pip install Flask==2.2.3 Werkzeug==2.2.3

REM Check if nycdogs.csv exists
if not exist nycdogs.csv (
    echo Error: nycdogs.csv file not found!
    echo Please make sure the dataset is in the current directory.
    exit /b 1
)

REM Check if ZCTA.gpkg exists
if not exist ZCTA.gpkg (
    echo Error: ZCTA.gpkg file not found!
    echo Please make sure the shapefile is in the current directory.
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