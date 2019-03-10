# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    b_cate = scrapy.Field()
    s_cate = scrapy.Field()
    book_name = scrapy.Field()
    book_img_url = scrapy.Field()
    book_price = scrapy.Field()
    book_comments_num = scrapy.Field()
    book_author = scrapy.Field()
    book_publisher = scrapy.Field()
    book_publish_date = scrapy.Field()
    s_cate_url = scrapy.Field()
    book_sku = scrapy.Field()
