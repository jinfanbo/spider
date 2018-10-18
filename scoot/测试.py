import requests
import random
from lxml import etree
import re
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
    def __init__(self, arrAirport, depAirport, departDate):
        self.start_url = 'https://makeabooking.flyscoot.com'
        self.data = {
            "revAvailabilitySearch.SearchInfo.Direction": "Oneway",
            "revAvailabilitySearch.SearchInfo.SearchStations[0].DepartureStationCode": arrAirport,
            "revAvailabilitySearch.SearchInfo.SearchStations[0].ArrivalStationCode": depAirport,
            "revAvailabilitySearch.SearchInfo.SearchStations[0].DepartureDate": departDate,
            "revAvailabilitySearch.SearchInfo.AdultCount": "1",
            "revAvailabilitySearch.SearchInfo.ChildrenCount": "0",
            "revAvailabilitySearch.SearchInfo.InfantCount": "0"
        }
        self.headers = {
            #需要设计cookie池
            'cookie': 'viewedOuibounceModal=true; hpu=/zh; loc=CN; _gcl_au=1.1.397183629.1539771074; country=CN; DG_IID=F715DA45-7692-39C1-BE92-2266DFFC637C; DG_UID=DEE901B6-4416-3C3E-B516-4B236FBBA343; DG_ZID=2D6BB047-8474-3A26-A028-D631138788FB; DG_ZUID=9B657BF1-A3F4-3AFA-AFEB-044F8F715C74; DG_HID=CA360D1E-BE4D-3BBF-A970-116A4F687154; DG_SID=222.171.151.227:mWzq9Yv1rAHItt8OcKjVONlNnxVKrx38q8NXGftnX7A; _ga=GA1.2.753997000.1539771084; _gid=GA1.2.1195610699.1539771084; rxVisitor=1539775831316GOKEH1DLN1H45JHG2QG4MQN4SHGL4J93; CS_FPC=CSCuoGgmitcSUVPDCDugXSxoewiImkWVnK5; jumpseat_uid=yuPfavsaEu4iztLgiL4iJ8; _ga=GA1.3.753997000.1539771084; _gid=GA1.3.1195610699.1539771084; Hm_lvt_c2b8e393697aacf76c5b1874762308ea=1539771077,1539775708,1539777546,1539831968; acw_tc=db939a4715398319831916782e26a2eb11ba2d2c3555ef6aacab2af8ad; ASP.NET_SessionId=4zrqvwpfn5uivhlpznibayvb; dotrez=3608208394.20480.0000; Hm_lpvt_c2b8e393697aacf76c5b1874762308ea=1539832079; startTime=MjAxOC0xMC0xOCAxMToxNDoyNw==; _gat_UA-26211105-1=1; dtPC=5$232906411_532h-vFAJILAAKOUCPMEECSIABXTBOKANABOUO; dtLatC=1; rxvt=1539834745984|1539831988741; dtCookie=5$45B133136D5D5511C030FC99A9D527DE|RUM+Default+Application|1; dtSa=true%7CC%7C-1%7C%E6%9F%A5%E6%89%BE%E8%88%AA%E7%8F%AD%EF%BC%81%7C-%7C1539832974210%7C232906411_532%7Chttps%3A%2F%2Fmakeabooking.flyscoot.com%2F%7CSearch%7C1539832945988%7C',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }

    def getHtml(self):
        r = requests.Session()
        r.headers = self.headers
        r.post("https://makeabooking.flyscoot.com/", data=self.data)
        s = r.get("https://makeabooking.flyscoot.com/Book/Flight")
        with open('flyscoot1.html', 'wb') as f:
            f.write(s.content)
        if s.status_code == 200:
            return s.text
        else:
            return None

    def getHtml_test(self):
        with open('flyscoot.html', 'rb') as f:
            html = f.read()
        return html

    def parseHtml(self, html):
        selector = etree.HTML(html)
        arr = selector.xpath('//*[@id="departure-results"]/div').extant  # 出发机票
        print(arr)



if __name__ == '__main__':
    # arrAirport = input('请输入出发地：')
    # depAirport = input('请输入目的地：')
    # departDate = input('请输入出发时间(格式为：月/日/年 例：00/00/0000)：')
    # returnDate = input('请输入返回时间(格式为：月/日/年 例：00/00/0000)：')
    arrAirport, depAirport, departDate = ['SHE', 'SIN', '10/31/2018']
    spider1 = FlyscootSpider(arrAirport, depAirport, departDate)
    # html = spider1.getHtml()
    # spider1.parseHtml(html)
    html = spider1.getHtml_test()
    spider1.parseHtml(html)
