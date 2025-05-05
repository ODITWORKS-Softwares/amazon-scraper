from scrapy.cmdline import execute
execute(["scrapy", "crawl", "main_categories", "-o", "main_categories.csv"])
