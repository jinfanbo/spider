import requests
import random
import json
import re
import pymongo

cookie = 'guider_quick_search=on; SESSION_HASH=5ea5faac944e0742b33be9469325ff0e18e5eb01; jy_refer=www.baidu.com; FROM_ST_ID=1764229; user_access=1; PHPSESSID=f058541869535ae08346792aa2ea1195; is_searchv2=1; COMMON_HASH=f55bf846489b9587c3e6f369d6d083a9; stadate1=183581237; myloc=21%7C2103; myage=21; mysex=m; myuid=183581237; myincome=30; PROFILE=184581237%3A%25E6%259D%25AF%25E4%25B8%25AD%25E6%2599%25AF%25E8%2589%25B2%25E9%25AC%25BC%25E9%25AD%2585%3Am%3Aimages1.jyimg.com%2Fw4%2Fglobal%2Fi%3A0%3A%3A1%3Azwzp_m.jpg%3A1%3A1%3A50%3A10; main_search:184581237=%7C%7C%7C00; RAW_HASH=OjXBbOpclK9TCRaAKcve-WqrvGerWhD5EKHnGHHXUM0%2AfOSJVn4tPVEq5Ilg2QKak7TmAa3abfo1rqsmmlsoosI%2ATAfNLd%2AF3dI81DwHYc8nOIs.; pop_avatar=1; pop_time=1541734258127'

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

ip = {"code": "0", "msg": [
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

uid = []

def get_json(data):
    print(data['p'])
    ip_proxy = random.choice(ip['msg'])
    ip_proxies = {'https': 'http://' + ip_proxy["ip"] + ':' + ip_proxy["port"]}
    print(ip_proxies)
    response = requests.post('http://search.jiayuan.com/v2/search_v2.php', data=data,
                  headers={'User-Agent': ua, 'Cookie': cookie, 'Connection': 'keep-alive'}, proxies=ip_proxies)
    # print(response.text)
    pageAll = json.loads(re.match(r'##jiayser##(.*)##jiayser##//',response.text).group(1))['pageTotal']
    # print(pageAll)
    dcts = json.loads(re.match(r'##jiayser##(.*)##jiayser##//',response.text).group(1))['userInfo'][1:]
    # print(dcts)
    lst = []
    for dct in dcts:
        print(dct)
        if dct['realUid'] not in uid:
            uid.append(dct['realUid'])
            lst.append(dct)
    sava_mongodb(lst)
    if data['p'] < 106:
        data['p'] += 1
        get_json(data)



def sava_mongodb(dct):
    mongo = pymongo.MongoClient()
    collection = mongo.sjjy.users
    collection.insert(dct)
    mongo.close()


if __name__ == '__main__':
    data = {
        'sex': 'f',
        'key': '',
        'stc': '',
        'sn': 'charm',
        'sv': 1,
        'p': 1,
        'f': 'select',
        'listStyle': 'bigPhoto',
        'pri_uid': 184581237,
        'jsversion': 'v5'
    }
    get_json(data)
