# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class FangjiaPipeline(object):
    def __init__(self):
        self.filename = open('fangjia.csv','wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False)+'\r\n'
        self.filename.write(line.encode('gbk'))
        return item

    def spider_close(self,spider):
        self.filename.close()