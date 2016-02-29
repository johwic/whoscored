# -*- coding: utf-8 -*-
import re
import os
import json
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from whoscored.utils import Utils
from whoscored.items import Player


class MatchSpider(CrawlSpider):
    name = "match"
    match_id = None
    allowed_domains = ["whoscored.com"]
    rules = (
        Rule(LinkExtractor(allow=(r"https://www.whoscored.com/Matches/\d+/MatchReport/.*",)),
             callback="parse_match_stats"),
    )

    def __init__(self, match_id, *args, **kwargs):
        super(MatchSpider, self).__init__(*args, **kwargs)
        self.match_id = match_id

    def start_requests(self):
        yield Request(url="https://www.whoscored.com/Matches/" + str(self.match_id) + "/Live/")

    def parse_start_url(self, response):
        needle = "matchCentreData"
        is_array = False
        match_data = response.xpath('//script[contains(., "var ' + needle + '")]/text()').extract()
        if len(match_data) == 0:
            needle = "initialMatchDataForScrappers"
            is_array = True
            match_data = response.xpath('//script[contains(., "var ' + needle + '")]/text()').extract()
            if len(match_data) == 0:
                raise CloseSpider("Match data not found")

        data = re.search(needle + r" = ([\w\W]*?);", match_data[0])

        if data:
            data = data.group(1)

            if is_array:
                data = Utils.parse_json(data)

            path = "data/" + str(self.match_id) + "/"
            filename = path + needle + ".json"
            try:
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise

            with open(filename, 'wb') as f:
                f.write(data.encode('utf8'))

        else:
            raise CloseSpider("Match data not found")
        # response.xpath('//script[contains(., "var matchCentData")]/text()').re(r"var matchCentreData = ([\w\W]*?);")
        # if needle == "matchCentreData":
        #     return Request(self.base_url.format(self.match_id) + "MatchReport/", self.parse_match_stats)

        return

    def parse_match_stats(self, response):
        match_data = response.xpath('//script[contains(., "var matchStats")]/text()').re_first(
            r"matchStats = ([\w\W]*?);")

        if match_data:
            data = Utils.parse_json(match_data)

            path = "data/" + str(self.match_id) + "/"
            filename = path + "matchStats.json"
            try:
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise

            with open(filename, 'wb') as f:
                f.write(data.encode('utf8'))
        else:
            self.logger.warning("No matchStats found.")

        return
        # players = json.loads(data)
        # for side in players[0][2]:
        #     for player in side[4]:
        #         request = Request("http://www.whoscored.com/Players/" + str(player[0]), self.parse_player)
        #         request.meta['id'] = player[0]
        #         return request
        #     else:
        #         self.logger.warning("No players found.")
        # else:
        #     self.logger.warning("No players found.")

    def parse_player(self, response):
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
        player_id = response.meta['id']
        request = Request(
            url="https://www.whoscored.com/StatisticsFeed/1/GetPlayerStatistics?category=summary&subcategory=all&statsAccumulationType=0&isCurrent=true&playerId=" + str(player_id) + "&teamIds=&matchId=&stageId=&tournamentOptions=&sortBy=Rating&sortAscending=&age=&ageComparisonType=&appearances=&appearancesComparisonType=&field=Overall&nationality=&positionOptions=&timeOfTheGameEnd=&timeOfTheGameStart=&isMinApp=false&page=&includeZeroValues=true&numberOfPlayersToPick=",
            headers={'X-Requested-With': 'XMLHttpRequest', 'Host': 'www.whoscored.com'},
            callback=self.parse_player2
        )

        request.meta['team_id'] = team_id
        request.meta['name'] = name
        request.meta['full_name'] = full_name
        request.meta['age'] = age
        request.meta['id'] = response.meta['id']

        return request

    def parse_player2(self, response):
        player_id = response.meta['id']
        stats = json.loads(response.body)
        try:
            data = stats['playerTableStats'][0]
        except (KeyError, IndexError):
            return self.error_player(response)
        else:
            player = Player()
            player['id'] = player_id
            player['first_name'] = data['firstName']
            player['last_name'] = data['lastName']
            player['known_name'] = data['name']
            player['age'] = data['age']
            player['current_team'] = response.meta['team_id']

        return player

    def error_player(self, response):
        player = Player()
        player['id'] = response.meta['id']
        player['first_name'] = None
        player['last_name'] = None
        player['known_name'] = response.meta['name']
        player['age'] = response.meta['age']
        player['current_team'] = response.meta['team_id']

        return player
