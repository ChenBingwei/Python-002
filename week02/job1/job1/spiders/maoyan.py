import scrapy
from scrapy.selector import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from job1.items import Job1Item


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    def start_requests(self):
        """
        Override the start_requests method of the spider
        class to make the request carry cookies
        """
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 cookies=self.settings.get('COOKIES'),
                                 callback=self.parse,
                                 errback=self.parse_err)

    def parse(self, response):
        # Movie details can be obtained directly on the first
        # page, here is just to verify the jump function
        movies = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        for number, movie_info in enumerate(movies[:10]):
            item = Job1Item()

            # Record ranking
            item['movie_rank'] = number + 1
            item['movie_name'] = movie_info.xpath('./div[1]/span[1]/text()').extract_first()
            item['movie_type'] = movie_info.xpath('./div[2]/text()').extract()[1].strip()
            item['movie_time'] = movie_info.xpath('./div[4]/text()').extract()[1].strip()
            yield item

    def parse_err(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
