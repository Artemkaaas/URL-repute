from URLRepute.source import URLSource
from tornado import gen
class HistorySource(URLSource):
    name = 'History'
    @gen.coroutine
    def get_site(self):
        URLSource.__init__(self)
        db = self.client.HistoryURL
        cursor =db.HistoryURL.find({ }, {'_id': 0})
        while (yield cursor.fetch_next):
            li = cursor.next_object().values()
            date=li[0]
            site=li[1]
            from_site=li[2][0]
            self.hist_urls[site]=(date,from_site)
        self.client.close()
