# All rights reserved by Changzhong Qian
# Date: 2023-07-11
# Version: 1.0
# Disclaimer: This is a personal project and not for commercial use.
# Not responsible for how it is used and assume no liability for any detrimental usage of the source code
# Description: This is a function to scrape product information from Amazon.com based on user input.
# The function will scrape the first page of search results and save the data to a CSV file for further analysis.
import json
import sys

import requests
import csv
from lxml import html
import re
import time
from datetime import datetime


def loading_console(percentage):
    num_bars = int(percentage // 5)
    bar = "|-" * num_bars

    # Output the loading bar and percentage
    output = f"{bar} {percentage:.0f}%\n"
    sys.stdout.write(output)
    sys.stdout.flush()

def scrape_amazon_products(url, pages, brand, retries=3, delay=2):
    retries = 3  # Number of retries
    delay = 2  # Delay in seconds between retries

    headers = {
        'User-Agent': 'Mozilla/7.0 (Windows NT 16.0; Win99; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    for attempt in range(retries):
        try:
            products = []
            legitimacy = True
            factor_price = 0
            search_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for i in range(pages):
                url = url + '&page=' + str(i)
                # Send a GET request to the URL with custom headers
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Raise an exception if the request was unsuccessful
                tree = html.fromstring(response.content)

                # Extract product information using XPath
                result_elements = tree.xpath("//div[@data-component-type='s-search-result']")
                for element in result_elements:
                    product = {}

                    # Extract ASIN
                    asin = element.get('data-asin')
                    if asin:
                        product['ASIN'] = asin
                    else:
                        legitimacy = False

                    # Add search date
                    product['Search Date'] = search_date

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
                    try:
                        if sale_element:
                            sale_amount = sale_element[0].strip().split()[0].strip('+')
                            product['Sale'] = sale_amount
                            if not sale_amount.strip('K').isdigit():
                                product['Sale'] = None
                        else:
                            legitimacy = False
                    except IndexError:
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

                    # Check Amazon Prime eligibility
                    prime_element = element.xpath(".//i[@aria-label='Amazon Prime']")
                    if prime_element:
                        product['Amazon Prime'] = True
                    else:
                        product['Amazon Prime'] = False

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
                    if brand == 'y':
                    # Proceed to product URL and extract brand information and review keywords
                        response_detail_page = requests.get(product['URL'], headers=headers)
                        response_detail_page.raise_for_status()  # Raise an exception if the request was unsuccessful
                        tree_detail_page = html.fromstring(response_detail_page.content)
                        product_brand = tree_detail_page.xpath("//tr[contains(@class, 'po-brand')]/td[2]/span["
                                                               "@class='a-size-base po-break-word']")
                        product['Brand'] = product_brand[0].text.strip() if product_brand else None
                        time.sleep(1)
                    # Extract key review ()
                    # time.sleep(delay)
                    # product_key_review = tree_detail_page.xpath('//span[contains(@data-cr-trigger-on-view, \'lighthouseTerms\')]/@data-cr-trigger-on-view')
                    # if product_key_review:
                    #     key_review = product_key_review[0].get('data-cr-trigger-on-view')
                    #     if key_review:
                    #         json_data = json.loads(key_review)
                    #         product['Key Review'] = json_data["ajaxParamsMap"]["lighthouseTerms"].split('/')
                    #     else:
                    #         product['Key Review'] = None
                    # else:
                    #     product['Key Review'] = None
                    loading_console(((len(products)) / (pages * 55)) * 100)



            # Write the data to a CSV file
            with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file,
                                        fieldnames=['Search Date', 'ASIN', 'Name', 'Price', 'Rating', 'Amazon Prime',
                                                    'Sale', 'Brand', 'Image', 'URL'])
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
    num_pages = int(input("number of page you expect to search: "))
    brand = input("Record for brand (y): ")
    scrape_amazon_products(url, num_pages, brand)


if __name__ == '__main__':
    main()
