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

def getScreenshotURL(screenshot_url):

    # The parameters.
    token = "CZDB9RBGNFLBE34PS6R3T3Z28HJKRSZI"
    width = 1920
    height = 1080
    output = "image"

    # build the target URL.
    target_url = "https://screenshotapi.net/api/v1/screenshot"
    target_url += f"?token={token}&url={screenshot_url}&width={width}&height={height}&output={output}"


    url = target_url
    proxy_host = "proxy.crawlera.com"
    proxy_port = "8010"
    proxy_auth = "3a906b17f3d24b9db99d5b75c093b020:" # Make sure to include ':' at the end
    proxies = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
        "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}

    response = requests.get(url, proxies=proxies, verify=False)
    return response.url

def downloadScreenshotImage(screenshot_url, screenshot_file_path):
    filename = wget.download(screenshot_url, out=screenshot_file_path)

def saveScreenshotImage(screenshot_url, screenshot_file_path):
    filename = wget.download(screenshot_url, out=screenshot_file_path)

# TODO DEV input bypassed
# system('clear')
# niche = input("Enter the niche: ")
niche = 'dui'
with_responders_subfolder = niche + '/csv_files/with_responders/'
with_screenshots = niche + '/csv_files/with_screenshots/'
base_url = 'https://www.yelp.com'

# grab csv from 'with_emails' folder
csv_with_responders = listdir(with_responders_subfolder)

for csv_file in csv_with_responders:
    city = csv_file.replace('dui_', '')
    city = city.replace('_with_responders.csv', '')
    city = city + '/'

    # create 'screenshots/city' subfolder if not exists
    screenshot_sub_folder_path = niche + '/screenshots/' + city
    if not path.exists(screenshot_sub_folder_path):
        makedirs(screenshot_sub_folder_path)

    # create 'csv_files/with_screenshots' subfolder if not exists
    if not path.exists(with_screenshots):
        makedirs(with_screenshots)
    
    # create 'with_screenshot' output csv file if not exist ################################################
    csv_with_screenshots = csv_file.split('_with_responders.csv')[0]
    csv_with_screenshots_output_file_name = with_screenshots + csv_with_screenshots + '_with_screenshots.csv'

   
    if not path.exists(csv_with_screenshots_output_file_name):
        # create file
        with open(csv_with_screenshots_output_file_name, 'w') as csvfile:
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


                ])
            # close file
            csvfile.close()
    # read csv ###############################################################
    with open(with_responders_subfolder + csv_file, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        # next(csv_reader)
        for row in csv_reader:
            # if row['business_email'].lower() != 'xxx' and row['business_email'].lower() != 'no_data':
            #     business_email = row['business_email'].lower()
            # get screenshot
            bdp_url = base_url + row['business_details_page']
            screenshot_file_name = row['business_details_page'].split('/biz/')[-1]
            screenshot_file_name = screenshot_file_name + '.png'

            screenshot_output = screenshot_sub_folder_path + screenshot_file_name

            try:                   
                screenshot_url = getScreenshotURL(bdp_url)
                print(screenshot_url)
                screenshot_image = downloadScreenshotImage(screenshot_url, screenshot_output)
                                
            except Exception as e:
                print(e)
                    
                    

                # write to output csv
            with open(csv_with_screenshots_output_file_name, 'a', newline='') as csvfile:
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
                    ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)              

                writer.writerow({
                    'business_details_page': row['business_details_page'], 
                    'bdp_screenshot': screenshot_file_name,
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

                    "cold_email_video_url": row['cold_email_video_url']                    

                })