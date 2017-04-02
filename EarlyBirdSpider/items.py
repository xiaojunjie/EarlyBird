# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item

class MojiItem(Item):
    create_time = Field()
    id = Field()
    # _id = Field()
    city_id = Field()
    location = Field()
    path = Field()
    city_name = Field()
    face = Field()
    latitude = Field()
    longitude= Field()
    message= Field()
    nick= Field()
    province_name= Field()
    weather= Field()
    webp_path= Field()
