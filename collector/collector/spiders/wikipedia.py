import scrapy
from pymysql import *
from ..items import JavaDescriptionItem
import re


host = 'localhost'
port = 3306
user = 'root'
password = 'good2739966538'
database = 'api_explanation_extractor_db'
page_size = 10
vector_size = 100


class WikipediaSpider(scrapy.Spider):
    # scrapy crawl wikipedia
    name = "wikipedia"
    pattern = re.compile('^[\n]+$')

    def start_requests(self):
        page_no = 1
        count = page_size
        conn = connect(host=host, port=port, user=user, password=password, database=database)
        cursor = conn.cursor()
        while count >= page_size:
            count = cursor.execute('select url from url where id > %d limit %d' % ((page_no - 1) * page_size, page_size))
            urls = cursor.fetchall()
            for url in urls:
                yield scrapy.Request(
                    url=url[0],
                    callback=self.parse
                )
            page_no += 1
        conn.commit()
        conn.close()

    def parse(self, response):
        description = response.xpath("string(/html/body/div[3]/div[3]/div[4]/div/p[1])")
        if description.get() and self.pattern.match(description.get()):
            description = response.xpath("string(/html/body/div[3]/div[3]/div[4]/div/p[2])")
        if description.get():
            item = JavaDescriptionItem()
            item['keyword'] = response.xpath('string(//*[@id="firstHeading"])').get()
            item['description'] = description.get()
            yield item
