from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        return title.text.strip() if title else ""
    except AttributeError:
        return ""

def get_price(soup):
    try:
        # Find the price container using the class name
        price_div = soup.find("span", class_="a-price aok-align-center reinventPricePriceToPayMargin priceToPay")
        if price_div:
            # Extract the price components
            price_symbol = price_div.find("span", class_="a-price-symbol").text.strip()
            price_whole = price_div.find("span", class_="a-price-whole").text.strip()
            
            # Combine the parts to form the complete price
            full_price = f"{price_symbol}{price_whole}"
            
            if full_price.endswith('.'):
                full_price = full_price[:-1]  
            
            return full_price
        else:
            return ""
    except AttributeError:
        return ""

def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
        return rating
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
            return rating
        except AttributeError:
            return ""

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
        return review_count
    except AttributeError:
        return ""

def get_availability(soup):
    try:
        availability = soup.find("div", attrs={'id': 'availability'})
        return availability.find("span").string.strip() if availability else "Not Available"
    except AttributeError:
        return "Not Available"

if __name__ == '__main__':
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    URL = "https://www.amazon.com/s?k=java+books&i=stripbooks-intl-ship"
    
    try:
        webpage = requests.get(URL, headers=HEADERS)
        webpage.raise_for_status()  # Check if request was successful
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        exit()

    soup = BeautifulSoup(webpage.content, "html.parser")
    links = soup.find_all("a", attrs={'class': 'a-link-normal s-no-outline'})
    links_list = []

    # Construct valid URLs
    for link in links:
        href = link.get('href')
        if href and href.startswith('/'):  # Check if href is a relative link
            links_list.append("https://www.amazon.com" + href)

    d = {"title": [], "price": [], "rating": [], "reviews": [], "availability": []}

    for link in links_list:
        try:
            new_webpage = requests.get(link, headers=HEADERS)
            new_webpage.raise_for_status()  
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['availability'].append(get_availability(new_soup))
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data from {link}: {e}")
            continue

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'] = amazon_df['title'].replace('', np.nan)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
    print(amazon_df)
