# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class JdbookPipeline(object):

    def open_spider(self, spider):
        self.f = open("./JDbook.txt", "a", encoding="utf-8")


    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):

        self.f.write(json.dumps(dict(item), ensure_ascii=False, indent=2))
        self.f.write("\n")

        return item
