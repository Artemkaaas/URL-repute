from tornadorpc.json import JSONRPCHandler
from URLRepute.reputedb import URLReputeDB
from URLRepute.sources.alexa import AlexaSource
from URLRepute.sources.openphish import OpenPhishSource
from URLRepute.sources.phishtank import PhishtankSource
import tornado.options
import tornado


class URLReputeHandler(JSONRPCHandler):
    repute_db = URLReputeDB()
    repute_db.initialize()

    def get_url_repute(self, url):
        found_in = self.repute_db.get_repute(url)
        return found_in

#update database
def update():
    AlexaSource.update()
    OpenPhishSource.update()
    PhishtankSource.update()

def get_day_update():
    f=open('config.txt','r')
    times=f.readline()
    n=times.index(':')
    day=int(times[n+1:])
    f.close()
    return day

print 'Starting server...'
tornado.options.parse_command_line()
app = tornado.web.Application(
        [
            (r"/", URLReputeHandler),
            ],
        )
app.listen(8881)
tornado.ioloop.PeriodicCallback(update, int(get_day_update())*60*60*24*100).start()
tornado.ioloop.IOLoop.instance().start()
