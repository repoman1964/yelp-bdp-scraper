# filter out non email rows

import csv, os, shutil, sys, requests
from csv import reader, writer
from os import listdir, getcwd, path, makedirs, remove, rename, system

import pandas as pd



# TODO DEV input bypassed
# system('clear')
# niche = input("Enter the niche: ")

niche = 'dui'
with_emails_subfolder = niche + '/csv_files/with_emails/'
with_responders_subfolder = niche + '/csv_files/with_responders/'
with_responders_greater_10_subfolder = niche + '/csv_files/with_responders_greater_10/'
has_responders = False

with_emails_suffix = '_with_emails.csv'
with_responders_suffix = '_with_responders.csv'
with_responders_greater_10_suffix = '_with_responders_greater_10.csv'


# create 'csv_files/with_responders' subfolder if not exists
if not path.exists(with_responders_subfolder):
    makedirs(with_responders_subfolder)

# create 'csv_files/with_responders > 10' subfolder if not exists
if not path.exists(with_responders_greater_10_subfolder):
    makedirs(with_responders_greater_10_subfolder)

# grab csv from 'with_emails' subfolder
csv_with_emails_list = listdir(with_emails_subfolder)

for csv_file in csv_with_emails_list:
    csv_df = pd.read_csv(with_emails_subfolder + csv_file)    

    csv_df.drop(csv_df[csv_df['response_time'] == 'no_data'].index, inplace = True)    
    if len(csv_df) > 0:
        csv_df.to_csv(with_responders_subfolder + csv_file.replace(with_emails_suffix, with_responders_suffix), index = False) 

        # request leaders and count
        csv_df = pd.read_csv(with_responders_subfolder + csv_file.replace(with_emails_suffix, with_responders_suffix))
        length = len(csv_df)
        csv_df1=csv_df[['business_name','recent_local_requests']][csv_df.recent_local_requests == csv_df['recent_local_requests'].max()]

        try:
            result_set = csv_df1.values[0]
            request_leader = result_set[0]
            request_leader_count = result_set[1]
        except IndexError:
            print('Array is empty or does not exist')
            request_leader = request_leader_count = 0


    # if (n)rows > 1 get requests_leader and requests_leader_count
    if len(csv_df) > 1 and request_leader_count != 0:
        csv_df['request_leader'] = request_leader
        csv_df['request_leader_count'] = request_leader_count
        csv_df.to_csv(with_responders_subfolder + csv_file.replace(with_emails_suffix, with_responders_suffix), index = False)        

# making responders > 10 min csvs
# grab csv from 'with_responders' subfolder
csv_with_responsers_list = listdir(with_responders_subfolder)

for csv_file in csv_with_responsers_list:
    csv_df = pd.read_csv(with_responders_subfolder + csv_file)
    csv_df.drop(csv_df[csv_df['response_time'] == 'no_data'].index, inplace = True)
    csv_df.drop(csv_df[csv_df['response_time'] == 10].index, inplace = True)
    csv_df.to_csv(with_responders_greater_10_subfolder + csv_file.replace(with_responders_suffix, with_responders_greater_10_suffix), index = False) 


    


  