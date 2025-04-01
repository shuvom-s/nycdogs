from http.server import BaseHTTPRequestHandler
from os.path import exists

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Check if index.html exists, if not create it
        if not exists('../index.html'):
            # Create a simple redirect page
            content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=https://shuvom-s.github.io/nycdogs/">
    <title>NYC Dogs Map - Redirecting</title>
</head>
<body>
    <h1>NYC Dogs Map</h1>
    <p>Redirecting you to the NYC Dogs Map...</p>
    <p>If you are not redirected automatically, <a href="https://shuvom-s.github.io/nycdogs/">click here</a>.</p>
</body>
</html>"""
        else:
            # Read the existing index.html
            with open('../index.html', 'r') as file:
                content = file.read()
        
        self.wfile.write(content.encode('utf-8')) 