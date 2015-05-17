from tornadorpc.json import JSONRPCHandler
from URLRepute.reputedb import URLReputeDB
from URLRepute.sources.Alexa import AlexaSource
from URLRepute.sources.OpenPhish import OpenPhishSource
from URLRepute.sources.Phishtank import PhishtankSource
import tornado.options
import tornado
import os.path
import logging
import uuid
import tornado.websocket
import tornado.web
from datetime import datetime, timedelta
import time
import motor
from tornado import gen
import json
from concurrent.futures import ThreadPoolExecutor

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
    source=[]
    Alexa=AlexaSource()
    source.append(Alexa)
    OpenPhish=OpenPhishSource()
    source.append(OpenPhish)
    Phishtank=PhishtankSource()
    source.append(Phishtank)
    with ThreadPoolExecutor(max_workers=3) as executor:
        for sourc in source:
            executor.submit(gen.Task(sourc.update))
    URLReputeHandler.update_history()
    URLReputeHandler.repute_db.initialize()



def get_day_update():
    with open("config.json") as json_file:
        json_data = json.load(json_file)
    time=json_data["update frequency"]
    time=time[:-1]
    a=time[-1:]
    if a=='s':pass
    elif a=='m':time*=60
    elif a=='h':time*=60*60
    elif a=='d':time*=60*60*24
    elif a=='w':time*=60*60*24*7
    else:time=60*60*60*60
    return time

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


tornado.ioloop.PeriodicCallback(update, int(get_day_update())).start()
tornado.ioloop.IOLoop.instance().start()
