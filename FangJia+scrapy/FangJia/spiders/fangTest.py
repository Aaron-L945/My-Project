# -*- coding: utf-8 -*-
import scrapy

from FangJia.items import FangjiaItem


class FangtestSpider(scrapy.Spider):
    name = 'fangTest'
    allowed_domains = ['cd.fang.lianjia.com']
    # start_urls = ['http://cd.fang.lianjia.com/']
    # start_urls = ['http://cd.fang.lianjia.com/loupan/p_hdwjhfaazop/']
    start_urls = []

    def start_requests(self):
        urlhead = 'http://cd.fang.lianjia.com/loupan/'
        for i in range(1,11):
            url = urlhead+'pg%s'% i
            self.start_urls.append(url)
        for url in self.start_urls:
            print(url)
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        fang_links = response.xpath(
            '//ul[@class="resblock-list-wrapper"]/li[@class="resblock-list"]/a/@href').extract()
        if fang_links:
            for link in fang_links:
                url = 'http://cd.fang.lianjia.com' + link
                yield scrapy.Request(url, callback=self.parse_fangjia)
        else:
            print('Not crawled')

    def parse_fangjia(self, response):
        name = response.xpath(
            '//div[@class="name-box"]/a/@title').extract()[0]
        try:
            price = response.xpath(
                '//p[@class="jiage"]/span[@class="junjia"]/text()').extract()[0]
        except IndexError:
            price = 'Null'
        try:
            yuan = response.xpath(
            '//p[@class="jiage"]/span[@class="yuan"]/text()').extract()[0]
        except IndexError:
            yuan = 'yuan'
        address = response.xpath(
            '//div[@class="bottom-info"]/p[3]/span/@title').extract()[0]
        update_time = response.xpath(
            '//div[@class="bottom-info"]/p[4]/span[2]/text()').extract()[0]
        url = response.xpath(
            '//div[@class="name-box"]/a/@href').extract()[0]
        item = FangjiaItem()
        item['name'] = name
        item['price'] = price+yuan
        item['address'] = address
        item['url'] = 'http://cd.fang.lianjia.com'+url
        item['update_time'] = update_time
        return item
