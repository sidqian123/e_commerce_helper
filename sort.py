import csv
import json


# laplace's rule of succession to sort the confidence of the products rating

def laplace_sort(file_path):
    with open(file_path, 'r') as file:
        extension = file_path.split('.')[-1]

        if extension == 'csv':
            reader = csv.DictReader(file)
        elif extension == 'json':
            data = json.load(file)
            reader = data['products']
        else:
            raise ValueError("Unsupported file format. Only CSV and JSON files are supported.")

        for row in reader:
            rating = int(row['Rating'])
            review_amount = int(row['Review Amount'])

            confidence = (rating + 1) / (review_amount + 2)  # Laplace's Rule of Succession

            row['Confidence'] = confidence

        sorted_rows = sorted(reader, key=lambda x: x['Confidence'], reverse=True)

        return sorted_rows
