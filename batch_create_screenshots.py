# using crawlera for proxy rotation and screenshot api's to grab the images

import csv, os, shutil, sys, requests
from csv import reader
from os import listdir, getcwd, path, makedirs, remove, rename

import urllib.request
import urllib.parse

from urllib3.exceptions import InsecureRequestWarning

import wget
import pandas as pd

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

with_responders_suffix = '_with_responders.csv'
with_screenshots_suffix = '_with_screenshots.csv'

# grab csv from 'with_emails' folder
csv_with_responders = listdir(with_responders_subfolder)

for csv_file in csv_with_responders:
    # read csv into dataframe
    csv_df = pd.read_csv(with_responders_subfolder + csv_file)

    city = csv_file.replace(niche + '_', '')
    city = city.replace(with_responders_suffix, '')
    city = city + '/'

    # create 'screenshots/city' subfolder if not exists
    screenshot_sub_folder_path = niche + '/screenshots/' + city
    if not path.exists(screenshot_sub_folder_path):
        makedirs(screenshot_sub_folder_path)

    # create 'csv_files/with_screenshots' subfolder if not exists
    if not path.exists(with_screenshots):
        makedirs(with_screenshots)

    # get screenshot
    rows = range(len(csv_df))
    for row in rows:
        bdp_url = base_url + csv_df.iloc[row].business_details_page        
        screenshot_file_name = csv_df.iloc[row].business_details_page.replace('/biz/', '')
        screenshot_file_name = screenshot_file_name + '.png'

        screenshot_output = screenshot_sub_folder_path + screenshot_file_name

        try:                   
            screenshot_url = getScreenshotURL(bdp_url)
            screenshot_image = downloadScreenshotImage(screenshot_url, screenshot_output)
                                
        except Exception as e:
            print(e) 
        
        # persist screenshot name to dataframe   
        # bdp_screenshot = csv_df.iloc[row].bdp_screenshot
        csv_df.at[row, 'bdp_screenshot'] = screenshot_file_name

    csv_df.to_csv(with_screenshots + csv_file.replace(with_responders_suffix, with_screenshots_suffix), index = False) 
          
       