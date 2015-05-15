from tornado import gen
import json
import imp
import os
import motor
class URLReputeDB(object):
    def __init__(self):
        self.sources=[]

    def update(self):
        raise NotImplementedError("You should define update method in every URLSource subclass")

    def initialize(self):
        with open("config.json") as json_file:
            json_data = json.load(json_file)
        source_from=json_data["sources"]
        for s_f in source_from:
            tree = os.walk(os.getcwd())
            for t in tree:
                try:
                    f,filename,description =imp.find_module(s_f,[t[0]])
                    package = imp.load_module(s_f, f, filename, description)
                    if s_f=='Alexa':
                        Alex=package.AlexaSource()
                        gen.Task(Alex.get_site)
                        self.sources.append(Alex)
                    if s_f=='Phishtank':
                        Phishtank=package.PhishtankSource()
                        gen.Task(Phishtank.get_site)
                        self.sources.append(Phishtank)
                    if s_f=='OpenPhish':
                        OpenPhish=package.OpenPhishSource()
                        gen.Task(OpenPhish.get_site)
                        self.sources.append(OpenPhish)
                except:pass



    @gen.coroutine
    def check_in_history(self,url):
        client=motor.MotorClient('localhost',27017)
        db = client.HistoryURL
        cursor =db.HistoryURL.find({ }, {'_id': 0}).limit(5)
        while (yield cursor.fetch_next):
            c = cursor.next_object().values()
            date=c[0]
            name=c[1]
            site=c[2]
            if site[0].strip()==url:
                self.found_in.append(name)
                self.found_in.append(date)
        client.close()


    def get_repute(self, url):
        self.found_in=[]
        for source in self.sources:
            if source.check_url(url):
                self.found_in.append(source.name)
        if not self.found_in:
            gen.Task(self.check_in_history(url))
        return self.found_in

