# -*- coding: utf-8 -*-
import scrapy


class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['guazi.com']
    start_urls = ['http://guazi.com/']


    def parse(self, response):
        pass
