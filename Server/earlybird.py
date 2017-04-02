import pymongo
from bson.json_util import dumps
import time,datetime

evening_time = time.mktime( datetime.date.today().timetuple() )
page_length = 100
client = pymongo.MongoClient("mongodb://admin@localhost")
db = client["EarlyBird"]
PictureList = list(db["Picture"].find({"create_time":{"$gt":evening_time},"latitude":{"$gt":0},"longitude":{"$gt":0}}))
PictureList = sorted(PictureList,key=lambda x:x["create_time"])
print dumps(PictureList[:page_length])
