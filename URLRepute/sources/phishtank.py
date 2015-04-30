from URLRepute.source import URLSource
import sqlite3
import csv
import urllib

class PhishtankSource(URLSource):
    name = 'Phishtank'
    def __init__(self):
        URLSource.__init__(self)
        list = self.cursor.execute('SELECT site FROM {0}  Limit 100;' .format(self.name))
        for li in list:
            n=str(li).find('u')
            n2=str(li).rfind(')')
            li=str(li)[n+2:n2-2]
            self.urls[li]=True
        self.connection.close()


    def update(self):
        URLSource.__init__(self)
        url = 'http://data.phishtank.com/data/online-valid.csv'
        urllib.urlretrieve(url, "phishtank.csv")
        self.cursor.execute("""Delete from Phishtank ;""")
        self.connection.commit()
        csv_iter =  csv.reader(file('phishtank.csv'))
        next(csv_iter)
        for row in csv_iter:
            row=self.slice_http(row[1])
            self.cursor.execute("""insert into Phishtank (site) values ("{0}");""".format(row))
        self.connection.commit()
        self.connection.close()
