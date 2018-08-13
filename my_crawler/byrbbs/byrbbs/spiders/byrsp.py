# -*- coding: utf-8 -*-
import scrapy
import re
re_nickname = r'发信人：(.*?)，信区'
re_time = r'\((.*?)\)'
from byrbbs.items import ByrbbsItem
from scrapy.http import Request
class ByrspSpider(scrapy.Spider):
    name = 'byrsp'
    allowed_domains = ['byr.cn']
    start_urls = ['http://bbs.byr.cn']
    loginurl="https://bbs.byr.cn/user/ajax_login.json"
    with open('log.txt','w') as f:
        f.write('started.\n')
    ldata = {"id": "yibanxianshi", "passwd": "********"}
    head = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        #'Cookie': '_ga=GA1.2.804287751.1497985719; login-user=yibanxianshi; nforum[UTMPUSERID]=yibanxianshi; nforum[PASSWORD]=TnE%2BUx3AMY%2B5W8W54qYVjQ%3D%3D; Hm_lvt_38b0e830a659ea9a05888b924f641842=1523947464,1524653875,1525404679; nforum[XWJOKE]=hoho; Hm_lpvt_38b0e830a659ea9a05888b924f641842=1525680984; nforum[UTMPKEY]=9313846; nforum[UTMPNUM]=4402',
        'Host': 'bbs.byr.cn',
        'Referer': 'https://bbs.byr.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
        }
    
    
    def parse(self, response):
        pass


    def start_requests(self):
        with open('log.txt','a') as f:
            f.write('to login.\n')
        yield scrapy.http.FormRequest(
            self.loginurl,
            formdata = self.ldata,
            headers = self.head,
            callback = self.login_after
            )

    def login_after(self,response):
        with open('log.txt','a') as f:
            f.write('original page got.\n')
        yield Request(
            self.start_urls[0]+'/default',
            headers = self.head,
            callback = self.parse_body
            )
    def parse_body(self,response):
        with open('log.txt','a') as f:
            f.write('body parsed.\n')
        hot_pas = response.xpath('//div/ul[@id="column2"]/li/div[@class="widget-content"]/ul[@class="w-list-line"]/li')
        if not hot_pas:
            with open('log.txt','a') as f:
                f.write('empty\n')
                f.write(response.text)
        for passage in hot_pas:
            try:
                url = passage.xpath('.//a/@href').extract()[0]
                with open('log.txt','a') as f:
                    f.write('new request generated:{0}\n'.format(url))
                yield Request(
                    '{0}{1}'.format(self.start_urls[0],url),
                    headers = self.head,
                    callback = self.parse_passage
                    )
            except IndexError:
                with open('log.txt','a') as f:
                    f.write('fail to transfer a new passage request\n')
            with open('log.txt','a') as f:
                f.write('new passage to parse\n')

    def parse_passage(self,response):
        item = ByrbbsItem()
        item['title'] = response.xpath('//body/div[@class="b-head corner"]/span/span[@id="a_share"]/@_c').extract()[0]
        replies = response.xpath('//body/div[@class="b-content corner"]/div/table')
        for rep in replies:
            item['nickname'] = ''
            try:
                item['number'] = rep.xpath('.//tr[@class="a-head"]/td/span[@class="a-pos"]/text()').extract()[0]
                item['author'] = rep.xpath('.//tr/td/span[@class="a-u-name"]/a/text()').extract()[0]
                if item['number'] == '楼主':
                    item['like'] = rep.xpath('.//tr/td/ul[@class="a-func"]/li/a[@class="a-func-support"]/text()').extract()[0]
                    item['dislike'] = rep.xpath('.//tr/td/ul[@class="a-func"]/li/a[@class="a-func-oppose"]/text()').extract()[0]
                else:
                    item['like'] = rep.xpath('.//tr/td/ul/li/a[@class="a-func-like"]/text()').extract()[0]
                    item['dislike'] = rep.xpath('.//tr/td/ul/li/a[@class="a-func-cai"]/text()').extract()

                pack =  rep.xpath('.//tr[@class="a-body"]/td/div[@class="a-content-wrap"]/text()').extract()
                item['time'] = re.search(re_time , pack[2]).group(1)
                item['content'] = ''.join(pack[3:-1])
                item['nickname'] = re.search(re_nickname , pack[0]).group(1)
            except IndexError:
                pass
            except AttributeError:
                pass
            finally:
                yield item
        with open('log.txt','a') as f:
            f.write('a passage is finished.\n')
        
                
if __name__ == '__main__':
    example = ByrspSpider()
    for i in example.start_requests():
        i
    
