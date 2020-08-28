import csv, os, shutil, sys, requests
from csv import reader
from os import listdir, getcwd, path, makedirs, remove, rename

import urllib.request
import urllib.parse

from urllib3.exceptions import InsecureRequestWarning

import wget
import pandas as pd

CRM_USERNAME = 'jose'
CRM_PASSWORD = '*8^jGCk4iO(XRNV6uA(l$5Bj'

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# TODO DEV input bypassed
# system('clear')
# niche = input("Enter the niche: ")
niche = 'dui'
# TODO DEV while  rendering video 
with_videos_subfolder = niche + '/csv_files/with_videos/'
with_landers_subfolder = niche + '/csv_files/with_landers/'
base_endpoint = 'https://crm.responderbot.net/api'
niche_prefix = niche + '_' 
with_videos_suffix = '_with_videos.csv'
with_landers_suffix = '_with_landers.csv'

# grab csvs from 'with_screenshots' folder
csv_with_videos = listdir(with_videos_subfolder)

for csv_file in csv_with_videos:
    city = csv_file.replace(niche_prefix, '')
    city = city.replace(with_videos_suffix, '/')   

    category_exists = False

    # get niche+city category from crm. create if not exist
    try:
        # post create page request to crm       
        endpoint = base_endpoint + '/categories' 
        r = requests.get(endpoint, auth=(CRM_USERNAME, CRM_PASSWORD), timeout=3)
        r.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        print ("Http Error:", errh)
        continue
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:", errc)
        continue
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:", errt)
        continue
    except requests.exceptions.RequestException as err:
        print ("Oops: Something Else", err)
        continue

    # get categories result   
    categories = r.json().get("categories")
    if categories:
        # correct 2 word cities
        # city.replace('_', '-')   
        category_alias = niche + '-' + city.replace('/', '')
        category_title = niche.upper() + ' ' + city.replace('/', '').title()
        # correct 2 word cities
        category_alias = category_alias.replace('_', '-')
        category_title = category_title.replace('_', ' ') 
    
        for category in categories:
            if category["alias"] == category_alias:
                category_exists = True
                category_id = category["id"]

            else:
                category_exists = False
        
                # create category in crm 
                try:                    
                    data = {
                        "title": category_title,
                        "alias": category_alias,
                        "bundle": "global",
                    }
                    endpoint = base_endpoint + '/categories/new' 
                    r = requests.post(endpoint, data=data, auth=(CRM_USERNAME, CRM_PASSWORD))
                    r.raise_for_status() 
                    # get category id
                    category_id = r.json().get("category")["id"]
                    break

                except requests.exceptions.HTTPError as errh:
                    print ("Http Error:", errh)
                    continue
                except requests.exceptions.ConnectionError as errc:
                    print ("Error Connecting:", errc)
                    continue
                except requests.exceptions.Timeout as errt:
                    print ("Timeout Error:", errt)
                    continue
                except requests.exceptions.RequestException as err:
                    print ("Oops: Something Else", err)
                    continue  

    
   

    # create 'csv_files/with_landers' subfolder if not exists
    if not path.exists(with_landers_subfolder):
        makedirs(with_landers_subfolder)
    
    # create 'with_landers' output csv file if not exist ################################################
    # csv_with_landers = csv_file.replace('_with_videos.csv', '_with_lahttps://crm.responderbot.net/law-offices-of-rondee-j.-eaglenders.csv')
    # csv_with_landers_output_file_name = with_landers + csv_with_landers

    # read csv into dataframe ###############################################################
    csv_df = pd.read_csv(with_videos_subfolder + csv_file)

    rows = range(len(csv_df))
    for row in rows:   # create lander

        ##########################################################
        # get lander dynamic data
        video_url = csv_df.iloc[row].cold_email_video_url
        if video_url:
            business_name = csv_df.iloc[row].business_name
            l = open('lander.txt','rt')
            lander_html = l.read()
            l.close()

            lander_html = lander_html.replace('video_url', video_url)
            lander_html = lander_html.replace('business_name', business_name)
        
            title = business_name.replace(' ', '-').lower()
            title = title.replace(',', '').lower()
            title = title.replace('.', '').lower()
            title = title.replace('&', '').lower()
            title = title.replace('--', '-').lower()
            lander_url = "https://crm.responderbot.net/" + title          

        try:
            # post create page request to crm
            data = {
                "title": title,
                "customHtml": lander_html,
                "redirectUrl": "https://responderbot.net",
                "category": category_id
            }
            endpoint = base_endpoint + '/pages/new' 
            r = requests.post(endpoint, data=data, auth=(CRM_USERNAME, CRM_PASSWORD))
            r.raise_for_status()               

        except requests.exceptions.HTTPError as errh:
            print ("Http Error:", errh)
            continue
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
            continue
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
            continue
        except requests.exceptions.RequestException as err:
            print ("Oops: Something Else", err)
            continue

        # persist video url to dataframe   
        csv_df.at[row, 'lander_url'] = lander_url

        # persist screenshot url to dataframe
        screenshot_url = csv_df.iloc[row].bdp_screenshot
        screenshot_url = 'https://responderbot.net/' + niche + '/' + city + screenshot_url
        csv_df.at[row, 'screenshot_url'] = screenshot_url    

        # write dataframe to csv 
        csv_df.to_csv(with_landers_subfolder + csv_file.replace(with_videos_suffix, with_landers_suffix), index = False)

       
            