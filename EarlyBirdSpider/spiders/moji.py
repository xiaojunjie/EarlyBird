# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from scrapy.http.headers import Headers
from EarlyBirdSpider.items import MojiItem
import time,datetime

def afterMorning(create_time):
    create_time  = create_time/1000
    evening_time = time.mktime( datetime.date.today().timetuple() )
    morning_time = evening_time+3600*4
    return create_time >= morning_time

class MojiSpider(scrapy.Spider):
    name = "EarlyBird"

    def start_requests(self):
        url = "http://ugc.moji001.com/sns/json/liveview/timeline/city"
        data = {
            "common": {
                "uid": "360383230",
                "platform": "Android",
                "language": "CN",
            },
            "params": {
                "is_webp": 1,
                # "city_id": 1,
                "page_length": 10,
                "page_past": 0,
                "is_wifi": 1
            }
        }
        for city_id in range(1, 3017):
            print city_id
            data["params"]["city_id"] = city_id
            yield Request(url=url, body=json.dumps(data).decode("utf8"), method='POST', headers=Headers({'Content-Type': 'application/json'}))

    def parse(self, response):
        """ 某个地点的图片信息 """
        CityData = json.loads(response.body)
        if not CityData or CityData.get("latest_picture_count", 0) == 0:
            pass
        elif afterMorning(CityData["picture_list"][0]["create_time"]):
            PictureList = CityData["picture_list"]
            data = json.loads(response.request.body)
            if afterMorning( PictureList[ len(PictureList)-1 ]["create_time"] ):
                data["params"]["page_length"] *= 5
                yield response.request.replace(body=json.dumps(data))
            else:
                mojiItem = MojiItem()
                p = [x for x in PictureList if afterMorning(x["create_time"])][-1]
                webp_cdn = "http://cdn.moji002.com/images/webp/simgs/"
                jpg_cdn = "http://cdn.moji002.com/images/sthumb/"
                cdn = webp_cdn if ".webp" in p["path"] else jpg_cdn
                mojiItem["id"] = p["id"]
                # mojiItem["city_id"] = data["params"]["city_id"]
                mojiItem["location"] = p["location"]
                mojiItem["create_time"] = p["create_time"]
                mojiItem["path"] = cdn+p["path"]
                yield mojiItem
                data["params"]["picture_id"] = p["id"]
                url = "http://ugc.moji001.com/sns/json/liveview/get_picture"
                yield Request(url,body=json.dumps(data).decode("utf8"), method='POST', headers=Headers({'Content-Type': 'application/json'}), callback=self.parse_picture)

    def parse_picture(self,response):
        """ 某个图片的详细信息 """
        PictureData = json.loads(response.body).get("picture")
        if not PictureData:
            pass
        else:
            webp_cdn = "http://cdn.moji002.com/images/webp/simgs/"
            mojiItem = MojiItem()
            mojiItem["id"] = PictureData["id"]
            mojiItem["city_id"] = PictureData["city_id"]
            mojiItem["city_name"] = PictureData["city_name"]
            mojiItem["face"] = PictureData["face"]
            mojiItem["latitude"] = PictureData.get("latitude")
            mojiItem["location"] = PictureData["location"]
            mojiItem["longitude"] = PictureData.get("longitude")
            mojiItem["message"] = PictureData.get("message")
            mojiItem["nick"] = PictureData["nick"]
            mojiItem["province_name"] = PictureData["province_name"]
            mojiItem["weather"] = PictureData.get("weather")
            mojiItem["webp_path"] = webp_cdn+PictureData.get("webp_path") if "webp_path" in PictureData else ""
            yield mojiItem
