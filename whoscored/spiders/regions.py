# -*- coding: utf-8 -*-
import scrapy
import re


class RegionsSpider(scrapy.Spider):
    name = "regions"
    allowed_domains = ["whoscored.com"]
    start_urls = (
        'http://www.whoscored.com/',
    )

    def parse(self, response):
        region_data = response.xpath('//script[contains(., "allRegions")]/text()').extract()
        if len(region_data) == 0:
            return
        
        regions = re.search("allRegions = ([\w\W]*?);", region_data[0])
        
        if regions:
            region = re.sub(r'\'(.*?)\'([,\]}])', r'"\1"\2', regions.group(1))
            region = re.sub(r'(\w*?):', r'"\1":', region)
            region = re.sub(r"\\'", r"'", region)
            
            filename = 'regions.json'
            with open(filename, 'wb') as f:
                f.write(region.encode('utf8'))
                
        return
