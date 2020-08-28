# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from urllib.parse import urlparse

class BDPScraperPipeline:
    def process_item(self, item, spider):
        if item.get('response_time') == 'no_data':           
            raise DropItem('returned no data')
        return item


class YelpScrapeDetailsPageProcessItemPipeline:
    def process_item(self, item, spider):

        # SCRAPE CITY
        if item.get('scrape_city') != 'no_data':            
            scrape_city = item.get('scrape_city')
            scrape_city = scrape_city.replace('%20', ' ')
            item['scrape_city'] = scrape_city
        else:
            item['scrape_city'] = 'no_data'

       
        # BUSINESS NAME
        if item.get('business_name') != 'no_data':
            business_name = item.get('business_name')
            if '&amp;' in business_name:
                business_name = business_name.replace('&amp;', '&')
            if '&amp' in business_name:
                business_name = business_name.replace('&amp', '&')
            if '&apos;s' in business_name:
                business_name = business_name.replace("&apos;s", "'s")
        else:
            item['business_name'] = 'no_data'


        # BUSINESS PHONE
        if item.get('business_phone') != 'no_data':
            business_phone = (item.get('business_phone').replace('(', ''))
            business_phone = (business_phone.replace(')', ''))
            business_phone = (business_phone.replace('-', ''))
            business_phone = (business_phone.replace(' ', ''))
            item['business_phone'] = business_phone

        # BUSINESS WEBSITE
        if item.get('business_website') != 'no_data':
            # bdp_path = urlparse(item.get('business_website')).path
            business_website = urlparse(item.get('business_website')).path
            business_website = business_website.split('/')[0]

            business_website = business_website.replace('www.', '')            
            business_website = business_website.lower()
            item['business_website'] = business_website
        else:
            item['business_website'] = 'no_data'

        # RESPONSE TIME        
        if item.get('response_time') == 'no_data':           
            raise DropItem('returned no data')
        else:
            response_time = item.get('response_time').split()
            response_time_quantity = int(response_time[0])
            response_time_unit = response_time[1]

            if response_time_unit == 'minutes':
                response_time = response_time_quantity
            elif response_time_unit == 'hour':
                response_time = response_time_quantity*60
            elif response_time_unit == 'hours':
                response_time = response_time_quantity*60
            elif response_time_unit == 'day':
                response_time = response_time_quantity*1440
            elif response_time_unit == 'days':
                response_time = response_time_quantity*1440
            elif response_time_unit == 'week':
                response_time = response_time_quantity*10080
            elif response_time_unit == 'weeks':
                response_time = response_time_quantity*10080
            else:
                response_time = ''
         
            item['response_time'] = response_time

        # RESPONSE RATE
        if item.get('response_rate') != 'no_data':
            response_rate = int(item.get('response_rate')[:-1])
            item['response_rate'] = response_rate

        # YELP ADVERTISER
        if len(item.get('yelp_advertiser')) > 0:
            item['yelp_advertiser'] = 'yelp advertiser'
        else:
            item['yelp_advertiser'] = 'not a yelp advertiser'

        # RECENT REQUESTS
        if item.get('recent_local_requests') != 'no_data':
            recent_local_requests = item['recent_local_requests'].split()
            recent_local_requests = recent_local_requests[0]
            item['recent_local_requests'] = recent_local_requests

        # RAQ EXISTS
        if len(item.get('raq')) > 0:

            if response_rate != 'no_data':
                item['raq'] = 'active'
            else:
                item['raq'] = 'enabled'

        else:
            item['raq'] = 'no_data'

        # PHOTO COUNT
        if item.get('photo_count') != 'no_data':
            item['photo_count'] = item.get('photo_count').split()[-1]

        # HIDDEN REVIEW COUNT
        if item.get('hidden_review_count') != 'no_data':
            item['hidden_review_count'] = item['hidden_review_count'].split()[0]

        return item



class YelpBdpScraperPipeline(object):
    def process_item(self, item, spider):
        return item
