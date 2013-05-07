import tempfile, cgi, os

from submission_tmpl import page
from navigation_tmpl import top
from datetime import datetime
from judge import run_judging
from collections import defaultdict

def td(s, attr=""):
    head = "<td %s>" % attr
    return head + "%s</td>" % s

def score_cell(score, best, is_TL, attr=""):
    head = "<td align=right %s>" % attr
    tail = "</td>"
    # tl_string = "<font color=\"red\" face=verdana size=2 style='font-weight: bold'>TL</font>" if is_TL else ""
    # body = "<font size=2>%.5f</font>%s<br><font size=4>%.4f</font>" % (tl_string, score)
    body = "<font size=4>%.4f</font>" % (score)

    return head + body + tail

def tr(s):
    return "<tr>%s</tr>" % s

def parse_logs(submissions_list, seeds):
    scores = defaultdict(int)
    times = defaultdict(str)
    info = defaultdict(str)

    for file in submissions_list:
        for seed in seeds:
            key = (file, seed)
            try:
                found = False
                for line in open("logs/{}_seed_{}.log".format(*key), "r"):
                    if line.startswith("Score"):
                        scores[key] = float(line.split()[-1])
                        found = True
                    if line.startswith("real"):
                        times[key] = line.split()[-1]
                    if line.startswith("!"):
                        info[key] += "\n" + line.strip()[2:]
                if not found:
                    scores[key] = "???"
                    times[key] = "N/A"
            except:
                pass

    return scores, times, info

def calc_max_for_seeds(scores, submissions_list, seeds):
    max_for_seeds = defaultdict(lambda: -10)
    for seed in seeds:
        for file in submissions_list:
            key = (file, seed)
            if key in scores:
                if isinstance(scores[key], float):
                    max_for_seeds[seed] = max(max_for_seeds[seed], scores[key])

    return max_for_seeds


def get_submissions_table():
    yield "<table id='submissions' cellpadding=5 cellspacing=0 border=1>"

    seeds = [line.strip() for line in open("seeds.txt", "r") if line.strip()]
    seeds_headers = "".join("<th>%s</th>" % x for x in seeds)

    yield tr("<th>Rejudge</th><th>Delete</th><th>Timestamp</th><th>Filename</th><th>Comment</th>" + \
        "<th>Overall</th>" + seeds_headers)

    submissions_list = [file for file in os.listdir("submissions") if not file.endswith(".info")][::-1]

    scores, times, info = parse_logs(submissions_list, seeds)
    max_for_seeds = calc_max_for_seeds(scores, submissions_list, seeds)

    for file in submissions_list:
        tok = file.partition("_")
        dt = datetime.strptime(tok[0], "%Y%m%dT%H%M%S")
        try:
            comment = open(os.path.join("submissions", file + ".info"), "r").readline().strip()
        except:
            comment = ""
        yield "<tr><td><a href='/rejudge?src={}'>Rejudge</a></td><td><a href='/submissions?delete={}'>Delete</a></td><td>{}</td><td>{}</td><td style='font-style: italic;'>{}</td>".format(
            file, file, dt.strftime("%d.%m %H:%M:%S"), "<a href='/download?file={0}'>{1}</a>".format(file, tok[2]), comment)

        results_cells = ""
        file_res = []

        for seed in seeds:
            key = (file, seed)
            if key in scores:
                title_param = ""
                is_TL = False
                if key in times and times[key] != 'N/A':
                    title_param = "title='{0}' ".format(times[key] + info[key])
                    tm = map(float, times[key][:-1].split('m'))
                    if tm[0] * 60 + tm[1] > 10:
                        is_TL = True
              
                if isinstance(scores[key], basestring):
                    if scores[key] == "???":
                        results_cells += td("<img src='http://localhost:8051/static/ajax-loader.gif'/>", "align=center")
                    else:
                        results_cells += td(scores[key])
                else:
                    file_res.append(max(scores[key], 0))
                    coeff = scores[key] / max_for_seeds[seed]
                    if coeff <= 0.8:
                        bgcolor = "#dd0000"
                    else:
                        if coeff <= 0.9:
                            d = int((coeff - 0.8) * 2210)
                            bgcolor = "#dd{0}00".format(hex(d)[2:])
                        else:
                            if coeff >= 1.0 - 1e-6:
                                bgcolor = "#00ff00"
                            else:
                                d = int((1.0 - coeff) * 2210)
                                bgcolor = "#{0}dd00".format(hex(d)[2:])

                    results_cells += score_cell(scores[key], max_for_seeds[seed], is_TL, title_param + "bgcolor={0}".format(bgcolor))
            else:
                results_cells += td("---")

        if file_res:
            overall = sum(file_res) / len(file_res)
        else:
            overall = "N/A"

        yield td(overall, "bgcolor=#7EE") + results_cells

        yield "</tr>"

    yield "</table>"

def SubmissionsPage(env):
    
    length = env['CONTENT_LENGTH']
    if not length: length = 0
    else: length = int(length)

    d = cgi.parse_qs(env['QUERY_STRING'])
    if 'delete' in d:
        fn = d['delete'][0]
        try:
            os.remove(os.path.join("submissions", fn))
            os.remove(os.path.join("submissions", fn + ".info"))
        except:
            print "Unable to delete " + fn + "(.info)"

    if 'rejudge' in d:
        fn = d['rejudge'][0]
        try:
            run_judging(fn)
        except:
            print "Unable to rejudge " + fn

    temp_file = tempfile.TemporaryFile()
    contents = env['wsgi.input'].read(length)
    temp_file.write(contents) # or use buffered read()
    temp_file.seek(0)
    form = cgi.FieldStorage(fp=temp_file, environ=env, keep_blank_values=True)

    try:
        fileitem = form['file']
    except KeyError:
        fileitem = None

    if fileitem is not None and fileitem.file is not None:
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
        basename = os.path.basename(fileitem.filename)
        fn = os.path.join("submissions", timestamp + "_" + basename)
        message = ""
        with open(fn, 'wb') as f:
            data = fileitem.file.read(1024)
            while data:
                f.write(data)
                data = fileitem.file.read(1024)

            message = 'The file "' + basename + '" was uploaded successfully.'

        message += "<br>" + run_judging(timestamp + "_" + basename)

        with open(fn + ".info", "w") as f:
            print >>f, form['comment'].value

    else:
        message = 'Upload your solution here.'

    temp_file.close()

    yield top + page.format(message=message)

    for token in get_submissions_table():
        yield token
