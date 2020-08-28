import csv, os, shutil
from csv import reader
from os import listdir, getcwd, path, makedirs, remove, rename, system
import time
import requests
from requests import get, post
from requests.auth import HTTPBasicAuth

PATH = os.path.dirname(os.path.realpath(__file__))
CLOUD_URL = 'https://video.responderbot.net'
CLOUD_AUTH = HTTPBasicAuth('ingbojigjvdjaz', 'qoECku1Ab13Y8F')

project_id = '2'
files_endpoint = f'/projects/{project_id}/files/'
clips_endpoint = f'/projects/{project_id}/clips/'
exports_endpoint = f'/projects/{project_id}/exports/'
project_url = f'https://video.responderbot.net/projects/{project_id}/'

# TODO DEV input bypassed
# system('clear')
# niche = input("Enter the niche: ")
niche = 'dui'
screenshots_subfolder = niche + '/screenshots/'
with_screenshots_subfolder = niche + '/csv_files/with_screenshots/'
with_videos_subfolder = niche + '/csv_files/with_videos/'
base_url = 'https://www.yelp.com'


##########################################################
for x in range(424, 600):
    endpoint = f'https://video.responderbot.net/exports/{x}'
    print(endpoint) 

    # Delete current bdp screenshot clip AND file    FILE ONLY NECESSARY                
    try:      
        r = requests.delete(url=endpoint, auth=CLOUD_AUTH)
        print(f'Deleted: {endpoint}')
    except Exception as e:
        print(e)

                    

                  



