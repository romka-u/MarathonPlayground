
from rejudge_tmpl import page
from navigation_tmpl import top

from judge import run_judging
from cgi import parse_qs

def RejudgePage(env):
    d = parse_qs(env['QUERY_STRING'])
    
    message = ""
    if 'src' in d:
        fn = d['src'][0]
        try:
            message = run_judging(fn)
        except:
            print "Unable to rejudge " + fn
            message = "Judging failed."

    return top + page.format(message=message)