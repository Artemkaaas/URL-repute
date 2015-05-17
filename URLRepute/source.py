import re
import motor

class URLSource(object):
    name = 'generic'
    def __init__(self):
        self.client=motor.MotorClient('localhost',27017)
        self.urls=dict()
        self.hist_urls=dict()

    def check_in_history(self,url):
        dif_urls=self.dif_url(url)
        self.v=[]
        for dif_ur in dif_urls:
            try:
                self.hist_urls[dif_ur]
                self.v.append(self.hist_urls[dif_ur])
            except:
                pass
        return self.v

    def check_url(self, url):
        dif_urls=self.dif_url(url)
        for dif_ur in dif_urls:
            try:
                self.urls[dif_ur]
                return True
            except:
                pass

    def slice_http(self,url):
        n=url.find('/')+1
        url=url[n+1:]
        return url

    #get different variants url
    def dif_url(self,url):
        dif_urls=[]
        reip = re.compile('[\d+\.]{4}')
        rettp = re.compile('^ttp')
        rehttp = re.compile('^http')
        if not rehttp.findall(url) and not rettp.findall(url):
            url='http://'+url
        if rettp.findall(url):
            type=3
        elif reip.findall(url):
            type=2
        else :
            type=1
        url=self.slice_http(url)
        if type==2:
            dif_urls.append(url)
            reip = re.compile('^[\d+\.]{4}$')
            while not reip.findall(url):
                try:
                    n=url.rindex('?param')
                except ValueError:
                    try:
                        n=url.rindex('/')
                    except ValueError:
                        break
                url=url[:n]
                dif_urls.append(url)
        if type==3:
            regx = re.compile('^\w+\.[a-z]+$')
            n=url.rfind('/')
            url3=url[:n]
            dif_urls.append(url)
            dif_urls.append(url3)
            while (not regx.findall(url3) and not regx.findall(url)) :
                n=url.find('.')+1
                url=url[n:]
                url3=url3[n:]
                dif_urls.append(url)
                dif_urls.append(url3)
        if type==1:
            regx = re.compile('^\w+\.[a-z]+$')
            url2=url
            try:
                n2=url.index('.')+1
            except:
                return dif_urls
            url2=url2[n2:]
            dif_urls.append(url)
            dif_urls.append(url2)
            while (not regx.findall(url) and not regx.findall(url2)) :
                try:
                    n=url.rindex('?param')
                except :
                    n=url.rfind('/')
                url=url[:n]
                dif_urls.append(url)
                try:
                    n2=url2.rindex('?param')
                except :
                    n2=url2.rfind('/')
                url2=url2[:n2]
                dif_urls.append(url2)

        return dif_urls
