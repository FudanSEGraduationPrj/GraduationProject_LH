import scrapy
from ..items import JavaDescriptionItem


class DocsSpider(scrapy.Spider):
    # scrapy crawl docs -o docs.json
    name = "docs"

    # start urls
    start_urls = ["https://docs.oracle.com/javase/8/docs/api/"]

    # parse
    def parse(self, response):
        # get the all classes frame url
        all_classes_frame_url = response.xpath("/html/frameset/frameset/frame[position()=2]/@src").get()
        if all_classes_frame_url:
            all_classes_frame_url = response.urljoin(all_classes_frame_url)
            yield scrapy.Request(all_classes_frame_url, callback=self.parse_class_url)

    # parse all classes' url
    def parse_class_url(self, response):
        for class_url in response.xpath("/html/body/div//a/@href"):
            class_url = response.urljoin(class_url.get())
            yield scrapy.Request(class_url, callback=self.parse_explanation)

    # extract explanation from class html
    def parse_explanation(self, response):
        # use the string() method of xpath to extract all the description of this class
        keyword = response.xpath("string(/html/body/div[4]/div[1]/ul/li/pre/span)")
        description = response.xpath("string(/html/body/div[4]/div[1]/ul/li/div)")
        if keyword.get() and description.get():
            item = JavaDescriptionItem()
            item['keyword'] = keyword.get()
            item['description'] = description.get()
            yield item
