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
        try:
            model_last_mode = data
        except ValueError:
            self.logger.warning("Model-Last-Mode not found: ")
            model_last_mode = None

        request = Request(
            url="http://www.whoscored.com/tournamentsfeed/{}/Fixtures?={}&isAggregate=false",
            headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com', 'Model-Last-Mode': model_last_mode},
            callback=self.parse_fixtures
        )

        return request

    def parse_fixtures(self, response):
        list = response.xpath('//script[contains(., "DataStore.prime(\'stagefixtures\'")]/text()').extract()

        if len(list) == 0:
            self.logger.warning("No matchStats found.")
            return

        data = re.search(r"calendar\.parameter\(\)\), ([\w\W]*?)\);", list[0])

        if data:
            data = re.sub(r',,', r',null,', data.group(1))
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
            ret['Id'] = record[0];
            ret['Status'] = record[1];
            ret['StartDate'] = record[2];
            ret['StartTime'] = record[3];
            ret['HomeTeamId'] = record[4];
            ret['HomeTeamName'] = record[5];
            ret['HomeRCards'] = record[6];
            ret['AwayTeamId'] = record[7];
            ret['AwayTeamName'] = record[8];
            ret['AwayRCards'] = record[9];
            ret['Score'] = record[10];
            ret['HTScore'] = record[11];
            ret['HasIncidents'] = record[12];
            ret['HasPreview'] = record[13];
            ret['Elapsed'] = record[14];
            ret['Result'] = record[15];
            ret['IsInternational'] = record[16];
            ret['IsOpta'] = record[19] or record[17];

            yield ret

        return

