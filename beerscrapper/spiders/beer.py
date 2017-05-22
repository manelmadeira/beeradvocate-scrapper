# -*- coding: utf-8 -*-
import scrapy


class BeerSpider(scrapy.Spider):
    name = 'beer'
    allowed_domains = ['www.beeradvocate.com']
    start_urls = ['https://www.beeradvocate.com/beer/style/128/']

    def parse(self, response):
        table = response.css('div#ba-content table')
        table_row = table.css('tr')

        table_len = len(table_row)
        idx = 1
        for row in table_row:
            if idx > 3 and idx < table_len:
                beer_url = row.css('td:nth-child(1) a::attr(href)').extract_first()
                yield response.follow(beer_url, self.parse_beer)

            if idx == table_len:
                next_url = row.css('td:nth-child(1) a:nth-child(3)::attr(href)').extract_first()
                yield response.follow(next_url, self.parse)

            idx += 1

    def parse_beer(self, response):
        main_content = response.css('div.mainContent')
        beer_info = response.xpath('//*[@id="ba-content"]/div[3]/div[2]')

        name = main_content.css('div.titleBar h1::text').extract_first()
        ba_score = main_content.css('span.ba-score::text').extract_first()
        ba_ratings = main_content.css('span.ba-ratings::text').extract_first()
        picture = beer_info.css('img::attr(src)').extract_first()
        producer = response.xpath('//*[@id="ba-content"]/div[3]/div[2]/a[1]/b/text()').extract_first()
        city = response.xpath('//*[@id="ba-content"]/div[3]/div[2]/a[2]/text()').extract_first()
        country = response.xpath('//*[@id="ba-content"]/div[3]/div[2]/a[3]/text()').extract_first()
        website = response.xpath('//*[@id="ba-content"]/div[3]/div[2]/a[4]/text()').extract_first()
        style = response.xpath('//*[@id="ba-content"]/div[3]/div[2]/a[5]/b/text()').extract_first()
        alcohol = response.xpath('//*[@id="ba-content"]/div[3]/div[2]/text()[14]').extract_first()

        yield {
            'name': name,
            'ba_score': ba_score,
            'ba_ratings': ba_ratings,
            'picture': picture,
            'producer': producer,
            'city': city,
            'country': country,
            'website': website,
            'style': style,
            'alcohol': alcohol,
        }
