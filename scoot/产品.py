import requests
from lxml import etree
import re
import json

'''
"arrAirport": "JHB",从JHB起飞
"arrTime": "201812111605", 起飞时间
"cabin": "1~E~~E00H01~AAB1~~2311~",仓位信息为E仓
"carrier": "AK",航班型号为AK
"depAirport": "KUL",落地城市为KUL
"depTime": "201812111505",落地时间
"flightNumber": "AK6044",航班编号
'''


class FlyscootSpider(object):
    def __init__(self, arrAirport, depAirport, arrDate):
        self.start_url = 'https://makeabooking.flyscoot.com/Book/AvailabilityAjax?AvailabilityAjax.LowFareMarketDate=0|{date}&AvailabilityAjax.Market={arr}|{dep}'
        self.arr = arrAirport
        self.dep = depAirport
        self.date = arrDate
        self.headers = {
            # 需要设计cookie池
            'cookie': 'viewedOuibounceModal=true; hpu=/zh; loc=CN; _gcl_au=1.1.397183629.1539771074; country=CN; DG_IID=F715DA45-7692-39C1-BE92-2266DFFC637C; DG_UID=DEE901B6-4416-3C3E-B516-4B236FBBA343; DG_SID=222.171.151.227:mWzq9Yv1rAHItt8OcKjVONlNnxVKrx38q8NXGftnX7A; _ga=GA1.2.753997000.1539771084; _gid=GA1.2.1195610699.1539771084; rxVisitor=1539775831316GOKEH1DLN1H45JHG2QG4MQN4SHGL4J93; CS_FPC=CSCuoGgmitcSUVPDCDugXSxoewiImkWVnK5; jumpseat_uid=yuPfavsaEu4iztLgiL4iJ8; _ga=GA1.3.753997000.1539771084; _gid=GA1.3.1195610699.1539771084; DG_ZID=2D6BB047-8474-3A26-A028-D631138788FB; DG_ZUID=9B657BF1-A3F4-3AFA-AFEB-044F8F715C74; DG_HID=CA360D1E-BE4D-3BBF-A970-116A4F687154; cookieconsent_status=dismiss; ASP.NET_SessionId=il1la5eogajtfygwdp5gype3; dotrez=3608208394.20480.0000; Hm_lvt_c2b8e393697aacf76c5b1874762308ea=1539842395,1539861458,1539861629,1539861670; Hm_lpvt_c2b8e393697aacf76c5b1874762308ea=1539862919; acw_tc=db9352a015398634971773488e337904efdf64d6afe15c6607de5dd93c; dtPC=3$263499884_962h1vNAFJILGMHOJBNPPHMAGIOMCIOKDJKTTG; dtSa=true%7CC%7C-1%7CScoot%7C-%7C1539862729048%7C261688082_561%7Chttps%3A%2F%2Fmakeabooking.flyscoot.com%2FBook%2FFlight%7C%E9%81%B8%E6%93%87%E8%88%AA%E7%8F%AD%7C1539861865522%7C; dtLatC=1; dtCookie=3$D5600E7B7CB6AFB458098D7C9F2D9BC0|RUM+Default+Application|1; rxvt=1539865307502|1539861605375; startTime=MjAxOC0xMC0xOCAxOTo1MjoxMQ==; AMP_TOKEN=%24ERROR; _gat_UA-26211105-1=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        self.info = []
        self.year = arrDate.split('/')[2]
        self.month = arrDate.split('/')[0]
        self.day = arrDate.split('/')[1]
        self.month_flag = {
            'Jan': '1',
            'Feb': '2',
            'Mar': '3',
            'Apr': '4',
            'May': '5',
            'Jun': '6',
            'Jul': '7',
            'Aug': '8',
            'Sep': '9',
            'Oct': '10',
            'Nov': '11',
            'Dec': '12'
        }

    def getHtml(self):
        # response = requests.get(self.start_url.format(date=self.date, arr=self.arr, dep=self.dep), headers=self.headers)
        # with open('flyscoot2.html', 'wb') as f:
        #     f.write(response.content)
        # if response.status_code == 200:
        #     return response.text
        # else:
        #     return None

        with open('flyscoot2.html', 'rb') as f:
            html = f.read()
        return html

    def parseHtml(self, html):
        selector = etree.HTML(html)
        dates = selector.xpath('//div[@class="flight-results__result"]')
        print(len(dates), type(dates))
        i = 0
        for data in dates:
            dct = dict()
            # 起飞城市
            dct["arrAirport"] = data.xpath('//div[@class="flight-results__result"]/@data-deptstation')[i]
            # 起飞时间
            arr_time = re.match('.* (.*):(.*)',
                                data.xpath('//div[@class="flight__from"]//li[@class="flight-time"]/text()')[i])
            time_minute = arr_time.group(1)
            time_second = arr_time.group(2)
            dct["arrTime"] = ''.join([self.year, self.month, self.day, time_minute, time_second])
            # 仓位信息
            dct["cabin"] = data.xpath('//*[@id="revAvailabilitySelect_MarketKeys_0_"]/@value')[i].split('|')[0]
            # 航班型号为AK
            dct["carrier"] = re.match('.*?: (.*?) ',
                                      data.xpath('//div[@class="flight__stop"]//div[@class="time"]/@data-content')[
                                          i]).group(1)
            # 落地城市为KUL
            dct["depAirport"] = data.xpath('//div[@class="flight-results__result"]/@data-arrstation')[i]
            # 落地时间
            # Nov 02, 2018 10:05
            dep_time = re.match('(.*?) (.*), (.*) (.*):(.*)',
                                data.xpath('//div[@class="flight-results__result"]/@data-time')[i])
            time_year = dep_time.group(3)
            time_month = self.month_flag[dep_time.group(1)]
            time_day = dep_time.group(2)
            time_minute = dep_time.group(4)
            time_second = dep_time.group(5)
            dct["depTime"] = ''.join([time_year, time_month, time_day, time_minute, time_second])
            # 航班编号
            dct["flightNumber"] = re.match('.*?: (.*?) \\(',
                                           data.xpath('//div[@class="flight__stop"]//div[@class="time"]/@data-content')[
                                               i]).group(1).replace(' ', '')
            self.info.append(dct)
            i += 1
        print(self.info)

    def ListToJson(self):
        json_ = json.dumps(self.info)
        with open('scoot.json', 'w') as f:
            f.write(json_)


# //*[@id="revAvailabilitySelect_MarketKeys_0_"]
if __name__ == '__main__':
    spider1 = FlyscootSpider('KUL', 'HKG', '11/30/2018')
    html = spider1.getHtml()
    spider1.parseHtml(html)
    spider1.ListToJson()
