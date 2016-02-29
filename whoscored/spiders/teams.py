# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from whoscored.items import Team
from whoscored.utils import Utils
import json


class TeamsSpider(Spider):
    name = "teams"
    allowed_domains = ["whoscored.com"]
    start_urls = ['https://www.whoscored.com']

    def parse(self, response):
        regions = json.load(open('regions.json'))
        requests = []

        model_last_mode = response.xpath('//script[contains(., "Model-Last-Mode")]/text()').re_first(
            r"'Model-Last-Mode': '(.*?)' }")

        for region in regions:
            if region['type'] == 0 or region['name'] == 'International':
                item = 'https://www.whoscored.com/teamsfeed/' + str(region['id']) + '/region'
                requests.append(Request(url=item, headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com', 'Model-Last-Mode': model_last_mode}, callback=self.parse_teams))

        return requests

    def parse_teams(self, response):
        teams = Utils.parse_json(response.body)
        teams = json.loads(teams)

        for team in teams:
            item = Team()
            item['id'] = team[0]
            item['name'] = team[1].encode('utf8')
            yield item
