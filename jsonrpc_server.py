from tornadorpc.json import JSONRPCHandler
from URLRepute.reputedb import URLReputeDB
from URLRepute.sources.alexa import AlexaSource
from URLRepute.sources.openphish import OpenPhishSource
from URLRepute.sources.phishtank import PhishtankSource
import tornado.options
import tornado
import os.path
import logging
import uuid
import tornado.websocket
import tornado.web
from pymongo import *
from datetime import datetime, timedelta
import time
import motor
from tornado import gen

class URLReputeHandler(JSONRPCHandler):
    repute_db = URLReputeDB()
    repute_db.initialize()

    def get(self):
        self.render("index.html", messages={"result": '',"url":''})

    def get_url_repute(self, url):
        logging.info("got message %r", url)
        found_in = self.repute_db.get_repute(url)
        return found_in

    @gen.coroutine
    def update_history(self):
        client=motor.MotorClient('localhost',27017)
        sources=URLReputeDB.sources
        time0 = timedelta(days=7)
        time0=time0.total_seconds()
        db = client.HistoryURL
        for source in sources:
            db1 = client[source.name]
            cursor =db1.find({ }, { 'site': 1, '_id': 0}).limit(10)
            while (yield cursor.fetch_next):
                post = cursor.next_object().values()
                future=db.HistoryURL.insert({u'from':source.name,u'site':post,u'date':datetime.datetime.now()})
                result=yield future

        result = yield db.HistoryURL.remove({'date':{ "$lt": datetime.datetime.fromtimestamp(time.time()-time0)}})
        client.close()

    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "body": self.get_argument("body"),
        }
        url=message['body']
        found_in = URLReputeHandler.repute_db.get_repute(url)
        result={
            "id": str(uuid.uuid4()),
            "result": str(found_in),
            "url":str(url)
            }
        self.render("index.html", messages=result)

#update database
def update():
    Alexa=AlexaSource()
    Alexa.update()
    OpenPhish=()
    OpenPhish.update()
    Phishtank=()
    Phishtank.update()
    URLReputeHandler.update_history


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
            (r"/a/url/new", URLReputeHandler),

        ],
cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
template_path=os.path.join(os.path.dirname(__file__),"templates"),
static_path=os.path.join(os.path.dirname(__file__),"static"),
debug=True,

        )
app.listen(8881)
tornado.ioloop.PeriodicCallback(update, int(get_day_update())*60*60*24*100).start()
tornado.ioloop.IOLoop.instance().start()
