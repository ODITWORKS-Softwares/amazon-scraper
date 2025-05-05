A robust Amazon web scraper built with Scrapy and Selenium WebDriver, designed for extracting product listings dynamically rendered on Amazon’s search pages.
 
 Features
🔎 Scrapes Amazon search result listings.

🧠 Uses Selenium WebDriver to handle JavaScript-rendered content.

🛡️ Proxy support (e.g., Oxylabs or any rotating proxy provider).

🍪 Cookie handling via parse_cookie_string() for authenticated sessions.

🧩 Modular utility functions for reuse across spiders.

🧪 Includes timeout and wait handling for Amazon page load issues.

🗂️ Category-Based Scraping
  You can specify Amazon categories (e.g., Electronics, Books, Toys) to scrape product listings for targeted segments.
  
    Accepts category either from:
    CSV input (e.g., categories.csv)
    Hardcoded or passed via command-line arguments
    Dynamically builds Amazon search URLs like: https://www.amazon.com/s?k=Headphones&i=electronics

 ⚙️ Setup Instructions
  git clone https://github.com/your-username/amazon-scraper.git
  cd amazon-scraper

  Install Dependencies:
  pip install -r requirements.txt

  Install WebDriver (e.g., ChromeDriver) Ensure your system has ChromeDriver installed and matches your browser version.

  🧪 Run the Spider:
  scrapy crawl main_categories
    scrapy crawl main_categories -o output.csv
  Extract data category wise
    scrapy crawl products -a main_category=Electronics -a sub_category=Headphones -o output.csv

 🔐 Proxy & Cookie Setup:
   In oditworks_scraper_utils.py, you can:

    Define your Oxylabs or other proxy credentials.
    
    Use parse_cookie_string(raw_cookie) to load cookies from raw headers and inject them into the Selenium driver.

📁 Example Utility Functions
    parse_cookie_string(cookie_string)
    
    get_random_user_agent()
    
    wait_for_amazon_products(driver, timeout, logger

🛠 Requirements:
  Python 3.8+
  Scrapy
  Selenium
  Chrome + ChromeDriver
  (Optional) Proxy provider account

✅ Disclaimer
This project is for educational and research purposes only. Scraping Amazon may violate their terms of service. Use at your own risk.

