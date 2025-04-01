#!/bin/bash
# Run script for NYC Dogs Map Flask app

echo "=========================================="
echo "NYC Dogs Map - Local Development Launcher"
echo "=========================================="

# Install specific Flask and Werkzeug versions
echo "Installing compatible Flask and Werkzeug versions..."
pip install Flask==2.2.3 Werkzeug==2.2.3

# Check if nycdogs.csv exists
if [ ! -f "nycdogs.csv" ]; then
    echo "Error: nycdogs.csv file not found!"
    echo "Please make sure the dataset is in the current directory."
    exit 1
fi

# Check if ZCTA.gpkg exists
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