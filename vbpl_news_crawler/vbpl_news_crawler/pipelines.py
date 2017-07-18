# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import sessionmaker
from models import News, db_connect


class VbplNewsCrawlerPipeline(object):
	def __init__(self):
		engine = db_connect()
		self.Session = sessionmaker(bind=engine)

	def process_item(self,item,spider):
		session = self.Session
		new = News(**item)
		try:
			session.add(new)
			session.commit()
		except:
			session.rollback()
			raise
		finally:
			session.close()
		return item
		# try:
		# 	self.cursor.execute("""INSERT INTO news (doc_title,doc_url,doc_id,doc_description,doc_content,doc_date) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')""".format(item['doc_title'],item['doc_url'],item['doc_id'],item['doc_description'],item['doc_content'],item['doc_date']))
		# 	self.conn.commit()
		# except 
		# return item