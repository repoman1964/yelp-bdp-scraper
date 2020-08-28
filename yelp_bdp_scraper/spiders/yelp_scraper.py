# -*- coding: utf-8 -*-
import scrapy, os
from os import listdir, system
from more_itertools import unique_everseen
from ..items import BDPScraperItem, YelpScraperItem

import json
import pandas as pd
from urllib.parse import urlparse
from more_itertools import unique_everseen

def get_geos_list():    

    # get cities
    cities_csv = '/home/jose/Projects/active/yelp_bdp_scraper/350_cities.csv'
    try:
        df = pd.read_csv(cities_csv)        

    except pd.errors.EmptyDataError:
        print('Note: filename.csv was empty. Skipping.')

    if not df.empty:
        rows = range(len(df))
        geos_list = []
        for row in rows:
            city = df.iloc[row].city
            city = city.strip()
            city = city.replace(' ', '%20')
            city = city.title()

            state = df.iloc[row].state
            state = state.strip()
            state = state.upper()

            geo = city + ':' + state
            geos_list.append(geo)

        return geos_list 

        



class YelpBDPSpider(scrapy.Spider):
    name = 'yelp_scraper'

    def start_requests(self):
       
        # niche = 'Divorce Attorney'
        # niche = 'Personal Injury Attorney'
        niche = 'Roofing'
        niche = niche.strip()
        niche = niche.replace(' ', '%20')
        niche = niche.replace('&', '%26')       
        
        base_url = 'https://www.yelp.com'

        for geo in get_geos_list():
            geo = geo.split(':')
            url = f"{base_url}/search?find_desc={niche}&find_loc={geo[0]}%2C%20{geo[1]}"
            print(url)       

            yield scrapy.Request(url=url, meta={'geo': geo})


    def parse(self, response):

        # geo values
        geo = response.meta["geo"]
        print(geo)              

        bdp_paths = []       

        # get business listing pages        
        bdp_urls = response.xpath("//a[starts-with(@href, '/biz')]/@href").getall()
        for bdp in bdp_urls:
            bdp_path = urlparse(bdp).path
            bdp_paths.append(bdp_path)

        unique_bdp_paths = list(unique_everseen(bdp_paths))
        for unique_bdp_path in unique_bdp_paths:

            base_url = 'https://www.yelp.com'
            bdp_url = base_url + unique_bdp_path

            yield scrapy.Request(url=bdp_url, callback=self.parse_details, meta={'business_details_page': unique_bdp_path, 'geo':geo})

        # follow pagination link
        next_page_snippet = response.xpath("//a[contains(@class, 'next-link')]/@href").get()

        if next_page_snippet:
            url = base_url + next_page_snippet
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_details(self, response):
        geo = response.meta["geo"]

        # initialize item container
        item = YelpScraperItem()

        item['scrape_city'] = geo[0]
        item['scrape_state'] = geo[1]


        # using json-ld data
        all_scripts = response.xpath('//script[@type="application/ld+json"]//text()').getall()
        # all_scripts = json.loads(response.xpath('//script[@type="application/ld+json"]//text()').getall())
        for script in all_scripts:
            data = json.loads(script)
            if data != 'no_data':
                if data['@type'] == 'LocalBusiness':
                    # # get business_name
                    # if data['name']:
                    #     item['business_name'] = data['name']
                    # else:
                    #     item['business_name'] = 'no_data'
                  
                    if data['address']:
                        # get business_zipcode
                        if data['address']['postalCode']:                       
                            item['business_zipcode'] = data['address']['postalCode']
                        else:
                            item['business_zipcode'] = 'no_data'
                             
                    
                        # get business_phone
                        if data['telephone']:                       
                            item['business_phone'] = data['telephone']
                        else:
                            item['business_phone'] = 'no_data'


                        # get business_phone
                        if data['address']['addressLocality']:                       
                            item['business_city'] = data['address']['addressLocality']
                        else:
                            item['business_city'] = 'no_data'

                        
            
                    aggregate_rating = data.get('aggregateRating')
                    if aggregate_rating:
                        # reviews count
                        if data['aggregateRating']['reviewCount']:                       
                            item['review_count'] = data['aggregateRating']['reviewCount']
                        else:
                            item['review_count'] = 'no_data'                        
                        
                        # get star count
                        if data['aggregateRating']['ratingValue']:                       
                            item['star_count'] = data['aggregateRating']['ratingValue']
                        else:
                            item['star_count'] = 'no_data'
                    else:
                        item['review_count'] = 'no_data'
                        item['star_count'] = 'no_data' 


        # get business_name
        business_name = response.css('h1::text').get()

        if business_name is not None:
            item['business_name'] = business_name
        else:
            item['business_name'] = 'no_data'

               
        # need this to get details page screen shot
        item['business_details_page'] = response.meta["business_details_page"]       

        # set bdp_screenshot to 'no_data'
        item['bdp_screenshot'] = 'no_data'
       
        # set business_email to 'no_data'
        item['business_email'] = 'no_data'
        
        # get business website
        item['business_website'] = response.xpath("//a[starts-with(@href, '/biz_redir')]/text()").get(default='no_data')

        # get response time. response times stored as minutes
        item['response_time'] = response.xpath("//p[contains(text(),'Response time')]/following-sibling::p//text()").get(default='no_data')

        # get response rate       
        item['response_rate'] = response.xpath("//p[contains(text(),'Response rate')]/following-sibling::p//text()").get(default='no_data')
        
        # get yelp advertiser
        item['yelp_advertiser'] = response.xpath("//p[contains(text(),'Yelp advertiser')]")

        # get recent local requests
        item['recent_local_requests'] = response.xpath("//div[contains(@data-testid, 'recent_requests_count')]/p/text()").extract_first()       

        # set request_leader to 'no_data'
        item['request_leader'] = 'no_data'

        # set request_leader_count to 'no_data'
        item['request_leader_count'] = 'no_data'    

        # get raq enabled        
        item['raq'] = response.xpath("//span[contains(text(),'Request ')]")

        # get photo count
        item['photo_count'] = response.xpath("//span[contains(text(),'See All')]//text()").get(default='no_data')

        # get hidden review count
        # item['hidden_review_count'] = response.xpath("//a[starts-with(@href, '/not_recommended_reviews/')]/text()").extract_first()

        item['hidden_review_count'] = response.xpath("//a[contains(text(),'not currently recommended')]//text()").get(default='no_data')

        # TODO DEV reviews and review author turned off
        item['reviews'] = 'no_data'
        item['reviews_author'] = 'no_data'

        yield item


    

    