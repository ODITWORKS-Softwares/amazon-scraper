import scrapy
from amazon_scraper.items import CategoryItem
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import debugpy
import re


class MainCategoriesSpider(scrapy.Spider):
    name = "main_categories"
    allowed_domains = ["amazon.com"]
    start_urls = ["https://www.amazon.com/nav/ajax/hamburgerMainContent?ajaxTemplate=hamburgerMainContent&pageType=Gateway&hmDataAjaxHint=1&navDeviceType=desktop&isSmile=0&isPrime=0&isBackup=false&hashCustomerAndSessionId=24067bffa62626315e1ec346bcfb7fd888e75721&languageCode=en_US&environmentVFI=AmazonNavigationCards%2Fdevelopment%40B6317002897-AL2_aarch64&secondLayerTreeName=unlimited_instant_videos_exports%2Bprm_digital_music_hawkfire%2Bkindle%2Bandroid_appstore%2Belectronics_exports%2Bcomputers_exports%2Bsbd_alexa_smart_home%2Barts_and_crafts_exports%2Bautomotive_exports%2Bbaby_exports%2Bbeauty_and_personal_care_exports%2Bwomens_fashion_exports%2Bmens_fashion_exports%2Bgirls_fashion_exports%2Bboys_fashion_exports%2Bhealth_and_household_exports%2Bhome_and_kitchen_exports%2Bindustrial_and_scientific_exports%2Bluggage_exports%2Bmovies_and_television_exports%2Bpet_supplies_exports%2Bsoftware_exports%2Bsports_and_outdoors_exports%2Btools_home_improvement_exports%2Btoys_games_exports%2Bvideo_games_exports%2Bgiftcards%2Bamazon_live%2BAmazon_Global&customerCountryCode=IN"]
    referer = "https://www.amazon.com/"

    def start_requests(self):
        cookies = {}

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers={"Referer": self.referer},
                cookies=cookies,
                callback=self.parse
            )

    def parse(self, response):
        try:    
            print("Main Category extraction started")
            clean_html = response.text.replace('\\"', '"').replace("\\n", "\n")
            soup = BeautifulSoup(clean_html,'html.parser')

            # Loop through all main category blocks
            for section in soup.find_all('section', class_=re.compile("category-section")):
                main_heading_tag = section.find('div', class_=re.compile('hmenu-item.*hmenu-title'))
                if not main_heading_tag:
                    continue
                
                main_category = main_heading_tag.get_text(strip=True)
                subcategories = []

                for link in section.find_all('a', class_=re.compile("hmenu-item")):
                    href = link.get('href', '').replace('"', '').strip()
                    text = link.get_text(strip=True)
                    if href and text:
                        subcategories.append({'title': text, 'url': href})
                        item = CategoryItem()
                        item['main_category'] = main_category
                        item['sub_category'] = text
                        item['sub_category_url'] = f"{self.referer}{href}"
                        yield item

        except Exception as e:
            self.logger.error("Exception in parse()", exc_info=True)