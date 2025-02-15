# Amazon Price Tracker  

This is a web application that allows users to track the price of a specific Amazon product and receive email alerts when the price drops below their target price.  

###
![ScreenShot Tool -20250214232711](https://github.com/user-attachments/assets/958355c0-f556-4a1f-b028-e7172ab2d118)
###

## Features  
- Scrapes the product's title and current price from Amazon.  
- Stores user details (name, email, phone, target price) in a MongoDB database.  
- Sends email alerts when the product's price reaches the user's target price.  
- Uses Flask for the web interface and ScraperAPI to bypass Amazon's scraping restrictions.  
- Implements a stylish frontend with **Glassmorphism UI**.  

## Tech Stack  
- **Frontend**: HTML, CSS (Glassmorphism Design)  
- **Backend**: Python (Flask)  
- **Web Scraping**: BeautifulSoup, ScraperAPI  
- **Database**: MongoDB  
- **Email Notifications**: SMTP with Gmail  

## Prerequisites  
Before running the project, ensure you have the following installed:  
- Python 3  
- MongoDB  
- `pip` (Python package manager)  
- A **ScraperAPI** account ([Get API Key](https://www.scraperapi.com/))
###
![ScreenShot Tool -20250214235127](https://github.com/user-attachments/assets/fdaf5265-4d80-4662-9cd6-a7fbe4bf7a09)
###
- A **Gmail account** with **less secure apps enabled** (or an App Password)  

## Installation & Setup  

### Clone the Repository  
```bash
git clone https://github.com/r0han01/amazon-price-tracker-webscraping-bs4.git
cd amazon-price-tracker
```

### Create a Virtual Environment (Optional but Recommended)  
```bash
python -m venv venv  
source venv/bin/activate  # On macOS/Linux  
venv\Scripts\activate  # On Windows  
```

### Install Dependencies  
```bash
pip install -r requirements.txt  
```

### Set Up Environment Variables  
Create a `.env` file in the project directory and add your credentials:  
```
GMAIL_USER=your-email@gmail.com  
GMAIL_PASSWORD=your-app-password  
```

### Start MongoDB  
Ensure MongoDB is running before you start the app. If you have MongoDB installed locally, start it with:  
```bash
mongod --dbpath /path/to/your/data  
```
Or use a **MongoDB Atlas Cloud Database**.  

### Run the Flask App  
```bash
python app.py  
```
The app will run on **http://127.0.0.1:8080/**.  

## How It Works  
1. Users enter their **name, phone, email, and target price** for the Amazon product.  
###
![ScreenShot Tool -20250214235854](https://github.com/user-attachments/assets/c2b3e3f6-8086-4807-afa8-cd50430f0372)
###
![ScreenShot Tool -20250215000752](https://github.com/user-attachments/assets/30e416fc-df89-4f0d-b694-00600d17c22c)
###
2. The app scrapes the **product title and current price**.  
###
![resetImage](https://github.com/user-attachments/assets/84490cd6-5418-4eeb-bc76-3625f28ccdce)
###
3. The user details are stored in **MongoDB**.
###
![Screenshot from 2025-02-15 00-10-35](https://github.com/user-attachments/assets/87d3184d-2f68-47a3-8bd2-06052f9f6351)
###
4. A background thread **checks the price periodically**.  
5. If the price **drops below the target**, an **email notification** is sent.
###
![ScreenShot Tool -20250215001126](https://github.com/user-attachments/assets/7b3b50a5-2788-45e6-88f8-fdedf6ea148e)
###

## Security Notes  
- **Do not use your main Gmail password.** Use an **App Password** instead.
  Please refer to my another repo in order to know more details about & how to create app password using gmail here is the link - https://github.com/r0han01/PHPMailer-Gmail-SMTP-Integration?tab=readme-ov-file#2-setting-up-gmail-app-password
- **Use a proxy service like ScraperAPI** to avoid IP bans while scraping.  

## Future Improvements  
- Add **user authentication** for tracking multiple products.  
- Implement **Twilio SMS notifications** for price alerts.  
- Support **multiple e-commerce websites** (e.g., eBay, Walmart).  
- Deploy the app on **Heroku or AWS**.  

## Contributing  
Feel free to fork this repo and submit a pull request!  

## License  
This project is open-source under the **MIT License**.  

