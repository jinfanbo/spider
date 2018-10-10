# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from datetime import datetime
import json
from maoyan.items import MaoyanItem

class MaoyanCommentSpider(Spider):
    name = 'maoyan_comment'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://m.maoyan.com/']

    comment_url = 'http://m.maoyan.com/mmdb/comments/movie/342166.json?_v_=yes&offset={}&startTime={}'
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def start_requests(self):
        yield Request(self.comment_url.format(0, self.date_now), callback=self.parse_all_page)

    def parse_all_page(self, response):
        comment_json = json.loads(response.text)
        for offset in range(0, 5000, 15):
            yield Request(self.comment_url.format(offset, self.date_now), callback=self.parse_info)

    def parse_info(self, response):
        result = json.loads(response.text)
        # print(result)
        item = MaoyanItem()
        cmts_list = result.get('cmts')
        for field in item.fields:
            for cmts in cmts_list:
                if field in cmts.keys():
                    item[field] = cmts.get(field)
        yield item
