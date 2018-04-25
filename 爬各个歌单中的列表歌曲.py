from bs4 import BeautifulSoup
import requests
import threading
import pymysql
import os
server = 'http://music.163.com/'
target = 'http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset=35'
names = []
names1 = []
urls = []
urls1 = []
nums = 0
nums1 = 0
headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
           'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           'Accept-Encoding':'gzip,deflate',
           'Host':'music.163.com',
           'Referer':'http://nmusic.163.com',
           'Origin':'http: // music.163.com'}
req = requests.get(url=target,headers=headers)
req.encoding = 'utf-8'
html = req.text
div_bf = BeautifulSoup(html,"lxml")
div = div_bf.find('ul', class_="m-cvrlst f-cb",id="m-pl-container")
a_bf = BeautifulSoup(str(div),"lxml")
b = a_bf.find_all('p',class_="dec")
b_bf = BeautifulSoup(str(b), "lxml")
a = b_bf.find_all('a')
nums = len(a)
for each in a:
   names.append(each.string)
   urls.append(server + each.get('href'))
print(names)
print("启动：")
for i in range(nums):
     print("开始扫描:%s歌单" % names[i])
     m = str(names[i])
     n = str(urls[i])
     os.chdir('f:/python代码/网易云音乐/')
     f = open('歌单.txt', 'a',encoding='utf-8')
     f.write(m)
     f.write('\n')
     f.write(n)
     f.write('\n')
     f.close()
     req1 = requests.get(url=urls[i],headers=headers)
     req1.encoding = 'utf-8'
     html1 = req1.text
     bf1 = BeautifulSoup(html1, "lxml")
     mus1 = bf1.find('ul', class_='f-hide')
     a1 = mus1.find_all('a')
     nums1 = len(a1)
     for each in a1:
         names1.append(each.string)
     for each in a1:
         urls1.append(server + each.get('href'))
     print("一共有%d首歌" % nums1)
     os.chdir('f:/python代码/网易云音乐/')
     f = open('歌单.txt', 'a', encoding='utf-8')
     f.write(str(nums1)+'首歌')
     f.write('\n')
     f.close()
     for i in range(nums1):
         print("添加：%s" %names1[i])
         m1 = str(names1[i])
         n1 = str(urls1[i])
         os.chdir('f:/python代码/网易云音乐/')
         f = open('歌单.txt', 'a',encoding='utf-8')
         f.write(m1)
         f.write('\n')
         f.write(n1)
         f.write('\n')
         f.close()
     names1 = []
     urls1 = []
     os.chdir('f:/python代码/网易云音乐/')
     f = open('歌单.txt', 'a', encoding='utf-8')
     f.write('\n\n')
     f.close()
print("扫描结束！")