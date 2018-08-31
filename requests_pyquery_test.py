import requests
import time
import json
from pyquery import PyQuery as pq

class BTCSpider(object):

    def __init__(self):
        self.url = "http://8btc.com/forum-61-{}.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        self.data_list = []

    def get_url(self):
        return [self.url.format(i) for i in range(1,11)]

    def get_html(self, url):
        html = requests.get(url, headers=self.headers)
        html_text = html.text
        return html_text

    def get_value(self, html):
        pyq_data = pq(html)
        a_list = pyq_data('.xst').items()
        for a in a_list:
            dict = {}
            dict["text"] = a.text()
            dict["url"] = a.attr('href')
            self.data_list.append(dict)

    def write_data(self):
        with open("btc.json", 'w') as f:
            f.write(json.dumps(self.data_list))

    def run(self):
        # 循环遍历 列表页面
        url_list = self.get_url()
        for url in url_list:
            print(url)
            html = self.get_html(url)
            self.get_value(html)
            for detail in self.data_list:
                detail_url = detail["url"]
                print(detail_url)
                detail_html = self.get_html(detail_url)
                # 解析详情页的数据
                detail_data = pq(detail_html)
                detail['result'] = detail_data('td .t_f').text().replace('\n', '')
            time.sleep(1)
        self.write_data()

a = BTCSpider()
a.run()