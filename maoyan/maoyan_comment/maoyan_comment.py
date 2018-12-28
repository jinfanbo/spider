import requests
import json
import random
import pymongo
import pandas as pd
from datetime import datetime


class MaoyanCommentSpider(object):
    user_agent = [
        'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
        'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1'
    ]
    ip = [
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
        {"port": "39917", "ip": "117.68.243.104"}
    ]

    def __init__(self, name):
        self.now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.movie_url = 'http://m.maoyan.com/ajax/search?kw={name}&cityId=1&stype=-1'.format(name=name)
        self.start_url = 'http://maoyan.com/{movieid}?_v_=yes'
        self.comment_url = 'http://m.maoyan.com/mmdb/comments/movie/{movieid}.json?_v_=yes&offset=15&startTime={date}'
        self.info = []

    def GetMovieId(self):
        '''
        根据用户输入的电影名返回电影的ID
        :return: movieID
        '''
        headers = {
            'User-Agent': random.choice(self.user_agent)
        }
        response = requests.get(self.movie_url, headers=headers)
        if response.status_code == 200:
            movies_list = response.text
            movies_list_json = json.loads(movies_list)
            movie_id = movies_list_json['movies']['list'][0]['id']
            return movie_id
        else:
            print("电影ID获取失败：状态码" + response.status_code)

    def GetCommentNums(self, movie_id):
        '''
        根据电影id进入电影详情页返回电影评论总数
        :return: commentNUM
        '''
        headers = {
            # 'Origin': 'http://m.maoyan.com',
            # 'Referer': 'http://m.maoyan.com/movie/{movieid}?_v_ = yes'.format(movieid=movie_id),
            'User-Agent': random.choice(self.user_agent)
        }
        response = requests.get(self.comment_url.format(movieid=movie_id, date=self.now_date), headers=headers)
        if response.status_code == 200:
            # print(movie_detail)
            # detail = etree.HTML(movie_detail)
            # print(detail)
            # comment_nums = detail.xpath('//a[@class="link link-more comments-link"]/h4/span[2]/text()')
            comments_list = json.loads(response.text)
            comment_nums = comments_list.get('total')
            return comment_nums
        else:
            print("电影评论总数获取失败：状态码" + response.status_code)

    def GetComment(self, movie_id, comment_nums):
        '''
        获取所有评论
        :param movie_id: GetMovieId()获取电影id
        :return:
        '''
        headers = {
            'User-Agent': random.choice(self.user_agent)
        }
        for num in range(0, comment_nums, 15):
            ip_proxy = random.choice(self.ip)
            ip_proxies = {'https': 'http://' + ip_proxy["ip"] + ':' + ip_proxy["port"]}
            print(ip_proxies)
            response = requests.get(self.comment_url.format(movieid=movie_id, date=self.now_date), headers=headers, proxies=ip_proxies)
            if response.status_code == 200:
                comments_list = json.loads(response.text)
                if comments_list.get('total') != 0:
                    comments = comments_list.get('cmts')
                    self.now_date = comments[0].get("startTime")
                    print(self.now_date)
                    for comment in comments:
                        cm = {}
                        cm["cityName"] = comment.get("cityName")
                        cm["content"] = comment.get("content")
                        cm["nickName"] = comment.get("nickName")
                        cm["score"] = comment.get("score")
                        cm["startTime"] = comment.get("startTime")
                        self.info.append(cm)
                else:
                    print('该url无评论！ ' + self.comment_url.format(movieid=movie_id, date=self.now_date))
            else:
                print("电影评论获取失败：状态码" + response.status_code)

    def DataSave(self):
        info_list = []
        for info in self.info:
            info_list.append(
                [info['nickName'], info['cityName'], info['score'], info['content'], info['startTime']])
        if self.info != []:
            # 写入csv
            # 表头
            name = ['nickName', 'cityName', 'score', 'content', 'startTime']
            # 建立DataFrame对象
            file_test = pd.DataFrame(columns=name, data=info_list)
            # 数据写入csv
            file_test.to_csv(r'E:/spider/spider/maoyan/maoyan_comment_TQYB_2018-12-28.csv', index=False)
            # 写入mongodb
            mongo = pymongo.MongoClient()
            collection = mongo.maoyan.comment_TQYB
            collection.insert(self.info)
            mongo.close()
        else:
            print('info无内容！')

    def RunSpider(self):
        movie_id = self.GetMovieId()
        print(movie_id)
        comment_num = self.GetCommentNums(movie_id)
        print(comment_num)
        self.GetComment(movie_id, comment_num)
        self.DataSave()


if __name__ == '__main__':
    spider1 = MaoyanCommentSpider('天气预爆')
    # movie_id = spider1.GetMovieId()
    # print(movie_id)
    # comment_num = spider1.GetCommentNums(movie_id)
    # print(comment_num)
    spider1.RunSpider()
