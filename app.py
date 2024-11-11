from bs4 import BeautifulSoup
from selenium import webdriver
import json
import pandas as pd
import sqlite3


#using selenium
#can change the link for more dynamica
#all = https://www.mudah.my/malaysia/all?q=nvx
# state = https://www.mudah.my/kelantan/all?q=nvx
# nextlink = https://www.mudah.my/malaysia/motorcycles-for-sale?o=2&q=nvx done
website_url = "https://www.mudah.my/malaysia/motorcycles-for-sale?q=nvx"

dr = webdriver.Chrome()
dr.get(website_url)

mudah_soup = BeautifulSoup(dr.page_source, 'html.parser')
json_data =mudah_soup.find_all("script", type="application/ld+json")
link_script_data = json.loads(json_data[0].get_text())

items_data= link_script_data[2]['itemListElement']

#create empty list for prices, name
prices=[]
names=[]
items_cond = []
images = []
urls = []

#testing 1
# print(link_script_data[2]['itemListElement'][0]['item']['offers']['price'])

#looping every item
for item in items_data:
    price = int(item['item']['offers']['price'])
    name = item['item']['name']
    item_cond = item['item']['itemCondition']
    image = item['item']['image']
    url = item['item']['url']
    prices.append(price)
    names.append(name)
    items_cond.append(item_cond)
    images.append(image)
    urls.append(url)

#create dataframe
df = pd.DataFrame({"name":names,"price":prices, "item_cond":items_cond, "image":images, "url":urls })

#sort data might do more sorting
df_sorted = df.sort_values(by=['price'])
df_sorted = df_sorted.reset_index(drop=True)

#create database
conn = sqlite3.connect('nvx.db')
df_sorted.to_sql('list_of_nvx', conn, if_exists='replace')
