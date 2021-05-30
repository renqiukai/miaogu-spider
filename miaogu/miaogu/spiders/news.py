import scrapy
from loguru import logger


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['miaogu.com']

    start_urls = ['http://www.miaogu.com/html/xinwenzixun/list_1_1.html']

    def parse(self, response):
        rows = response.xpath("//div[@class='newsList-wrap']/ul/li/h4/a")
        for row in rows:
            title = row.xpath("./text()").extract_first()
            url = row.xpath("./@href").extract_first()

            item = {
                "title": title,
                "url": url,
            }
            logger.debug(item)
            yield item
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url:
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={"item": item}
            )
