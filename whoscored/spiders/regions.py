# -*- coding: utf-8 -*-
from scrapy import Spider
import re


class RegionsSpider(Spider):
    name = "regions"
    allowed_domains = ["whoscored.com"]
    start_urls = (
        'https://www.whoscored.com/',
    )

    def parse(self, response):
        region_data = response.xpath('//script[contains(., "allRegions")]/text()').re_first(r"allRegions = ([\w\W]*?);")
        
        if region_data:
            region = re.sub(r'\'(.*?)\'([,\]}])', r'"\1"\2', region_data)
            region = re.sub(r'(\w*?):', r'"\1":', region)
            region = re.sub(r"\\'", r"'", region)
            
            filename = 'regions.json'
            with open(filename, 'wb') as f:
                f.write(region.encode('utf8'))
        else:
            self.logger.warning("Variable allRegions not found.")
                
        return
