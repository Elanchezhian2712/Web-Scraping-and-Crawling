# Automated Amazon Product Scraper

This project is an automated Amazon product scraper built with Python and Selenium. The script scrapes product information (names and links) based on a given search query from Amazon's search results page and  It also incorporates a basic form of crawling by handling pagination to move through multiple pages of search results. Then stores the data in a CSV file for further analysis or use.

## Features

- **Headless Scraping:** The script runs in headless mode, meaning it doesn't open a browser window while performing the scraping.
- **User-Agent Spoofing:** To mimic a real user and avoid detection as a bot, a User-Agent string is added to the request.
- **CSV Export:** The scraped product names and links are saved in a `amazon_products.csv` file.
- **Robust Error Handling:** The script handles common Selenium exceptions like stale element references and missing elements.

## Requirements

Before running the script, ensure that the following packages are installed:

- **Selenium**
- **webdriver_manager**
- **Chrome WebDriver**

You can install the required packages using `pip`:

```bash
pip install selenium webdriver-manager
```


# Amazon Product Scraper with BeautifulSoup

This project is an automated Amazon product scraper built with Python, BeautifulSoup, and Requests. The script scrapes detailed product information (title, price, rating, review count, and availability) based on a given search query from Amazon and stores the data in a CSV file for further analysis or use.

## Features

- **Scrapes Multiple Product Attributes:** The script extracts the product title, price, rating, review count, and availability from individual product pages on Amazon.
- **CSV Export:** The extracted data is stored in a CSV file (`amazon_data.csv`) for easy access and analysis.
- **Robust Error Handling:** The script handles HTTP request exceptions and skips invalid or unavailable product pages.

## Requirements

Before running the script, ensure that the following packages are installed:

- **BeautifulSoup4**
- **Requests**
- **Pandas**
- **NumPy**

You can install the required packages using `pip`:

```bash
pip install beautifulsoup4 requests pandas numpy
```
