# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd

class AmazonScraperPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        return item
    
    def close_spider(self, spider):
        if self.items:
            df = pd.DataFrame(self.items)
            df.to_excel("sheets/category_products.xlsx", index=False)
