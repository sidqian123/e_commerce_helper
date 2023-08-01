import os
import http.server
import socketserver
import json
import glob

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the product name from the path
        product_name = self.path[1:].split('/')[0]

        # Get the latest JSON file for the product
        file_list = glob.glob(f'./product_data/amz_{product_name}*.json')
        if not file_list:
            print(f"No JSON files found for product '{product_name}'")
            self.send_response(404)
            self.end_headers()
            return

        latest_file = max(file_list, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            data = json.load(f)

        # Create the HTTP response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

PORT = 8000

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
