# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # 电影排名
    ranking = scrapy.Field()
    # 电影名称
    name = scrapy.Field()
    # 电影评分
    score = scrapy.Field()
    # 评论人数
    comment_num = scrapy.Field()
    # 电影简介
    quote = scrapy.Field()
    # 电影详情页链接
    detail_url = scrapy.Field()
    # 电影封面图片链接
    cover_url = scrapy.Field()
