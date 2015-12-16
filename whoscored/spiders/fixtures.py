# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import Spider
from whoscored.items import Fixture
import json


class FixtureSpider(Spider):

    name = "fixtures"
    stage_id = None
    allowed_domains = ["whoscored.com"]

    def __init__(self, player_id, *args, **kwargs):
        super(PlayerSpider, self).__init__(*args, **kwargs)
        self.player_id = player_id

    def start_requests(self):
        yield Request(url="http://www.whoscored.com/Regions/%d/Tournaments/%d/Seasons/%d/Stages/&d")

    def parse(self, response):
        data = response.xpath('//script[contains(., "Model-Last-Mode")]/text()').re_first(r"'Model-Last-Mode': '(.*?)' }")
        try:
            model_last_mode = data
        except ValueError:
            self.logger.warning("Model-Last-Mode not found: ")
            model_last_mode = None

        request = Request(
            url="http://www.whoscored.com/",
            headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com', 'Model-Last-Mode': model_last_mode},
            callback=self.parse_fixtures
        )

        return request

    def parse_fixtures(self, response):
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

