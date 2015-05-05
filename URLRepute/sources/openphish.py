from URLRepute.source import URLSource
import pymongo
import urllib
import motor
from tornado import gen
from tornado.web import asynchronous
class OpenPhishSource(URLSource):
    name = 'OpenPhish'
    @gen.coroutine
    def get_site(self):
        URLSource.__init__(self)
        db = self.client.OpenPhish
        cursor =db.OpenPhish.find({ }, { 'site': 1, '_id': 0}).limit(10)
        while (yield cursor.fetch_next):
            li = cursor.next_object().values()
            n=str(li).find('u')
            n2=str(li).rfind(')')
            li=str(li)[n+2:n2-3]
            self.urls[li]=True
        self.client.close()




    def update(self):
        URLSource.__init__(self)
        db=self.client.drop_database('OpenPhish')
        db = self.client.OpenPhish
        url = 'https://www.openphish.com/feed.txt'
        urllib.urlretrieve(url, "feed.txt")
        for row in open('feed.txt','r'):
            row=self.slice_http(row)
            db.OpenPhish.insert({'site':row})



