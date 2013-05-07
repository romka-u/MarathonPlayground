import cgi
from os.path import join

def DownloadPage(env):
    d = cgi.parse_qs(env['QUERY_STRING'])

    filename = d['file'][0]
    print filename

    yield "<pre>"
    for line in open(join('submissions', filename), "r"):
        yield line.replace("<", "&lt;").replace(">", "&gt;")
    yield "</pre>"
