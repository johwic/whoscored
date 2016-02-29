# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.exceptions import CloseSpider
from whoscored.items import Player
import json


class SquadSpider(Spider):
    name = "squad"
    team_id = None
    stage_id = None
    allowed_domains = ["whoscored.com"]

    def __init__(self, team_id=None, stage_id=None, *args, **kwargs):
        super(SquadSpider, self).__init__(*args, **kwargs)
        self.team_id = team_id
        self.stage_id = stage_id

    def start_requests(self):
        if self.team_id is not None:
            yield Request(url="https://www.whoscored.com/Teams/" + self.team_id)
        elif self.stage_id is not None:
            raise CloseSpider("Stage id not supported")
        else:
            raise CloseSpider("Not enough args")

    def parse(self, response):
        model_last_mode = response.xpath('//script[contains(., "Model-Last-Mode")]/text()').re_first(
            r"'Model-Last-Mode': '(.*?)' }")

        request = Request(
            url="https://www.whoscored.com/StatisticsFeed/1/GetPlayerStatistics?category=summary&subcategory=all&statsAccumulationType=0&isCurrent=true&playerId=&teamIds=" + self.team_id + "&matchId=&stageId=&tournamentOptions=&sortBy=Rating&sortAscending=&age=&ageComparisonType=&appearances=&appearancesComparisonType=&field=Overall&nationality=&positionOptions=&timeOfTheGameEnd=&timeOfTheGameStart=&isMinApp=false&page=&includeZeroValues=true&numberOfPlayersToPick=",
            headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com',
                     'Model-Last-Mode': model_last_mode},
            callback=self.parse_player
        )

        return request

    def parse_player(self, response):
        stats = json.loads(response.body)
        player_ids = []
        players = []
        for data in stats['playerTableStats']:
            player = Player()
            player['id'] = data['playerId']
            player['first_name'] = data['firstName']
            player['last_name'] = data['lastName']
            player['known_name'] = data['name']
            player['age'] = data['age']
            if data['isActive']:
                team = self.team_id
            else:
                team = None
            player['current_team'] = team
            if player['id'] not in player_ids:
                player_ids.append(player['id'])
                players.append(player)

        return players
