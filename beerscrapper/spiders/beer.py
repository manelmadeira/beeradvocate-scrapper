# -*- coding: utf-8 -*-
import scrapy
import urlparse

from beerscrapper.items import *


class BeerSpider(scrapy.Spider):
    name = 'beer'
    allowed_domains = ['www.beeradvocate.com']
    start_urls = ['https://www.beeradvocate.com/beer/style/']

    def parse(self, response):
        table = response.xpath('//*[@id="ba-content"]/table')
        styles = table.xpath('//a[contains(@href, "/style/")]/@href')

        for style in styles:
            yield response.follow(style, self.parse_style)

    def parse_style(self, response):
        table = response.css('div#ba-content table')
        table_row = table.css('tr')

        table_len = len(table_row)
        idx = 1
        for row in table_row:
            if idx > 3 and idx < table_len:
                beer_url = row.css('td:nth-child(1) a::attr(href)').extract_first()
                request = scrapy.Request(urlparse.urljoin(response.url, beer_url), self.parse_beer)
                style_id = response.url.split("/")[-2]
                request.meta['style_id'] = style_id
                yield request

            if idx == table_len:
                next_url = row.xpath('//td/span/a[contains(text(), "next")]/@href').extract_first()
                yield response.follow(next_url, self.parse)

            idx += 1

    def parse_beer(self, response):
        main_content = response.css('div.mainContent')
        beer_info = response.xpath('//*[@id="ba-content"]/div[3]/div[2]')

        name = main_content.css('div.titleBar h1::text').extract_first()
        ba_score = main_content.css('span.ba-score::text').extract_first()
        ba_ratings = main_content.css('span.ba-ratings::text').extract_first()
        picture = beer_info.css('img::attr(src)').extract_first()
        producer = response.xpath(
            '//*[@id="ba-content"]/div[3]/div[2]/a[contains(@href, "beer/profile")]/b/text()'
        ).extract_first()

        location = response.xpath(
            '//*[@id="ba-content"]/div[3]/div[2]/a[contains(@href, "place")]/text()'
        ).extract()

        city = ''
        country = ''
        if len(location) > 1:
            city = location[0]
            country = location[1]
        else:
            country = location[0]

        website = response.xpath(
            '//*[@id="ba-content"]/div[3]/div[2]/a[contains(@target, "_blank")]/text()'
        ).extract_first()
        style_id = response.meta['style_id']
        style = response.xpath(
            '//*[@id="ba-content"]/div[3]/div[2]/a[contains(.//@href, "style")]/b/text()'
        ).extract_first()
        alcohol = response.xpath('//*[@id="ba-content"]/div[3]/div[2]/text()[14]').extract_first()

        yield BeerItem(
            name=name,
            ba_score=ba_score,
            ba_ratings=ba_ratings,
            picture=picture,
            producer=producer,
            city=city,
            country=country,
            website=website,
            style=style,
            style_id=style_id,
            alcohol=alcohol
        )
