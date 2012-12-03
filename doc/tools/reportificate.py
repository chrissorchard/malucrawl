#!/usr/bin/python

#
# github API abusing script for report metrics
#
# C. Orchard - 29/11/2012
#

import requests
import getpass
from urlparse import urljoin
import tempfile
import os
import codecs
from subprocess import PIPE, Popen
import dateutil.parser
import datetime

username = raw_input("Username: ")
#WARNING: password contains the password, do not print!!!
password = getpass.getpass()

rf = [
    "doc/report/analysis.tex",
    "doc/report/conclusion.tex",
    "doc/report/description.tex",
    "doc/report/control.tex",
    "doc/report/evaluation.tex",
    "doc/report/review.tex",
    "doc/report/testing.tex",
    "doc/report/Literature research.tex",
    "doc/report/tech-sections/capture-hpc/design.tex",
    "doc/report/tech-sections/capture-hpc/results.tex",
    "doc/report/tech-sections/capture-hpc/testing.tex",
    "doc/report/tech-sections/clam-av/design.tex",
    "doc/report/tech-sections/clam-av/results.tex",
    "doc/report/tech-sections/clam-av/testing.tex",
    "doc/report/lit-review.tex"
    ]
report_files = set(rf)

github_url = "https://api.github.com/"
repo_url = "repos/chrissorchard/malucrawl/commits"
commit_url = "repos/chrissorchard/malucrawl/commits/"
status_url = "rate_limit"

param = {
    'path': 'doc/report'
        }

r = requests.get(urljoin(github_url, repo_url), auth=(username, password), params=param)

#print json.dumps(r.json, sort_keys=True, indent=2)
data = {}

for commit in r.json:
    print commit["sha"]

    u = urljoin(github_url, commit_url + commit["sha"])
    rc = requests.get(u, auth=(username, password))
    fd, fname = tempfile.mkstemp(prefix="gdp-")
    fd2, fname2 = tempfile.mkstemp(prefix="rgdp-")
    os.close(fd)
    os.close(fd2)
    try:
        g_used = False
        f_used = False
        with codecs.open(fname, 'a', encoding='utf-8') as f:
            with codecs.open(fname2, 'a', encoding='utf-8') as g:
                for changedf in rc.json["files"]:
                    if changedf["filename"] in report_files:
                        rcf = requests.get(changedf["raw_url"], auth=(username, password))
                        if "removed" in changedf["status"]:
                            g.write(rcf.text)
                            g_used = True
                        elif "added" in changedf["status"] and changedf["additions"] == 0:
                            pass
                        else:
                            f.write(rcf.text)
                            f_used = True
                g.close()
            f.close()
        cmd = os.path.join(os.getcwd(), "texcount.pl")

        if f_used:
            p1 = Popen([cmd, "-1", "-sum", fname], stdout=PIPE)
            all_result = p1.communicate()[0]
            lines_result = all_result.splitlines(False)
            ret = int(lines_result[0])
        else:
            ret = 0
        if g_used:
            p2 = Popen([cmd, "-1", "-sum", fname2], stdout=PIPE)
            all_result2 = p2.communicate()[0]
            lines_result2 = all_result2.splitlines(False)
            ret2 = int(lines_result2[0])
        else:
            ret2 = 0
    except ValueError:
        print lines_result
        print lines_result2
        raise
    except KeyError:
        print rc.json

    print ret
    print -ret2

    os.unlink(fname)
    os.unlink(fname2)

    dt = dateutil.parser.parse(commit["commit"]["committer"]["date"])
    data[commit["sha"]] = commit["author"]["login"], dt, ret - ret2
    #print json.dumps(rc.json, sort_keys=True, indent=2)

#print data

rstatus = requests.get(urljoin(github_url, status_url), auth=(username, password))
print rstatus.json


#
# Graphing
#

import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter


sdata = sorted(data.values(), key=itemgetter(1))

mindate = sdata[0][1].date()
maxdate = sdata[-1][1].date()

delta = maxdate - mindate

dateList = [mindate + datetime.timedelta(days=x) for x in range(0, delta.days + 1)]

#make four lists for y values

namecount = {}
for name, dt, count in sdata:
    if name not in namecount:
        namecount[name] = []
    namecount[name].append((dt, count))
    namecount[name].sort()


nameadd = {}
bars = []
width = 0.35
colours = ["b", "g", "r", "c", "m", "y"]
currc = 0
pltbars = {}

for name in namecount.keys():
    amounts = np.zeros(len(dateList))
    running_total = np.zeros(len(dateList))

    for dt, count in namecount[name]:
        amounts[dateList.index(dt.date())] += count

    total = 0
    for i, count in enumerate(amounts):
        total += count
        running_total[i] = total

    nameadd[name] = running_total

    if not bars:
        pltbars[name] = plt.bar(dateList, nameadd[name], color=colours[currc])
        currc += 1
        bars.append(name)
    else:
        pltbars[name] = plt.bar(dateList, nameadd[name], bottom=nameadd[bars[-1]], color=colours[currc])
        currc = (currc + 1) % len(colours)
        bars.append(name)

print dateList
print nameadd

plt.xticks(rotation='vertical')
plt.ylabel('Words')
plt.title('Report Word Count Breakdown')

legend = map(itemgetter(0), pltbars.values())
plt.legend(legend, bars, loc="upper left")

plt.subplots_adjust(bottom=.2)
plt.show()
