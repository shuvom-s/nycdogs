import json
import os
import folium
import pandas as pd
from folium.plugins import HeatMap
import requests
import geopandas as gpd
import numpy as np
from folium.features import GeoJsonTooltip
import io

def get_nyc_zipcode_geojson():
    """
    Get NYC zipcode boundary data from the provided ZCTA.gpkg file.
    """
    print("Loading NYC zipcode boundary data from ZCTA.gpkg...")
    
    try:
        # Load the provided ZCTA.gpkg file
        zipcode_gdf = gpd.read_file('ZCTA.gpkg')
        print(f"Successfully loaded {len(zipcode_gdf)} zip code boundaries")
        
        # Print columns to debug
        print(f"Original columns: {zipcode_gdf.columns.tolist()}")
        
        # Check if ZCTA column exists - this is the zipcode column
        if 'ZCTA' in zipcode_gdf.columns:
            # Convert ZCTA to string to ensure consistent behavior
            zipcode_gdf['ZCTA'] = zipcode_gdf['ZCTA'].astype(str)
            # No need to rename for now, we'll handle it in the mapping functions
        
        # Print the first few rows to debug
        print("First 5 rows of the GeoDataFrame:")
        print(zipcode_gdf.head())
        
        return zipcode_gdf
    except Exception as e:
        print(f"Error loading ZCTA.gpkg: {e}")
        print("Using simplified zipcode boundaries as fallback...")
        
        # If loading fails, create a simplified GeoJSON with basic NYC zipcode boundaries
        simple_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {"postalCode": "10001", "borough": "Manhattan", "neighborhood": "Chelsea"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-73.9972, 40.7503], [-73.9872, 40.7503], 
                            [-73.9872, 40.7603], [-73.9972, 40.7603], 
                            [-73.9972, 40.7503]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {"postalCode": "10002", "borough": "Manhattan", "neighborhood": "Lower East Side"},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-73.9862, 40.7159], [-73.9762, 40.7159], 
                            [-73.9762, 40.7259], [-73.9862, 40.7259], 
                            [-73.9862, 40.7159]
                        ]]
                    }
                },
                # Add more simplified zipcode boundaries as needed
            ]
        }
        
        # Save the simplified data locally for reference
        os.makedirs('data', exist_ok=True)
        with open('data/nyc_zipcodes_simplified.geojson', 'w') as f:
            json.dump(simple_geojson, f)
        
        return gpd.read_file('data/nyc_zipcodes_simplified.geojson')

def create_breed_choropleth_maps():
    """Create choropleth maps for dog breeds by NYC zip code"""
    # Load breed data
    with open('data/popular_breeds.json', 'r') as f:
        breed_data = json.load(f)
    
    # Check if zipcode stats exist
    zipcode_stats = {}
    if os.path.exists('data/zipcode_stats.json'):
        with open('data/zipcode_stats.json', 'r') as f:
            zipcode_stats = json.load(f)
    
    # Filter for breeds with at least 500 dogs
    filtered_breeds = {breed: info for breed, info in breed_data.items() if info['total_count'] >= 500}
    print(f"Found {len(filtered_breeds)} breeds with at least 500 dogs")
    
    # Get NYC zipcode boundaries
    try:
        nyc_zipcodes = get_nyc_zipcode_geojson()
        
        # Identify the zipcode field in the GeoDataFrame
        zipcode_field = 'ZCTA'  # Default
        if 'postalCode' in nyc_zipcodes.columns:
            zipcode_field = 'postalCode'
        elif 'ZCTA' in nyc_zipcodes.columns:
            zipcode_field = 'ZCTA'
        else:
            # Try to find a suitable zipcode column
            zipcode_candidates = [col for col in nyc_zipcodes.columns if any(x in col.lower() for x in ['zip', 'postal', 'zcta'])]
            zipcode_field = zipcode_candidates[0] if zipcode_candidates else 'ZCTA'
        
        print(f"Using {zipcode_field} as the zipcode field")
        print(f"Available columns in GeoDataFrame: {', '.join(nyc_zipcodes.columns)}")
        print(f"First few zipcode values: {nyc_zipcodes[zipcode_field].head().tolist()}")
        
        # Make sure all zipcodes in the geodata are strings without decimals
        nyc_zipcodes[zipcode_field] = nyc_zipcodes[zipcode_field].astype(str)
        nyc_zipcodes[zipcode_field] = nyc_zipcodes[zipcode_field].apply(lambda x: x.split('.')[0] if '.' in x else x)
    except Exception as e:
        print(f"Error loading NYC zipcode boundaries: {e}")
        return
    
    # Create output directory
    os.makedirs('maps/breeds', exist_ok=True)
    
    # Create a choropleth map for each breed
    for breed, breed_info in filtered_breeds.items():
        safe_name = breed.replace('/', '_').replace(' ', '_')
        print(f"Creating choropleth map for breed: {breed}")
        
        # Create the map centered on NYC
        nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=10, 
                             tiles='CartoDB positron')
        
        # Create a DataFrame with zipcode and dog count
        zipcode_counts = pd.DataFrame(list(breed_info['zipcode_counts'].items()), 
                                      columns=['zipcode', 'count'])
        
        # Make sure zipcode is a string for proper join
        zipcode_counts['zipcode'] = zipcode_counts['zipcode'].astype(str)
        
        # Calculate the percentage of this breed in each zipcode
        zipcode_counts['percentage'] = zipcode_counts['count'] / zipcode_counts['count'].sum() * 100
        
        # Print a sample of the zipcode counts for debugging
        print(f"Sample zipcode counts for {breed}:")
        print(zipcode_counts.head())
        
        # Print the first few zipcodes to verify format
        print(f"First few zipcodes in data: {zipcode_counts['zipcode'].head().tolist()}")
        
        # Create dictionaries for easy lookup - convert to string and ensure no decimal points
        zipcode_to_count = {}
        zipcode_to_percent = {}
        for _, row in zipcode_counts.iterrows():
            # Remove decimal point if it exists
            zip_str = str(row['zipcode']).split('.')[0]
            zipcode_to_count[zip_str] = row['count']
            zipcode_to_percent[zip_str] = row['percentage']
        
        # Update the dataframe with cleaned zipcodes (no decimal points)
        zipcode_counts['zipcode'] = zipcode_counts['zipcode'].astype(str).apply(lambda x: x.split('.')[0])
        
        # Ensure zip codes in GeoDataFrame are strings for proper matching
        if nyc_zipcodes[zipcode_field].dtype != 'object':
            nyc_zipcodes[zipcode_field] = nyc_zipcodes[zipcode_field].astype(str)
        
        # Check for any matching zipcodes between the data and the GeoDataFrame
        matching_zipcodes = set(zipcode_counts['zipcode']) & set(nyc_zipcodes[zipcode_field])
        print(f"Number of matching zipcodes: {len(matching_zipcodes)} out of {len(zipcode_counts)} in data")
        
        # If there are too few matching zipcodes, we need to transform the zipcodes to match
        if len(matching_zipcodes) < 5:
            print(f"Warning: Very few matching zipcodes for {breed}. Attempting to fix...")
            
            # Try to format zipcodes differently (handles different formats like '00123' vs '123')
            # This helps if the data has zipcode formats different from the GeoDataFrame
            geo_zips = set(nyc_zipcodes[zipcode_field])
            
            # Try with and without leading zeros
            fixed_counts = {}
            for zip_str, count in zipcode_to_count.items():
                # Try adding leading zeros if needed
                if zip_str not in geo_zips and zip_str.isdigit():
                    zip_5digit = zip_str.zfill(5)
                    if zip_5digit in geo_zips:
                        fixed_counts[zip_5digit] = count
                        continue
                
                # Try removing leading zeros
                if zip_str not in geo_zips and zip_str.startswith('0'):
                    zip_no_zero = zip_str.lstrip('0')
                    if zip_no_zero in geo_zips:
                        fixed_counts[zip_no_zero] = count
                        continue
                
                # Keep original if no matches found
                fixed_counts[zip_str] = count
            
            # Recreate the zipcode_counts DataFrame with fixed zipcodes
            fixed_zipcode_counts = pd.DataFrame(list(fixed_counts.items()), columns=['zipcode', 'count'])
            fixed_zipcode_counts['percentage'] = fixed_zipcode_counts['count'] / fixed_zipcode_counts['count'].sum() * 100
            
            # Check if we have more matches now
            fixed_matching = set(fixed_zipcode_counts['zipcode']) & set(nyc_zipcodes[zipcode_field])
            print(f"After fixing, matching zipcodes: {len(fixed_matching)} out of {len(fixed_zipcode_counts)}")
            
            # Use the fixed data if we have more matches
            if len(fixed_matching) > len(matching_zipcodes):
                zipcode_counts = fixed_zipcode_counts
                zipcode_to_count = fixed_counts
                print("Using fixed zipcode format for better map matching")
                
        # Add the choropleth layer
        choropleth = folium.Choropleth(
            geo_data=nyc_zipcodes,
            name=f'{breed} Distribution',
            data=zipcode_counts,
            columns=['zipcode', 'percentage'],
            key_on='feature.properties.' + zipcode_field,
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f'Percentage of {breed} Dogs (%)',
            highlight=True
        ).add_to(nyc_map)
        
        # Create tooltip fields based on available columns
        tooltip_fields = [zipcode_field]
        tooltip_aliases = ['Zip Code:']
        
        # Add borough and neighborhood if available
        if 'borough' in nyc_zipcodes.columns:
            tooltip_fields.append('borough')
            tooltip_aliases.append('Borough:')
        if 'neighborhood' in nyc_zipcodes.columns:
            tooltip_fields.append('neighborhood')
            tooltip_aliases.append('Neighborhood:')
        
        # Add tooltips to show data on hover with a zipcode link
        tooltip = folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
        )
        
        # Add a simple popup with a button for each zipcode
        popup = folium.GeoJsonPopup(
            fields=[zipcode_field],
            aliases=[''],
            localize=True,
            labels=False,
            style='display:none;',  # Hide the zipcode text
            html=f"""
            <div style="text-align:center;">
                <button class="btn btn-primary btn-sm" 
                  onclick="window.parent.showZipcodeStats(this.getAttribute('data-zipcode'))" 
                  data-zipcode="{{{zipcode_field}}}">
                    View Statistics for ZIP {{{zipcode_field}}}
                </button>
            </div>
            """
        )
        
        # Add GeoJSON layer with tooltips
        geojson = folium.GeoJson(
            nyc_zipcodes,
            name='NYC Zipcodes',
            tooltip=tooltip,
            style_function=lambda feature: {
                'fillColor': 'transparent',
                'color': 'black',
                'weight': 1
            },
            highlight_function=lambda feature: {
                'weight': 3,
                'color': 'blue',
                'fillOpacity': 0.2
            },
            overlay=True,
            popup=popup
        ).add_to(nyc_map)
        
        # Add a click handler using JavaScript instead
        folium.Element(f"""
            <script>
                // Define a global showZipcodeStats function if not already defined
                window.showZipcodeStats = function(zipcode) {{
                    console.log('Showing stats for zipcode: ' + zipcode);
                    
                    // Try to call parent window's function if in iframe
                    if (window.parent && window.parent !== window && typeof window.parent.showZipcodeStats === 'function') {{
                        window.parent.showZipcodeStats(zipcode);
                        return;
                    }}
                    
                    // Otherwise show modal directly if modal exists
                    var modal = document.getElementById('zipcodeModal');
                    if (modal) {{
                        var modalTitle = document.querySelector('#zipcodeModal .modal-title');
                        var modalContent = document.querySelector('#zipcodeModal #zipcodeModalContent');
                        
                        if (modalTitle) modalTitle.textContent = 'ZIP Code ' + zipcode + ' Dog Statistics';
                        if (modalContent) modalContent.innerHTML = '<div class="text-center"><h4>Loading data for ZIP Code ' + zipcode + '...</h4><div class="spinner-border" role="status"></div></div>';
                        
                        var bsModal = new bootstrap.Modal(modal);
                        bsModal.show();
                        
                        // This would normally fetch data, but for standalone maps we just show a message
                        setTimeout(function() {{
                            if (modalContent) {{
                                modalContent.innerHTML = '<div class="alert alert-info">To view detailed statistics, please use the app from the main page where API access is available.</div>';
                            }}
                        }}, 1500);
                    }} else {{
                        alert('Statistics for ZIP code ' + zipcode + ' are available in the main application.');
                    }}
                }};
                
                // Add click handlers to each zipcode polygon
                document.addEventListener('DOMContentLoaded', function() {{
                    // Wait a moment for the map to fully initialize
                    setTimeout(function() {{
                        // Find all leaflet path elements (polygons) 
                        var paths = document.querySelectorAll('path.leaflet-interactive');
                        
                        paths.forEach(function(path) {{
                            path.addEventListener('click', function(e) {{
                                // Find the containing element with data attributes
                                var element = e.target.closest('[data-zipcode]') || e.target;
                                var zipcode = element.getAttribute('data-zipcode');
                                
                                // If no zipcode attribute, try to get it from the popup content
                                if (!zipcode) {{
                                    var popups = document.querySelectorAll('.leaflet-popup-content button[data-zipcode]');
                                    if (popups.length > 0) {{
                                        zipcode = popups[0].getAttribute('data-zipcode');
                                    }}
                                }}
                                
                                if (zipcode) {{
                                    // Call the zipcode stats function
                                    try {{
                                        if (window.parent && window.parent.showZipcodeStats) {{
                                            window.parent.showZipcodeStats(zipcode);
                                        }} else if (window.showZipcodeStats) {{
                                            window.showZipcodeStats(zipcode);
                                        }}
                                    }} catch (e) {{
                                        console.error('Error showing zipcode stats: ' + e);
                                    }}
                                }}
                            }});
                        }});
                    }}, 1000);
                }});
            </script>
        """).add_to(nyc_map.get_root())
        
        # Add a title
        title_html = f'''
            <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index:9999; background-color: white; 
                 padding: 10px; border: 2px solid grey; border-radius: 5px;">
                <h3 style="text-align: center; margin: 0;">{breed} Distribution in NYC</h3>
                <p style="text-align: center; margin: 0;">Total: {breed_info['total_count']} dogs</p>
            </div>
        '''
        nyc_map.get_root().html.add_child(folium.Element(title_html))
        
        # Add modal structure for zipcode statistics
        modal_html = '''
        <div class="modal fade" id="zipcodeModal" tabindex="-1" aria-labelledby="zipcodeModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="zipcodeModalLabel">ZIP Code Dog Statistics</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body" id="zipcodeModalContent">
                        <!-- Content will be loaded dynamically -->
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        '''
        nyc_map.get_root().html.add_child(folium.Element(modal_html))
        
        # Add Bootstrap JS for modal functionality
        bootstrap_js = '''
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        '''
        nyc_map.get_root().html.add_child(folium.Element(bootstrap_js))
        
        # Add layer control
        folium.LayerControl().add_to(nyc_map)
        
        # Save the map
        nyc_map.save(f'maps/breeds/{safe_name}_map.html')
    
    print(f"Breed maps created in maps/breeds/ directory")

def create_name_choropleth_maps():
    """Create choropleth maps for dog names by NYC zip code"""
    # Load name data
    with open('data/popular_names.json', 'r') as f:
        name_data = json.load(f)
    
    # Check if zipcode stats exist
    zipcode_stats = {}
    if os.path.exists('data/zipcode_stats.json'):
        with open('data/zipcode_stats.json', 'r') as f:
            zipcode_stats = json.load(f)
    
    # Filter for names with at least 500 dogs
    filtered_names = {name: info for name, info in name_data.items() if info['total_count'] >= 500}
    print(f"Found {len(filtered_names)} names with at least 500 dogs")
    
    # Get NYC zipcode boundaries
    try:
        nyc_zipcodes = get_nyc_zipcode_geojson()
        
        # Identify the zipcode field in the GeoDataFrame
        zipcode_field = 'ZCTA'  # Default
        if 'postalCode' in nyc_zipcodes.columns:
            zipcode_field = 'postalCode'
        elif 'ZCTA' in nyc_zipcodes.columns:
            zipcode_field = 'ZCTA'
        else:
            # Try to find a suitable zipcode column
            zipcode_candidates = [col for col in nyc_zipcodes.columns if any(x in col.lower() for x in ['zip', 'postal', 'zcta'])]
            zipcode_field = zipcode_candidates[0] if zipcode_candidates else 'ZCTA'
        
        print(f"Using {zipcode_field} as the zipcode field")
        print(f"Available columns in GeoDataFrame: {', '.join(nyc_zipcodes.columns)}")
        print(f"First few zipcode values: {nyc_zipcodes[zipcode_field].head().tolist()}")
        
        # Make sure all zipcodes in the geodata are strings without decimals
        nyc_zipcodes[zipcode_field] = nyc_zipcodes[zipcode_field].astype(str)
        nyc_zipcodes[zipcode_field] = nyc_zipcodes[zipcode_field].apply(lambda x: x.split('.')[0] if '.' in x else x)
    except Exception as e:
        print(f"Error loading NYC zipcode boundaries: {e}")
        return
    
    # Create output directory
    os.makedirs('maps/names', exist_ok=True)
    
    # Create a choropleth map for each name
    for name, name_info in filtered_names.items():
        safe_name = name.replace('/', '_').replace(' ', '_')
        print(f"Creating choropleth map for name: {name}")
        
        # Create the map centered on NYC
        nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=10, 
                             tiles='CartoDB positron')
        
        # Create a DataFrame with zipcode and dog count
        zipcode_counts = pd.DataFrame(list(name_info['zipcode_counts'].items()), 
                                      columns=['zipcode', 'count'])
        
        # Make sure zipcode is a string for proper join
        zipcode_counts['zipcode'] = zipcode_counts['zipcode'].astype(str)
        
        # Calculate the percentage of this name in each zipcode
        zipcode_counts['percentage'] = zipcode_counts['count'] / zipcode_counts['count'].sum() * 100
        
        # Print a sample of the zipcode counts for debugging
        print(f"Sample zipcode counts for {name}:")
        print(zipcode_counts.head())
        
        # Print the first few zipcodes to verify format
        print(f"First few zipcodes in data: {zipcode_counts['zipcode'].head().tolist()}")
        
        # Create dictionaries for easy lookup - convert to string and ensure no decimal points
        zipcode_to_count = {}
        zipcode_to_percent = {}
        for _, row in zipcode_counts.iterrows():
            # Remove decimal point if it exists
            zip_str = str(row['zipcode']).split('.')[0]
            zipcode_to_count[zip_str] = row['count']
            zipcode_to_percent[zip_str] = row['percentage']
        
        # Update the dataframe with cleaned zipcodes (no decimal points)
        zipcode_counts['zipcode'] = zipcode_counts['zipcode'].astype(str).apply(lambda x: x.split('.')[0])
        
        # Ensure zip codes in GeoDataFrame are strings for proper matching
        if nyc_zipcodes[zipcode_field].dtype != 'object':
            nyc_zipcodes[zipcode_field] = nyc_zipcodes[zipcode_field].astype(str)
        
        # Check for any matching zipcodes between the data and the GeoDataFrame
        matching_zipcodes = set(zipcode_counts['zipcode']) & set(nyc_zipcodes[zipcode_field])
        print(f"Number of matching zipcodes: {len(matching_zipcodes)} out of {len(zipcode_counts)} in data")
        
        # If there are too few matching zipcodes, we need to transform the zipcodes to match
        if len(matching_zipcodes) < 5:
            print(f"Warning: Very few matching zipcodes for {name}. Attempting to fix...")
            
            # Try to format zipcodes differently (handles different formats like '00123' vs '123')
            # This helps if the data has zipcode formats different from the GeoDataFrame
            geo_zips = set(nyc_zipcodes[zipcode_field])
            
            # Try with and without leading zeros
            fixed_counts = {}
            for zip_str, count in zipcode_to_count.items():
                # Try adding leading zeros if needed
                if zip_str not in geo_zips and zip_str.isdigit():
                    zip_5digit = zip_str.zfill(5)
                    if zip_5digit in geo_zips:
                        fixed_counts[zip_5digit] = count
                        continue
                
                # Try removing leading zeros
                if zip_str not in geo_zips and zip_str.startswith('0'):
                    zip_no_zero = zip_str.lstrip('0')
                    if zip_no_zero in geo_zips:
                        fixed_counts[zip_no_zero] = count
                        continue
                
                # Keep original if no matches found
                fixed_counts[zip_str] = count
            
            # Recreate the zipcode_counts DataFrame with fixed zipcodes
            fixed_zipcode_counts = pd.DataFrame(list(fixed_counts.items()), columns=['zipcode', 'count'])
            fixed_zipcode_counts['percentage'] = fixed_zipcode_counts['count'] / fixed_zipcode_counts['count'].sum() * 100
            
            # Check if we have more matches now
            fixed_matching = set(fixed_zipcode_counts['zipcode']) & set(nyc_zipcodes[zipcode_field])
            print(f"After fixing, matching zipcodes: {len(fixed_matching)} out of {len(fixed_zipcode_counts)}")
            
            # Use the fixed data if we have more matches
            if len(fixed_matching) > len(matching_zipcodes):
                zipcode_counts = fixed_zipcode_counts
                zipcode_to_count = fixed_counts
                print("Using fixed zipcode format for better map matching")
        
        # Add the choropleth layer
        choropleth = folium.Choropleth(
            geo_data=nyc_zipcodes,
            name=f'{name} Distribution',
            data=zipcode_counts,
            columns=['zipcode', 'percentage'],
            key_on='feature.properties.' + zipcode_field,
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name=f'Percentage of Dogs Named {name} (%)',
            highlight=True
        ).add_to(nyc_map)
        
        # Create tooltip fields based on available columns
        tooltip_fields = [zipcode_field]
        tooltip_aliases = ['Zip Code:']
        
        # Add borough and neighborhood if available
        if 'borough' in nyc_zipcodes.columns:
            tooltip_fields.append('borough')
            tooltip_aliases.append('Borough:')
        if 'neighborhood' in nyc_zipcodes.columns:
            tooltip_fields.append('neighborhood')
            tooltip_aliases.append('Neighborhood:')
        
        # Add tooltips to show data on hover with a zipcode link
        tooltip = folium.GeoJsonTooltip(
            fields=tooltip_fields,
            aliases=tooltip_aliases,
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: #F0EFEF;
                border: 2px solid black;
                border-radius: 3px;
                box-shadow: 3px;
            """,
        )
        
        # Add a simple popup with a button for each zipcode
        popup = folium.GeoJsonPopup(
            fields=[zipcode_field],
            aliases=[''],
            localize=True,
            labels=False,
            style='display:none;',  # Hide the zipcode text
            html=f"""
            <div style="text-align:center;">
                <button class="btn btn-primary btn-sm" 
                  onclick="window.parent.showZipcodeStats(this.getAttribute('data-zipcode'))" 
                  data-zipcode="{{{zipcode_field}}}">
                    View Statistics for ZIP {{{zipcode_field}}}
                </button>
            </div>
            """
        )
        
        # Add GeoJSON layer with tooltips
        geojson = folium.GeoJson(
            nyc_zipcodes,
            name='NYC Zipcodes',
            tooltip=tooltip,
            style_function=lambda feature: {
                'fillColor': 'transparent',
                'color': 'black',
                'weight': 1
            },
            highlight_function=lambda feature: {
                'weight': 3,
                'color': 'blue',
                'fillOpacity': 0.2
            },
            overlay=True,
            popup=popup
        ).add_to(nyc_map)
        
        # Add a click handler using JavaScript instead
        folium.Element(f"""
            <script>
                // Define a global showZipcodeStats function if not already defined
                window.showZipcodeStats = function(zipcode) {{
                    console.log('Showing stats for zipcode: ' + zipcode);
                    
                    // Try to call parent window's function if in iframe
                    if (window.parent && window.parent !== window && typeof window.parent.showZipcodeStats === 'function') {{
                        window.parent.showZipcodeStats(zipcode);
                        return;
                    }}
                    
                    // Otherwise show modal directly if modal exists
                    var modal = document.getElementById('zipcodeModal');
                    if (modal) {{
                        var modalTitle = document.querySelector('#zipcodeModal .modal-title');
                        var modalContent = document.querySelector('#zipcodeModal #zipcodeModalContent');
                        
                        if (modalTitle) modalTitle.textContent = 'ZIP Code ' + zipcode + ' Dog Statistics';
                        if (modalContent) modalContent.innerHTML = '<div class="text-center"><h4>Loading data for ZIP Code ' + zipcode + '...</h4><div class="spinner-border" role="status"></div></div>';
                        
                        var bsModal = new bootstrap.Modal(modal);
                        bsModal.show();
                        
                        // This would normally fetch data, but for standalone maps we just show a message
                        setTimeout(function() {{
                            if (modalContent) {{
                                modalContent.innerHTML = '<div class="alert alert-info">To view detailed statistics, please use the app from the main page where API access is available.</div>';
                            }}
                        }}, 1500);
                    }} else {{
                        alert('Statistics for ZIP code ' + zipcode + ' are available in the main application.');
                    }}
                }};
                
                // Add click handlers to each zipcode polygon
                document.addEventListener('DOMContentLoaded', function() {{
                    // Wait a moment for the map to fully initialize
                    setTimeout(function() {{
                        // Find all leaflet path elements (polygons) 
                        var paths = document.querySelectorAll('path.leaflet-interactive');
                        
                        paths.forEach(function(path) {{
                            path.addEventListener('click', function(e) {{
                                // Find the containing element with data attributes
                                var element = e.target.closest('[data-zipcode]') || e.target;
                                var zipcode = element.getAttribute('data-zipcode');
                                
                                // If no zipcode attribute, try to get it from the popup content
                                if (!zipcode) {{
                                    var popups = document.querySelectorAll('.leaflet-popup-content button[data-zipcode]');
                                    if (popups.length > 0) {{
                                        zipcode = popups[0].getAttribute('data-zipcode');
                                    }}
                                }}
                                
                                if (zipcode) {{
                                    // Call the zipcode stats function
                                    try {{
                                        if (window.parent && window.parent.showZipcodeStats) {{
                                            window.parent.showZipcodeStats(zipcode);
                                        }} else if (window.showZipcodeStats) {{
                                            window.showZipcodeStats(zipcode);
                                        }}
                                    }} catch (e) {{
                                        console.error('Error showing zipcode stats: ' + e);
                                    }}
                                }}
                            }});
                        }});
                    }}, 1000);
                }});
            </script>
        """).add_to(nyc_map.get_root())
        
        # Add a title
        title_html = f'''
            <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index:9999; background-color: white; 
                 padding: 10px; border: 2px solid grey; border-radius: 5px;">
                <h3 style="text-align: center; margin: 0;">Dogs Named {name} in NYC</h3>
                <p style="text-align: center; margin: 0;">Total: {name_info['total_count']} dogs</p>
            </div>
        '''
        nyc_map.get_root().html.add_child(folium.Element(title_html))
        
        # Add modal structure for zipcode statistics
        modal_html = '''
        <div class="modal fade" id="zipcodeModal" tabindex="-1" aria-labelledby="zipcodeModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="zipcodeModalLabel">ZIP Code Dog Statistics</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body" id="zipcodeModalContent">
                        <!-- Content will be loaded dynamically -->
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        '''
        nyc_map.get_root().html.add_child(folium.Element(modal_html))
        
        # Add Bootstrap JS for modal functionality
        bootstrap_js = '''
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        '''
        nyc_map.get_root().html.add_child(folium.Element(bootstrap_js))
        
        # Add layer control
        folium.LayerControl().add_to(nyc_map)
        
        # Save the map
        nyc_map.save(f'maps/names/{safe_name}_map.html')
    
    print(f"Name maps created in maps/names/ directory")

def create_web_interface():
    """Create a simple web interface to view the maps"""
    os.makedirs('website', exist_ok=True)
    
    # Create an index.html file
    with open('website/index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NYC Dogs - Geographic Distribution</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <style>
        body { padding: 20px; }
        .map-container { height: 600px; margin-top: 20px; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">NYC Dogs - Geographic Distribution</h1>
        
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h3>Dog Breeds</h3>
                    </div>
                    <div class="card-body">
                        <select id="breed-select" class="form-select">
                            <option value="">Select a breed</option>
                            <!-- Will be populated by JavaScript -->
                        </select>
                    </div>
                </div>
                <div class="map-container" id="breed-map-container">
                    <p class="text-center">Select a breed to view its distribution</p>
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
                            <!-- Will be populated by JavaScript -->
                        </select>
                    </div>
                </div>
                <div class="map-container" id="name-map-container">
                    <p class="text-center">Select a name to view its distribution</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Load breed data
        fetch('../data/popular_breeds.json')
            .then(response => response.json())
            .then(data => {
                const breedSelect = document.getElementById('breed-select');
                
                // Sort breeds by count
                const sortedBreeds = Object.entries(data)
                    .sort((a, b) => b[1].total_count - a[1].total_count);
                
                // Add options for each breed
                sortedBreeds.forEach(([breed, breedInfo]) => {
                    const option = document.createElement('option');
                    option.value = breed.replace('/', '_').replace(' ', '_');
                    option.textContent = `${breed} (${breedInfo.total_count} dogs)`;
                    breedSelect.appendChild(option);
                });
            });
        
        // Load name data
        fetch('../data/popular_names.json')
            .then(response => response.json())
            .then(data => {
                const nameSelect = document.getElementById('name-select');
                
                // Sort names by count
                const sortedNames = Object.entries(data)
                    .sort((a, b) => b[1].total_count - a[1].total_count);
                
                // Add options for each name
                sortedNames.forEach(([name, nameInfo]) => {
                    const option = document.createElement('option');
                    option.value = name.replace('/', '_').replace(' ', '_');
                    option.textContent = `${name} (${nameInfo.total_count} dogs)`;
                    nameSelect.appendChild(option);
                });
            });
        
        // Event listeners for selects
        document.getElementById('breed-select').addEventListener('change', function() {
            const breed = this.value;
            const mapContainer = document.getElementById('breed-map-container');
            
            if (breed) {
                mapContainer.innerHTML = `<iframe src="../maps/breeds/${breed}_map.html"></iframe>`;
            } else {
                mapContainer.innerHTML = `<p class="text-center">Select a breed to view its distribution</p>`;
            }
        });
        
        document.getElementById('name-select').addEventListener('change', function() {
            const name = this.value;
            const mapContainer = document.getElementById('name-map-container');
            
            if (name) {
                mapContainer.innerHTML = `<iframe src="../maps/names/${name}_map.html"></iframe>`;
            } else {
                mapContainer.innerHTML = `<p class="text-center">Select a name to view its distribution</p>`;
            }
        });
    </script>
</body>
</html>
""")
    
    print("Created web interface in website/index.html")

if __name__ == "__main__":
    # Create maps
    create_breed_choropleth_maps()
    create_name_choropleth_maps()
    
    # Create web interface
    create_web_interface()
    
    print("\nAll done! Open website/index.html in a browser to explore the maps") 