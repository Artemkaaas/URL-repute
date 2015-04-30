from URLRepute.source import URLSource
import sqlite3
import csv
import urllib
from zipfile import ZipFile

class AlexaSource(URLSource):
    name = 'Alex'
    def __init__(self):
        URLSource.__init__(self)
        list = self.cursor.execute('SELECT site FROM {0} LIMIT 100;' .format(self.name))
        for li in list:
            n=str(li).find('u')
            n2=str(li).rfind(')')
            li=str(li)[n+2:n2-2]
            self.urls[li]=True
        self.connection.close()


    def update(self):
        URLSource.__init__(self)
        url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
        urllib.urlretrieve(url, "alex.zip")
        zfile = ZipFile('alex.zip', 'r')
        zfile.extractall()
        self.cursor.execute("""Delete from Alex ;""")
        self.connection.commit()
        for row in zfile.open('top-1m.csv'):
            n=str(row).find(',')
            row=str(row)[n+1:]
            self.cursor.execute("""insert into Alex (site) values ("{0}");""".format(row))
        self.connection.commit()
        self.connection.close()
