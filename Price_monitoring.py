import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import schedule
import time

# Database setup
engine = create_engine('sqlite:///prices.db')
my_prices = pd.DataFrame({
    'product': ['product_1', 'product_2'],
    'price': [100.00, 200.00]
})


competitor_urls = {
    'product_1': 'https://competitor1.com/product1', #Suppose this is the URL of the competitor's product
    'product_2': 'https://competitor2.com/product2'
}

# Function to scrape price data
def scrape_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price = soup.find('span', {'class': 'price'}).text
    return float(price.replace('$', ''))

# Function to store price data
def store_price_data(product, price):
    df = pd.DataFrame({'product': [product], 'price': [price], 'timestamp': [pd.Timestamp.now()]})
    df.to_sql('prices', engine, if_exists='append', index=False)

# Function to compare and adjust prices
def adjust_prices():
    # Load your product prices
    my_prices = pd.read_sql('my_prices', engine)
    
    # Load competitors' prices
    competitor_prices = pd.read_sql('prices', engine)
    
    # Compare and adjust prices
    for product in my_prices['product']:
        my_price = my_prices.loc[my_prices['product'] == product, 'price'].values[0]
        competitor_price = competitor_prices.loc[competitor_prices['product'] == product, 'price'].values[-1]
        
        if competitor_price < my_price:
            new_price = competitor_price - 0.01  # Adjust price to be slightly lower
            my_prices.loc[my_prices['product'] == product, 'price'] = new_price
            print(f"Adjusted price for {product} to {new_price}")
    
    # Update your prices in the database
    my_prices.to_sql('my_prices', engine, if_exists='replace', index=False)

# Function to run the entire process
def run_monitoring():
    for product, url in competitor_urls.items():
        price = scrape_price(url)
        store_price_data(product, price)
    adjust_prices()

# Schedule the script to run every hour
schedule.every().hour.do(run_monitoring)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)