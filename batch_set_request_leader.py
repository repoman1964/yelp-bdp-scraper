# filter out non email rows

import csv, os, shutil, sys, requests
from csv import reader, writer
from os import listdir, getcwd, path, makedirs, remove, rename, system

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

# grab data from csv
source_files = listdir('150s/')

for source_file in source_files:
    source_file = '150s/'+source_file

    df = pd.read_csv(source_file)
    scrape_city_series = df["scrape_city"]
    scrape_city_series = list(dict.fromkeys(scrape_city_series))

    scrape_city_series.sort()
    for scrape_city in scrape_city_series:
        scrape_city_subset = df.loc[df['scrape_city'] == scrape_city]

        request_leader_row = scrape_city_subset[scrape_city_subset.recent_local_requests == scrape_city_subset.recent_local_requests.max()]
       
        request_leader = request_leader_row.iloc[0]['business_name']
        request_leader_count = request_leader_row.iloc[0]['recent_local_requests']
    

        rows = range(len(df))
        for row in rows:
            target_city = df.iloc[row].scrape_city
            if df.iloc[row].scrape_city == scrape_city:
                target_business_name = df.iloc[row].business_name
                if df.at[row, 'business_name'] != request_leader:
                    df.at[row, 'request_leader'] = request_leader
                    df.at[row, 'request_leader_count'] = request_leader_count
               

       

    
    df.to_csv(source_file, index = False)   