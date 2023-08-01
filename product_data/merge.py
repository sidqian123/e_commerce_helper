import json
from collections import defaultdict

def merge_json_files(file_names, output_file):
    # Initialize a dictionary to store merged product data
    merged_data = defaultdict(lambda: defaultdict(list))

    for file_name in file_names:
        with open(file_name, 'r') as f:
            data = json.load(f)
            for product in data:
                asin = product['ASIN']
                date = product['Search Date']
                if date not in merged_data[asin]['Search Date']:
                    for key, value in product.items():
                        # Add product brand as 'null' if it does not exist in the JSON data
                        if key == 'Brand':
                            merged_data[asin][key] = value if value else 'null'
                        # Store single values for 'ASIN', 'Name', 'Amazon Prime', 'Image', and 'URL'
                        elif key in ['ASIN', 'Name', 'Amazon Prime', 'Image', 'URL']:
                            merged_data[asin][key] = value
                        else:
                            merged_data[asin][key].append(value)

    # Convert defaultdict back to regular dict
    merged_data = {k: dict(v) for k, v in merged_data.items()}

    # Write merged data to output file
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

# Test the function
file_names = ['amz_sex+toys_2023-07-16_.json', 'amz_sex+toys_2023-07-17_.json', 'amz_sex+toys_2023-07-20_.json', 'amz_sex+toys_2023-07-23_.json', 'amz_sex+toys_2023-07-26_.json', 'amz_sex+toys_2023-07-31_.json']
output_file = 'amz_sex+toys.json'
merge_json_files(file_names, output_file)
