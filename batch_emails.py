# using crawlera for proxy rotation and screenshot api's to grab the images

import csv, os, shutil, sys, requests
from csv import reader
from os import listdir, getcwd, path, makedirs, remove, rename

import urllib.request
import urllib.parse

from urllib3.exceptions import InsecureRequestWarning

import wget

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# TODO DEV input bypassed
# system('clear')
# niche = input("Enter the niche: ")
niche = 'dui'
with_landers_subfolder = niche + '/csv_files/with_landers/'
with_campaigns = niche + '/csv_files/with_campaigns/'
base_crm_endpoint = 'https://crm.responderbot.net/api'
base_video_endpoint = 'https://video.responderbot.net'

# grab csvs from 'with_screenshots' folder
csv_with_landers = listdir(with_landers_subfolder)

for csv_file in csv_with_videos:
    city = csv_file.replace('dui_', '')
    city = city.replace('_with_videos.csv', '')
    city = city + '/'
   

    # create 'csv_files/with_landers' subfolder if not exists
    if not path.exists(with_landers):
        makedirs(with_landers)
    
    # create 'with_landers' output csv file if not exist ################################################
    csv_with_landers = csv_file.replace('_with_videos.csv', '')
    csv_with_landers_output_file_name = with_landers + csv_with_landers + '_with_landers.csv'

   
    if not path.exists(csv_with_landers_output_file_name):
        # create file
        with open(csv_with_landers_output_file_name, 'w') as csvfile:
            newfile = csv.writer(csvfile)      
            # set header row
            # create header row
            newfile.writerow([
                "business_details_page", 
                "bdp_screenshot", 
                "business_email", 
                "business_website",
                "business_name", 
                "business_phone", 
                "business_zipcode",

                "raq", 
                "response_time", 
                "response_rate",
                "recent_local_requests",

                "request_leader",
                "request_leader_count",

                "yelp_advertiser",

                "photo_count",
                "star_count",

                "review_count",
                "reviews", 
                "reviews_author",
                "hidden_review_count",

                "cold_email_video_url",

                "lander_url",

                ])
            # close file
            csvfile.close()
    # read csv ###############################################################
    with open(with_videos_subfolder + csv_file, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # next(csv_reader)
        for row in csv_reader:                      
            # get video url
            video_url = row['cold_email_video_url']
            l = open('lander.txt','rt')
            lander_html = l.read()
            l.close()

            lander_html = lander_html.replace('XXX', video_url)
            

            title = row['business_name']
            title = title.replace(' ', '-').lower()
            lander_url = "https://crm.responderbot.net/" + title
          

            try:
                # post create page request to crm
                data = {
                    "title": title,
                    "customHtml": lander_html,
                    "redirectUrl": "https://responderbot.net"
                }
                endpoint = base_endpoint + '/pages/new' 
                r = requests.post(endpoint, data=data, auth=('jose', 'maddog152fo###'))

                # get result
                file_url = r.json().get("url")
                file_id = r.json().get("id")

            except Exception as e:
                print(e)                    
                    

            # write to output csv
            with open(csv_with_landers_output_file_name, 'a', newline='') as csvfile:
                fieldnames = [
                    'business_details_page', 
                    'bdp_screenshot', 
                    'business_email',
                    'business_website', 
                    'business_name',
                    'business_phone',                    
                    'business_zipcode',

                    "raq", 
                    "response_time", 
                    "response_rate",
                    "recent_local_requests",

                    "request_leader",
                    "request_leader_count",

                    "yelp_advertiser",

                    "photo_count",
                    "star_count",

                    "review_count",
                    "reviews", 
                    "reviews_author",
                    "hidden_review_count",

                    "cold_email_video_url",

                    "lander_url"
                    ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)              

                writer.writerow({
                    'business_details_page': row['business_details_page'], 
                    'bdp_screenshot': row['bdp_screenshot'],
                    'business_email': row['business_email'],
                    'business_website': row['business_website'],
                    'business_name': row['business_name'],
                    'business_phone': row['business_phone'],
                    'business_zipcode': row['business_zipcode'],                    

                    'raq': row['raq'],
                    'response_time': row['response_time'],
                    'response_rate': row['response_rate'],
                    'recent_local_requests': row['recent_local_requests'],

                    'request_leader': row['request_leader'],
                    'request_leader_count': row['request_leader_count'],

                    'yelp_advertiser': row['yelp_advertiser'],

                    'photo_count': row['photo_count'],
                    'star_count': row['star_count'],

                    'review_count': row['review_count'],
                    'reviews': row['reviews'],
                    'reviews_author': row['reviews_author'],
                    'hidden_review_count': row['hidden_review_count'],

                    "cold_email_video_url": row['cold_email_video_url'],

                    "lander_url": lander_url,


                })