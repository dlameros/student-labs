import scrapy
class QuotesSpider(scrapy.Spider):
    name = "quotes"

start_urls = ['https://quotes.toscrape.com']
def parse(self, response):
    self.logger.info('Hi, its my spider')
    pass