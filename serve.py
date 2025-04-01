#!/usr/bin/env python3
"""
Simple HTTP server to serve static files for the NYC Dogs Map application.
"""

import os
import http.server
import socketserver
from urllib.parse import urlparse
import subprocess
import time

# Get port from environment variable (Heroku sets this)
PORT = int(os.environ.get("PORT", 8000))

# Check if we need to generate maps
if not os.path.exists('maps') or not os.path.isdir('maps/breeds') or not os.path.isdir('maps/names'):
    print("Maps directory not found. Generating maps...")
    # Run the map generation script
    try:
        subprocess.run(["python", "generate_netlify_maps.py"], check=True)
        print("Maps generated successfully.")
    except Exception as e:
        print(f"Error generating maps: {e}")
        # Create directory structure anyway
        os.makedirs('maps/breeds', exist_ok=True)
        os.makedirs('maps/names', exist_ok=True)

# Create a custom request handler
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL path
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # If the root path or an invalid path is requested, serve index.html
        if path == "/" or not os.path.exists(path[1:]):
            self.path = "/index.html"
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        """Override to provide more useful logging info"""
        message = "%s - - [%s] %s" % (
            self.address_string(),
            self.log_date_time_string(),
            format % args
        )
        print(message)

# Set up the server
Handler = MyHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Serving at port {PORT}")
print(f"Open http://localhost:{PORT}/ in your browser")

# Start the server
httpd.serve_forever() 