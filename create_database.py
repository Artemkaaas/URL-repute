import csv
import urllib
from zipfile import ZipFile
import sys
import sqlite3

def slice_http(url):
    n=url.find('/')+1
    url=url[n+1:]
    return url

dbPath = 'sites.db'
connection = sqlite3.connect(dbPath)
cursor = connection.cursor()
url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
urllib.urlretrieve(url, "alex.zip")
zfile = ZipFile('alex.zip', 'r')
zfile.extractall()
connection.commit()
for row in zfile.open('top-1m.csv'):
    n=str(row).find(',')
    row=str(row)[n+1:]
    cursor.execute("""insert into Alex (site) values ("{0}");""".format(row))
connection.commit()


url = 'https://www.openphish.com/feed.txt'
urllib.urlretrieve(url, "feed.txt")
connection.commit()
for row in open('feed.txt','r'):
    row=slice_http(row)
    cursor.execute("""insert into OpenPhish (site) values ("{0}");""".format(row))
connection.commit()


url = 'http://data.phishtank.com/data/online-valid.csv'
urllib.urlretrieve(url, "phishtank.csv")
cursor.execute("""Delete from Phishtank ;""")
connection.commit()
csv_iter =  csv.reader(file('phishtank.csv'))
next(csv_iter)
for row in csv_iter:
    row=slice_http(row[1])
    cursor.execute("""insert into Phishtank (site) values ("{0}");""".format(row))
connection.commit()
connection.close()
