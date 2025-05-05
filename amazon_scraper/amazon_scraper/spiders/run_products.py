from scrapy.cmdline import execute
execute(["scrapy", "crawl", "products","-o", "productlist.csv"])
