# encoding=utf-8

import pymongo
from items import *

class MongoDBPipleline(object):

    def __init__(self):
        client = pymongo.MongoClient("mongodb://admin@localhost")
        db = client["EarlyBird"]
        self.Picture = db["Picture"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, MojiItem):
            self.Picture.update_one({"id":item["id"]},{"$set":dict(item)},upsert=True)
        else:
            raise ValueError("MongoDBPipleline ERROR")
        return item
