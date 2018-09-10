import requests
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup as bf
import time
import re


class CarSpider(object):
    def __init__(self):
        self.url = "https://k.autohome.com.cn/835/index_{}.html#dataList"
        self.headers = {
            "Cookie": "__ah_uuid=6CCC98AA-7E4C-4D73-8B24-F49140DB7A2A; fvlid=1536145873941Xv9lcLlop9; sessionip=222.171.151.227; sessionid=48A72157-526C-4478-8C6D-E0E3D88BD4D2%7C%7C2018-09-05+19%3A11%3A14.035%7C%7Ccn.bing.com; sessionvid=58A4E956-7F1A-4F17-B427-AB60D67CFFDC; area=230103; ahpau=1; sessionuid=48A72157-526C-4478-8C6D-E0E3D88BD4D2%7C%7C2018-09-05+19%3A11%3A14.035%7C%7Ccn.bing.com; ASP.NET_SessionId=hxedeaj4xxuns31smmsimahf; guidance=true; autoac=63C0BCADF3F194376535F385AAE837D3; autotc=BF19012F76D3AB68B6217C310F83B471; papopclub=6871FC2617DC247A524067660A25E9A5; pvidchain=2112108,2112108,2112108,2112108,103600,2112108,103600,103600,103600,103600; pbcpopclub=a19db2e0-7618-418f-b997-737349ef8c33; pepopclub=954F35BA2AADD0903E87C8EFFC095385; ahpvno=59; ref=cn.bing.com%7C0%7C0%7C0%7C2018-09-05+21%3A27%3A32.733%7C2018-09-05+19%3A11%3A14.035; _fmdata=mZsrcn0OnkGB4HonuDz4pd7kWyo2dE%2BWp6f0fMvzS5wUtTHMBywgJ0svFAt7Pyy%2Fha3f4xGAdO3sz5uRB1WQ1Oa8fb9sWf1t%2FrQ2Wc2H2n0%3D; ahrlid=1536153948373QE49YA0r35-1536154128236",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }

    #分页
    def get_url(self):
        return self.url.format(1)
        # return [self.url.format(i) for i in range(1,11)]

    #获取页面html
    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        html = response.text
        return html

    #获取口碑网址列表
    def get_comment_url(self, html):
        self.url_list = []
        pyq_data = pq(html)
        a_list = pyq_data('.btn.btn-small.fn-left')
        for a in a_list.items():
            self.url_list.append('https:{}'.format(a.attr('href')))

    #获取口碑
    # def get_comment(self, html):
    #     pyq_comment = pq(html)
    #     comment = pyq_comment('.text-con')
    #     comment.find('style').remove()
    #     comment.find('script').remove()
    #     print(comment.text())

    def get_comment(self, html):
        bs4_comment = bf(html, 'lxml')
        comment = bs4_comment.find(name = 'div', class_ = 'mouth-main')
        comment = str(comment)
        res1 = re.compile('<style.*?>.*?</style>', re.S)
        content = res1.sub('', comment)
        res2 = re.compile('<script.*?>.*?</script>', re.S)
        content = res2.sub('', content)
        res3 = re.compile('\n', re.S)
        content = res3.sub('', content)
        # comment = bs4_comment.select('div .mouth-main')
        bs4_comment = bf(content, 'lxml')
        print(bs4_comment.get_text())

    # def write_html(self, html):
    #     with open("car.html", "w") as f:
    #         f.write(html)

    def run(self):
        url = self.get_url()
        html = self.get_html(url)
        self.get_comment_url(html)
        print(self.url_list)
        time.sleep(2)
        for comment_url in self.url_list:
            print(comment_url)
            comment_html = self.get_html(comment_url)
            self.get_comment(comment_html)
            time.sleep(4)

    # def run(self):
    #     comment_html = self.get_html('https://k.autohome.com.cn/detail/view_01cnmyg52c68rkcchk64sg0000.html?st=7&piap=0|835|0|0|1|0|0|0|0|0|1#pvareaid=2112108')
    #     self.get_comment(comment_html)
    #     time.sleep(5)

spider = CarSpider()
spider.run()