import scrapy


class OpenclassroomsSpider(scrapy.Spider):
    name = 'openclassrooms'
    allowed_domains = ['openclassrooms.com']
    start_urls = ['http://openclassrooms.com/']

    def parse(self, response):
        pass
