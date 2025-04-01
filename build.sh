#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "Starting Netlify build process..."

# Create netlify_build directory
mkdir -p netlify_build

# Install Python dependencies
pip install -r requirements.txt

# Generate the maps for Netlify
echo "Generating maps for Netlify..."
python generate_netlify_maps.py

# Verify that the index.html file was created
if [ -f "netlify_build/index.html" ]; then
    echo "Created index.html file successfully!"
    echo "Contents of netlify_build directory:"
    ls -la netlify_build/
else
    echo "ERROR: Failed to create index.html file"
    exit 1
fi

echo "Build process completed successfully!" 