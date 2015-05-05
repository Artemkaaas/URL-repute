from pymongo import *
import time
import sqlite3
import csv
import urllib
from zipfile import ZipFile
client=MongoClient('localhost',27017)
db=client.drop_database('OpenPhish')



def slice_http(url):
    n=url.find('/')+1
    url=url[n+1:]
    return url

db = client.OpenPhish

url = 'https://www.openphish.com/feed.txt'
urllib.urlretrieve(url, "feed.txt")
for row in open('feed.txt','r'):
    row=slice_http(row)
    db.OpenPhish.insert({'site':row})


client.close()
