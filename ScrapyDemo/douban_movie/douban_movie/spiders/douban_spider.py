import scrapy
from douban_movie.douban_movie.items import DoubanMovieItem
from scrapy.http import Request
from fake_useragent import UserAgent


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    # 设置自定义请求头
    headers = {
        'User-Agent': UserAgent(browsers=['chrome']).random
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = DoubanMovieItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')

        for movie in movies:
            item['ranking'] = movie.xpath('.//div[@class="pic"]/em/text()').extract()[0]
            item['name'] = movie.xpath('.//div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            item['comment_num'] = movie.xpath('.//div[@class="star"]/span[4]/text()').extract()[0]
            item['quote'] = movie.xpath('.//p[@class="quote"]/span/text()').extract()[0] \
                if movie.xpath('.//p[@class="quote"]/span/text()') else ''
            item['detail_url'] = movie.xpath('.//div[@class="hd"]/a/@href').extract()[0]
            item['cover_url'] = movie.xpath('.//div[@class="pic"]/a/img/@src').extract()[0]
            yield item

    # 处理下一页
    def parse_next(self, response):
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(url=next_url, headers=self.headers, callback=self.parse)
