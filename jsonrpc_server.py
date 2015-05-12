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

class URLReputeHandler(JSONRPCHandler):
    repute_db = URLReputeDB()
    repute_db.initialize()

    def get(self):
        self.render("index.html", messages=[])

    def get_url_repute(self, url):
        logging.info("got message %r", url)
        found_in = self.repute_db.get_repute(url)
        return found_in


class SocketHandler(tornado.websocket.WebSocketHandler):

    repute_db = URLReputeDB()
    repute_db.initialize()
    waiters = set()

    def open(self):
        SocketHandler.waiters.add(self)

    def on_close(self):
        SocketHandler.waiters.remove(self)

    @classmethod
    def send_result(cls, chat):
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, url):
        parsed = tornado.escape.json_decode(url)
        url=parsed['body']
        found_in = self.repute_db.get_repute(url)
        result={
            "id": str(uuid.uuid4()),
            "result": str(found_in),
            "url":str(url)
            }
        result["html"] = tornado.escape.to_basestring(self.render_string("message.html", message=result))
        SocketHandler.send_result(result)

def update_history():
    client=MongoClient('localhost',27017)
    time0 = timedelta(days=7)
    time0=time0.total_seconds()
    db = client.HistoryURL
    db1 = client.OpenPhish
    for post1 in db1.OpenPhish.find({ }, { 'site': 1, '_id': 0}).limit(10):
        post = post1.values()
        db.HistoryURL.insert({u'from':u'OpenPhish',u'site':post,u'date':datetime.datetime.now()})

    db1 = client.Alex
    for post1 in db1.Alex.find({ }, { 'site': 1, '_id': 0}).limit(10):
        post = post1.values()
        db.HistoryURL.insert({u'from':u'Alex',u'site':post,u'date':datetime.datetime.now()})

    db1 = client.Phishtank
    for post1 in db1.Phishtank.find({ }, { 'site': 1, '_id': 0}).limit(10):
        post = post1.values()
        db.HistoryURL.insert({u'from':u'Phishtank',u'site':post,u'date':datetime.datetime.now()})

    db.HistoryURL.remove({'date':{ "$lt": datetime.datetime.fromtimestamp(time.time()-time0)}})
    client.close()


#update database
def update():
    Alexa=AlexaSource()
    Alexa.update()
    OpenPhish=()
    OpenPhish.update()
    Phishtank=()
    Phishtank.update()
    update_history()


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
            (r"/urlsocket", SocketHandler),

        ],
cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
template_path=os.path.join(os.path.dirname(__file__),"templates"),
static_path=os.path.join(os.path.dirname(__file__),"static"),
debug=True,
xsrf_cookies=True,

        )
app.listen(8881)
tornado.ioloop.PeriodicCallback(update, int(get_day_update())*60*60*24*100).start()
tornado.ioloop.IOLoop.instance().start()
