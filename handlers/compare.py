import cgi, os

from navigation_tmpl import top

def gen_compare_table(file1, file2, compress):
    conv = lambda x: x.replace('\t', ' ' * 4).replace('<', '&lt;').replace('>', '&gt;')

    a = open(os.path.join('submissions', file1), "r").readlines()
    a = map(conv, a)
    b = open(os.path.join('submissions', file2), "r").readlines()
    b = map(conv, b)

    n = len(a)
    m = len(b)

    row = [0] * m
    f = []
    for i in xrange(n):
        f.append(list(row))

    for i in xrange(n):
        for j in xrange(m):
            if i == 0 or j == 0:
                f[i][j] = 1 if a[i].strip() == b[j].strip() else 0
            else:
                f[i][j] = max(f[i-1][j], f[i][j-1])
                if a[i].strip() == b[j].strip():
                    f[i][j] = max(f[i][j], f[i-1][j-1] + 1)

    ua = [False] * n
    ub = [False] * m
    corr = [0] * n

    ci, cj = n - 1, m - 1
    while ci >= 0 and cj >= 0:
        if a[ci].strip() == b[cj].strip():
            ua[ci] = True
            ub[cj] = True
            corr[ci] = cj
            ci -= 1
            cj -= 1
        else:
            if ci == 0:
                cj -= 1
            elif cj == 0:
                ci -= 1
            elif f[ci-1][cj] > f[ci][cj-1]:
                ci -= 1
            else:
                cj -= 1

    skip = [False] * n
    sides = 7
    if compress:
        for i in xrange(n):
            if ua[i]:
                if i == 0 or not ua[i-1]:
                    j = i
                    while j < n and ua[j]:
                        j += 1

                    si = sides if i > 0 else 0
                    sj = sides if j < n else 0
                    if j - i > si + sj:
                        for q in xrange(i, j):
                            if q >= i + si and q < j - sj:
                                skip[q] = True

    yield "<table cellspacing=0>"
    row = "<tr><td bgcolor='{2}'><pre>{0}</pre></td><td bgcolor='{3}'><pre>{1}</pre></td></tr>"
    j = 0
    skipped_flag = False
    for i in xrange(n):
        if ua[i]:
            while j < corr[i]:
                yield row.format("", b[j], "#FFFFFF", "#AAFFAA")
                j += 1
                skipped_flag = False

            if skip[i]:
                if not skipped_flag:
                    skipped_flag = True
                    yield row.format('.' * 12, '.' * 12, "#fff", "#fff")
            else:
                yield row.format(a[i], b[j], "#FFFFFF", "#FFFFFF")

            j += 1
        else:
            yield row.format(a[i], "", "#FFAAAA", "#FFFFFF")
            skipped_flag = False

    yield "</table>"

def ComparePage(env):
    d = cgi.parse_qs(env['QUERY_STRING'])
    file1 = d['file1'][0] if 'file1' in d else ''
    file2 = d['file2'][0] if 'file2' in d else ''

    submissions_list = [file for file in os.listdir("submissions") if not file.endswith(".info")][::-1]

    yield top
    yield "<h1>Compare page</h1><hr>"

    yield "<form action='http://localhost:8051/compare' method='get'>"

    yield "File1:&nbsp;<select id='file1' name='file1'>"
    for sol in submissions_list:
        tag = "<option selected value={0}>" if sol == file1 else "<option value={0}>"
        comment = " ".join(open(os.path.join("submissions", sol + ".info"), "r").readlines())
        yield tag.format(sol) + sol + " | " + comment + "</option>"
    yield "</select><br>"

    yield "File2:&nbsp;<select id='file2' name='file2'>"
    for sol in submissions_list:
        tag = "<option selected value={0}>" if sol == file2 else "<option value={0}>"
        comment = " ".join(open(os.path.join("submissions", sol + ".info"), "r").readlines())
        yield tag.format(sol) + sol + " | " + comment + "</option>"
    yield "</select><br>"

    yield "<input type='checkbox' name='full_source'>Show full source</input><br>"
    yield "<input type='submit' value='Compare'></form><hr>"

    if 'file1' in d:
        for item in gen_compare_table(file1, file2, 'full_source' not in d):
            yield item
