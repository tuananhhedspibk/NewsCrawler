from scrapy import Spider
from scrapy.selector import Selector
from scrapy.item import Item, Field
import scrapy
import html2text

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

    	config_html = html2text.HTML2Text()
    	config_html.ignore_links = True

    	news_other = config_html.handle(news_other_html)
    	news_content = config_html.handle(news_content_html)
    	news_content = news_content.replace(news_other,'')
    	news_content = news_content.replace('*','')

    	item['doc_content'] = news_content.encode('utf-8').strip()
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