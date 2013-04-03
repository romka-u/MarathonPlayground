from wsgiref.simple_server import make_server
from handlers import *


def application(environ, start_response):
    # use cgi module to read data
    start_response('200 OK', [('Content-type','text/html')])

    route = environ['PATH_INFO']
    handler = MainPage
    if route == '/submissions':
        handler = SubmissionsPage
    if route == '/config':
        handler = ConfigPage
    if route == '/rejudge':
        handler = RejudgePage

    for item in handler(environ):
        yield item

make_server('localhost', 8051, application).serve_forever()
