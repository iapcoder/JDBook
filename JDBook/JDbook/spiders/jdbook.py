# -*- coding: utf-8 -*-
import scrapy
from JDbook.items import JdbookItem
import urllib
from copy import deepcopy
import re


class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):

        b_list = response.xpath("//div[@class='mc']/dl/dt") # 大分类列表
        item = JdbookItem()

        for b in b_list:
            item["b_cate"] = b.xpath("./a/text()").extract_first()
            s_list = b.xpath("./following-sibling::dd[1]/em")  # 小分类列表

            for s in s_list:
                item['s_cate'] = s.xpath('./a/text()').extract_first()
                item['s_cate_url'] = s.xpath('./a/@href').extract_first()
                item['s_cate_url'] = urllib.parse.urljoin(response.url,item['s_cate_url'])


                yield scrapy.Request(
                    item['s_cate_url'],
                    callback=self.parse_cate,
                    meta={"item":deepcopy(item)}
                )

    # 处理每一个分类下的图书
    def parse_cate(self, response):

        item = response.meta['item']

        book_list = response.xpath('//div[@id="plist"]/ul/li')

        for book in book_list:
            item['book_img_url'] = book.xpath('.//div[@class="p-img"]/a/img/@src').extract_first()
            if item['book_img_url'] is None:
                item['book_img_url'] = book.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img').extract_first()
            item['book_img_url'] = urllib.parse.urljoin(response.url, item['book_img_url'])
            item["book_name"] = book.xpath('.//div[@class="p-name"]//em/text()').extract_first().strip()
            item['book_author'] = book.xpath('.//span[@class="author_type_1"]/a/text()').extract()
            item['book_publisher'] = book.xpath('.//span[@class="p-bi-store"]/a/text()').extract_first()
            item['book_publish_date'] = book.xpath('.//span[@class="p-bi-date"]/text()').extract_first().strip()

            # 获取价格信息
            item["book_sku"] = book.xpath("./div/@data-sku").extract_first()

            yield scrapy.Request(
                "https://p.3.cn/prices/mgets?skuIds=J_{}".format(item["book_sku"]),
                callback=self.parse_book_price,
                meta={"item":deepcopy(item)}
            )

        # 翻页
        next_page = response.xpath('.//a[@class="pn-next"]/@href').extract_first()
        if next_page is not None:
            next_page = urllib.parse.urljoin(response.url, next_page)

            scrapy.Request(
                next_page,
                callback=self.parse_cate,
                meta={"item":deepcopy(item)}
            )

    # 获取价格信息
    def parse_book_price(self, response):

        item = response.meta['item']
        item["book_price"] = re.findall('"op":"(.*?)",', response.body.decode())[0] if len(re.findall('"op":"(.*?)",', response.body.decode()))>0 else None
        del item['book_sku']
        print(item)
        yield item








