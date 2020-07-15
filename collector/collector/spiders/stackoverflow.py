import scrapy
from ..items import StackOverflowAnswerItem


class StackOverflowSpider(scrapy.Spider):
    # scrapy crawl stackoverflow -o stackoverflow.json
    name = "stackoverflow"
    page_index = 1

    def start_requests(self):
        with open("spider.cfg", "r") as lines:
            for line in lines:
                if line.find("page_index") >= 0:
                    self.page_index = int(line[13:])
        url = "https://stackoverflow.com/questions/tagged/java?tab=newest&page=%d" % self.page_index
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )

    def parse(self, response):
        # select only question summary with more than 0 answers
        for question_summary in response.xpath('//*[@id="questions"]//div[@class="question-summary"]'):
            answer_num = int(question_summary.xpath('./div[1]/div[1]/div[2]/strong/text()').get())
            # if number of answers bigger than 0, crawl corresponding answers
            if answer_num > 0:
                answers_url = question_summary.xpath('./div[2]/h3/a/@href').get()
                answers_url = response.urljoin(answers_url)
                yield scrapy.Request(answers_url, callback=self.parse_answer)

        # the url of next page
        next_page_url = response.xpath('//a[@rel="next"]/@href').get()
        next_page_url = response.urljoin(next_page_url)
        self.page_index += 1
        with open("spider.cfg", "w") as out:
            out.write("page_index = %d" % self.page_index)
        yield scrapy.Request(next_page_url, callback=self.parse)

    # extract answer
    def parse_answer(self, response):
        for answer in response.xpath('string(//div[contains(@class, "answer")]//div[@class="post-text"]/p)'):
            item = StackOverflowAnswerItem()
            item["answer"] = answer.get()
            yield item
