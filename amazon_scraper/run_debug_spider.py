# run_debug_spider.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from amazon_scraper.spiders.main_categories import MainCategoriesSpider
from amazon_scraper.spiders.product_scraper import ProductScraperSpider

import debugpy

# OPTIONAL: Attach debugger
debugpy.listen(("localhost", 5678))
print("🪲 Waiting for debugger to attach...")
debugpy.wait_for_client()
debugpy.breakpoint()

process = CrawlerProcess(get_project_settings())
process.crawl(ProductScraperSpider)
process.start()
