#!/usr/bin/env python3
"""
Simplified build script for Vercel deployment.

Creates a static website that redirects to the GitHub Pages site
because Vercel has limitations with GIS dependencies.
"""

import os
import json

def create_redirect():
    """Create a static HTML file that redirects to GitHub Pages"""
    print("Creating redirect page to GitHub Pages site...")
    
    # Create index.html with redirect
    with open("index.html", "w") as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=https://shuvom-s.github.io/nycdogs/">
    <title>NYC Dogs Map - Redirecting</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            padding: 40px 20px;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
        }
        h1 {
            color: #2c3e50;
        }
        p {
            margin-bottom: 20px;
        }
        .redirect-link {
            display: inline-block;
            padding: 10px 20px;
            background-color: #4a6fa5;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin-top: 20px;
        }
        .redirect-link:hover {
            background-color: #385d8a;
        }
    </style>
</head>
<body>
    <h1>NYC Dogs Map</h1>
    <p>Redirecting you to the NYC Dogs Map hosted on GitHub Pages...</p>
    <p>If you are not redirected automatically, click the link below:</p>
    <a class="redirect-link" href="https://shuvom-s.github.io/nycdogs/">Go to NYC Dogs Map</a>
    
    <div style="margin-top: 40px;">
        <p>The NYC Dogs Map project uses geospatial libraries that require additional system dependencies not available in Vercel's serverless environment, so we're hosting the full interactive version on GitHub Pages.</p>
    </div>
</body>
</html>""")
    
    print("Created redirect page in index.html")

if __name__ == "__main__":
    create_redirect() 