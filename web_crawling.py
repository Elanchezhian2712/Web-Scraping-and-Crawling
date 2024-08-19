# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# import numpy as np

# def get_title(soup):
#     try:
#         title = soup.find("span", attrs={"id": 'productTitle'})
#         title_value = title.text
#         title_string = title_value.strip()
#     except AttributeError:
#         title_string = ""
#     return title_string

# def get_price(soup):
#     try:
#         # Find the price container using the class name
#         price_div = soup.find("span", class_="a-price a-text-price a-size-medium apexPriceToPay")
#         if price_div:
#             # Extract the price text from the nested span with class 'a-offscreen'
#             price = price_div.find("span", class_="a-offscreen").text.strip()
#         else:
#             price = ""
#     except Exception as e:
#         price = ""
#     return price

# def get_rating(soup):
#     try:
#         rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
#     except AttributeError:
#         try:
#             rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
#         except:
#             rating = ""	
#     return rating

# def get_review_count(soup):
#     try:
#         review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
#     except AttributeError:
#         review_count = ""	
#     return review_count

# def get_availability(soup):
#     try:
#         available = soup.find("div", attrs={'id': 'availability'})
#         available = available.find("span").string.strip()
#     except AttributeError:
#         available = "Not Available"	
#     return available

# if __name__ == '__main__':
#     HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
#     URL = "https://www.amazon.com/s?k=playstation+4&ref=nb_sb_noss_2"
#     webpage = requests.get(URL, headers=HEADERS)
#     soup = BeautifulSoup(webpage.content, "html.parser")
#     links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
#     links_list = [link.get('href') for link in links]

#     d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}
    
#     for link in links_list:
#         new_webpage = requests.get("https://www.amazon.com" + link, headers=HEADERS)
#         new_soup = BeautifulSoup(new_webpage.content, "html.parser")

#         d['title'].append(get_title(new_soup))
#         d['price'].append(get_price(new_soup))
#         d['rating'].append(get_rating(new_soup))
#         d['reviews'].append(get_review_count(new_soup))
#         d['availability'].append(get_availability(new_soup))

#     amazon_df = pd.DataFrame.from_dict(d)
#     amazon_df['title'] = amazon_df['title'].replace('', np.nan)
#     amazon_df = amazon_df.dropna(subset=['title'])
#     amazon_df.to_csv("amazon_data.csv", header=True, index=False)
#     print(amazon_df)




import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize Chrome WebDriver with custom options
def get_driver():
    options = webdriver.ChromeOptions()
    options.headless = True  # Run in headless mode (no UI)
    
    # Add a User-Agent string to mimic a real browser
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    
    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    return driver

# Scraping Amazon for products based on search query
def scrape_amazon(search_query):
    driver = get_driver()
    
    try:
        # Construct Amazon search URL
        amazon_url = f"https://www.amazon.com/s?k={search_query.replace(' ', '+')}&i=stripbooks-intl-ship"
        driver.get(amazon_url)
        
        # Allow time for the page to fully load
        time.sleep(5)
        
        # Locate product elements on the page
        products = driver.find_elements(By.CSS_SELECTOR, "h2 a")
        
        # Open a CSV file to write product data
        with open('amazon_products.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Product Name', 'Product Link'])  # CSV header
            
            # Iterate through the products found on the page
            for index, product in enumerate(products):
                try:
                    # Retrieve the product link and name
                    product_link = product.get_attribute('href')
                    product_name = product.text
                    
                    # Write product data to CSV
                    writer.writerow([product_name, product_link])
                    
                    print(f"Product {index + 1}: {product_name}")
                    print(f"Link: {product_link}\n")
                    
                except StaleElementReferenceException:
                    print("Encountered stale element reference, retrying...")
                    products = driver.find_elements(By.CSS_SELECTOR, "h2 a")  # Re-fetch the elements
                    
                except NoSuchElementException:
                    print("Product link not found. Skipping this product.")
                    continue
    
    except Exception as e:
        print(f"Failed to retrieve data from Amazon: {e}")
    
    finally:
        # Close the driver after scraping
        driver.quit()

if __name__ == '__main__':
    search_query = "java books"  # Modify this search query as needed
    scrape_amazon(search_query)
