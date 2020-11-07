# -*- coding: utf-8 -*-
import scrapy,requests,re,random,base64,time
from fontTools.ttLib import TTFont
from ..items import *

class SameCitySpider(scrapy.Spider):
    name = 'same_city'
    allowed_domains = ['zz.58.com']
    start_urls = ['https://zz.58.com/pinpaigongyu/pn/{0}/']
    def __init__(self):
        UA = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        ]

        self.headers = {
            "User-Agent": random.choice(UA)
        }
    def start_requests(self):
        for i in range(1,3):
            url = self.start_urls[0].format(i)
            yield scrapy.Request(url=url,callback=self.parse,headers=self.headers)

    def resp(self):
        UA = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        ]

        headers = {
            "User-Agent": random.choice(UA)
        }
        base_url = "https://zz.58.com/pinpaigongyu/pn/2/"
        response = requests.get(base_url, headers=headers)
        print("正在下载:", response.url)
        return response

    def get_base64_str(self,response):
        base_font = re.compile("base64,(.*?)\'")
        base64_str = re.search(base_font, response.text).group().split(',')[1].split('\'')[0]
        return base64_str
    def make_font_file(self,base64_str):
        b = base64.b64decode(base64_str)
        with open("58.ttf", "wb") as f:
            f.write(b)

    def make_dict(self):
        font = TTFont('58.ttf')
        b = font['cmap'].tables[2].ttFont.getReverseGlyphMap()  # 编码对应的数字
        c = font['cmap'].tables[2].ttFont.tables['cmap'].tables[1].cmap  # 页面的十六进制数对应的编码
        return b, c

    def parse(self, response):
        # response = self.resp()
        base64_str = self.get_base64_str(response)
        self.make_font_file(base64_str)
        self.make_dict()
        print(response.url)
        titles = response.xpath('//div[@class="des strongbox"]/h2/text()').extract()
        prices = response.xpath('//div[@class="money"]/span[@class="strongbox"]/b/text()').extract()
        rooms = response.xpath('//p[@class="room"]/text()').extract()
        dists = response.xpath('//p[@class="dist"]/text()').extract()
        specs = response.xpath('//p[@class="spec"]/span/text()').extract()

        title_list = []
        price_list = []
        room_list = []
        dist_list = []
        spec_list = []
        for title in titles:
            s = ''
            title_re = re.compile('\s')
            title = re.sub(title_re, '', title)
            for i in title:
                encode_str = str(i.encode("unicode-escape")).split(r'\\u')[-1].replace('\'', '').replace(r'b(', '').strip()
                num, code = self.make_dict()
                if len(encode_str) != 4:
                    i = i
                elif int(encode_str, 16) not in code:
                    i = i
                else:
                    i = str(num[code[int(encode_str, 16)]] - 1)
                s += i
            print('123')
            # print(s)
            title_list.append(s)
        for price in prices:
            s = ''
            title_re = re.compile('\s')
            title = re.sub(title_re, '', price)
            for i in title:
                encode_str = str(i.encode("unicode-escape")).split(r'\\u')[-1].replace('\'', '').replace(r'b(',
                                                                                                         '').strip()
                num, code = self.make_dict()
                if len(encode_str) != 4:
                    i = i
                elif int(encode_str, 16) not in code:
                    i = i
                else:
                    i = str(num[code[int(encode_str, 16)]] - 1)
                s += i
            print('123')
            # print(s)
            price_list.append(s)
        for room in rooms:
            s = ''
            title_re = re.compile('\s')
            title = re.sub(title_re, '', room)
            for i in title:
                encode_str = str(i.encode("unicode-escape")).split(r'\\u')[-1].replace('\'', '').replace(r'b(',
                                                                                                         '').strip()
                num, code = self.make_dict()
                if len(encode_str) != 4:
                    i = i
                elif int(encode_str, 16) not in code:
                    i = i
                else:
                    i = str(num[code[int(encode_str, 16)]] - 1)
                s += i
            print('123')
            # print(s)
            room_list.append(s)
        for dist in dists:
            s = ''
            title_re = re.compile('\s')
            title = re.sub(title_re, '', dist)
            for i in title:
                encode_str = str(i.encode("unicode-escape")).split(r'\\u')[-1].replace('\'', '').replace(r'b(',
                                                                                                         '').strip()
                num, code = self.make_dict()
                if len(encode_str) != 4:
                    i = i
                elif int(encode_str, 16) not in code:
                    i = i
                else:
                    i = str(num[code[int(encode_str, 16)]] - 1)
                s += i
            dist_list.append(s)
        for i in range(len(dist_list)):
            if i % 2 == 0:
                del dist_list[0]
            else:
                dist_list.append(dist_list[0])
                del dist_list[0]
        for spec in specs:
            s = ''
            title_re = re.compile('\s')
            title = re.sub(title_re, '', spec)
            for i in title:
                encode_str = str(i.encode("unicode-escape")).split(r'\\u')[-1].replace('\'', '').replace(r'b(',
                                                                                                         '').strip()
                num, code = self.make_dict()
                if len(encode_str) != 4:
                    i = i
                elif int(encode_str, 16) not in code:
                    i = i
                else:
                    i = str(num[code[int(encode_str, 16)]] - 1)
                s += i
            spec_list.append(s)
        house = House_infor()
        nums = min(len(title_list),len(price_list),len(room_list),len(dist_list))
        for i in range(nums):
            house['title'] = title_list[i]
            house['price'] = price_list[i]
            house['room'] = room_list[i]
            house['dist'] = dist_list[i]
            # house[title] = title_list[i]
            yield house
            print(house)


        # print(title_list)
        # print(price_list)
        # print(room_list)
        # print(dist_list)
        # print(spec_list)
        # print(len(title_list),len(price_list),len(room_list),len(dist_list),len(spec_list))
        # time.sleep(10)





