import requests
from bs4 import BeautifulSoup

url = 'http://www.xicidaili.com/wt'
headers  = {
            'User - Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 67.0.3396.99 Safari / 537.36'
        }
html = requests.get(url, headers = headers)
txt = html.content.decode('utf-8')

print(txt)
bs_txt = BeautifulSoup(txt, 'lxml')

# ip = bs_txt.select_one('tr .odd')

print(bs_txt)