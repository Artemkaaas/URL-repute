from URLRepute.sources.alexa import AlexaSource
from URLRepute.sources.openphish import OpenPhishSource
from URLRepute.sources.phishtank import PhishtankSource
import motor
from tornado import gen
from tornado.web import asynchronous
class URLReputeDB(object):
    @asynchronous
    @gen.coroutine
    def __init__(self):
        self.sources = []
        c=yield gen.Task(OpenPhishSource().gets)
        self.sources.append(c)
        #self.sources.append(AlexaSource())
        #self.sources.append(PhishtankSource())


    def get_repute(self, url):
        found_in = []
        for source in self.sources:
            if source.check_url(url):
                found_in.append(source.name)
        return found_in
