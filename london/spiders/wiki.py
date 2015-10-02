# -*- coding: utf-8 -*-
import scrapy
from london.items import BoroughItem

import re

class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["wikipedia.org"]
    start_urls = (
        "http://www.wikipedia.org/wiki/List_of_districts_in_Barking_and_Dagenham",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Barnet",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Bexley",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Brent",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Bromley",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Camden",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Croydon",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Ealing",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Enfield",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Greenwich",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Hackney",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Hammersmith_and_Fulham",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Haringey",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Harrow",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Havering",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Hillingdon",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Hounslow",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Islington",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Kensington_and_Chelsea",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Kingston_upon_Thames",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Lambeth",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Lewisham",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Merton",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Newham",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Redbridge",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Richmond_upon_Thames",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Southwark",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Sutton",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Tower_Hamlets",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Waltham_Forest",
        "http://www.wikipedia.org/wiki/List_of_districts_in_Wandsworth",
        "http://www.wikipedia.org/wiki/List_of_districts_in_the_City_of_Westminster",
    )

    def parse(self, response):
        borough = response.url[51:].replace('_', ' ')
        
        xpath = '//*[@id="mw-content-text"]/ul/li/a[1]/@href'
        
        if 'Lewisham' in borough:
            xpath = '//*[@id="mw-content-text"]/table[1]/tr/td[2]/a/@href'
        elif 'Kensington' in borough:
            xpath = '//*[@id="mw-content-text"]/div/ul/li/a[1]/@href'
        elif re.search('(Barking|Havering|Haringey)', borough):
            xpath = '//*[@id="mw-content-text"]/table[2]/tr/td[1]/a/@href'
            
        links = response.xpath(xpath).extract()

        
        # links2 = response.xpath('//*[@id="mw-content-text"]/table[2]/tr/td[1]/a/@href').extract()
        # links3 = response.xpath('//*[@id="mw-content-text"]/table[3]/tr/td[1]/a/@href').extract()

        # if len(links2) > len(links):
        #     links = links2
        # if len(links3) > len(links):
        #     links = links3

        if len(links) < 6:
            links = response.xpath('//*[@id="mw-content-text"]/table[1]/tr/td[1]/a/@href').extract()
        
            

        names = [s.split('/')[-1].split(',')[0].replace('_', ' ') for s in links]



        print 'found %d in %s' % (len(links), borough)

        for name, link in zip(names, links):
            item = BoroughItem()
            item['name'] = name
            item['link'] = link
            item['borough'] = borough
            yield item
