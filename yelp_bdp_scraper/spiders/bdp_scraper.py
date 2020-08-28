# scrapy crawl bdp_scraper -a FIND_DESC=Dwi%20Attorney -a FIND_LOC_CITY=Long%20Beach -a FIND_LOC_STATE=CA -o csv_files/with_nothing/dui/dui_long_beach_with_nothing.csv

# -*- coding: utf-8 -*-
import scrapy, os
from os import listdir, system
from more_itertools import unique_everseen
from ..items import BDPScraperItem

import pandas as pd

def get_urls_from_cities_list():

    # system('clear')
    # niche = input("Enter the niche: ")
    # niche = niche.title()
    niche = 'DUI%20Lawyer'
    # niche = 'Divorce%20%26%20Family%20Law'
    # niche = 'Personal%20Injury%20Attorney'    
    niche = niche.strip()
    niche = niche.replace(' ', '%20')
    # niche = niche.title()


    # get cities
    cities_csv = '/home/jose/Projects/active/fb_scraper/150_cities.csv'
    try:
        df = pd.read_csv(cities_csv)        

    except pd.errors.EmptyDataError:
        print('Note: filename.csv was empty. Skipping.')

    if not df.empty:
        rows = range(len(df))
        scrape_urls = []
        cities_urls_list = []
        for row in rows:
            city = df.iloc[row].city
            city = city.strip()
            city = city.replace(' ', '%20')
            city = city.title()

            state = df.iloc[row].state
            state = state.strip()
            state = state.upper()

            base_url = 'https://www.yelp.com'

            # url = base_url + '/search?find_desc=' + self.FIND_DESC + '&find_loc=' + self.FIND_LOC_CITY + '%2C%20' + self.FIND_LOC_STATE 

            url = f"{base_url}/search?find_desc={niche}&find_loc={city}%2C%20{state}"


            cities_urls_list.append(url)

            cities_urls_list = 'https://www.yelp.com/search?cflt=mortgagebrokers&find_desc=Mortgage+Brokers&find_loc=Denver%2C+CO'
        return cities_urls_list



class BDPScraperSpider(scrapy.Spider):
    name = 'bdp_scraper'

    def start_requests(self):
        for city_url in get_urls_from_cities_list():
            yield scrapy.Request(url=city_url)

        # city_url = 'https://www.yelp.com/search?find_desc=Dui%20Attorney&find_loc=Austin%2C%20TX'
        # city_from_url = city_url.split('&find_loc=')[-1]
        # city_from_url = city_from_url.split('%2C')[0]
        # city_from_url = city_from_url.lower()        
        # # yield scrapy.Request(url=city_url, meta={'city_from_url': city_from_url})
        # yield scrapy.Request(city_url, callback=self.parse, meta={'city_from_url': city_from_url})



    def parse(self, response):          

        cleaned_bdp_urls = []       

        # get business listing pages        
        bdp_urls = response.xpath("//a[starts-with(@href, '/biz')]/@href").extract()       

        for bdp in bdp_urls:
            bdp_url = bdp.split('?')[0]
            cleaned_bdp_urls.append(bdp_url)

        unique_bdp_urls = list(unique_everseen(cleaned_bdp_urls))
        for unique_bdp_url in unique_bdp_urls:

            base_url = 'https://www.yelp.com'
            unique_detail_url = base_url + unique_bdp_url

            yield scrapy.Request(url=unique_detail_url, callback=self.parse_details, meta={'business_details_page': unique_bdp_url})

        # follow pagination link
        next_page_snippet = response.xpath("//a[contains(@class, 'next-link')]/@href").get()
        
        if next_page_snippet:
            url = base_url + next_page_snippet
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_details(self, response):

        # initialize item container
        item = BDPScraperItem()

        # need this to get details page screen shot
        business_details_page = response.meta["business_details_page"]

        if business_details_page is not None:

            business_details_page = business_details_page.split('?osq=')[0]
            item['business_details_page'] = business_details_page
        else:
            item['business_details_page'] = 'no_data'        

        # set bdp_screenshot to 'no_data'
        bdp_screenshot = 'no_data'
        item['bdp_screenshot'] = bdp_screenshot       

        # get business_name
        business_name = response.css('h1::text').get()

        if business_name is not None:
            item['business_name'] = business_name
        else:
            item['business_name'] = 'no_data'

        # set business_email to 'no_data'
        business_email = 'no_data'
        item['business_email'] = business_email
        
        # get business website       
        business_website = response.xpath("//a[starts-with(@href, '/biz_redir')]/@href").extract_first()
        # format business website

        if business_website is not None:
            start_split = '%3A%2F%2F'
            end_split = '&website_link_type'
            business_website = (business_website.split(start_split))[1].split(end_split)[0]
            business_website = business_website.split('%2F')
            business_website = business_website[0].split('www.')
            business_website = business_website[-1]
            
            business_website = business_website.lower()

            item['business_website'] = business_website

        else:
            item['business_website'] = 'no_data'

        # get business_zipcode
        business_zipcode = response.xpath("//span[@itemprop='postalCode']//text()").get()

        last_address = response.xpath('//address/p[last()]/span/text()').get()
        business_zipcode = last_address.split()[-1]
        
        # format business_zipcode
        if business_zipcode is not None:
            item['business_zipcode'] = business_zipcode    
        else:
            item['business_zipcode'] = 'no_data'

        # get business_phone
        business_phone = response.xpath("//p[contains(text(),'Phone number')]/following-sibling::p//text()").get()
        
        # format business_phone
        if business_phone is not None:
            business_phone = (business_phone.replace('(', ''))
            business_phone = (business_phone.replace(')', ''))
            business_phone = (business_phone.replace('-', ''))
            business_phone = (business_phone.replace(' ', ''))

            item['business_phone'] = business_phone    #put link to sales pitch landing page in a text messsage. kewl!
        else:
            item['business_phone'] = 'no_data'

        # business_city = response.xpath("//address/p[4]//text()").get()
        business_city = response.xpath("//address/p[last()]/span/text()").get()
        if business_city is not None:
            business_city = business_city.split(',')[0].lower()
            item['business_city'] = business_city

        # get response time. response times stored as minutes
        response_time = response.xpath("//p[contains(text(),'Response time')]/following-sibling::p//text()").get()

        if response_time is not None:

            response_time = response_time.split()
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

        else:
            item['response_time'] = 'no_data'


        # get response rate       
        response_rate = response.xpath("//p[contains(text(),'Response rate')]/following-sibling::p//text()").get()
        # format response rate
        if response_rate is not None:
            response_rate = int(response_rate[:-1])

            item['response_rate'] = response_rate
        else:
            item['response_rate'] = 'no_data'          

        # get yelp advertiser
        yelp_advertiser = response.xpath("//p[contains(text(),'Yelp advertiser')]")

        if len(yelp_advertiser) > 0:
            item['yelp_advertiser'] = 'yelp advertiser'
        else:
            item['yelp_advertiser'] = 'not a yelp advertiser'


        # get recent local requests
        recent_local_requests = response.xpath("//div[contains(@data-testid, 'recent_requests_count')]/p/text()").extract_first()
        if recent_local_requests is not None:
            recent_local_requests = recent_local_requests.split()
            recent_local_requests = recent_local_requests[0]           

            item['recent_local_requests'] = recent_local_requests
        else:
            item['recent_local_requests'] = 'no_data'

        # set request_leader to 'no_data'
        request_leader = 'no_data'
        item['request_leader'] = request_leader

        # set request_leader_count to 'no_data'
        request_leader_count = 'no_data'
        item['request_leader_count'] = request_leader_count       

        # get raq enabled        
        # raq = response.xpath("//h4[text() = 'Request a Quote']//text()").get()
        # legal niche
        raq = response.xpath("//h4[text() = 'Request a Consultation']//text()").get()
        # format raq enabled
        if raq is not None:
            if raq and recent_local_requests:
                raq = 'active'
            elif raq and not recent_local_requests:
                raq = 'enabled'
            elif not raq:
                raq = 'no_data'

            item['raq'] = raq
        else:
            item['raq'] = 'no_data'

        # get photo count
        photo_count = response.xpath("//a[contains(text(),'See All')]//text()").get()
        # format photo count
        if photo_count is None:
            photo_count = response.xpath("//span[contains(text(),'See All')]//text()").get()
        
        if photo_count is not None:
            photo_count_split = photo_count.split()
            photo_count = photo_count_split[2]

            item['photo_count'] = int(photo_count)
        else:
            item['photo_count'] = 0

        # get review count
        # review_count = response.css(".text-color--mid__373c0__3G312.text-size--large__373c0__1568g::text").get()
        review_count = response.xpath('//*[@class="lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa- text-size--large__373c0__3t60B"]/text()').get()
        
        # item['review_count'] = review_count
        # format review count
        if review_count is not None:
            review_count_split = review_count.split()
            review_count = review_count_split[0]
            
            item['review_count'] = int(review_count)
        else:
            item['review_count'] = 0


        # get star count
        item['star_count'] = response.xpath("//div[contains(@class, 'i-stars--large-')]/@aria-label").extract_first()
        # format star count
        if item['star_count'] is not None:

            star_count = item['star_count']
            star_count = star_count.split()
            star_count = star_count[0]          

            item['star_count'] = star_count
      
        else:
            item['star_count'] = 'no_data'

        # get hidden review count
        item['hidden_review_count'] = response.xpath("//a[starts-with(@href, '/not_recommended_reviews/')]/text()").extract_first()

        if item['hidden_review_count'] is not None:
    
            hidden_review_count = item['hidden_review_count']
            hidden_review_count = hidden_review_count.split()
            hidden_review_count = hidden_review_count[0]          

            item['hidden_review_count'] = int(hidden_review_count)
      
        else:
            item['hidden_review_count'] = 0

        # TODO DEV reviews and review author turned off
        item['reviews'] = 'no_data'
        item['reviews_author'] = 'no_data'

        # # get reviews
        # reviews = response.xpath("//p[contains(@class, 'comment')]/span/text()").extract()       

        # if reviews is not None:
        #     item['reviews'] = reviews      
        # else:
        #     item['reviews'] = 'no_data'


        # # get reviews_author
        # reviews_author =response.xpath("//div[contains(@class, 'user-passport-info')]/a/span/text()").extract()

        # if reviews_author is not None:
        #     item['reviews_author'] = reviews_author      
        # else:
        #     item['reviews_author'] = 'no_data'



        # set cold_email_video_url to 'no_data'
        cold_email_video_url = 'no_data'
        item['cold_email_video_url'] = cold_email_video_url
      

        yield item



