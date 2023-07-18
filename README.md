# e_commerce_pro


## Description
The e_commerce_pro project aims to develop an automated system for trend analysis in e-commerce. The system utilizes web scraping techniques, specifically XPath and Python, to obtain data on top-selling products from influential marketplaces like Amazon and eBay. The collected data is then processed using AI algorithms to transform it into visualized insights, which can aid business owners in making informed product selection decisions and enhancing their overall sales performance.

## Disclaimer
This project is a personal endeavor and is not intended for commercial use. The provided source code and system are shared for educational and informational purposes only. The project developers are not responsible for how the code is used and assume no liability for any detrimental usage or consequences arising from it.

## Features
- Automated web scraping of top-selling products from Amazon and eBay.
- Data collection includes product information such as name, price, rating, availability, and more.
- Ability to specify search keywords and the number of pages to scrape.
- Optional recording of brand information for each product.
- Data processing and analysis using AI algorithms.
- Visualization of insights to assist in product selection and sales performance enhancement.

## Dependencies
The following dependencies are required to run the project:

- Python (version 3.0 or higher)
- requests
- lxml
- json
- tqdm
- csv
- re
- time
- datetime

Ensure that these dependencies are installed before running the project.

## Usage
1. Clone the project repository to your local machine.
2. Install the required dependencies listed above.
3. Execute the provided Python script (`amz_s.py`) using a Python interpreter or IDE.
4. Follow the instructions provided by the script to input search keywords, the number of pages to scrape, and whether to record brand information. (input y to record brand name, however, it will take significantly longer time to scrape) 
5. The script will initiate web scraping, retrieving product data from Amazon based on the provided search criteria.
6. the collected data will be saved to a CSV file named `amz_keyword_date.csv` and a JSON file named `amz_keyword_date.json` in the data directory after scraping.
7. Visualize data
   - You can use the plot function from plot.py to visualize the data easily
   - You can also open the html file in the `../visual/web.html` folder for easier visualization (_in developing_).
      - web visualization tool update:
         - display all the products based on the JSON file.
         - image for each product will be loaded.
         - able to load in earlier date JSON/CSV file for price trend.
8. Laplace sorting algo
   - `sort.py` uses Laplace's rule of succession rate to sort the product based on rating and review amount (_in developing_).
10. The saved data can then be further processed and analyzed using AI algorithms and visualization techniques (_in developing_).

## Contact
For any inquiries or issues regarding the e_commerce_pro project, please contact Changzhong Qian.
© 2023 Changzhong Qian
"""
