import requests
from bs4 import BeautifulSoup

class BTCSpider(object):
    def __init__(self):
        self.url = "http://8btc.com/forum-61-{}.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        self.data_list = []
        self.data_detai_list = []

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        # 当前页面的字符集 是gbk ;
        # 一般都是 转成对应的字符串处理 但是 可能转码的时候有小问题
        # 出现问题之后, 使用原生的 bytes
        data = response.text
        return data

    # 批量的url
    def get_url_list(self):
        return [self.url.format(i) for i in range(1, 5)]

    def bs4_demo_parse_data(self, data):
        # 解析 bs4
        parse_data = BeautifulSoup(data, 'lxml')
        # 解析数据 title 和url list
        # 拿到了目标标签的 list
        a_list = parse_data.select('.xst')
        for a in a_list:
            dict = {}
            dict['text'] = a.get_text()
            dict['url'] = a.get('href')
            self.data_list.append(dict)

    def run(self):
        # 循环遍历 列表页面
        url_list = self.get_url_list()
        for url in url_list[:1]:
            print(url)
            data = self.get_data(url)
            self.bs4_demo_parse_data(data)

        # 等列表页 抓取完毕; 在抓取详情页
        for detail in self.data_list:
            detail_url = detail['url']
            print(detail_url)

            detail_data = self.get_data(detail_url)

            #解析详情页的数据
            detail_parse = BeautifulSoup(detail_data,'lxml')

            detail['result'] = detail_parse.select('.t_f')[0].get_text().replace('\n','')
        print(self.data_list)

spider = BTCSpider()
spider.run()
