# NYC Dogs Dataset Explorer

This project visualizes the geographic distribution of dog breeds and names across NYC zip codes based on the nycdogs.csv dataset.

## Features

- Deduplicate the NYC dogs dataset
- Generate bar charts showing the top zip codes for each breed and name
- Create choropleth maps with NYC zip code boundaries colored by dog distribution
- Interactive web interface to explore distributions
- Flask web application for local viewing
- Netlify deployment option for sharing on the web

## Requirements

- Python 3.6+
- pandas
- matplotlib
- seaborn
- folium
- geopandas
- requests
- flask (for web app)

## Setup

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Make sure your `nycdogs.csv` file is in the root directory

3. Run the preprocessing script:

```bash
python preprocess_data.py
```

This will:
- Load the dataset
- Remove duplicates
- Save a deduplicated version to `data/nycdogs_unique.csv`
- Create example bar chart visualizations in `examples/` directory

4. Create choropleth maps and web interface:

```bash
python create_heatmaps.py
```

This will:
- Use the NYC zip code boundary data from ZCTA.gpkg
- Generate choropleth maps for popular dog breeds in `maps/breeds/`
- Generate choropleth maps for popular dog names in `maps/names/`
- Create a web interface in `website/index.html`

5. Alternatively, run everything at once:

```bash
python run.py
```

## Usage Options

### Option 1: Static HTML

1. Open `website/index.html` in a web browser
2. Select a breed or name from the dropdown to see its geographic distribution
3. Explore different breeds and names to compare distributions

### Option 2: Flask Web App

1. Run the Flask application:

```bash
python app.py
```

2. Open a web browser and navigate to `http://localhost:5000`
3. If data hasn't been processed yet, you'll be prompted to process it
4. Select breeds and names from the dropdowns to see their distributions

### Option 3: Deploy to Netlify

To deploy the application to the web using Netlify:

1. Run the build script to generate a static site:

```bash
python build_netlify.py
```

2. Follow the deployment instructions in `NETLIFY_DEPLOYMENT.md`

## Data Notes

- Only breeds and names with at least 100 dogs are included
- The deduplicated dataset is used for all analyses
- Example bar chart visualizations are saved in the `examples/` directory
- Choropleth maps showing the percentage distribution are saved in the `maps/` directory

## Deployment

See `NETLIFY_DEPLOYMENT.md` for detailed instructions on deploying this application to Netlify. 