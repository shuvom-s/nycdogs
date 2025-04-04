#!/usr/bin/env python3
"""
Generate maps for dog breeds and names in NYC with at least 500 dogs.

This script will:
1. Ensure data exists by running preprocessing if necessary
2. Generate maps for all dog breeds and names with at least 500 dogs
3. Create a simple website to display the maps
"""

import os
import json
import shutil
import subprocess
from pathlib import Path
import pandas as pd

def ensure_data_exists():
    """Make sure the data directory exists with required JSON files"""
    print("Checking if data exists...")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Check if the required JSON files exist
    breeds_file = Path("data/popular_breeds.json")
    names_file = Path("data/popular_names.json")
    
    if not breeds_file.exists() or not names_file.exists():
        print("Data files missing. Running preprocessing script...")
        # Run the preprocessing script
        subprocess.run(["python", "preprocess_data.py"], check=True)
    
    # Verify the files exist now
    if not breeds_file.exists() or not names_file.exists():
        raise FileNotFoundError("Required data files could not be created. Please run preprocess_data.py manually.")
    
    print("Data files verified.")

def generate_maps_by_count(min_count=500):
    """Generate maps for all breeds and names with at least min_count dogs"""
    print(f"Generating maps for breeds and names with at least {min_count} dogs...")
    
    # Load the breed data
    with open("data/popular_breeds.json", "r") as f:
        breed_data = json.load(f)
    
    # Load the name data
    with open("data/popular_names.json", "r") as f:
        name_data = json.load(f)
    
    # Create directories for maps
    os.makedirs("maps/breeds", exist_ok=True)
    os.makedirs("maps/names", exist_ok=True)
    
    # Import the necessary functions and modules for map creation
    from create_heatmaps import get_nyc_zipcode_geojson, create_breed_map, create_name_map
    
    # Get the NYC zipcode GeoJSON
    nyc_zipcodes = get_nyc_zipcode_geojson()
    
    # Filter breeds by minimum count
    filtered_breeds = {breed: info for breed, info in breed_data.items() 
                      if info.get('total_count', 0) >= min_count}
    
    # Filter names by minimum count
    filtered_names = {name: info for name, info in name_data.items() 
                     if info.get('total_count', 0) >= min_count}
    
    # Sort breeds and names by total count
    sorted_breeds = sorted(filtered_breeds.items(), key=lambda x: x[1].get('total_count', 0), reverse=True)
    sorted_names = sorted(filtered_names.items(), key=lambda x: x[1].get('total_count', 0), reverse=True)
    
    print(f"Found {len(sorted_breeds)} breeds and {len(sorted_names)} names with at least {min_count} dogs")
    
    # Generate maps for breeds
    print(f"Generating breed maps...")
    for i, (breed, info) in enumerate(sorted_breeds):
        print(f"Processing {i+1}/{len(sorted_breeds)}: {breed}")
        create_breed_map(breed, info, nyc_zipcodes)
    
    # Generate maps for names
    print(f"Generating name maps...")
    for i, (name, info) in enumerate(sorted_names):
        print(f"Processing {i+1}/{len(sorted_names)}: {name}")
        create_name_map(name, info, nyc_zipcodes)
    
    print(f"Generated {len(sorted_breeds)} breed maps and {len(sorted_names)} name maps")
    
    # Save the filtered breeds and names data for the website
    filtered_breeds_dict = {breed: info for breed, info in sorted_breeds}
    filtered_names_dict = {name: info for name, info in sorted_names}
    
    with open("maps/filtered_breeds.json", "w") as f:
        json.dump(filtered_breeds_dict, f)
    
    with open("maps/filtered_names.json", "w") as f:
        json.dump(filtered_names_dict, f)
    
    return filtered_breeds_dict, filtered_names_dict

def create_website(filtered_breeds, filtered_names):
    """Generate HTML file to display the maps"""
    print("Creating website...")
    
    # Create HTML content
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NYC Dog Population Maps</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding-top: 20px;
            padding-bottom: 40px;
            background-color: #f8f9fa;
        }
        .map-container {
            height: 75vh;
            width: 100%;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
        }
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
        .btn-selector {
            margin-bottom: 10px;
        }
        h1, h2, h3 {
            color: #343a40;
        }
        .nav-tabs {
            margin-bottom: 20px;
        }
        .github-link {
            margin-top: 15px;
        }
        .selector-row {
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12 text-center">
                <h1>NYC Dog Population Visualization</h1>
                <p class="lead">Explore the distribution of dog breeds and names across NYC zip codes</p>
                <div class="github-link">
                    <a href="https://github.com/shuvom-s/dogsofnyc" target="_blank" class="btn btn-outline-secondary">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.7-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                        </svg>
                        View on GitHub
                    </a>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <ul class="nav nav-tabs" id="mapTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="breeds-tab" data-bs-toggle="tab" data-bs-target="#breeds" type="button" role="tab" aria-controls="breeds" aria-selected="true">Dog Breeds</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="names-tab" data-bs-toggle="tab" data-bs-target="#names" type="button" role="tab" aria-controls="names" aria-selected="false">Dog Names</button>
                    </li>
                </ul>
                <div class="tab-content" id="mapTabsContent">
                    <div class="tab-pane fade show active" id="breeds" role="tabpanel" aria-labelledby="breeds-tab">
                        <div class="row selector-row">
                            <div class="col">
                                <label for="breedSelector" class="form-label">Select a dog breed:</label>
                                <select class="form-select" id="breedSelector">
                                    <!-- Breed options will be inserted here by JavaScript -->
                                </select>
                            </div>
                        </div>
                        <div class="map-container">
                            <iframe id="breedMap" src="maps/breeds/FIRST_BREED_MAP.html"></iframe>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="names" role="tabpanel" aria-labelledby="names-tab">
                        <div class="row selector-row">
                            <div class="col">
                                <label for="nameSelector" class="form-label">Select a dog name:</label>
                                <select class="form-select" id="nameSelector">
                                    <!-- Name options will be inserted here by JavaScript -->
                                </select>
                            </div>
                        </div>
                        <div class="map-container">
                            <iframe id="nameMap" src="maps/names/FIRST_NAME_MAP.html"></iframe>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">About This Project</h5>
                        <p class="card-text">
                            This visualization shows the distribution of the most popular dog breeds and names across New York City, 
                            based on zipcode data. The heatmaps display where specific breeds and names are most concentrated.
                        </p>
                        <p class="card-text">
                            Data source: <a href="https://data.cityofnewyork.us/Health/NYC-Dog-Licensing-Dataset/nu7n-tubp" target="_blank">NYC Dog Licensing Dataset</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
        // Load breed and name data and populate selectors
        document.addEventListener('DOMContentLoaded', function() {
            // Breed data
            const breedData = BREED_DATA_PLACEHOLDER;
            const breedSelector = document.getElementById('breedSelector');
            const firstBreed = Object.keys(breedData)[0];
            
            // Populate breed selector
            for (const breed in breedData) {
                const option = document.createElement('option');
                option.value = breed;
                option.textContent = `${breed} (${breedData[breed].total_count} dogs)`;
                breedSelector.appendChild(option);
            }
            
            // Set first breed map
            document.getElementById('breedMap').src = `maps/breeds/${firstBreed.replace('/', '_').replace(' ', '_')}_map.html`;
            
            // Add event listener for breed selection
            breedSelector.addEventListener('change', function() {
                const selectedBreed = this.value;
                const safeBreed = selectedBreed.replace('/', '_').replace(' ', '_');
                document.getElementById('breedMap').src = `maps/breeds/${safeBreed}_map.html`;
            });
            
            // Name data
            const nameData = NAME_DATA_PLACEHOLDER;
            const nameSelector = document.getElementById('nameSelector');
            const firstName = Object.keys(nameData)[0];
            
            // Populate name selector
            for (const name in nameData) {
                const option = document.createElement('option');
                option.value = name;
                option.textContent = `${name} (${nameData[name].total_count} dogs)`;
                nameSelector.appendChild(option);
            }
            
            // Set first name map
            document.getElementById('nameMap').src = `maps/names/${firstName.replace('/', '_').replace(' ', '_')}_map.html`;
            
            // Add event listener for name selection
            nameSelector.addEventListener('change', function() {
                const selectedName = this.value;
                const safeName = selectedName.replace('/', '_').replace(' ', '_');
                document.getElementById('nameMap').src = `maps/names/${safeName}_map.html`;
            });
        });
    </script>
</body>
</html>
"""
    
    # Replace placeholders with actual data
    html_content = html_content.replace('BREED_DATA_PLACEHOLDER', json.dumps(filtered_breeds))
    html_content = html_content.replace('NAME_DATA_PLACEHOLDER', json.dumps(filtered_names))
    
    # Get the first breed and name to set default maps
    first_breed = list(filtered_breeds.keys())[0].replace('/', '_').replace(' ', '_')
    first_name = list(filtered_names.keys())[0].replace('/', '_').replace(' ', '_')
    
    html_content = html_content.replace('FIRST_BREED_MAP.html', f"{first_breed}_map.html")
    html_content = html_content.replace('FIRST_NAME_MAP.html', f"{first_name}_map.html")
    
    # Write the HTML file
    with open("index.html", "w") as f:
        f.write(html_content)
    
    print("Created website in index.html")

def main():
    """Main function to run all steps"""
    # Step 1: Ensure data exists
    ensure_data_exists()
    
    # Step 2: Generate maps for breeds and names with at least 500 dogs
    filtered_breeds, filtered_names = generate_maps_by_count(min_count=500)
    
    # Step 3: Create website
    create_website(filtered_breeds, filtered_names)
    
    print("Done! The maps and website are ready.")

if __name__ == "__main__":
    main() 