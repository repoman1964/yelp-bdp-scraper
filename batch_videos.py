import csv, os, shutil
from csv import reader
from os import listdir, getcwd, path, makedirs, remove, rename, system
import pysftp
import requests
from requests import get, post
from requests.auth import HTTPBasicAuth
import time

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

##########################################################

# grab with_screenshots csv from niches folder
csv_with_screenshots = listdir(with_screenshots_subfolder)

for csv_file in csv_with_screenshots:
    city = csv_file.replace(niche + '_', '')
    city = city.replace('_with_screenshots.csv', '')
    city = city + '/'

    # sftp copy screenshot folder to server as thumbnail
    # <niche/city/png>

    payload_city = csv_file.replace(niche + '_', '')
    payload_city = payload_city.replace('_with_screenshots.csv', '')
    source = screenshots_subfolder + payload_city    

    with pysftp.Connection('138.68.255.55', username='root', private_key='/home/jose/.ssh/home_machine') as sftp:
        try:
            sftp.cwd('/var/www/html')
            if not sftp.isdir(niche + '/' + payload_city):           
                sftp.makedirs(niche + '/' + payload_city)
                sftp.cwd(niche)

                target_directory = os.path.join(PATH, niche, 'screenshots/', city)
                sftp.put_r(target_directory, payload_city, preserve_mtime=True)
        except Exception as e:
            print(e)
    
    # create 'csv_files/with_videso' subfolder if not exists
    if not path.exists(with_videos_subfolder):
        makedirs(with_videos_subfolder)

    # create 'with_video' output csv file if not exist ################################################
    csv_output_file_name = csv_file.split('_with')[0]
    csv_output_file_name = csv_output_file_name + '_with_videos.csv'  
    csv_output_file_name = with_videos_subfolder + csv_output_file_name

    # create csv if not exist
    if not path.isfile(csv_output_file_name):
        # create output file and write header. then close
        with open(csv_output_file_name, 'w') as csvfile:
            newfile = csv.writer(csvfile)      
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
                "cold_email_video_thumbnail_url"   
                ])
            # close file
            csvfile.close()


    # open source csv
    with open(with_screenshots_subfolder + csv_file, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            if row['bdp_screenshot']:
                
                # get screenshot path and file name
                screenshot_source_path = os.path.join(PATH, screenshots_subfolder, city, row['bdp_screenshot'])
                # screenshot_source_path = path.cwd().joinpath(screenshots_subfolder, city, row['bdp_screenshot'])

                ##########################################################
                # upload screenshot to project template (files_endpoint)
                
                screenshot_source_name = os.path.split(screenshot_source_path)[1]
                file_data = {
                    "media": None,
                    "project": project_url,
                    "json": "{}"
                }              

                try:                       
                    r = requests.post(CLOUD_URL + files_endpoint, data=file_data, files={"media": (screenshot_source_name, open(screenshot_source_path, "rb"))}, auth=CLOUD_AUTH)

                    # get result
                    file_url = r.json().get("url")
                    file_id = r.json().get("id")

                except Exception as e:
                    print(e)

                ##########################################################
                # assign screenshot file to a clip (clips_endpoint)
                clip_data = {
                    "file": file_url,
                    "position": 0.0,
                    "start": 0.0,                       
                    "end": 135.0,
                    "layer": 1,
                    "project": project_url,
                    "json": "{}"
                }

                try:
                    r = post(CLOUD_URL + clips_endpoint, data=clip_data, auth=CLOUD_AUTH)

                    # get clip id (for later delete)
                    clip_url = r.json().get("url")
                    clip_id = r.json().get("id")

                except Exception as e:
                    print(e)
              

                ##########################################################
                # create export for final rendered video (exports_endpoint)                    
                export_data = {
                    "video_format": "mp4",
                    "video_codec": "libx264",
                    "video_bitrate": 8000000,
                    "audio_codec": "libfdk_aac",
                    "audio_bitrate": 1920000,
                    "start_frame": 1,
                    "end_frame": None,
                    "project": project_url,                    
                    "json": "{}"
                }

                try:
                    r = post(CLOUD_URL + exports_endpoint, data=export_data, auth=CLOUD_AUTH)
                    export_url = r.json().get("url")
                    print(export_url)

                except Exception as e:
                    print(e)                  

                ##########################################################
                # wait for export to finish (5000 seconds max)
                export_output_url = None
                is_exported = False
                countdown = 500
                while not is_exported and countdown > 1:
                    r = get(export_url, auth=CLOUD_AUTH)
                    progress = float(r.json().get("progress", 0.0))
                    os.system('clear')
                    print(f'Rendering. Progress = {progress}%')
                    is_exported = float(r.json().get("progress", 0.0)) == 100.0
                    countdown -= 1
                    time.sleep(10)

                # get url rendered output
                r = get(export_url, auth=CLOUD_AUTH)
                export_output_url = r.json().get('output')


                # write to output csv
                with open(csv_output_file_name, 'a', newline='') as csvfile:
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

                        "cold_email_video_url"
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
                        'request_leader': row['request_leader_count'],

                        'yelp_advertiser': row['yelp_advertiser'],

                        'photo_count': row['photo_count'],
                        'star_count': row['star_count'],

                        'review_count': row['review_count'],
                        'reviews': row['reviews'],
                        'reviews_author': row['reviews_author'],
                        'hidden_review_count': row['hidden_review_count'],

                        'cold_email_video_url': export_output_url
                        })

                # Delete current bdp screenshot clip AND file    FILE ONLY NECESSARY                
                try:
                    # delete clip
                    # r = requests.delete(url=clip_url, auth=CLOUD_AUTH)
                    # delete file
                    r = requests.delete(url=file_url, auth=CLOUD_AUTH)
                    print(f'Export Completed. URL = {export_output_url}')
                except Exception as e:
                    print(e)

                    

                  



