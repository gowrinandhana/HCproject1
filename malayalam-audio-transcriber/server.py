from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

# Change to the directory containing index.html
os.chdir('templates')

# Create an HTTP server
server_address = ('', 8000)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print('Server running at http://localhost:8000/')
httpd.serve_forever() 