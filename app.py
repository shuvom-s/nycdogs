from flask import Flask, render_template, redirect, url_for, send_from_directory, jsonify
import os
import json
from run import main as run_preprocessing

app = Flask(__name__)

@app.route('/')
def index():
    # Check if data has been processed
    if not os.path.exists('data/popular_breeds.json') or not os.path.exists('data/popular_names.json'):
        # Run preprocessing and create maps if data doesn't exist
        return render_template('processing.html')
    
    # Load breed data
    with open('data/popular_breeds.json', 'r') as f:
        breed_data = json.load(f)
    
    # Load name data
    with open('data/popular_names.json', 'r') as f:
        name_data = json.load(f)
    
    # Filter for breeds and names with at least 500 dogs
    filtered_breeds = {breed: info for breed, info in breed_data.items() if info['total_count'] >= 500}
    filtered_names = {name: info for name, info in name_data.items() if info['total_count'] >= 500}
    
    # Sort breeds and names by total count
    sorted_breeds = sorted(filtered_breeds.items(), key=lambda x: x[1]['total_count'], reverse=True)
    sorted_names = sorted(filtered_names.items(), key=lambda x: x[1]['total_count'], reverse=True)
    
    return render_template('index.html', 
                          breeds=sorted_breeds,
                          names=sorted_names,
                          min_count=500)

@app.route('/process')
def process():
    """Run the data processing and map creation pipeline"""
    try:
        run_preprocessing()
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/maps/<map_type>/<map_name>')
def show_map(map_type, map_name):
    """Display a specific map"""
    return send_from_directory(f'maps/{map_type}', map_name)

@app.route('/api/zipcode/<zipcode>')
def get_zipcode_stats(zipcode):
    """Get statistics for a specific zipcode"""
    if not os.path.exists('data/zipcode_stats.json'):
        return jsonify({"error": "Zipcode statistics not available"}), 404
    
    with open('data/zipcode_stats.json', 'r') as f:
        zipcode_stats = json.load(f)
    
    if zipcode in zipcode_stats:
        return jsonify(zipcode_stats[zipcode])
    else:
        return jsonify({"error": "Zipcode not found"}), 404

@app.route('/api/zipcodes')
def get_all_zipcodes():
    """Get a list of all available zipcodes with statistics"""
    if not os.path.exists('data/zipcode_stats.json'):
        return jsonify({"error": "Zipcode statistics not available"}), 404
    
    with open('data/zipcode_stats.json', 'r') as f:
        zipcode_stats = json.load(f)
    
    # Return a simplified list with just zipcode and dog count
    simplified_stats = {
        zipcode: {
            "total_dogs": stats["total_dogs"], 
            "has_data": len(stats.get("top_breeds", [])) > 0 or len(stats.get("top_names", [])) > 0
        } 
        for zipcode, stats in zipcode_stats.items()
    }
    
    return jsonify(simplified_stats)

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

@app.route('/data/<path:filename>')
def serve_data(filename):
    """Serve data files"""
    return send_from_directory('data', filename)

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Create maps directory if it doesn't exist
    os.makedirs('maps/breeds', exist_ok=True)
    os.makedirs('maps/names', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 