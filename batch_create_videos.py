import csv, os, shutil
from csv import reader
from os import listdir, getcwd, path, makedirs, remove, rename, system
import pysftp
import requests
from requests import get, post
from requests.auth import HTTPBasicAuth
import time
import pandas as pd

PATH = os.path.dirname(os.path.realpath(__file__))
CLOUD_URL = 'https://video.responderbot.net'
CLOUD_AUTH = HTTPBasicAuth('ingbojigjvdjaz', 'qoECku1Ab13Y8F')

# video api endpoints
project_id = '5'
# TODO DEV input bypassed
# system('clear')
# niche = input("Enter the niche: ")
# niche = niche.lower()
# project_id = input("Enter the project id: ")
files_endpoint = f'/projects/{project_id}/files/'
clips_endpoint = f'/projects/{project_id}/clips/'
exports_endpoint = f'/projects/{project_id}/exports/'
project_url = f'https://video.responderbot.net/projects/{project_id}/'

niche = 'dui'
screenshots_subfolder = niche + '/screenshots/'
with_screenshots_subfolder = niche + '/csv_files/with_screenshots/'
with_videos_subfolder = niche + '/csv_files/with_videos/'

with_screenshots_suffix = '_with_screenshots.csv'
with_videos_suffix = '_with_videos.csv'

##########################################################



# functions##########################################################
# read csv into dataframe
def read_csv(csv_file, with_screenshots_subfolder):
    df = pd.read_csv(with_screenshots_subfolder + csv_file)
    return df


### MAIN #####################################################

# grab with_screenshots csv from niches folder
csv_with_screenshots = listdir(with_screenshots_subfolder)

for csv_file in csv_with_screenshots:
    os.system('clear')
    try:
        df = read_csv(csv_file, with_screenshots_subfolder)

    except pd.errors.EmptyDataError:
        print('Note: filename.csv was empty. Skipping.')
        continue # will skip the rest of the block and move to next file

    if not df.empty:
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

    # create 'csv_files/with_videos' subfolder if not exists
    if not path.exists(with_videos_subfolder):
        makedirs(with_videos_subfolder)

    
    ## wtf is this?
    # set csv output filename ################################################
    csv_output_file_name = csv_file.split('_with')[0]
    csv_output_file_name = csv_output_file_name + '_with_videos.csv'  
    csv_output_file_name = with_videos_subfolder + csv_output_file_name
    #################################################

    
    if not df.empty:
        rows = range(len(df))
        for row in rows:   # create video

            ##########################################################
            # upload screenshot to project template (files_endpoint)
            bdp_screenshot = df.iloc[row].bdp_screenshot   
                
            # get screenshot path and file name
            screenshot_source_path = os.path.join(PATH, screenshots_subfolder, city, bdp_screenshot)
            # screenshot_source_path = path.cwd().joinpath(screenshots_subfolder, city, row['bdp_screenshot'])

            file_data = {
                "media": None,
                "project": project_url,
                "json": "{}"
            }
         
            try:                       
                r = requests.post(CLOUD_URL + files_endpoint, data=file_data, files={"media": (bdp_screenshot, open(screenshot_source_path, "rb"))}, auth=CLOUD_AUTH)          

                # get result
                file_url = r.json().get("url")
                file_id = r.json().get("id")

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


            ##########################################################
            # assign screenshot file to a clip (clips_endpoint)
            clip_data = {
                "file": file_url,
                "position": 0.0,
                "start": 0.0,                       
                "end": 270.0,
                "layer": 1,
                "project": project_url,
                "json": "{}"
            }

            try:
                r = post(CLOUD_URL + clips_endpoint, data=clip_data, auth=CLOUD_AUTH)

                # get clip id (for later delete)
                clip_url = r.json().get("url")
                clip_id = r.json().get("id")

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

            ##########################################################
            # wait for export to finish (5000 seconds max) 
            # TODO webhhook to signal file complete 
            export_output_url = None
            is_exported = False
            countdown = 500
            while not is_exported and countdown > 1:
                try:

                r = get(export_url, auth=CLOUD_AUTH)

                progress = float(r.json().get("progress", 0.0))
                # os.system('clear')
                print(f'Rendering. Progress = {progress}%')
                is_exported = float(r.json().get("progress", 0.0)) == 100.0
                countdown -= 1
                time.sleep(10)

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

                

            # get url rendered output
            try:
            r = get(export_url, auth=CLOUD_AUTH)
            export_output_url = r.json().get('output')

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

            if export_output_url:

                # persist video url to dataframe   
                df.at[row, 'cold_email_video_url'] = export_output_url
                # write dataframe to csv 
                df.to_csv(with_videos_subfolder + csv_file.replace(with_screenshots_suffix, with_videos_suffix), index = False)

                # delete current bdp screenshot file                 
                try:           
                    # delete file
                    r = requests.delete(url=file_url, auth=CLOUD_AUTH)
                    print(f'Export Completed. URL = {export_output_url}')
                except requests.exceptions.HTTPError as errh:
                    print ("Http Error:", errh)
                    break
                except requests.exceptions.ConnectionError as errc:
                    print ("Error Connecting:", errc)
                    break
                except requests.exceptions.Timeout as errt:
                    print ("Timeout Error:", errt)
                    break
                except requests.exceptions.RequestException as err:
                    print ("Oops: Something Else", err)
                    break



                    

                  



