from URLRepute.sources.alexa import AlexaSource
from URLRepute.sources.openphish import OpenPhishSource
from URLRepute.sources.phishtank import PhishtankSource
from tornado import gen

class URLReputeDB(object):
    def __init__(self):
        self.sources=[]

    @gen.coroutine
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

    def get_repute(self, url):
        found_in = []
        for source in self.sources:
            if source.check_url(url):
                found_in.append(source.name)
        return found_in
