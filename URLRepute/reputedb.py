from URLRepute.sources.alexa import AlexaSource
from URLRepute.sources.openphish import OpenPhishSource
from URLRepute.sources.phishtank import PhishtankSource

class URLReputeDB(object):
    def __init__(self):
        self.sources = []
        self.sources.append(AlexaSource())
        self.sources.append(OpenPhishSource())
        self.sources.append(PhishtankSource())

    def get_repute(self, url):
        found_in = []
        for source in self.sources:
            if source.check_url(url):
                found_in.append(source.name)
        return found_in
