#!/usr/bin/env python3
"""
Build script for Netlify deployment.
This script processes the NYC Dogs dataset and creates a static website.
"""

import os
import json
import shutil
from run import main as run_preprocessing
from create_heatmaps import create_breed_choropleth_maps, create_name_choropleth_maps, create_web_interface

def build_static_site():
    print("="*60)
    print("Building NYC Dogs Static Site for Netlify")
    print("="*60)
    
    # Create output directory for Netlify
    netlify_dir = 'netlify_build'
    os.makedirs(netlify_dir, exist_ok=True)
    
    # Run the preprocessing pipeline
    print("\nStep 1: Processing data...")
    try:
        run_preprocessing()
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return
    
    # Create index.html for Netlify
    print("\nStep 2: Creating static HTML files...")
    try:
        # Load breed data
        with open('data/popular_breeds.json', 'r') as f:
            breed_data = json.load(f)
        
        # Load name data
        with open('data/popular_names.json', 'r') as f:
            name_data = json.load(f)
        
        # Filter for breeds and names with at least 500 dogs
        filtered_breeds = {breed: info for breed, info in breed_data.items() if info['total_count'] >= 500}
        filtered_names = {name: info for name, info in name_data.items() if info['total_count'] >= 500}
        
        print(f"Found {len(filtered_breeds)} breeds and {len(filtered_names)} names with at least 500 dogs")
        
        # Sort breeds and names by total count
        sorted_breeds = sorted(filtered_breeds.items(), key=lambda x: x[1]['total_count'], reverse=True)
        sorted_names = sorted(filtered_names.items(), key=lambda x: x[1]['total_count'], reverse=True)
        
        # Create index.html with the sorted breeds and names embedded directly
        with open(f'{netlify_dir}/index.html', 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NYC Dogs - Geographic Distribution</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <style>
        body { 
            padding: 20px; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .map-container { 
            height: 600px; 
            margin-top: 20px; 
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
        }
        iframe { 
            width: 100%; 
            height: 100%; 
            border: none; 
        }
        .card {
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .card-header {
            background-color: #4a6fa5;
            color: white;
            font-weight: bold;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
        }
        .form-select {
            cursor: pointer;
        }
        .intro {
            margin-bottom: 30px;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">NYC Dogs - Geographic Distribution</h1>
        
        <div class="intro">
            <p>Welcome to the NYC Dogs Geographic Distribution viewer! This application visualizes the distribution of dog breeds and names across New York City's zip codes. Select a breed or name from the dropdown menus below to see where these dogs are most commonly found.</p>
            <p class="text-center"><strong>Showing all breeds and names with at least 500 dogs in NYC</strong></p>
        </div>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h3>Dog Breeds</h3>
                    </div>
                    <div class="card-body">
                        <select id="breed-select" class="form-select">
                            <option value="">Select a breed</option>
""")
            
            # Add breed options
            for breed, info in sorted_breeds:
                safe_name = breed.replace('/', '_').replace(' ', '_')
                f.write(f'                            <option value="{safe_name}">{breed} ({info["total_count"]} dogs)</option>\n')
            
            f.write("""                        </select>
                    </div>
                </div>
                <div class="map-container" id="breed-map-container">
                    <p class="text-center p-5">Select a breed to view its distribution</p>
                </div>
            </div>
            
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h3>Dog Names</h3>
                    </div>
                    <div class="card-body">
                        <select id="name-select" class="form-select">
                            <option value="">Select a name</option>
""")
            
            # Add name options
            for name, info in sorted_names:
                safe_name = name.replace('/', '_').replace(' ', '_')
                f.write(f'                            <option value="{safe_name}">{name} ({info["total_count"]} dogs)</option>\n')
            
            f.write("""                        </select>
                    </div>
                </div>
                <div class="map-container" id="name-map-container">
                    <p class="text-center p-5">Select a name to view its distribution</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Event listeners for selects
        document.getElementById('breed-select').addEventListener('change', function() {
            const breed = this.value;
            const mapContainer = document.getElementById('breed-map-container');
            
            if (breed) {
                mapContainer.innerHTML = `<iframe src="maps/breeds/${breed}_map.html"></iframe>`;
            } else {
                mapContainer.innerHTML = `<p class="text-center p-5">Select a breed to view its distribution</p>`;
            }
        });
        
        document.getElementById('name-select').addEventListener('change', function() {
            const name = this.value;
            const mapContainer = document.getElementById('name-map-container');
            
            if (name) {
                mapContainer.innerHTML = `<iframe src="maps/names/${name}_map.html"></iframe>`;
            } else {
                mapContainer.innerHTML = `<p class="text-center p-5">Select a name to view its distribution</p>`;
            }
        });
    </script>
</body>
</html>""")
    except Exception as e:
        print(f"Error creating static HTML: {e}")
        return
    
    # Copy maps to Netlify directory
    print("\nStep 3: Copying maps to Netlify build directory...")
    try:
        # Copy maps directory
        shutil.copytree('maps', f'{netlify_dir}/maps')
        print(f"  - Copied maps to {netlify_dir}/maps")
        
        # Copy data directory (needed for any AJAX calls)
        shutil.copytree('data', f'{netlify_dir}/data')
        print(f"  - Copied data to {netlify_dir}/data")
        
        # Create netlify.toml file for configuration
        with open(f'{netlify_dir}/netlify.toml', 'w') as f:
            f.write("""[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
""")
        print(f"  - Created netlify.toml configuration file")
        
    except Exception as e:
        print(f"Error copying files: {e}")
        return
    
    print("\n" + "="*60)
    print("Static site built successfully!")
    print("="*60)
    print("\nTo deploy to Netlify:")
    print("1. Install the Netlify CLI: npm install -g netlify-cli")
    print("2. Navigate to the netlify_build directory: cd netlify_build")
    print("3. Deploy to Netlify: netlify deploy")
    print("   - Choose 'Create & configure a new site'")
    print("   - Follow the prompts to set up your site")
    print("4. To make your deployment live: netlify deploy --prod")

if __name__ == "__main__":
    build_static_site() 