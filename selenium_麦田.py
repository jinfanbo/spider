import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pymongo

client = pymongo.MongoClient()
db = client['maitian1']

chromeOptions = webdriver.ChromeOptions()
# 设置代理
chromeOptions.add_argument("--proxy-server=http://221.7.255.168:8080")
browser = webdriver.Chrome(chrome_options=chromeOptions)
wait = WebDriverWait(browser, 10)
browser.set_window_size(1400, 900)

browser.get('http://bj.maitian.cn/esfall/PG1')

def get_products():
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'body > section.esf_list.clearfix > div.list_right')
        )
    )
    html = browser.page_source
    doc = BeautifulSoup(html, 'lxml')
    rooms = doc.select('.list_title')
    for room in rooms:
        room_dict = {}
        room_dict['title'] = room.select_one('h1 a').get_text()
        room_dict['url'] = 'http://bj.maitian.cn' + room.select_one('h1 a').get('href')
        room_dict['info'] = room.select_one('p').get_text().replace('\r', '').replace('\n', '').replace(' ', '').replace('\xa0', '')
        room_dict['price'] = room.select_one('.the_price').get_text().replace('\n', '')
        room_dict['others'] = room.select_one('.morel.clearfix').get_text().replace('\n', '')
        print(room_dict)
        save_to_mongo(room_dict)

def next_page():
    print('正在翻页')
    try:
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '''a[onclick="ga('send', 'event', 'fanye', 'dangqianyema', 'xiayiye');"]''')
            )
        )
        submit.click()
        get_products()
    except TimeoutException:
        next_page()

def save_to_mongo(result):
    try:
        if db['room'].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONGODB失败', result)

def main():
    get_products()
    try:
        while EC.element_to_be_clickable((By.CSS_SELECTOR, "onclick=ga('send', 'event', 'fanye', 'dangqianyema', 'xiayiye');")):
            next_page()
            time.sleep(5)
    except Exception:
        print('出错啦')
    finally:
        browser.close()
        client.close()

if __name__ == '__main__':
    main()