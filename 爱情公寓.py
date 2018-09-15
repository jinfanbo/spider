import requests
import time
import random
import json

# 获取每一页数据
def get_one_page(url):
    headers = {
        'Cookie': 'uuid_n_v = v1;uuid = 9C2C4390B89311E8952B171B1DEA3B56DD363AD9FFFA4920A5621E992E5D2270;_csrf = b186f97ad6710d30a9ce051cb8fbdd1e58bd1f0ced9630cc036289d5f2173d04;_lxsdk_cuid = 165db2cded8c8 - 08da7d3123432e - 47e1039 - 1fa400 - 165db2cded9c8;_lxsdk = 9C2C4390B89311E8952B171B1DEA3B56DD363AD9FFFA4920A5621E992E5D2270;__mta = 152007302.1536980475837.1536980487540.1536980492172.5;_lxsdk_s = 165db2cdeda - 5cf - b01 - ef1 % 7C % 7C17',
        'User - Agent':'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 67.0.3396.99 Safari / 537.36'
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

# 解析每一页数据
def parse_one_page(html):
    data = json.loads(html)['cmts']  # 获取评论内容   ...将str变成dict和list
    for item in data:
        yield {
            'data': item['time'].split(' ')[0],
            'nickname': item['nickName'],
            'city': item['cityName'],
            'rate': item['score'],
            'conment': item['content']
        }

# 保存到文本文档中
def save_to_txt():
    for i in range(1, 1001):
        print("开始保存第%d" % i)
        url = 'http://m.maoyan.com/mmdb/comments/movie/1175253.json?_v_=yes&offset=' + str(i)
        html = get_one_page(url)  # ...一页的数据
        for item in parse_one_page(html):
            with open('爱情公寓.txt', 'a', encoding='utf-8') as f:
                f.write(item['data'] + ',' + item['nickname'] + ',' + item['city'] + ','
                        + str(item['rate']) + ',' + item['conment'] + '\n')
                # item.sleep(random.randint(1,100)/20)
                time.sleep(2)

# 去重重复的评论内容
def delet_repeat(old, new):
    oldfile = open(old, 'r', encoding='utf-8')
    newfile = open(new, 'w', encoding='utf-8')
    content_list = oldfile.readlines()  # 获取所有评论数据集
    content_alread = []  # 储存去重后的评论数据集
    for line in content_list:
        if line not in content_alread:
            newfile.write(line + '\n')
            content_alread.append(line)
    oldfile.close()
    newfile.close()
# save_to_txt()
delet_repeat(r'爱情公寓.txt', r'爱情公寓_new.txt')
