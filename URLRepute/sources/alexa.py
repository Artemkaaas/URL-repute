from URLRepute.source import URLSource
import csv
import urllib
from zipfile import ZipFile
from tornado import gen
import motor
class AlexaSource(URLSource):
    name = 'Alex'
    @gen.coroutine
    def get_site(self):
        URLSource.__init__(self)
        db = self.client.Alex
        cursor =db.Alex.find({ }, { 'site': 1, '_id': 0}).limit(10)
        while (yield cursor.fetch_next):
            li = cursor.next_object().values()
            n=str(li).find('u')
            n2=str(li).rfind(')')
            li=str(li)[n+2:n2-3]
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
            db.Alex.insert({'site':row}, callback=None)
