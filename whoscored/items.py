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
    stage = Field()
    status = Field()
    start_date = Field()
    start_time = Field()
    home_team_id = Field()
    home_team_name = Field()
    home_red_cards = Field()
    away_team_id = Field()
    away_team_name = Field()
    away_red_cards = Field()
    score = Field()
    ht_score = Field()
    has_incidents = Field()
    has_preview = Field()
    elapsed = Field()
    result = Field()
    is_international = Field()
    is_opta = Field()


class MatchData(Item):
    id = Field()
    match_data = Field()
    match_header = Fixture()
