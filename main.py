import requests
import csv
from lxml import html
import re
import time


def scrape_amazon_products(url):
    retries = 3  # Number of retries
    delay = 2  # Delay in seconds between retries

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    for attempt in range(retries):
        try:
            # Send a GET request to the URL with custom headers
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            tree = html.fromstring(response.content)

            # Extract product information using XPath
            products = []

            result_elements = tree.xpath("//div[@data-component-type='s-search-result']")
            for element in result_elements:
                product = {}

                # Extract ASIN
                asin = element.get('data-asin')
                if asin:
                    product['ASIN'] = asin

                # Extract product name
                name_element = element.xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']")
                if name_element:
                    product['Name'] = name_element[0].text

                # Extract product price
                price_element = element.xpath(".//span[@class='a-offscreen']/text()")
                if price_element:
                    product['Price'] = price_element[0].strip('$')

                # Extract product rating
                rating_element = element.xpath(".//div[@class='a-row a-size-small']/span[@aria-label]")
                if rating_element:
                    rating_text = rating_element[0].get('aria-label')
                    rating_match = re.search(r'\d+\.\d+', rating_text)
                    if rating_match:
                        product['Rating'] = rating_match.group()

                # Extract product image
                image_element = element.xpath(
                    ".//div[contains(@class, 'a-section') and contains(@class, 'aok-relative')]/img/@src")
                if image_element:
                    product['Image'] = image_element[0]

                # Extract product URL
                url_element = element.xpath(".//a[@class='a-link-normal s-underline-text s-underline-link-text "
                                            "s-link-style a-text-normal']/@href")
                if url_element:
                    product['URL'] = 'https://www.amazon.com' + url_element[0]

                products.append(product)

            # Write the data to a CSV file
            with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['ASIN', 'Name', 'Price', 'Rating', 'Image', 'URL'])
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


# Main
def main():
    key_word = input("search key words").replace(" ", "&")
    url = 'https://www.amazon.com/s?k=' + key_word + '&s=exact-aware-popularity-rank'
    scrape_amazon_products(url)


if __name__ == '__main__':
    main()
