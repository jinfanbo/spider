import requests
from bs4 import BeautifulSoup
import re

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

a_list = []
useragent_list = []

def get_html(url):
    response = requests.get(url, headers=headers)
    html = response.text
    return html
    # with open("useragent_get.html", "w") as f:
    #     f.write(html)

def get_list(html):
    html_bf = BeautifulSoup(html, 'lxml')
    ul_list = html_bf.find_all('ul')
    print(len(ul_list))
    for ul in ul_list:
        a = ul.find_all('a')
        a_list.append(a[0])
    # print(a_list)
    for a in a_list:
        pattern = re.compile('<a.*?>(.*?)</a>')
        useragent_list.append(re.match(pattern, str(a)).group(1))
    return useragent_list

def write_txt(list):
    for i in list:
        with open("useragent_get.txt", "a") as f:
            f.write(i)
            f.write('\n')

if __name__ == '__main__':
    url = 'http://useragentstring.com/pages/useragentstring.php?name=All'
    html = get_html(url)
    useragentlist = get_list(html)
    write_txt(useragentlist)