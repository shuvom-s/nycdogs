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

GitHub Actions automatically generates the maps when changes are pushed to the repository.

## Running Locally

To run this project locally:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the map generation script: `python generate_netlify_maps.py`
4. Open `index.html` in your browser

## Live Demo

Visit the [NYC Dogs Map](https://shuvom-s.github.io/dogsofnyc/) to see the interactive visualization. 