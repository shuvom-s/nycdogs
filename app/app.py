from flask import Flask, render_template, jsonify, request
import json
import os
from preprocess import preprocess_data

app = Flask(__name__)

# Load the preprocessed data or generate it if it doesn't exist
if not (os.path.exists('app/data/valid_breeds.json') and 
        os.path.exists('app/data/valid_names.json') and
        os.path.exists('app/data/breed_data.json') and
        os.path.exists('app/data/name_data.json')):
    valid_breeds, valid_names = preprocess_data()
else:
    with open('app/data/valid_breeds.json', 'r') as f:
        valid_breeds = json.load(f)
    with open('app/data/valid_names.json', 'r') as f:
        valid_names = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', 
                          valid_breeds=valid_breeds, 
                          valid_names=valid_names)

@app.route('/api/breed/<breed>')
def get_breed_data(breed):
    with open('app/data/breed_data.json', 'r') as f:
        breed_data = json.load(f)
    
    if breed in breed_data:
        return jsonify(breed_data[breed])
    else:
        return jsonify({"error": "Breed not found"}), 404

@app.route('/api/name/<name>')
def get_name_data(name):
    with open('app/data/name_data.json', 'r') as f:
        name_data = json.load(f)
    
    if name in name_data:
        return jsonify(name_data[name])
    else:
        return jsonify({"error": "Name not found"}), 404

@app.route('/api/breeds')
def get_breeds():
    with open('app/data/valid_breeds.json', 'r') as f:
        valid_breeds = json.load(f)
    return jsonify(valid_breeds)

@app.route('/api/names')
def get_names():
    with open('app/data/valid_names.json', 'r') as f:
        valid_names = json.load(f)
    return jsonify(valid_names)

if __name__ == '__main__':
    app.run(debug=True) 