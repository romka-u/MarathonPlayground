import tempfile, cgi, os

from submission_tmpl import page
from navigation_tmpl import top
from datetime import datetime
from judge import run_judging
from collections import defaultdict

def td(s, attr=""):
    head = "<td %s>" % attr
    return head + "%s</td>" % s

def score_cell(score, best, attr=""):
    head = "<td align=right %s>" % attr
    tail = "</td>"
    body = "<font size=2>%.5f</font><br><font size=4>%.4f</font>" % (max(score, 0) / best, score)

    return head + body + tail

def tr(s):
    return "<tr>%s</tr>" % s

def get_scores(submissions_list, seeds):
    scores = defaultdict(int)

    for file in submissions_list:
        for seed in seeds:
            try:
                found = False
                for line in open("logs/%s_seed_%s.log" % (file, seed), "r"):
                    if line.startswith("Score"):
                        scores[(file, seed)] = float(line.split()[-1])
                        found = True
                if not found:
                    scores[(file, seed)] = "???"
            except:
                pass

    return scores

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
    table = "<table cellpadding=5 cellspacing=0 border=1>"

    seeds = [line.strip() for line in open("seeds.txt", "r") if line.strip()]
    seeds_headers = "".join("<th>%s</th>" % x for x in seeds)

    table += tr("<th>Rejudge</th><th>Delete</th><th>Timestamp</th><th>Filename</th><th>Comment</th>" + \
        "<th>Overall</th>" + seeds_headers)

    submissions_list = [file for file in os.listdir("submissions") if not file.endswith(".info")]

    scores = get_scores(submissions_list, seeds)
    max_for_seeds = calc_max_for_seeds(scores, submissions_list, seeds)

    for file in submissions_list:
        tok = file.partition("_")
        dt = datetime.strptime(tok[0], "%Y%m%dT%H%M%S")
        try:
            comment = open(os.path.join("submissions", file + ".info"), "r").readline().strip()
        except:
            comment = ""
        row = "<td><a href='/rejudge?src={}'>Rejudge</a></td><td><a href='/submissions?delete={}'>Delete</a></td><td>{}</td><td>{}</td><td style='font-style: italic;'>{}</td>".format(
            file, file, dt.strftime("%d.%m %H:%M:%S"), tok[2], comment)

        results_cells = ""
        file_res = []

        for seed in seeds:
            key = (file, seed)
            if key in scores:
                if isinstance(scores[key], basestring):
                    results_cells += td(scores[key], "bgcolor=gray" if scores[key] == "???" else "")
                else:
                    file_res.append(max(scores[key], 0))
                    if scores[key] > max_for_seeds[seed] - 1e-6:
                        results_cells += score_cell(scores[key], max_for_seeds[seed], "bgcolor=green;")
                    else:
                        results_cells += score_cell(scores[key], max_for_seeds[seed])
            else:
                results_cells += td("---")

        if file_res:
            overall = sum(file_res) / len(file_res)
        else:
            overall = "N/A"

        row += td(overall, "bgcolor=#7EE") + results_cells

        table += tr(row)

    table += "</table>"
    return table

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

    table = get_submissions_table();

    return top + page.format(message=message, table=table)
