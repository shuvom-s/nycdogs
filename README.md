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

### Setup

#### Option 1: Using the setup scripts (recommended)

**On Linux/Mac:**
```bash
# Make the script executable
chmod +x run_local.sh

# Run the app
./run_local.sh
```

**On Windows:**
```
run_local.bat
```

These scripts will:
1. Install the required dependencies with the correct versions
2. Check if the required data files exist
3. Create necessary directories
4. Start the Flask development server

#### Option 2: Manual setup

1. Install specific versions of Flask and Werkzeug:
   ```bash
   pip install Flask==2.2.3 Werkzeug==2.2.3
   ```

2. Install other dependencies:
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

## Troubleshooting

If you encounter issues:

1. **Flask import errors**: Make sure you have Flask 2.2.3 and Werkzeug 2.2.3 installed:
   ```bash
   pip install Flask==2.2.3 Werkzeug==2.2.3
   ```

2. **Missing files**: Ensure both `nycdogs.csv` and `ZCTA.gpkg` are in the project root directory

3. **Other package errors**: Try the setup helper:
   ```bash
   python setup_local.py
   ```

## Live Demo

Visit the [NYC Dogs Map](https://shuvom-s.github.io/nycdogs/) to see the interactive visualization. 