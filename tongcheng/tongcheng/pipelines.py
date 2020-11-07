# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo

class TongchengPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient(settings['MONGO_HOST'], settings['MONGO_PORT'])
        db = clinet[settings['MONGO_DB']]
        self.col = db[settings['MONGO_COLNAME']]
    def process_item(self, item, spider):
        dic = dict(item)
        self.col.insert(dic)
        return item

