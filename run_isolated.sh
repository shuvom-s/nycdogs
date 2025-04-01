#!/bin/bash
# Run the NYC Dogs Map app in an isolated environment

echo "=========================================="
echo "NYC Dogs Map - Isolated Environment Runner"
echo "=========================================="

# Check if virtual environment exists, if not create it
if [ ! -d "dogs_env" ]; then
    echo "Creating virtual environment..."
    python -m venv dogs_env
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source dogs_env/bin/activate

# Install dependencies
echo "Installing required packages..."
pip install -r requirements.txt

# Check data files
if [ ! -f "nycdogs.csv" ]; then
    echo "Error: nycdogs.csv file not found!"
    echo "Please make sure the dataset is in the current directory."
    exit 1
fi

if [ ! -f "ZCTA.gpkg" ]; then
    echo "Error: ZCTA.gpkg file not found!"
    echo "Please make sure the shapefile is in the current directory."
    exit 1
fi

# Create necessary directories
mkdir -p data
mkdir -p maps/breeds
mkdir -p maps/names
mkdir -p templates
mkdir -p static

echo "Starting Flask app..."
python app.py

# Deactivate the virtual environment when done
deactivate 