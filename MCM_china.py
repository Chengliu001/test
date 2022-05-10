import json
import random
import re
import db
from bs4 import BeautifulSoup
import requests
from lxml import etree
import logging
import time
import datetime
import logging
import sys
import pandas

sys.setrecursionlimit(10000)
logger = logging.getLogger('mcm_china')


class MCM():
    num = 0
    df = pandas.DataFrame()
    times = int(round(time.time() * 1000))
    women = 'https://cn.mcmworldwide.com/zh_CN/%E5%A5%B3%E5%A3%AB/%E5%8C%85%E8%A2%8B/%E6%89%80%E6%9C%89%E5%8C%85%E8' \
            '%A2%8B? '
    man = 'https://cn.mcmworldwide.com/zh_CN/%E7%94%B7%E5%A3%AB/%E5%8C%85%E8%A2%8B/%E6%89%80%E6%9C%89%E5%8C%85%E8%A2' \
          '%8B? '
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/97.0.4692.71 Safari/537.36',
        'cookie': 'SECKEY_ABVK=77SdlOJ7yLqsmCeb6KLKPo1QwZ2MUp1I1IBtwIzmq6s%3D; '
                  'BMAP_SECKEY=o0lunQvWFMa8rLq4OvuFwLuKOlrKxRY4RRZbtjjWsvP2BZ5LKp1lE_atXayvnjX6gJrsdPcheTKBaDi65'
                  '-tZ34Mx4zkTADHTWGBx3dPClJ1zQvgZiEns_SseAbQIK9Rj0CFU8IEkEqOZ6Z1WxCAS1Wzxjl5T87xIDi1pOFrW3lpx7xuWikMVJsztf0VODkmV; SECKEY_ABVK=77SdlOJ7yLqsmCeb6KLKPlImoJRlz3srxfgYXX4EQgQ%3D; BMAP_SECKEY=o0lunQvWFMa8rLq4OvuFwA4QE8s6-KQkhJEuYPY4qfIK8TXkde9rsb6HUV6z0Yegi1HYa5BnaLCkScM7Brich43LAKZbaybi1ZgymwC8hUE1YS9LNnJXZyvKAXWk3Gy6wLFEFOGQcXC4l5e-RasVPUmGfFAR0PQmwces9Q6mkShRy7JhWZgrqUnTDtwP_ybK; dwanonymous_3fc7a99b2adc73da6dc143d2546c1cf5=abHKqN0FLHyoRKmhLQPAaEyyOY; _gcl_au=1.1.1331392698.1642409139; OptanonAlertBoxClosed=2022-01-17T08:46:30.825Z; __cq_uuid=abHKqN0FLHyoRKmhLQPAaEyyOY; _gid=GA1.2.2006436142.1642409420; _ga=GA1.2.1008142555.1642409420; _ga=GA1.3.1008142555.1642409420; _gid=GA1.3.2006436142.1642409420; a1ashgd=fbu63gist5000000fbu63gist5000000; _ga_tng=GA1.3.1741daf2-165e-493c-94c4-3cdbc3742866; _ga_tng_gid=GA1.3.1181629308.1642470037; tangiblee:widget:user=1741daf2-165e-493c-94c4-3cdbc3742866; dwac_d75963d753a4e1665f124eeb8d=OaU4uFmhyGaeeziyRFm7EETQ8pl5O2glIhw%3D|dw-only|||CNY|false|Asia%2FShanghai|true; cqcid=abHKqN0FLHyoRKmhLQPAaEyyOY; cquid=||; sid=OaU4uFmhyGaeeziyRFm7EETQ8pl5O2glIhw; __cq_dnt=0; dw_dnt=0; dwsid=nZeAqMJq6VttFrUg1BwL2-DiSoni8EkY0XFhwlsiocYF2bvym80OlKtl3VwE2qvcftV6-BLsfAD4UqPbgQRRXQ==; dw=1; dw_cookies_accepted=1; newsletter-signup=true; tangiblee_user_flow=0-18012022; Hm_lvt_a843b864b439f5340589816107bbe100=1642469977,1642470275,1642470358,1642470549; Hm_lvt_2eaae98ec5aef0cc2c22e919196f93ca=1642469977,1642470275,1642470358,1642470549; __cq_bc=%7B%22aazr-MCM-CN%22%3A%5B%7B%22id%22%3A%229270%22%2C%22sku%22%3A%22MWRBAWO05CO001%22%7D%2C%7B%22id%22%3A%229120%22%2C%22sku%22%3A%22MWSCSXT03CO001%22%7D%2C%7B%22id%22%3A%228861%22%2C%22sku%22%3A%22MWTCSBO01WT001%22%7D%2C%7B%22id%22%3A%229268%22%2C%22sku%22%3A%22MWRBAWO03Y4001%22%7D%2C%7B%22id%22%3A%229286%22%2C%22sku%22%3A%22MWTBSNN04Y4001%22%7D%5D%7D; __cq_seg=0~0.21!1~0.33!2~0.47!3~0.22!4~0.38!5~-0.03!6~0.13!7~-0.32!8~0.36!9~0.43; Hm_lpvt_a843b864b439f5340589816107bbe100=1642473667; Hm_lpvt_2eaae98ec5aef0cc2c22e919196f93ca=1642473667; _dc_gtm_UA-90477107-1=1; _dc_gtm_UA-83810126-1=1; _gat_UA-83810126-1=1; _gat_UA-90477107-1=1; visited=24; __atuvc=28%7C3; __atuvs=61e61a8c42ae513a01a; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jan+18+2022+10%3A41%3A07+GMT%2B0800+(%E4%B8%AD%E5%9C%8B%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.28.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false; inside-asia2=67490725-8ca8ca3bac6ad44ee803ea38d89d7f745d543344c66bb27f55c0aa6c1d879506-0-0 '
    }

    list = [
        {
            'url': women,
            'uri': '/zh_CN/女士/包袋/所有包袋',
            'url_short': '/zh_CN/%E5%A5%B3%E5%A3%AB/%E5%8C%85%E8%A2%8B/%E6%89%80%E6%9C%89%E5%8C%85%E8%A2%8B'
        },
        {
            'url': man,
            'uri': 'zh_CN/男士/包袋/所有包袋',
            'url_short': '/zh_CN/%E7%94%B7%E5%A3%AB/%E5%8C%85%E8%A2%8B/%E6%89%80%E6%9C%89%E5%8C%85%E8%A2%8B'
        }
    ]

    def __init__(self, ):
        self.sql = db.Sql()
        self.sql.sql()

    def get_id(self,sku, item):
        for name in item:
            if sku == name:
                return False
        return True

    def get_htm(self, htm):
        return htm.replace('\n', '').replace('\r', '').replace('\t', '')

    def get_list(self):
        for param in self.list:
            page = 0
            session = requests.Session()
            while True:
                print(page)
                start = page * 40
                logger.info('正在爬取%s:%d' % (param['uri'], page))
                params = {'start': start, 'sz': 40, 'format': 'page-element', 'source': 'showmore'}
                resp = session.get(url=param['url'], headers=self.headers, params=params)
                html = etree.HTML(resp.text)
                soup = BeautifulSoup(resp.text, features="lxml")
                info_url = html.xpath('//*[@class="grid-cell"]/a[1]/@href')
                if info_url:
                    j = 1
                    for i in info_url:
                        itemcode = re.findall("(.*)\&sz={0}.*", i)[0].format(start)
                        self.get_goods_info(itemcode)
                        time.sleep(random.randint(2, 3))
                        print(j)
                        j += 1
                else:
                    break
                page += 1
        self.df.to_excel('mcm_china.xlsx', index=False, engine='openpyxl')

    def get_goods_info(self, itemcode):
        url = 'https://cn.mcmworldwide.com%s' % itemcode
        session = requests.Session()
        resp = session.get(url, headers=self.headers)
        soup = BeautifulSoup(resp.text, features="lxml")
        html = etree.HTML(resp.text)
        htm = self.get_htm(resp.text)
        try:
            if html.xpath('//*[@class="low-stock-message "]/p/text()') == []:
                statu = '有货'
            else:
                statu = html.xpath('//*[@class="low-stock-message "]/p/text()')[0]
            statu = statu.replace('\n', '').replace(' ', '')
            ProductName = soup.find_all('h1', class_="product-name")[0].get_text()
            print(ProductName)
            Size = html.xpath('//*[@class="selected-size"]/text()')[0]  # 尺寸
            print(Size)
            Color = html.xpath('//*[@class="selected-color"]/text()')[0]  # 颜色
            ProductNote = html.xpath('//*[@class="product-long-description txt-lg-regular"]/text()')[0]  # 商品描述
            ProductNote = ProductNote.replace('\n', '').replace(' ', '')

            details = html.xpath('//*[@class="panel-body-wrapper"]/ul/li/text()')
            for i in range(len(details)):
                details[i] = details[i].replace('\n', '').replace(' ', '')
            ProductMarket = ';'.join(details).replace('"', '').replace("'", "").replace("‘", "").replace("“",
                                                                                                         "")  # 详情描述
            price = soup.find_all('span', class_="sales price-sales")[0].get_text()
            price = price.replace('\n', '').replace(' ', '')
            PriceTag = price[0]
            Price = price[1:]
            piclist = soup.find('div', class_="image-groups-wrapper")
            piclist2 = piclist.find_all('img')
            l = int(len(piclist2) / 2)
            piclist3 = piclist2[0:l]
            piclist4 = [0 for x in range(0, len(piclist3))]
            for i in range(len(piclist3)):
                p = piclist3[i].attrs
                piclist4[i] = p["src"]
            main_pic = piclist4[0]
            id = re.findall(".*/mcmworldwide/(.*)_.*", main_pic)[0]
            other_pic = piclist4[1:]
            other_pic2 = ';'.join(other_pic)
            print(id)
            data1 = {
                '一级平台': 'MCM官网',
                '国家': '中国大陆',
                '官网ID': id,
                '货币符号': PriceTag,
                '专柜价': Price,
                '爬取时间': datetime.datetime.now(),
                '更新后价格': '',
                '更新时间': '',
                '下架时间': '',
                '库存状态': statu,
                '下架状态': '',
                '商品名称': ProductName,
                '品牌名': 'MCM',
                '品类': '箱包',
                '颜色': Color,
                '材质': '',
                '尺寸': Size,
                '长': '',
                '高': '',
                '宽': '',
                '简介': ProductNote,
                '详情': ProductMarket,
                '主图': main_pic,
                '副图': other_pic2,
                '官网链接': url,
            }
            sql_excute= ('''insert into mcm_china(platform_name,country,id,monetary,money,crawling_time,
            inventory_status, package_name,brand,type2,color,description,content,main_picture,
            auxiliary_picture,package_url, measurement)
            values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''
                             .format
                             ('MCM官网', '中国大陆', id, PriceTag, Price, datetime.datetime.now(), statu, ProductName, 'MCM',
                              '箱包', Color,
                              ProductNote, ProductMarket, main_pic, other_pic2, url, Size))

            if self.num == 0:
                self.df = self.df.append(data1, ignore_index=True)
                # self.sql.execute(sql_excute)
            elif self.get_id(id, self.df['官网ID']):
                self.df = self.df.append(data1, ignore_index=True)
                # self.sql.execute(sql_excute)
            else:
                self.num -= 1
                print('---------------------------%s重复--------------------------------' % id)
            self.num += 1
        except Exception as e:
            print(e)
            print(url)


def main():
    try:
        logging.basicConfig(
            level='INFO',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='MCM_china_log.txt'
        )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logger.addHandler(console)
        dem = MCM()
        dem.get_list()
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
