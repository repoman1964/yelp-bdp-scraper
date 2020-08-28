# correct with_screenshots_csv


import csv, os, shutil, sys, requests
from csv import reader, writer
from os import listdir, getcwd, path, makedirs, remove, rename, system

import pandas as pd


niche = 'dui'
with_responders_subfolder = niche + '/csv_files/with_responders/'
with_screenshots_subfolder = niche + '/csv_files/with_screenshots/'

with_responders_suffix = '_with_responders.csv'
with_screenshots_suffix = '_with_screenshots.csv'

# grab csv from 'with_screenshots_subfolder' subfolder
csv_with_responders = listdir(with_responders_subfolder)

for csv_file in csv_with_responders:    
    df=pd.read_csv(with_responders_subfolder + csv_file)
    rows = range(len(df))
    for row in rows:
        bdp_screenshot = df.iloc[row].business_details_page.replace('/biz/', '') + '.png'
        df.at[row,'bdp_screenshot'] = bdp_screenshot
    df.to_csv(with_screenshots_subfolder + csv_file.replace(with_responders_suffix, with_screenshots_suffix), index = False)

    # for df_row in df.itertuples():
        # if df_row.bdp_screenshot == 'no_data' or df_row.bdp_screenshot == 'no data':
        #     bdp_screenshot = df_row.business_details_page.replace('/biz/', '') + '.png'
        #     df.update(bdp_screenshot) 
           

# # grab csv from 'with_screenshots_subfolder' subfolder
# csv_with_screenshots = listdir(with_screenshots_subfolder)

# for csv_file in csv_with_screenshots:    
#     df=pd.read_csv(with_screenshots_subfolder + csv_file)
#     for df_row in df.itertuples():
#         if df_row.bdp_screenshot == 'no_data': 
#             if df_row.bdp_screenshot == 'no data':
#                 print(csv_file)
#                 print(df_row.bdp_screenshot)
#                 print(';############################')
       
    