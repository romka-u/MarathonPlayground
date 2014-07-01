from wsgiref.simple_server import make_server
import handlers
from handlers import *


def application(environ, start_response):
    route = environ['PATH_INFO']

    if route.startswith('/static'):
        route = route[1:]
        filelike = open(route, "rb")
        block_size = 1024
        start_response('200 OK',[('Content-Type', 'image/gif')])
        if 'wsgi.file_wrapper' in environ:
            gen = environ['wsgi.file_wrapper'](filelike, block_size)
        else:
            gen = iter(lambda: filelike.read(block_size), '')
        for x in gen:
            yield x
    else:
        start_response('200 OK', [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*')])

        handler = MainPage
        if route == '/submissions':
            handler = SubmissionsPage
        if route == '/config':
            handler = ConfigPage
        if route == '/rejudge':
            handler = RejudgePage
        if route == '/download':
            handler = DownloadPage
        if route == '/compare':
            handler = ComparePage

        for item in handler(environ):
            yield item


make_server('localhost', 8051, application).serve_forever()
