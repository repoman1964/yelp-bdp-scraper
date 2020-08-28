# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    scrape_city = scrapy.Field()
    scrape_state = scrapy.Field()

    business_details_page = scrapy.Field()
    bdp_screenshot = scrapy.Field()
    business_email = scrapy.Field()
    business_name = scrapy.Field()
    business_website = scrapy.Field()    
    business_zipcode = scrapy.Field()
    business_phone = scrapy.Field()
    business_city = scrapy.Field()

    raq = scrapy.Field()    
    response_time = scrapy.Field()
    response_rate = scrapy.Field()

    recent_local_requests = scrapy.Field()
    request_leader = scrapy.Field()
    request_leader_count = scrapy.Field()

    yelp_advertiser = scrapy.Field()
    
    photo_count = scrapy.Field()
    review_count = scrapy.Field()
    star_count = scrapy.Field()
    hidden_review_count = scrapy.Field()

    reviews = scrapy.Field()
    reviews_author = scrapy.Field()
    
    cold_email_video_url = scrapy.Field()


class BDPScraperItem(scrapy.Item):
    # define the fields for your item here like:    

    business_details_page = scrapy.Field()
    bdp_screenshot = scrapy.Field()
    business_email = scrapy.Field()
    business_name = scrapy.Field()
    business_website = scrapy.Field()    
    business_zipcode = scrapy.Field()
    business_phone = scrapy.Field()
    business_city = scrapy.Field()

    raq = scrapy.Field()    
    response_time = scrapy.Field()
    response_rate = scrapy.Field()

    recent_local_requests = scrapy.Field()
    request_leader = scrapy.Field()
    request_leader_count = scrapy.Field()

    yelp_advertiser = scrapy.Field()
    
    photo_count = scrapy.Field()
    review_count = scrapy.Field()
    star_count = scrapy.Field()
    hidden_review_count = scrapy.Field()

    reviews = scrapy.Field()
    reviews_author = scrapy.Field()
    
    cold_email_video_url = scrapy.Field()
