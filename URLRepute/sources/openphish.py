from URLRepute.source import URLSource
import sqlite3
import urllib

class OpenPhishSource(URLSource):
    name = 'OpenPhish'
    def __init__(self):
        URLSource.__init__(self)
        list = self.cursor.execute('SELECT site FROM {0}  Limit 100;' .format(self.name))
        for li in list:
            n=str(li).find('u')
            n2=str(li).rfind(')')
            li=str(li)[n+2:n2-4]
            self.urls[li]=True
        self.connection.close()


    def update(self):
        URLSource.__init__(self)
        url = 'https://www.openphish.com/feed.txt'
        urllib.urlretrieve(url, "feed.txt")
        self.cursor.execute("""Delete from OpenPhish ;""")
        self.connection.commit()
        for row in open('feed.txt','r'):
            row=self.slice_http(row)
            self.cursor.execute("""insert into OpenPhish (site) values ("{0}");""".format(row))
        self.connection.commit()
        self.connection.close()



