from tornado import gen
import json
import imp
import os
from URLRepute.sources.History import HistorySource

class URLReputeDB(object):
    def __init__(self):
        self.sources=[]

    def update(self):
        raise NotImplementedError("You should define update method in every URLSource subclass")

    def initialize(self):
        with open("config.json") as json_file:
            json_data = json.load(json_file)
        source=[]
        handler=[]
        name=[]
        for j_d in json_data["sources"]:
            source.append(j_d['source'])
            handler.append(j_d['handler'])
            name.append(j_d['name'])

        for i in range(len(name)):
            tree = os.walk(os.getcwd())
            for t in tree:
                try:
                    f,filename,description =imp.find_module(name[i],[t[0]])
                    package = imp.load_module(name[i], f, filename, description)
                    c= getattr(package,str(handler[i]))
                    c=c()
                    gen.Task(c.get_site)
                    self.sources.append(c)
                except:pass
        History=HistorySource()
        gen.Task(History.get_site)


    def get_repute(self, url):
        self.found_in=[]
        for source in self.sources:
            if source.check_url(url):
                self.found_in.append(source.name)
        if not self.found_in:
            self.found_in=source.check_in_history(url)
        return self.found_in
