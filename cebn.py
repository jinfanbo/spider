import requests
from lxml import etree
# from fake_useragent import UserAgent
import time
import threading
import queue
import pymongo
import random
import re
import math


class cebn_spider(object):
    def __init__(self):
        self.start_url = 'http://www.cebn.cn/'
        self.hot_url_sum_dict = dict()
        self.ua = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
                   'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
                   ]
        self.ip = {"code": "0", "msg": [
            {"port": "30426", "ip": "114.103.157.16"},
            {"port": "42436", "ip": "115.210.67.45"},
            {"port": "36180", "ip": "116.115.209.232"},
            {"port": "33191", "ip": "49.81.83.138"},
            {"port": "45395", "ip": "114.230.146.48"},
            {"port": "25873", "ip": "180.122.144.135"},
            {"port": "48255", "ip": "221.235.208.30"},
            {"port": "33219", "ip": "121.230.208.244"},
            {"port": "47512", "ip": "182.202.220.113"},
            {"port": "35776", "ip": "114.226.220.49"},
            {"port": "29473", "ip": "113.103.117.55"},
            {"port": "37439", "ip": "220.165.26.79"},
            {"port": "24475", "ip": "49.75.0.30"},
            {"port": "46899", "ip": "125.112.231.22"},
            {"port": "26846", "ip": "14.115.71.216"},
            {"port": "34025", "ip": "49.81.19.131"},
            {"port": "45330", "ip": "114.99.20.159"},
            {"port": "42605", "ip": "220.165.29.153"},
            {"port": "20855", "ip": "125.105.130.143"},
            {"port": "39917", "ip": "117.68.243.104"}]
                   }
        self.goods_ = list()

    def get_html(self, url):
        ua = random.choice(self.ua)
        ip_proxy = random.choice(self.ip['msg'])
        ip_proxies = {'https': 'http://' + ip_proxy["ip"] + ':' + ip_proxy["port"]}
        try:
            response = requests.get(url, headers={'User-Agent': ua}, proxies=ip_proxies, timeout=1)
            print(response.status_code)
            print(ua)
            print(ip_proxies)
            return response.content.decode('utf-8')
        except Exception as e:
            print(e)
            print(ip_proxies)
            self.get_html(url)

    def parse_hot_html(self, response_html):
        p = etree.HTML(response_html)
        hots = p.xpath("//li[@class='fd-clr']/a/@href")
        for hot in hots:
            hot_html = self.get_html(hot)
            hot_sum = etree.HTML(hot_html).xpath("//li[@class='fr mr-10']/b/text()")[0]
            new_hot = re.sub('.html', '-{}.html', hot)
            self.hot_url_sum_dict[new_hot] = math.ceil(int(hot_sum) / 20)

    def goods(self, url):
        html = self.get_html(url)
        if isinstance(html, str):
            html_ = etree.HTML(html)
            htmls = html_.xpath("//div[@class='goods']")
            for p_html in htmls:
                a = {}
                try:
                    a['name'] = p_html.xpath(".//h3/a/@title")[0]
                except Exception as e:
                    print('name ' + str(e))
                    a['name'] = 'None'
                try:
                    a['info'] = p_html.xpath(".//div[@class='goods-con']/p/text()")[0]
                except Exception as e:
                    print('info ' + str(e))
                    a['info'] = 'None'
                try:
                    a['price'] = p_html.xpath(".//div[@class='goods-info']/span/text()")[0]
                except Exception as e:
                    print('price ' + str(e))
                    a['price'] = 'None'
                try:
                    a['company'] = p_html.xpath(".//div[@class='goods-company']/span/a/@title")[0]
                except Exception as e:
                    print('company ' + str(e))
                    a['company'] = 'None'
                self.goods_.append(a)
        else:
            self.goods(url)

    def save_mongodb(self):
        mongo = pymongo.MongoClient()
        collection = mongo.cebn.goods
        collection.insert(self.goods_)
        mongo.close()


if __name__ == '__main__':
    Spider = cebn_spider()
    html = Spider.get_html(Spider.start_url)
    Spider.parse_hot_html(html)
    # print(Spider.hot_url_sum_dict)
    urls = Spider.hot_url_sum_dict
    for url in urls.keys():
        for i in range(1, urls[url] + 1):
            print(url.format(i))
            Spider.goods(url.format(i))
    Spider.save_mongodb()
#15多万条数据