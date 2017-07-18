from sqlalchemy import *
from sqlalchemy.engine.url import URL 

import settings

DeclarativeBase = declarative_base()

def db_connect():
	return create_engine(URL(**setting.DATABASE))

class News(DeclarativeBase):
	__tablename__ = "news"
	doc_title = Column('doc_title',String)
	doc_url = Column('doc_url',String)
	doc_id = Column('doc_id',String)
	doc_description = Column('doc_description',String)
	doc_content = Column('doc_content',String)
	doc_date = Column('doc_date',String)