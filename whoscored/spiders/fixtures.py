# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import Spider
from whoscored.items import Fixture
import re
import json


class FixtureSpider(Spider):

    name = "fixtures"
    arg_list = None
    base_url = "http://www.whoscored.com/Regions/{}/Tournaments/{}/Seasons/{}/Stages/{}"
    allowed_domains = ["whoscored.com"]

    def __init__(self, arg_list, *args, **kwargs):
        super(FixtureSpider, self).__init__(*args, **kwargs)
        self.arg_list = arg_list.split(',')

    def start_requests(self):
        yield Request(url=self.base_url.format(self.arg_list[0], self.arg_list[1], self.arg_list[2], self.arg_list[3]))

    def parse(self, response):
        data = response.xpath('//script[contains(., "Model-Last-Mode")]/text()').re_first(r"'Model-Last-Mode': '(.*?)' }")
        model_last_mode = data

        request = Request(
            url="http://www.whoscored.com/tournamentsfeed/{}/Fixtures?d={}&isAggregate=false".format(self.arg_list[3], self.arg_list[4]),
            headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com', 'Model-Last-Mode': model_last_mode},
            callback=self.parse_fixtures
        )

        return request

    def parse_fixtures(self, response):
        data = response.body
        if data:
            data = re.sub(r',,', r',null,', data)
            data = re.sub(r',,', r',null,', data)
            data = re.sub(r'"', r'\"', data)
            data = re.sub(r"\\'", r"'", data)
            data = re.sub(r',]', r',null]', data)
            data = re.sub(r"'(.*?)'(\s*[,\]])", r'"\1"\2', data)
            fixtures = json.loads(data);
        else:
            return

        for record in fixtures:
            ret = Fixture()
            ret['stage'] = self.arg_list[3]
            ret['id'] = record[0];
            ret['status'] = record[1];
            ret['start_date'] = record[2];
            ret['start_time'] = record[3];
            ret['home_team_id'] = record[4];
            ret['home_team_name'] = record[5];
            ret['home_red_cards'] = record[6];
            ret['away_team_id'] = record[7];
            ret['away_team_name'] = record[8];
            ret['away_red_cards'] = record[9];
            ret['score'] = record[10];
            ret['ht_score'] = record[11];
            ret['has_incidents'] = record[12];
            ret['has_preview'] = record[13];
            ret['elapsed'] = record[14];
            ret['result'] = record[15];
            ret['is_international'] = record[16];
            ret['is_opta'] = record[19] or record[17];

            yield ret

        return

