import scrapy
from scrapy.selector import Selector

from job2 import constants
from job2.items import Job2Item


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
                                 cookies=constants.COOKIES,
                                 callback=self.parse)

    def parse(self, response):
        # Movie details can be obtained directly on the first
        # page, here is just to verify the jump function
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        numbers = 0
        for movie_info in movies:
            numbers += 1

            # Take only the top ten movies
            if numbers > 10:
                break

            item = Job2Item()

            # Record ranking
            item['movie_rank'] = numbers

            # Splicing movie details page address
            link = movie_info.xpath('./a/@href')
            whole_link = constants.MAOYAN_BASE_URL + link.extract()[0]

            yield scrapy.Request(url=whole_link, meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        Parse the movie details page
        """
        item = response.meta['item']
        movie_details = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        for detail_info in movie_details:
            item['movie_name'] = \
                detail_info.xpath('./h1/text()').extract_first().strip()

            # Only keep time format
            item['movie_time'] = \
                detail_info.xpath('./ul/li[3]/text()').extract_first().strip()[:10]
            movie_types = []
            for t in detail_info.xpath('./ul/li[1]/a/text()'):
                movie_types.append(str(t.extract()).strip())
            item['movie_type'] = '/'.join(movie_types)
            yield item
