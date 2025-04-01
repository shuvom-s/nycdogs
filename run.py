#!/usr/bin/env python3
"""
NYC Dogs Dataset Visualizer
This script runs the entire pipeline to process and visualize the NYC dogs dataset.
"""

import os
import subprocess
import sys

def check_requirements():
    try:
        import pandas
        import matplotlib
        import seaborn
        import folium
        print("All required packages are installed.")
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    print("="*60)
    print("NYC Dogs Dataset Visualizer")
    print("="*60)
    
    # Check if requirements are installed
    if not check_requirements():
        return
    
    # Check if the dataset exists
    if not os.path.exists('nycdogs.csv'):
        print("Error: nycdogs.csv not found in the current directory.")
        print("Please place the dataset file in the current directory and try again.")
        return
    
    # Create directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('examples', exist_ok=True)
    os.makedirs('maps', exist_ok=True)
    os.makedirs('maps/breeds', exist_ok=True)
    os.makedirs('maps/names', exist_ok=True)
    os.makedirs('website', exist_ok=True)
    
    # Run preprocessing
    print("\nStep 1: Preprocessing the dataset...")
    print("-"*60)
    try:
        import preprocess_data
        preprocess_data.preprocess_data()
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return
    
    # Create heatmaps
    print("\nStep 2: Creating choropleth maps...")
    print("-"*60)
    try:
        from create_heatmaps import create_breed_choropleth_maps, create_name_choropleth_maps, create_web_interface
        
        # Create the maps
        create_breed_choropleth_maps()
        create_name_choropleth_maps()
        create_web_interface()
    except Exception as e:
        print(f"Error creating maps: {e}")
        return
    
    # Success message
    print("\n" + "="*60)
    print("Process completed successfully!")
    print("="*60)
    print("\nYou can now:")
    print("1. View example visualizations in the 'examples/' directory")
    print("2. Open 'website/index.html' in a web browser to explore the interactive maps")
    print("3. Find the deduplicated dataset at 'data/nycdogs_unique.csv'")

if __name__ == "__main__":
    main() 