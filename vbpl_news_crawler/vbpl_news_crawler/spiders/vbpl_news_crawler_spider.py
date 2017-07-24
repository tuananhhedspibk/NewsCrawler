# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.item import Item, Field
import scrapy
import html2text
import time
import datetime
from bs4 import BeautifulSoup
#<a  class="toanvan" href="/tw/pages/vbpq-timkiem.aspx?type=0&amp;s=1&amp;Keyword=70/2017/NĐ-CP&amp;SearchIn=Title,Title1&amp;IsRec=1">70/2017/NĐ-CP</a>
#<a target="_blank" class="toanvan" href="/tw/pages/vbpq-timkiem.aspx?type=0&amp;s=1&amp;Keyword=20/2015/NĐ-CP ngày&amp;SearchIn=Title,Title1&amp;IsRec=1">20/2015/NĐ-CP&nbsp;ngày</a>
#<a href="/articles/so_ki_hieu/20/2015/N%C4%90-CP%C2%A0ng%C3%A0y">20/2015/N%C4%90-CP%C2%A0ng%C3%A0y</a>
def replace_href_link(context):
    context = context.replace(" target=\"_blank\"",'')
    soup = BeautifulSoup(context,"html.parser")
    for link in soup.findAll('a'):
        try:
            href = str(link.get('href'))
            tmp1 = href.split("Keyword=")[1]
            tmp2 = tmp1.split("&")[0]
            # tmp = tmp2.split(' '.decode("utf8"))
            tmp = tmp2.split("%C2%A0")
            tmp3 = tmp[0]
            tmp4 = "<a href="+"/articles/so_ki_hieu/"+tmp3+">"+str(tmp3).decode('utf8')+"</a>"
            if len(tmp)==2:
                tmp4 = tmp4 + " "+tmp[1] + " "
            context = context.replace(str(link),str(tmp4).encode('utf-8'))
        except IndexError:
            pass
    return context.encode("ascii","ignore")

from vbpl_news_crawler.items import VbplNewsCrawlerItem
class NewsSpider(Spider):
    name = "vbpl_news"
    allowed_domains = ['vbpl.vn', 'www.vbpl.vn','http://vbpl.vn']
    start_urls = [
        "http://vbpl.vn/noidung/news/Lists/ThongBao/View_Detail.aspx",
    ]
    def parse_document(self,response):
    	meta = response.meta
    	item = VbplNewsCrawlerItem()
    	item['doc_id'] = str(meta['doc_id']).encode('utf-8')
    	item['doc_title'] = meta['doc_title'].encode('utf-8').strip()
    	item['doc_url'] ="http://vbpl.vn/" + str(meta['doc_url']).encode('utf-8')
    	item['doc_date'] = str(meta['doc_date']).encode('utf-8')
    	item['doc_description'] = meta['doc_description'].encode('utf-8').strip()

    	news_content = response.xpath('//div[@class="box-news box-news-home "]//div[@class="content"]')
    	
    	news_content_html = news_content.extract()[0]
    	news_other_html = news_content.xpath('//div[@class="news-other"]').extract()[0]

    	# config_html = html2text.HTML2Text()
    	# config_html.ignore_links = True

    	# news_other = config_html.handle(news_other_html)
    	# news_content = config_html.handle(news_content_html)
    	# news_content = news_content.replace(news_other,'')
    	# news_content = news_content.replace('*','')
        news_content = str(news_content_html.encode('utf-8')).replace(str(news_other_html.encode('utf-8')),'')
        item['doc_content'] = replace_href_link(news_content).strip()
        item['updated_at'] = str(datetime.datetime.now())
        item['created_at'] = str(datetime.datetime.now())

    	yield item


    def parse(self,response):
    	news_items = Selector(response).xpath('//div[@class="news-item"]')
    	for news_item in news_items:
            meta = {}
            meta['doc_title'] = news_item.xpath('p[@class="title"]/a/text()').extract()[0]
            meta['doc_url'] = news_item.xpath('p[@class="title"]/a/@href').extract()[0]
            meta['doc_id'] = str(meta['doc_url']).split('=')[1]
            meta['doc_date'] = news_item.xpath('p[@class="title"]/span/text()').extract()[0]
            meta['doc_description'] = news_item.xpath('div[@class="description"]/text()').extract()[0]
            url = "http://vbpl.vn/" + str(meta['doc_url'])
            yield scrapy.Request(url,callback = self.parse_document,meta = meta)