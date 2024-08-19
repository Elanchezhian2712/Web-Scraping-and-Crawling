# Amazon Product Scraper

This project is an automated Amazon product scraper built with Python and Selenium. The script scrapes product information (names and links) based on a given search query from Amazon's search results page and stores the data in a CSV file for further analysis or use.

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
