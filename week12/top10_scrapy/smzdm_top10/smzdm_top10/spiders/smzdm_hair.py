import scrapy
from scrapy.selector import Selector

from smzdm_top10.items import SmzdmTop10Item


class SmzdmHairSpider(scrapy.Spider):
    name = 'smzdm_hair'
    allowed_domains = ['smzdm.com']
    start_urls = ['https://www.smzdm.com/fenlei/xifahufa/h5c4s0f0t0p1/#feed-main/']

    def start_requests(self):
        """
        Override the start_requests method of the spider
        class to make the request carry cookies
        """
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse)

    def parse(self, response):
        # Movie details can be obtained directly on the first
        # page, here is just to verify the jump function
        shampoos = Selector(response=response).xpath('//*[@id="feed-main-list"]/li')
        for number, shampoo_info in enumerate(shampoos[:10]):
            item = SmzdmTop10Item()

            # Record ranking
            item['shampoo_rank'] = number + 1
            item['shampoo_name'] = \
                shampoo_info.xpath('./div/div[2]/h5/a/text()').extract_first().strip().replace('\'', '')
            good = \
                shampoo_info.xpath('./div/div[2]/div[4]/div[1]/span/a[1]/span[1]/span/text()').extract_first()
            bad = \
                shampoo_info.xpath('./div/div[2]/div[4]/div[1]/span/a[2]/span[1]/span/text()').extract_first()
            good = good if good else '0'
            bad = bad if bad else '0'
            item['shampoo_evaluate'] = int(good) - int(bad)
            item['shampoo_comments'] = []

            link = shampoo_info.xpath('./div/div[2]/h5/a/@href').extract_first().strip()

            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        Parse the shampoo details page
        """
        item = response.meta['item']
        shampoo_comments = Selector(response=response).xpath('//*[@id="commentTabBlockNew"]/ul/li')

        for comment_info in shampoo_comments:
            try:
                comment = comment_info.xpath('./div[2]/div[2]/div[1]/p/span/text()').extract_first().strip()

                item['shampoo_comments'].append(comment)
            except AttributeError:
                continue
        yield item

