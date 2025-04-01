#!/usr/bin/env python3
"""
Simplified build script for Netlify deployment.
This script creates a static website with placeholder content
that can be deployed on Netlify without requiring large data files.
"""

import os
import shutil

def build_static_site():
    print("="*60)
    print("Building NYC Dogs Static Site for Netlify")
    print("="*60)
    
    # Create output directory for Netlify
    netlify_dir = 'netlify_build'
    os.makedirs(netlify_dir, exist_ok=True)
    
    # Create index.html for Netlify
    print("\nCreating static HTML files...")
    
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
            line-height: 1.6;
        }
        .container {
            max-width: 800px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 30px;
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
        .btn-primary {
            background-color: #4a6fa5;
            border-color: #4a6fa5;
        }
        .btn-primary:hover {
            background-color: #385d8a;
            border-color: #385d8a;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">NYC Dogs - Geographic Distribution</h1>
        
        <div class="alert alert-info" role="alert">
            <h4 class="alert-heading">Application Deployed Successfully!</h4>
            <p>This is a placeholder page for the NYC Dogs Geographic Distribution application. 
               The full interactive version requires the complete dataset to be processed locally.</p>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h3>About This Project</h3>
            </div>
            <div class="card-body">
                <p>This project visualizes the geographic distribution of dog breeds and names across NYC zip codes based on the nycdogs.csv dataset.</p>
                <p>The application creates choropleth maps showing where different dog breeds and names are most popular across New York City neighborhoods.</p>
            </div>
        </div>
        
        <div class="card mb-4">
            <div class="card-header">
                <h3>How to Run Locally</h3>
            </div>
            <div class="card-body">
                <p>To run the full interactive version:</p>
                <ol>
                    <li>Clone the repository: <code>git clone https://github.com/YOUR_USERNAME/nyc-dogs-map.git</code></li>
                    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                    <li>Make sure the nycdogs.csv and ZCTA.gpkg files are in the root directory</li>
                    <li>Run the Flask app: <code>python app.py</code></li>
                    <li>Open your browser to <code>http://localhost:5000</code></li>
                </ol>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h3>Features</h3>
            </div>
            <div class="card-body">
                <ul>
                    <li>Visualize distribution of dog breeds across NYC</li>
                    <li>Visualize distribution of dog names across NYC</li>
                    <li>Filter for breeds and names with at least 500 dogs</li>
                    <li>Interactive choropleth maps with tooltips</li>
                </ul>
            </div>
        </div>
        
        <div class="text-center mt-4">
            <a href="https://github.com/YOUR_USERNAME/nyc-dogs-map" class="btn btn-primary btn-lg">View on GitHub</a>
        </div>
    </div>
</body>
</html>""")
    
    # Create netlify.toml file for configuration (in case it's needed in the build dir)
    with open(f'{netlify_dir}/netlify.toml', 'w') as f:
        f.write("""[build]
  publish = "."
  
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
""")
    
    print("\n" + "="*60)
    print("Static site built successfully!")
    print("="*60)

if __name__ == "__main__":
    build_static_site() 