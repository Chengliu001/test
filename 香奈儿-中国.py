# -*- coding: utf-8 -*-
# @Time : 2021-12-22 17:31
# @Author : 郭强
# @File : 香奈儿官网爬虫.py
# @Software: PyCharm
import datetime
import getpass
import json
import requests
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import db
class Chanel():
    def __init__(self):
        self.urls=[]
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Origin': "https://www.chanel.com"
        }
        self.urls2=['https://www.chanel.com/zh_CN/fashion/products/handbags/classic-handbag.html',
                    'https://www.chanel.com/zh_CN/fashion/products/handbags/2-55-handbag.html',
                    'https://www.chanel.com/zh_CN/fashion/products/handbags/chanel-19.html',
                    'https://www.chanel.com/zh_CN/fashion/products/handbags/boy-chanel.html',
                    'https://www.chanel.com/zh_CN/fashion/products/handbags/chanel-gabrielle.html',
                    'https://www.chanel.com/zh_CN/fashion/products/handbags/new-this-season.html']
        self.baourls=[]
        self.baourls2=[]
    def url(self):
        baseurl='https://www.chanel.com/zh_CN/fashion/products/handbags.html'
        driver=webdriver.Chrome()
        driver.get(baseurl)
        driver.implicitly_wait(10)
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())
        ans=soup.find_all('a',class_='fs-button__link')
        # print(len(ans))
        for url2 in ans[:6]:
            detailurl='https://www.chanel.com{}'.format(url2.get('href'))
            # print(detailurl)
            self.urls.append(detailurl)


    def baourl(self):
        #进入口袋包
        try:
            for url in self.urls2[:5]:
                # url=self.urls2[0]
                print(url)
                # driver = webdriver.Chrome()
                # driver.get(url)
                # driver.implicitly_wait(10)
                # html = driver.page_source
                # driver.quit()
                res=requests.get(url=url,headers=self.headers)
                html=res.text
                soup=BeautifulSoup(html,'html.parser')
                ans=soup.find_all('a',class_='push__link')
                urls = []
                for i in ans:
                    try:
                        urls.append('https://www.chanel.com{}'.format(i.get('href')))
                        # print('https://www.chanel.com{}'.format(i.get('href')))
                    except:
                        pass
                #获取各种种包的链接
                urls=list(set(urls))
                print(len(urls))
                for n2,url3 in enumerate(urls):
                    # print(url3)
                    # self.baourls.append(url3)
                    # print(n2)
                    try:
                        # driver2=webdriver.Chrome()
                        # driver2.get(url3)
                        # driver2.implicitly_wait(10)
                        # html2 = driver2.page_source
                        # driver2.quit()
                        # print(url3)
                        res5 = requests.get(url=url3, headers=self.headers)
                        html2 = res5.text
                        html3 = BeautifulSoup(html2, 'html.parser')
                        # print(url3)
                        # print(html3.prettify())
                        lis = html3.find_all('a', class_='')
                        # print(lis)
                        # html6=res5.content.decode('utf-8')
                        # hrefs=etree.HTML(html6)
                        # url4s=hrefs.xpath('//*[@id="main-wrapper"]/section/div/div[1]/div[4]/div[1]/div[4]/div[2]/div/div/ul/div/div/li/a/text()')
                        # lis2=[]
                        # for i in lis:
                        #     if '-bag' in i.get('href'):
                        #         lis2.append(i)
                        #     else:
                        #         pass
                        for j in lis:
                            if j.get('data-id'):
                                try:
                                    # print(j.a.get('href'))
                                    self.baourls.append('https://www.chanel.com{}'.format(j.get('href')))
                                except:
                                    pass
                            else:
                                pass
                    except:
                        pass
            self.baourls=list(set(self.baourls))
            print(len(self.baourls),self.baourls)
            #包链接存数据库
            now2 = datetime.datetime.now()
            sql2 = db.Sql()
            sql2.sql()
            for url2 in self.baourls:
                sql2.execute("insert into chanel_urls(url,flag,flag2,sys_creat_time)VALUES"
                             "('{}','{}','{}','{}')".format(url2, 0,'China',now2))
        except Exception as e:
            print(e)
    def zaochunurl(self):
        url = self.urls2[5]
        # driver = webdriver.Chrome()
        # driver.get(url)
        # driver.implicitly_wait(10)
        # html = driver.page_source
        # driver.quit()
        res=requests.get(url=url,headers=self.headers)
        html=res.text
        soup = BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())
        ans = soup.find_all('div', class_='fs-products-grid__product__wrapper')
        # urls=[]
        for i in ans:
            a='https://www.chanel.com{}'.format(i.a.get('href'))
            print(a)
            # urls.append(a)
            self.baourls2.append(a)
        #存包链接进数据库
        now2=datetime.datetime.now()
        sql2 = db.Sql()
        sql2.sql()
        for url2 in self.baourls2:
            sql2.execute("insert into chanel_urls(url,flag,flag2,sys_creat_time)VALUES"
                         "('{}','{}','{}','{}')".format(url2, 0,'China',now2))
    def xiangqing(self):
        # 获取详细包的内容
        sql = db.Sql()
        sql.sql()
        res = sql.select(
            '''SELECT url FROM "chanel_urls" where flag = 0 and flag2 ='China' limit 1''')
        result = res[0]
        detailurl=result['url']
        print(detailurl)
        sql.execute(
            '''update chanel_urls set flag = 2 where url = '{}'and flag2 ='China' '''.format(detailurl))

        res2 = requests.get(url=detailurl, headers=self.headers)
        html4 = res2.content.decode('utf-8')
        html4=res2.text
        soup = BeautifulSoup(html4, 'html.parser')
        # print(soup.prettify())
        # 一级源
        yijiyuan = 'Chanel官网'
        # 二级源
        erjiyuan = '中国大陆'
        # 官网id
        try:
            guanwangid = soup.find('p', class_='fs-productsheet__ref font-family-basic').text.replace('参考:',
                                                                                                      '').strip()
            # print(guanwangid)
        except:
            guanwangid = ''
        # 货币单位和官网价格
        try:
            # price = soup.find('span', class_='fs-productsheet__price_value fs-price__value').text.strip().replace(
            #     "'", '')
            res = requests.get(url=detailurl, headers=self.headers)
            html9 = res.content.decode('utf-8')
            html9 = etree.HTML(html9)
            color_links = html9.xpath('//div[@class="fs-productsheet__materials-section_container"]/div/ul/li/a/@href')
            # print(color_links)
            output = []
            price=[]
            for uri in color_links[:1]:
                uri = "https://www.chanel.com" + uri if "http" not in detailurl else detailurl
                # print(url)

                resp = requests.get(uri, headers=self.headers)
                page = etree.HTML(resp.text)
                # print(page)

                p_list = uri.split('/')
                sku_list = p_list[p_list.index('p') + 1: p_list.index('p') + 4]
                sku = sku_list[1].upper()
                # logger.info(sku)
                p_url = "https://www.chanel.com/asset/frontstage/api/m/v1/prices/" \
                        + '?references=' + sku \
                        + '&locale=' + "zh_CN" \
                        + '&productLines={%22' + sku_list[0] + '%22:[%22' + sku + '%22]}'
                resp = requests.get(
                    p_url,
                    headers=self.headers | {
                        'dpr': '1.25',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'
                    },
                    # cookies=session.cookies
                )
                data = json.loads(resp.text)
                # print(str(data).replace("[",'').replace("]",''))
                data2 = str(data).replace("[", '').replace("]", '')
                data3 = json.loads(data2)
                price.append(data3['price']['formatted-amount'])
            # print(price)
            huobidanwei = '￥'
            guanwangjiage = str(price[0]).replace('￥', '')
        except:
            huobidanwei = '￥'
            guanwangjiage = ''
        # 爬取时间
        paqushijian = datetime.datetime.now()
        # 取商品名称
        try:
            shangpingmingcheng = soup.find('span', class_='fs-productsheet__title').text \
                .strip().replace("'", '')
        except:
            shangpingmingcheng = ''
        # 品牌
        pingpai = 'Chanel'
        # 颜色
        try:
            yanse = soup.find('span',
                              class_='fs-productsheet__desc fs-productsheet__color fs-productsheet__desc__label font-family-basic').text \
                .strip().replace("'", '')
            # print(yanse)
        except:
            yanse = ''
        # 材质
        try:
            caizhi = soup.find('span',
                               class_='fs-productsheet__desc fs-productsheet__material fs-productsheet__desc__label font-family-basic').text \
                .strip().replace("'", '')
            # print(caizhi)
        except:
            caizhi = ''
        # 尺寸
        try:
            chicun = soup.find('span', class_='fs-size__label').text \
                .strip().replace("'", '').replace('cm', '')
            chicun = chicun.split('×')
            try:
                gao = chicun[0]
            except:
                gao = ''
            try:
                chang = chicun[1]
            except:
                chang = ''
            try:
                kuan = chicun[2]
            except:
                kuan = ''
        except:
            chang = ''
            gao = ''
            kuan = ''
        # 图片链接
        # try:
        #     # zhutu = soup.find('picture', class_='fs-productsheet__pictures-img').img
        #     # zhutu = zhutu.get('src')
        #     zhutu = soup.find('meta', property="og:image").get('content')
        #     # print(zhutu.get('src'))
        #
        # except:
        #     zhutu = ''
        # 主图/其他图
        try:
            with open('香奈儿中国.txt', 'w', encoding='utf-8') as f:
                f.write(html4)

            with open('香奈儿中国.txt', 'r', encoding='utf-8') as f2:
                futuhtml = f2.read()

            soup2 = BeautifulSoup(futuhtml, 'html.parser')
            uls = soup2.find('ul', class_='fs-productsheet__zoom__content')
            lis = uls.find_all('li')
            picturerls = []
            for i in lis:
                imgs = i.find_all('img')
                picturerls.append(imgs[1].get('src'))

            zhutu=str(picturerls[0])
            futuurls = ':\n'.join(picturerls[1:])

        except:
            futuurls = ''
            zhutu=''
        # 官网链接
        guanwanglianjie = detailurl
        #品类
        pinlei='箱包'
        # print(zhutu)
        print(guanwangid, huobidanwei, guanwangjiage, paqushijian,
              shangpingmingcheng, pingpai, yanse, caizhi, chang, kuan, gao)
        if shangpingmingcheng !='':
            sql.execute("insert into chanel(yijiyuan,erjiyuan,guanwangid,huobidanwei,\
                        guanwangjiage,paqushijian,pinlei,shangpingmingcheng,pingpai,yanse,\
                        caizhi,chang,kuan,gao,guanwanglianjie,zhutu,qitatu)VALUES"
                        "('{}','{}','{}','{}','{}','{}','{}','{}',\
                        '{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(yijiyuan, erjiyuan, guanwangid, huobidanwei,
                                                               guanwangjiage, paqushijian,pinlei,
                                                               shangpingmingcheng,pingpai,yanse, caizhi, chang, kuan,
                                                               gao, guanwanglianjie,zhutu,futuurls))
            sql.execute(
                '''update chanel_urls set flag = 1 where url = '{}'and flag2 ='China' '''.format(detailurl))
        else:
            sql.execute(
                '''update chanel_urls set flag = 1 where url = '{}'and flag2 ='China' '''.format(detailurl))





if __name__ == '__main__':
    chanel=Chanel()
    #chanel.url()
    chanel.baourl()
    chanel.zaochunurl()
    try:
        while True:
            chanel.xiangqing()
    except:
        print('爬虫结束')
