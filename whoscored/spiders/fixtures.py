# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import Spider
from whoscored.items import Fixture
from whoscored.utils import Utils, Url
import json


class FixtureSpider(Spider):
    name = "fixtures"
    allowed_domains = ["whoscored.com"]

    def __init__(self, region, tournament, season, stage, dates=None, is_aggregate='false', *args, **kwargs):
        super(FixtureSpider, self).__init__(*args, **kwargs)
        self.region = region
        self.tournament = tournament
        self.season = season
        self.stage = stage
        self.dates = dates
        self.is_aggregate = is_aggregate

    def start_requests(self):
        yield Request(url=Url.get('stage', {
            'r': self.region,
            't': self.tournament,
            's': self.season,
            'id': self.stage
        }))

    def parse(self, response):
        if self.dates is None:
            fixtures = response.xpath('//script[contains(., "DataStore.prime(\'stagefixtures\'")]/text()').re_first(
                r"\$\.extend\(.*?\), ([\w\W]*?)\);")
            if fixtures:
                return self.get_fixture(fixtures)
            return

        model_last_mode = response.xpath('//script[contains(., "Model-Last-Mode")]/text()').re_first(
            r"'Model-Last-Mode': '(.*?)' }")
        requests = []

        for d in self.dates.split(','):
            requests.append(Request(
                url=Url.get('stagefixtures', {'stageId': self.stage, 'd': d, 'isAggregate': self.is_aggregate}),
                headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com',
                     'Model-Last-Mode': model_last_mode},
                callback=self.parse_fixtures
            ))

        return requests

    def parse_fixtures(self, response):
        data = response.body
        if data:
            return self.get_fixture(data)
        return

    def get_fixture(self, raw):
        fixtures = json.loads(Utils.parse_json(raw))

        for record in fixtures:
            ret = Fixture()
            ret['stage'] = self.stage
            ret['id'] = record[0]
            ret['status'] = record[1]
            ret['start_date'] = record[2]
            ret['start_time'] = record[3]
            ret['home_team_id'] = record[4]
            ret['home_team_name'] = record[5]
            ret['home_red_cards'] = record[6]
            ret['away_team_id'] = record[7]
            ret['away_team_name'] = record[8]
            ret['away_red_cards'] = record[9]
            ret['score'] = record[10]
            ret['ht_score'] = record[11]
            ret['has_incidents'] = record[12]
            ret['has_preview'] = record[13]
            ret['elapsed'] = record[14]
            ret['result'] = record[15]
            ret['is_international'] = record[16]
            ret['is_opta'] = record[19] or record[17]

            yield ret
