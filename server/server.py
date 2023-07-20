import os
import http.server
import socketserver
import json
import glob

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the product name, 'history', and 'asin' from the path
        path_parts = self.path[1:].split('/')
        product_name = path_parts[0]
        asin = None

        if len(path_parts) > 2 and path_parts[1] == 'history':
            asin = path_parts[2]  # Extract ASIN from the URL
            # For '/history' URLs, return all matching JSON files
            file_list = glob.glob(f'./product_data/amz_{product_name}*.json')

            data = []
            for file_name in file_list:
                with open(file_name, 'r') as f:
                    file_content = f.read().lstrip()
                    if file_content and file_content[0] == '[':
                        # Filter the data for the specific ASIN
                        file_data = json.loads(file_content)
                        data += [item for item in file_data if item.get('ASIN') == asin]
                    else:
                        print(f"Warning: '{file_name}' is not a valid JSON array or is empty")
        else:
            # Otherwise, return only the latest JSON file
            file_list = glob.glob(f'./product_data/amz_{product_name}*.json')
            if not file_list:
                print(f"No JSON files found for product '{product_name}'")
                self.send_response(404)
                self.end_headers()
                return

            latest_file = max(file_list, key=os.path.getctime)
            with open(latest_file, 'r') as f:
                file_content = f.read().lstrip()
                if file_content and file_content[0] == '[':
                    data = json.loads(file_content)
                else:
                    print(f"Warning: '{latest_file}' is not a valid JSON array or is empty")

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
