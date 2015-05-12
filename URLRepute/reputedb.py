from URLRepute.sources.alexa import AlexaSource
from URLRepute.sources.openphish import OpenPhishSource
from URLRepute.sources.phishtank import PhishtankSource
from tornado import gen
from pymongo import *

class URLReputeDB(object):
    def __init__(self):
        self.sources=[]

    def initialize(self):
        OpenPhish=OpenPhishSource()
        gen.Task(OpenPhish.get_site)
        self.sources.append(OpenPhish)
        Alex=AlexaSource()
        gen.Task(Alex.get_site)
        self.sources.append(Alex)
        Phishtank=PhishtankSource()
        gen.Task(Phishtank.get_site)
        self.sources.append(Phishtank)

    def check_in_history(self,url):
        found=[]
        client=MongoClient('localhost',27017)
        db = client.HistoryURL
        for post1 in db.HistoryURL.find({ }, {'_id': 0}):
            c= post1.values()
            date=c[0]
            name=c[1]
            site=c[2]
            if site[0].strip()==url:
                found.append(name)
                found.append(date)
        client.close()
        return found

    def get_repute(self, url):
        found_in = []
        for source in self.sources:
            if source.check_url(url):
                found_in.append(source.name)
        if not found_in:
            found_in=self.check_in_history(url)
        return found_in

