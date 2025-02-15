import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")  # Connect to local MongoDB server
db = client['priceTrackerDB']  # Create a database called 'priceTrackerDB'
users_collection = db['users']  # Create a collection called 'users'

# ScraperAPI configuration
api_key = "5bfd295c94da447b824bd66f93f31d15"
api_url = "https://api.scraperapi.com"

# Gmail credentials for sending emails (loaded from .env)
GMAIL_USER = os.getenv("GMAIL_USER")  # Load Gmail email from .env
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")  # Load Gmail password from .env

# Define the Amazon URL that you want to scrape
TARGET_URL = "https://www.amazon.com/iPhone-Pro-256GB-Black-Titanium/dp/B0DHT1DDXR/ref=sr_1_4?sr=8-4"

def send_email(target_email, product_title, current_price):
    """Send an email notification when the price hits the target."""
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USER
    msg['To'] = target_email
    msg['Subject'] = f"Price Alert: {product_title}"

    body = f"The price of '{product_title}' has dropped to ${current_price}. Check it out now!"
    msg.attach(MIMEText(body, 'plain'))

    # Sending the email using SMTP
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, target_email, msg.as_string())
        server.close()
        print(f"Email sent to {target_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_price(target_price, target_email):
    """Check the product price periodically and send an email if the target price is hit."""
    params = {
        "api_key": api_key,
        "url": TARGET_URL,
        "render": "true"
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product title
        title = soup.find("span", {"id": "productTitle"})
        if title:
            title = title.get_text(strip=True)
        else:
            title = "Title not found"

        # Extract product price
        price = soup.find("span", {"class": "a-price-whole"})
        if price:
            price = price.get_text(strip=True)
            price = float(price.replace(",", ""))  # Convert to float for comparison
        else:
            price = "Price not found"

        if price != "Price not found" and price <= target_price:
            send_email(target_email, title, price)
            return True  # Price hit, stop checking
        else:
            return False  # Price not hit yet
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    # Scrape product title and price once when page loads
    params = {
        "api_key": api_key,
        "url": TARGET_URL,
        "render": "true"
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract product title
        title = soup.find("span", {"id": "productTitle"})
        if title:
            title = title.get_text(strip=True)
        else:
            title = "Title not found"

        # Extract product price
        price = soup.find("span", {"class": "a-price-whole"})
        if price:
            price = price.get_text(strip=True)
            price = float(price.replace(",", ""))  # Convert to float
        else:
            price = "Price not found"

    else:
        title = "Product not found"
        price = "Price not found"

    if request.method == "POST":
        target_price = float(request.form['target_price'])
        target_email = request.form['email']
        user_name = request.form['name']
        user_phone = request.form['phone']

        # Store user data in MongoDB
        user_data = {
            "name": user_name,
            "phone": user_phone,
            "email": target_email,
            "target_price": target_price
        }
        users_collection.insert_one(user_data)

        # Start the price check in a separate thread so it doesn't block the server
        threading.Thread(target=check_price, args=(target_price, target_email)).start()

        return render_template('index.html', product_title=title, current_price=price,
                               message="Price tracking started! You will be notified when the price is reached.")

    return render_template('index.html', product_title=title, current_price=price)

if __name__ == "__main__":
    # Run the app on localhost and port 8080
    app.run(host='127.0.0.1', port=8080, debug=True)
