# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VbplNewsCrawlerItem(scrapy.Item):
    doc_title = scrapy.Field()
    doc_url = scrapy.Field()
    doc_id = scrapy.Field()
    doc_description = scrapy.Field()
    doc_content = scrapy.Field()
    doc_date = scrapy.Field()
    

