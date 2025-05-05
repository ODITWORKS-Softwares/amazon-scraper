# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    main_category = scrapy.Field()
    sub_category = scrapy.Field()
    sub_category_url  = scrapy.Field()
    pass

class CategoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    main_category = scrapy.Field()
    sub_category = scrapy.Field()
    sub_category_url  = scrapy.Field()

class ProductItem(scrapy.Item):
    main_category = scrapy.Field()
    sub_category = scrapy.Field()
    product_url = scrapy.Field()
    title =  scrapy.Field()
    asin =  scrapy.Field()
    productTitle = scrapy.Field()
    reviewStars = scrapy.Field()
    reviewCount = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    pacingMicro = scrapy.Field()
    aboutThisItem = scrapy.Field()
    altImages = scrapy.Field()
    productDescription = scrapy.Field()
    videoLinks = scrapy.Field()
    productInformation = scrapy.Field()
    warrantySupport = scrapy.Field()
    feedback = scrapy.Field()
