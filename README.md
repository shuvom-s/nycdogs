# NYC Dogs Map

Interactive visualization of NYC dog breeds and names by zip code, showing the geographic distribution of different dog breeds and names across New York City neighborhoods.

## Features

- Choropleth maps for popular dog breeds in NYC
- Choropleth maps for popular dog names in NYC
- Interactive selection of breeds and names
- Tooltips showing details on hover
- Filtering for dogs with at least 500 occurrences in the dataset

## Data Source

This visualization uses data from the [NYC Dog Licensing Dataset](https://data.cityofnewyork.us/Health/NYC-Dog-Licensing-Dataset/nu7n-tubp).

## How It Works

The visualization uses:
- Python for data processing
- GeoPandas for working with geospatial data
- Folium (based on Leaflet.js) for interactive maps
- Bootstrap for the user interface

## Running Locally

### Prerequisites

1. Python 3.8 or newer
2. Required data files:
   - `nycdogs.csv` - The NYC Dog Licensing Dataset
   - `ZCTA.gpkg` - NYC ZIP Code Tabulation Areas shapefile

### Option 1: Using the isolated environment scripts (recommended)

To avoid package compatibility issues, we've provided scripts that run the app in an isolated virtual environment:

**On Linux/Mac:**
```bash
# Make the script executable
chmod +x run_isolated.sh

# Run the app
./run_isolated.sh
```

**On Windows:**
```
run_isolated.bat
```

These scripts will:
1. Create a virtual environment specifically for this project
2. Install the required dependencies with compatible versions
3. Check if the required data files exist
4. Create necessary directories
5. Start the Flask development server

### Option 2: Manual setup

If you prefer to set up manually:

1. Create and activate a virtual environment:
   ```bash
   # On Linux/Mac
   python -m venv dogs_env
   source dogs_env/bin/activate
   
   # On Windows
   python -m venv dogs_env
   dogs_env\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```bash
   python app.py
   ```

### Using the App

Once the server is running, open your browser to: http://localhost:5000

The interface allows you to:
1. Select dog breeds to see their distribution across NYC zip codes
2. Select dog names to see their distribution across NYC zip codes
3. View detailed statistics when hovering over each zip code

## Live Demo

Visit the [NYC Dogs Map](https://shuvom-s.github.io/nycdogs/) to see the interactive visualization. 