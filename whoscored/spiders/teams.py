# -*- coding: utf-8 -*-
import scrapy
import re
import json
from whoscored.items import Team
from scrapy.http import Request


class TeamsSpider(scrapy.Spider):
    name = "teams"
    allowed_domains = ["whoscored.com"]

    def start_requests(self):
        regions = json.load(open('regions.json'))
        requests = []
        for region in regions:
            if region['type'] == 0 or region['name'] == 'International':
                item = 'http://www.whoscored.com/teamsfeed/' + str(region['id']) + '/region'
                requests.append(Request(url=item,
                                headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com',
                                         'Referer': 'http://www.whoscored.com'}))

        return requests

    def parse(self, response):
        teams = re.sub(r',,', r',null,', response.body)
        teams = re.sub(r',,', r',null,', teams)
        teams = re.sub(r'"', r'\"', teams)
        teams = re.sub(r"\\'", r"'", teams)
        teams = re.sub(r',]', r',null]', teams)
        teams = re.sub(r"'(.*?)'(\s*[,\]])", r'"\1"\2', teams)
        teams = json.loads(teams)

        for team in teams:
            item = Team()
            item['id'] = team[0]
            item['name'] = team[1].encode('utf8')
            yield item
