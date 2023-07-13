import requests
import csv
from lxml import html
import re
import time

def scrape_amazon_products(url):
    retries = 3  # Number of retries
    delay = 2  # Delay in seconds between retries

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    for attempt in range(retries):
        try:
            # Send a GET request to the URL with custom headers
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            tree = html.fromstring(response.content)

            # Extract product information using XPath
            product_names = tree.xpath("//span[contains(@class, 'a-size-base-plus') and contains(@class, 'a-color-base') and contains(@class, 'a-text-normal')]/text()")
            prices_with_dollar = tree.xpath("//span[@class='a-offscreen']/text()")
            prices = [price.strip('$') for price in prices_with_dollar]
            ratings_with_text = tree.xpath("//span[@class='a-icon-alt']/text()")
            #ratings = [rating.strip(' out of 5 stars') for rating in ratings_with_text]
            ratings = [re.findall(r'\d+\.\d+', rating)[0] if re.findall(r'\d+\.\d+', rating) else '' for rating in ratings_with_text]
            images = tree.xpath("//div[contains(@class, 'a-section') and contains(@class, 'aok-relative')]/img/@src")
            second_URLs_wo_head = tree.xpath("//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']/@href")
            second_URLs = ["https://www.amazon.com/" + URL for URL in second_URLs_wo_head]

            # Create a list of dictionaries to store the data
            products = []
            for i in range(len(product_names)):
                rating = ratings[i] if i < len(ratings) else ''  # Handle case where rating is not available
                product = {
                    'Name': product_names[i],
                    'Price': prices[i],
                    'Rating': rating,
                    'Image': images[i],
                    'Second_URL' : second_URLs[i]
                }
                products.append(product)

            # Write the data to a CSV file
            with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['Name', 'Price', 'Rating', 'Image', 'Second_URL'])
                writer.writeheader()
                writer.writerows(products)

            print("Data scraped and saved to 'amazon_products.csv'")
            return  # Exit the function after successful scraping

        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            print(f"Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            continue

    print(f"Failed to scrape data after {retries} retries")

# Example usage
url = 'https://www.amazon.com/s?k=chair&s=exact-aware-popularity-rank'
scrape_amazon_products(url)
