# filter out non email rows

import csv, os, shutil, sys, requests
from csv import reader, writer
from os import listdir, getcwd, path, makedirs, remove, rename, system

import pandas as pd


# TODO DEV input bypassed
# system('clear')
niche = input("Enter the niche: ")
# niche = 'dui'
with_nothing_subfolder = niche + '/csv_files/with_nothing/'
with_emails_subfolder = niche + '/csv_files/with_emails/'

with_nothing_suffix = '.csv'
with_emails_suffix = '_with_emails.csv'

# create 'csv_files/with_screenshots' subfolder if not exists
if not path.exists(with_emails_subfolder):
    makedirs(with_emails_subfolder)

# grab csv from 'niche' subfolder
csv_with_nothing_list = listdir(with_nothing_subfolder)

for csv_file in csv_with_nothing_list:
    csv_df = pd.read_csv(with_nothing_subfolder + csv_file)
    csv_df.drop(csv_df[csv_df['business_email'] == 'no data'].index, inplace = True)
    csv_df.drop(csv_df[csv_df['business_email'] == 'no_data'].index, inplace = True)
    csv_df.drop(csv_df[csv_df['business_email'] == 'xxx'].index, inplace = True)
    csv_df.drop(csv_df[csv_df['business_email'] == 'XXX'].index, inplace = True)

    csv_df.to_csv(with_emails_subfolder + csv_file.replace(with_nothing_suffix, with_emails_suffix), index = False)

    csv_df = pd.read_csv(with_emails_subfolder + csv_file.replace(with_nothing_suffix, with_emails_suffix))
    
    #  convert emails to lower case
    rows = range(len(csv_df))
    for row in rows:
        business_email = csv_df.iloc[row].business_email.lower()
        csv_df.at[row, 'business_email'] = business_email
        business_website = csv_df.iloc[row].business_website.lower()
        csv_df.at[row, 'business_website'] = business_website

    csv_df.to_csv(with_emails_subfolder + csv_file.replace(with_nothing_suffix, with_emails_suffix), index = False) 

  