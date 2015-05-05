from tornadorpc.json import JSONRPCHandler
from tornadorpc import private, start_server
from URLRepute.reputedb import URLReputeDB
import time
from URLRepute.sources.alexa import AlexaSource
from URLRepute.sources.openphish import OpenPhishSource
from URLRepute.sources.phishtank import PhishtankSource

from tornado import gen

class URLReputeHandler(JSONRPCHandler):
    def get_url_repute(self, url):
        repute_db = URLReputeDB()
        found_in = repute_db.get_repute(url)
        return found_in

print 'Starting server...'
start_server(URLReputeHandler, port=8188)


#update database
while True:
    f=open('config.txt','r')
    times=f.readline()
    n=times.index(':')
    day=int(times[n+1:])
    f.close()
    time.sleep(day*24*60*60)
    AlexaSource.update()
    OpenPhishSource.update()
    PhishtankSource.update()
