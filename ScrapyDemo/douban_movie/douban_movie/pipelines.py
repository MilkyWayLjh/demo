# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json
import pymongo


class DoubanMoviePipeline(object):
    def __init__(self):
        # 可选：保存到JSON文件
        self.file = open('douban_movie.json', 'w', encoding='utf-8')
        # 可选：连接MongoDB
        # self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # self.db = self.client['douban_movie']
        # self.collection = self.db['movie']

    def process_item(self, item, spider):
        # 检查必要字段是否存在
        if not all(item.get(field) for field in ['name', 'score', 'detail_url']):
            raise DropItem(f'Missing required fields in {item}')
        # 保存到JSON文件
        line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + '\n'
        self.file.write(line)
        # 保存到MongoDB
        # self.collection.insert_one(ItemAdapter(item).asdict())

        return item

    def close_spider(self, spider):
        # 关闭文件
        self.file.close()
        # 关闭MongoDB连接
        # self.client.close()

        print('Pipeline closed.')
        # print('Movie saved to MongoDB.')
        print('Movie saved to JSON file.')
        print('Spider closed.')
