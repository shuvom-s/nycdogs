#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Netlify build process..."

# Create netlify_build directory
mkdir -p netlify_build
mkdir -p netlify_build/maps/breeds
mkdir -p netlify_build/maps/names

# Create a simple HTML file with instructions and explanation
cat > netlify_build/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NYC Dog Population Maps</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            padding-top: 20px;
            padding-bottom: 40px;
            background-color: #f8f9fa;
        }
        .card {
            margin-bottom: 20px;
        }
        .github-link {
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-md-12 text-center">
                <h1>NYC Dog Population Visualization</h1>
                <p class="lead">This app visualizes the distribution of dog breeds and names across NYC zip codes</p>
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
                <div class="card">
                    <div class="card-body">
                        <h3 class="card-title">Running this Application</h3>
                        <div class="alert alert-info">
                            <p>This application requires geospatial libraries that can't be installed on Netlify's build environment. To run the full application:</p>
                            <ol>
                                <li>Clone the repository: <code>git clone https://github.com/shuvom-s/dogsofnyc.git</code></li>
                                <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                                <li>Run the script: <code>python generate_netlify_maps.py</code></li>
                            </ol>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-body">
                        <h3 class="card-title">About This Project</h3>
                        <p>This project generates interactive choropleth maps showing the distribution of dog breeds and names across NYC zip codes. The maps use data from the NYC Dog Licensing Dataset.</p>
                        <p>Features include:</p>
                        <ul>
                            <li>Visualizations of popular dog breeds by zip code</li>
                            <li>Visualizations of popular dog names by zip code</li>
                            <li>Interactive maps with hover tooltips showing detailed information</li>
                            <li>Selection interface to easily switch between different breeds and names</li>
                        </ul>
                    </div>
                </div>

                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">Data Source</h5>
                        <p class="card-text">
                            Data: <a href="https://data.cityofnewyork.us/Health/NYC-Dog-Licensing-Dataset/nu7n-tubp" target="_blank">NYC Dog Licensing Dataset</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
EOF

echo "Created index.html file successfully!"
echo "Contents of netlify_build directory:"
ls -la netlify_build/

echo "Build process completed successfully!" 