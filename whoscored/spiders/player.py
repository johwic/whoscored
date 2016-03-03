# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import Spider
from whoscored.items import Player
from whoscored.utils import Url
import json


class PlayerSpider(Spider):
    name = "player"
    player_id = None
    allowed_domains = ["whoscored.com"]

    def __init__(self, player_id, *args, **kwargs):
        super(PlayerSpider, self).__init__(*args, **kwargs)
        self.player_id = player_id

    def start_requests(self):
        yield Request(url="https://www.whoscored.com/Players/" + str(self.player_id))

    def parse(self, response):
        data = response.xpath('//script[contains(., "var currentTeamId")]/text()') \
            .re_first(r"var currentTeamId = (\d*?);")
        try:
            team_id = int(data)
        except ValueError:
            self.logger.warning("Team id not found: ")
            team_id = None

        dls = response.xpath('//div[@id="player-profile"]//dl')
        name = dls.xpath('dt[contains(., "Name:")]/following-sibling::dd/text()').extract_first()
        full_name = dls.xpath('dt[contains(., "Full Name:")]/following-sibling::dd/text()').extract_first()

        data = dls.xpath('dt[contains(., "Age:")]/following-sibling::dd/text()').re_first(r'(\d+).*')
        try:
            age = int(data)
        except ValueError:
            self.logger.warning("Age not found")
            age = 0

        model_last_mode = response.xpath('//script[contains(., "Model-Last-Mode")]/text()').re_first(
            r"'Model-Last-Mode': '(.*?)' }")

        request = Request(
            url=Url.get('player-statistics', {
                'category': 'summary', 'subcategory': 'all', 'statsAccumulationType': '0', 'isCurrent': 'true',
                'playerId': self.player_id, 'teamIds': '', 'matchId': '', 'stageId': '', 'tournamentOptions': '',
                'sortBy': 'Rating', 'sortAscending': '', 'age': '', 'ageComparisonType': '', 'appearances': '',
                'appearancesComparisonType': '', 'field': 'Overall', 'nationality': '', 'positionOptions': '',
                'timeOfTheGameEnd': '', 'timeOfTheGameStart': '', 'isMinApp': 'false', 'page': '',
                'includeZeroValues': 'true', 'numberOfPlayersToPick': ''}),
            headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com',
                     'Model-Last-Mode': model_last_mode},
            callback=self.parse_player
        )

        request.meta['team_id'] = team_id
        request.meta['name'] = name
        request.meta['full_name'] = full_name
        request.meta['age'] = age

        return request

    def parse_player(self, response):
        stats = json.loads(response.body)
        try:
            data = stats['playerTableStats'][0]
        except (KeyError, IndexError):
            return self.error_player(response)
        else:
            player = Player()
            player['id'] = self.player_id
            player['first_name'] = data['firstName']
            player['last_name'] = data['lastName']
            player['known_name'] = data['name']
            player['age'] = data['age']
            player['current_team'] = response.meta['team_id']

        return player

    def error_player(self, response):
        player = Player()
        player['id'] = self.player_id
        player['first_name'] = None
        player['last_name'] = None
        player['known_name'] = response.meta['name']
        player['age'] = response.meta['age']
        player['current_team'] = response.meta['team_id']

        return player
