from scrapy import Spider, Request
from amazon_scraper.items import ProductItem
import csv
import time
from selenium.common.exceptions import TimeoutException
import random
from bs4 import BeautifulSoup
from amazon_scraper.spiders.helpers.soup_helper import SoupHelper
from oditworks_scraper_utils import get_chrome_driver, make_scrapy_response, parse_cookie_string, wait_for_amazon_products



class ProductScraperSpider(Spider):
    name = "products"
    allowed_domains = ["amazon.com"]
    cookie = ''
    categoryurlcsvfilepath = 'C:\\scraper\\amazon_scraper\\main_categories.csv'
    

    def __init__(self, main_category=None, sub_category=None, *args, **kwargs):
        super(ProductScraperSpider, self).__init__(*args, **kwargs)
        self.main_category = main_category
        self.sub_category = sub_category
        
        # Setup headless Chrome
        driver = get_chrome_driver(headless=True,proxy=False)
        self.driver = driver

    def _recreate_driver(self):
        if self.driver:
            self.driver.quit()

            driver = get_chrome_driver(headless=True,proxy=False)
            self.driver = driver

            
    def start_requests(self):
        with open(self.categoryurlcsvfilepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                main = row.get('main_category')
                sub = row.get('sub_category')
                url = row.get('sub_category_url')

                if url:
                    if self.main_category and self.sub_category:
                        if main == self.main_category and sub == self.sub_category:
                            yield Request(url=url, callback=self.parse_with_selenium, meta={'main_category': main, 'sub_category': sub})
                    else:
                        yield Request(url=url, callback=self.parse_with_selenium, meta={'main_category': main, 'sub_category': sub})

    def parse_with_selenium(self, response):
        #main_category = response.meta.get('main_category')
        #sub_category = response.meta.get('sub_category')

        if response.status == 503:
            self.logger.warning("503 received, retrying with new proxy and user-agent...")
            self._recreate_driver()  # Recreate with a new agent/proxy
            yield response.request.replace(dont_filter=True)
            return

        url = response.url
        #meta = response.meta if response.meta else {}
        # Step 1: Go to base domain first to allow cookie setting
        self.driver.get("https://www.amazon.com")

        # Step 2: Set cookies (replace with actual cookie parsing logic if needed)
        cookies = parse_cookie_string(self.cookie);
        for key, value in cookies.items():
            self.driver.add_cookie({'name': key, 'value': value, 'domain': '.amazon.com'})

        # Step 3: Navigate to the actual URL
        self.driver.get(url)

        # Optional wait logic for JavaScript-rendered elements
        time.sleep(3)  # or use WebDriverWait

        # ⏳ Wait for Amazon product results (by role="listitem") to be present
        try:
            wait_for_amazon_products(self.driver, 15)
        except TimeoutException:
            self.logger.warning("Product list didn't load in time.")

        # Step 4: Get content and process
        # ✅ Construct Scrapy HtmlResponse from the fully rendered page
        sel_response = make_scrapy_response(self.driver,url)

        # if meta:
        #     sel_response.meta.update(response.meta)

        # Example: Extract all links
        #return self.parse_product_list(sel_response)
        yield from self.parse_product_list(sel_response)

    def parse_product_list(self, response):
        self.logger.info("Parsing rendered product list")
        product_links = response.css('a.a-link-normal.s-no-outline::attr(href)').getall()
        print(len(product_links));
        for link in product_links:
            yield response.follow(link, self.parse_productdata, meta={'main_category': "", 'sub_category': ""})

        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page:
            self.logger.info(f"Following pagination to: {next_page}")
            yield response.follow(next_page, self.parse_product_list)
        else:
            self.logger.info("No next page found.")

    def parse_productdata(self, response):
        item = ProductItem()
        try:
            soup = BeautifulSoup(response.text, "html.parser")

            item['main_category'] = response.meta['main_category']
            item['sub_category'] = response.meta['sub_category']
            item['product_url'] = response.url
            item['title'] = response.css('title::text').get()
            divAsin = soup.find('div', id='title_feature_div')
            asin = divAsin.get('data-csa-c-asin')
            item['asin'] = asin
            item['productTitle']= SoupHelper.extract_text("#productTitle",soup)
            item['reviewStars']= SoupHelper.extract_text("i[data-asin] span.a-icon-alt",soup)
            item['reviewCount']= SoupHelper.extract_text("#acrCustomerReviewText",soup)
            item['price']= SoupHelper.extract_text("span.a-price span.a-offscreen",soup)
            item['brand']= SoupHelper.extract_text("#bylineInfo",soup)
            item['pacingMicro']= SoupHelper.extract_key_value_pairs("productOverview_feature_div",soup)
            item['aboutThisItem']= SoupHelper.extract_text("#feature-bullets ul li",soup,multiple=True)
            item['altImages']= [img.get("src") for img in soup.select("#altImages img") if img.get("src")]
            item['productDescription']= SoupHelper.extract_text("#productDescription_feature_div",soup)
            item['videoLinks']= [video.get("src") for video in soup.select(".a-carousel-viewport video") if video.get("src")]
            item['productInformation']= SoupHelper.extract_key_value_pairs("productDetails_detailBullets_sections1",soup)
            item['warrantySupport']= SoupHelper.extract_text("#productSupportAndReturnPolicy",soup)
            item['feedback']= SoupHelper.extract_text("#dp-feedback-section",soup)

        except Exception as e:
            self.logger.error(f"Error parsing product data: {e}")
        
        yield item

        

    def closed(self, reason):
        self.driver.quit()
