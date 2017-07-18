# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2


class VbplNewsCrawlerPipeline(object):
	# def __init__(self):
	# 	self.conn = psycopg2.connect(database="testdb",user="linhtm",password="123",host="127.0.0.1",port="5432")
	# 	self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
    	# self.cursor.execute("""INSERT INTO news (doc_title,doc_url,doc_id,doc_description,doc_content,doc_date) VALUES (%s,%s,%d,%s,%s,%s)""" %
    	# 	item['doc_title'],item['doc_url'],item['doc_id'],item['doc_description'],item['doc_content'],item['doc_date'])
    	# self.conn.commit()
        return item
