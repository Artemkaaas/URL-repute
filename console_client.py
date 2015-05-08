import os
import sys
import argparse
from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient
import tornado.escape
import uuid
from tornado.concurrent import return_future
import functools
from tornado.stack_context import ExceptionStackContext
import traceback

class WorkPool(object):
    def __init__(self, inp,async_client,  io_loop=None, pool_size=10):
        self.file = open(inp, 'r')
        self.io_loop = io_loop or ioloop.IOLoop.instance()
        self.active_count = 0
        self.size = pool_size
        self.async_client=async_client


    def _handle_response(self, url,response):
        result=tornado.escape.json_decode(response.body)
        print (u"%(url)s, %(source)s" % {"url": url, "source": result['result']})
        self.active_count = self.active_count - 1
        if not self._add_to_pool() and self.active_count == 0: # work is done
            self.final_callback(None)

    def _handle_error(self, url, typ, value, tb):
        print("u%(url)s,  ERROR" % {"url": url})
        sys.stderr.write("Unhandled error in Fetching\n")
        traceback.print_exception(typ, value, tb)
        self.active_count = self.active_count - 1
        if not self._add_to_pool() and self.active_count == 0: # work is done
            self.final_callback(None)
        return True

    def resolve(self,domain,method='get_url_repute'):
        data={
            "method":method,
            "id":unicode(uuid.uuid4()),
            "jsonrpc":"2.0",
            "params":[domain]
        }
        request=tornado.escape.json_encode(data)
        result_cb = functools.partial(self._handle_response, domain)
        self.async_client.fetch('http://localhost:8881', method="POST", body=request,callback=result_cb)

    def _add_to_pool(self):
        url = None
        line = self.file.readline()
        if line == '':
            return False
        url = line.strip()
        with ExceptionStackContext(functools.partial(self._handle_error, url)):
            self.resolve(url)

        self.active_count = self.active_count + 1
        return True

    @return_future
    def run(self, callback):
        self.final_callback = callback
        # Create initial pool
        while self.active_count < self.size:
            if not self._add_to_pool():
                break
        #Empty list
        if self.active_count == 0:
            self.final_callback(None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input: list of urls")
    parser.add_argument("--pool-size", help="max count of urls that can be resolved simultaneously",
                        type=int, default=10)
    args = parser.parse_args()
    AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")
    io_loop = ioloop.IOLoop.instance()
    async_client = AsyncHTTPClient()
    pool = WorkPool(args.input, async_client,io_loop=io_loop, pool_size=args.pool_size)
    io_loop.run_sync(pool.run)

if __name__ == "__main__":
    main()