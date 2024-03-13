import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['bookstore']
collection = db['books']

# Function to scrape book data from a given page
def scrape_books(page_url):
    response = requests.get(page_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            title = book.h3.a['title']
            price = book.select('div p.price_color')[0].get_text()
            availability = book.select('div p.availability')[0].get_text().strip()
            rating = book.p['class'][1]
            
            # Create a dictionary to represent the book
            book_data = {
                'title': title,
                'price': price,
                'availability': availability,
                'rating': rating
            }
            
            # Insert the book data into MongoDB
            collection.insert_one(book_data)

# Scrape all 50 pages
base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
for page_num in range(1, 51):
    page_url = base_url.format(page_num)
    scrape_books(page_url)

# Close the MongoDB connection
client.close()
