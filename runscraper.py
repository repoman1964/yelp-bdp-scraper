import pandas as pd
import os

# TODO DEV input bypassed
os.system('clear')
niche = input("Enter the niche: ")
niche_alias = input("Enter one word alias for the niche: ")
how_deep = int(input("How deep do you want to go baby? (default = 50): ") or "50")

niche_for_spider = niche.replace(' ', '%20')
niche_for_spider = niche_for_spider.replace('&', '%26')
niche_for_spider = niche_for_spider.title()


# get city list
csv_df = pd.read_csv('5000_US_Cities_By_Population.csv')

# rows = range(len(csv_df))
rows = range(how_deep)
for row in rows: 
    city = csv_df.iloc[row].city
    city_for_spider = city
    city_for_spider = city_for_spider.strip()
    city_for_spider = city_for_spider.replace(' ', '%20')
    city_for_spider = city_for_spider.title()

    city_for_file = city
    city_for_file = city_for_file.replace(' ', '_')

    state_for_spider = csv_df.iloc[row].state 
    state_for_spider = state_for_spider.upper()

    assmunch = f'scrapy crawl bdp_scraper -a FIND_DESC={niche_for_spider} -a FIND_LOC_CITY={city_for_spider} -a FIND_LOC_STATE={state_for_spider} -o {niche_alias}/csv_files/with_nothing/{niche_alias}_{city_for_file}_with_nothing.csv'   

    os.system(assmunch)