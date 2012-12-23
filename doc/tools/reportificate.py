#!/usr/bin/python

#
# github API abusing script for report metrics
#
# C. Orchard - 29/11/2012
#

import itertools
import requests
import getpass
import tempfile
import os
import dateutil.parser
import datetime
import percache

from copy import deepcopy
from contextlib import closing
from xdg import BaseDirectory
from subprocess import PIPE, Popen
from urlparse import urljoin

from link_header import parse_link_value

report_files = [
    "doc/report/analysis.tex",
    "doc/report/spec-cust.tex"
    "doc/report/conclusion.tex",
    "doc/report/description.tex",
    "doc/report/control.tex",
    "doc/report/problem-definition.tex",
    "doc/report/evaluation.tex",
    "doc/report/review.tex",
    "doc/report/testing.tex",
    "doc/report/Literature research.tex",
    "doc/report/tech-sections/capture-hpc/design.tex",
    "doc/report/tech-sections/capture-hpc/results.tex",
    "doc/report/tech-sections/capture-hpc/testing.tex",
    "doc/report/tech-sections/clam-av/design.tex",
    "doc/report/tech-sections/clam-av/evaluation.tex",
    "doc/report/tech-sections/clam-av/testing.tex",
    "doc/report/tech-sections/clam-av/results.tex",
    "doc/report/tech-sections/wine/design.tex",
    "doc/report/tech-sections/wine/evaluation.tex",
    "doc/report/tech-sections/wine/testing.tex",
    "doc/report/tech-sections/wine/results.tex",
    "doc/report/lit-review.tex",
    "doc/report/group-approach.tex",
    "doc/report/tech-sections/celery-framework/design.tex",
    "doc/report/tech-sections/celery-framework/results.tex",
    "doc/report/tech-sections/celery-framework/testing.tex",
    "doc/report/tech-sections/celery-framework/search-engine.tex",
    "doc/report/tech-sections/celery-framework/trend-sources.tex",
    "doc/report/tech-sections/malware-lists/design.tex",
    "doc/report/tech-sections/malware-lists/results.tex",
    "doc/report/tech-sections/malware-lists/testing.tex",
    "doc/report/Evaluation(classifer+HTML).tex",
    "doc/report/tech-sections/Classification/design.tex",
    "doc/report/tech-sections/Classification/implementation.tex",
    "doc/report/tech-sections/Classification/evaluation.tex",
    "doc/report/tech-sections/HTML-malware/design.tex",
    "doc/report/tech-sections/HTML-malware/implementation.tex",
    "doc/report/tech-sections/HTML-malware/evaluation.tex",
    "doc/report/tech-sections/Classification/evaluation.tex",
    "doc/report/Conclusion(Nafiseh).tex",
    "doc/report/Future development.tex",
    "doc/report/Liteature(Nafiseh).tex",
    "doc/report/Related work.tex"
    ]

github_url = "https://api.github.com/"
repo_url = "repos/chrissorchard/malucrawl/commits"
commit_url = "repos/chrissorchard/malucrawl/commits/"
status_url = "rate_limit"


def commits_generator():
    url = urljoin(github_url, repo_url)
    param = {
        'path': 'doc/report',
        'per_page': '100'
    }
    while True:
        r = requests.get(
            url,
            auth=(username, password),
            params=param
        )
        yield r.json

        for key_url, prop in parse_link_value(r.headers["link"]).items():
            if prop.get("rel", None) == "next":
                url = key_url
                param = {}
                break
        else:
            "Not found a next URL? Then the generator is empty"
            break


def filefromraw(rawurl):
    parts = rawurl.split('/')
    return '/'.join(parts[-3:])


username = raw_input("Username: ")
#WARNING: password contains the password, do not print!!!
password = getpass.getpass()

with closing(percache.Cache(
    os.path.join(BaseDirectory.save_cache_path("malucrawl_reportificate"), "cache")
)) as cache:

    @cache
    def lacount(count_url):
        response = requests.get(count_url, auth=(username, password))

        fd, fname = tempfile.mkstemp(prefix="gdp-")
        os.close(fd)

        with open(fname, 'w') as f:
            f.write(response.content)
            f.close()

        cmd = os.path.join(os.getcwd(), "texcount.pl")

        try:
            p = Popen([cmd, "-1", "-sum", fname], stdout=PIPE)
            all_result = p.communicate()[0]
            lines_result = all_result.splitlines(False)
            os.unlink(fname)

            res = int(lines_result[0])

        except ValueError:
            return -1

        return res

    data = {}
    filecount = {}

    all_commits = list(itertools.chain.from_iterable(commits_generator()))

    for commit in all_commits:
        if commit["committer"] is None:
            commit["author"] = {
                "login": u"nafisehvahabi"
            }

    sortcommits = sorted(
        all_commits,
        key=lambda x: dateutil.parser.parse(x["commit"]["committer"]["date"])
    )

    print sortcommits

    for commit_number, commit in enumerate(sortcommits):
        print (commit_number, commit["sha"])
        if commit["sha"] == "[":
            print commit
        oldcount = deepcopy(filecount)

        commit_details = requests.get(commit["url"], auth=(username, password)).json
        try:
            for changedf in commit_details["files"]:
                fn = changedf["filename"]
                if fn in report_files:
                    #print "I found: " + fn
                    if "removed" in changedf["status"]:
                        filecount[fn] = 0
                    elif not changedf["sha"]:
                        #print filecount
                        filecount[fn] = filecount[filefromraw(changedf["raw_url"])]
                        filecount[filefromraw(changedf["raw_url"])] = 0
                    else:
                        filecount[fn] = lacount(changedf["raw_url"])
                        if filecount[fn] == -1:
                            filecount[fn] = oldcount[fn]
        #except ValueError:
        #    print json.dumps(commit_details, sort_keys=True, indent=2)
            #print lines_result
            #print lines_result2
        #    raise
        except KeyError:
            print commit
            print commit_details
            raise

        #TODO: sum file changes
        changes = sum(filecount.values()) - sum(oldcount.values())

        try:
            dt = dateutil.parser.parse(commit["commit"]["committer"]["date"])
            data[commit["sha"]] = commit["author"]["login"], dt, changes
        except TypeError:
            print commit
            raise
        #print data[commit["sha"]]
        #print json.dumps(rc.json, sort_keys=True, indent=2)

    #print data

rstatus = requests.get(
        urljoin(github_url, status_url), auth=(username, password))
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

dateList = [mindate + datetime.timedelta(days=x)
        for x in range(0, delta.days + 1)]

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
barsum = np.zeros(len(dateList))

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
        pltbars[name] = plt.bar(
                dateList,
                nameadd[name],
                bottom=barsum,
                color=colours[currc])
        currc = (currc + 1) % len(colours)
        bars.append(name)
    barsum += running_total

print dateList
print nameadd

plt.xticks(rotation='vertical')
plt.ylabel('Words')
plt.title('Report Word Count Breakdown')

legend = map(itemgetter(0), pltbars.values())
plt.legend(legend, bars, loc="upper left")

plt.subplots_adjust(bottom=.2)
plt.show()
