from URLRepute.source import URLSource
import sqlite3
import csv
import urllib
from zipfile import ZipFile

class AlexaSource(URLSource):
    name = 'Alex'

    def __init__(self):
        URLSource.__init__(self)
        db = self.client.Alex
        cursor =db.Alex.find({ }, { 'site': 1, '_id': 0}).limit(40)
        for document in cursor:
            li=document.values()
            n=str(li).find('u')
            n2=str(li).rfind(')')
            li=str(li)[n+2:n2-2]
            self.urls[li]=True
        self.client.close()


    def update(self):
        URLSource.__init__(self)
        db=self.client.drop_database('Alex')
        db = self.client.Alex
        url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
        urllib.urlretrieve(url, "alex.zip")
        zfile = ZipFile('alex.zip', 'r')
        zfile.extractall()
        for row in zfile.open('top-1m.csv'):
            n=str(row).find(',')
            row=str(row)[n+1:]
            db.Alex.insert({'site':row})
