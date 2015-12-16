# -*- coding: utf-8 -*-
from scrapy import Item, Field


class Region(Item):
    id = Field()
    name = Field()
    flag = Field()
    type = Field()
    

class Tournament(Item):
    id = Field()
    name = Field()
    region = Field()
    

class Team(Item):
    id = Field()
    name = Field()
    
    
class Player(Item):
    id = Field()
    first_name = Field()
    last_name = Field()
    known_name = Field()
    age = Field()
    current_team = Field()


class Fixture(Item):
    id = Field()
    home_team = Field()
    away_team = Field()
    date = Field()
    stage = Field()
