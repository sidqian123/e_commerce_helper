# All rights reserved by Changzhong Qian
# Date: 2023-07-11
# Version: 1.0
# Description: This is a function to scrape product information from Amazon.com based on user input.
# The function will scrape the first page of search results and save the data to a CSV file for further analysis.


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
            legitimacy = True
            factor_price = 0
            result_elements = tree.xpath("//div[@data-component-type='s-search-result']")
            for element in result_elements:
                product = {}

                # Extract ASIN
                asin = element.get('data-asin')
                if asin:
                    product['ASIN'] = asin
                else:
                    legitimacy = False

                # Extract product name
                name_element = element.xpath(".//span[@class='a-size-base-plus a-color-base a-text-normal']")
                if name_element:
                    product['Name'] = name_element[0].text
                else:
                    legitimacy = False

                # Extract product price
                price_element = element.xpath(".//span[@class='a-offscreen']/text()")
                if price_element:
                    product['Price'] = price_element[0].strip('$')
                    factor_price = factor_price + float(product['Price'])
                else:
                    legitimacy = False

                # Extract product sale
                sale_element = element.xpath(".//span[@class='a-size-base a-color-secondary']/text()")
                if sale_element:
                    sale_amount = sale_element[0].strip().split()[0].strip('+')
                    # check if there is k inside the sale amount
                    # if 'K' in sale_amount:
                    #     sale_amount = sale_amount.strip('K')
                    #     sale_amount = float(sale_amount) * 1000
                    # else:
                    #     sale_amount = float(sale_amount)
                    product['Sale'] = sale_amount
                else:
                    legitimacy = False

                # Extract product rating
                rating_element = element.xpath(".//div[@class='a-row a-size-small']/span[@aria-label]")
                if rating_element:
                    rating_text = rating_element[0].get('aria-label')
                    rating_match = re.search(r'\d+\.\d+', rating_text)
                    if rating_match:
                        product['Rating'] = rating_match.group()
                else:
                    legitimacy = False

                # Extract product image
                image_element = element.xpath(
                    ".//div[contains(@class, 'a-section') and contains(@class, 'aok-relative')]/img/@src")
                if image_element:
                    product['Image'] = image_element[0]
                else:
                    legitimacy = False

                # Extract product URL
                url_element = element.xpath(".//a[@class='a-link-normal s-underline-text s-underline-link-text "
                                            "s-link-style a-text-normal']/@href")
                if url_element:
                    product['URL'] = 'https://www.amazon.com' + url_element[0]
                else:
                    legitimacy = False
                if legitimacy:
                    products.append(product)
                else:
                    legitimacy = True

            # Write the data to a CSV file
            with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['ASIN', 'Name', 'Price', 'Rating', 'Sale', 'Image', 'URL'])
                writer.writeheader()
                writer.writerows(products)
            file.close()
            return  # Exit the function after successful scraping

        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            print(f"Error: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
            continue

    print(f"Failed to scrape data after {retries} retries")


# Main
def main():
    key_word = input("search key words: ").replace(" ", "&")
    url = 'https://www.amazon.com/s?k=' + key_word + '&s=exact-aware-popularity-rank'
    scrape_amazon_products(url)


if __name__ == '__main__':
    main()
