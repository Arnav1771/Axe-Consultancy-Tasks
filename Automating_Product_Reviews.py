import scrapy
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent

class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    start_urls = [
        'https://ecommercewebsite.com/product1/reviews',
        'https://ecommercewebsite.com/product2/reviews'
    ]

    def parse(self, response):
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        page = requests.get(response.url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        reviews = []
        for review in soup.find_all('div', class_='review'):
            review_data = {
                'title': review.find('h2', class_='review-title').text.strip(),
                'rating': review.find('span', class_='review-rating').text.strip(),
                'content': review.find('p', class_='review-content').text.strip(),
                'author': review.find('span', class_='review-author').text.strip(),
                'date': review.find('span', class_='review-date').text.strip()
            }
            reviews.append(review_data)
        
        # Save reviews to a CSV file
        df = pd.DataFrame(reviews)
        df.to_csv('reviews.csv', mode='a', header=False, index=False)

# To run the spider, save this script as `reviews_spider.py` and run:
# scrapy runspider reviews_spider.py