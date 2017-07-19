# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy.orm import scoped_session,sessionmaker
from models import News, db_connect,create_news_table


class VbplNewsCrawlerPipeline(object):
	def __init__(self):
		engine = db_connect()
		create_news_table(engine)
		self.Session = scoped_session(sessionmaker(bind=engine))

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