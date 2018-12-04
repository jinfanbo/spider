from scrapy import Spider, Request
from datetime import datetime
import json
from maoyan.items import MaoyanItem


class MaoyanCommentSpider(Spider):
    name = 'maoyan_comment'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://m.maoyan.com/42964?_v_=yes']
    comment_url = 'http://m.maoyan.com/mmdb/comments/movie/42964.json?_v_=yes&offset={}&startTime={}'
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # def start_requests(self):
    #     yield Request(self.movie_url, callback=self.parse_all_page)

    def parse_all_page(self, response):
        comment_num = response.xpath('//*[@id="app"]/div/div[4]/section[8]/a/h4/span[2]/text()')
        print(comment_num)
        page = int(comment_num) // 15

        for offset in range(0, page, 15):
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