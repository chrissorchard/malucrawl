#!/usr/bin/python

#
# github API abusing script for report metrics
#
# C. Orchard - 29/11/2012
#

import itertools
import requests
import getpass
import os
import dateutil.parser
import datetime
import percache
import keyring
import httplib

import matplotlib.pyplot as plt
import numpy as np

from operator import itemgetter
from contextlib import closing
from fnmatch import fnmatchcase
from subprocess import Popen, PIPE
from urlparse import urljoin
from collections import defaultdict, deque

from xdg import BaseDirectory

from link_header import parse_link_value

from six.moves import configparser

github_url = "https://api.github.com/"
repo_url = "repos/chrissorchard/malucrawl/commits"
commit_url = "repos/chrissorchard/malucrawl/commits/"
status_url = "rate_limit"
full_repo_url = urljoin(github_url, repo_url)
path = "doc/report"
valid_files = "doc/report/*.tex"

working_dir = os.path.dirname(os.path.realpath(__file__))


def get_auth():
    def check_auth(auth):
        return requests.head(full_repo_url, auth=auth).status_code != httplib.UNAUTHORIZED

    # config file init
    config_file = os.path.join(BaseDirectory.save_config_path("malucrawl_reportificate"), "settings.ini")
    config = configparser.SafeConfigParser()
    config.read(config_file)

    if not config.has_section('auth'):
        config.add_section('auth')

    try:
        username = config.get('auth', 'username')
    except configparser.NoOptionError:
        username = raw_input("Username: ")

    password = keyring.get_password(github_url, username)
    if password is None:
        password = getpass.getpass()

    while not check_auth((username, password)):
        print "Authorization Failed"
        username = raw_input("Username: ")
        password = getpass.getpass()

    keyring.set_password(github_url, username, password)
    config.set('auth', 'username', username)
    config.write(open(config_file, 'w'))

    return (username, password)

session = requests.Session(auth=get_auth())


def commits_generator():
    url = full_repo_url
    param = {
        'path': path,
        'per_page': '100'
    }
    while True:
        r = session.get(
            url,
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

with closing(percache.Cache(
    os.path.join(BaseDirectory.save_cache_path("malucrawl_reportificate"), "cache")
)) as cache:

    @cache
    def get_commit_details(commit_url):
        return session.get(commit_url).json

    @cache
    def count_words_in_tree(tree_url):
        return sum(
            map(
                lambda tree: blob_lacount(tree["url"]),
                itertools.ifilter(
                    lambda tree: tree["type"] == "blob" and fnmatchcase(tree["path"], valid_files),
                    session.get(tree_url, params={"recursive": 1}).json["tree"]
                )
            )
        )

    @cache
    def blob_lacount(blob_url):
        response = session.get(blob_url,
            headers={"Accept": "application/vnd.github.v3.raw"}
        )

        cmd = os.path.join(working_dir, "texcount.pl")
        count_proc = Popen([cmd, "-1", "-sum", "-"], stdin=PIPE, stdout=PIPE)

        try:
            stdout, stderr = count_proc.communicate(input=response.content)
            return int(stdout.splitlines(False)[0])
        except (ValueError):
            return 0

    all_commits = itertools.chain.from_iterable(commits_generator())

    # Count the total number of words in each commit
    # Append to data: the author of the commit, the time it was made
    # and the absolute word count at that commit.
    #
    # Note: This no-longer counts deltas
    data = []
    for commit_number, commit in enumerate(all_commits):
        print (commit_number, commit["sha"])

        if commit["committer"] is None:
            commit["author"] = {
                "login": u"nafisehvahabi"
        }

        data.append(
            (
                commit["author"]["login"],
                dateutil.parser.parse(commit["commit"]["committer"]["date"]),
                count_words_in_tree(commit["commit"]["tree"]["url"])
            )
        )

print session.get(urljoin(github_url, status_url)).json


#
# Graphing
#


sdata = sorted(data, key=itemgetter(1))

mindate = sdata[0][1].date()
maxdate = sdata[-1][1].date()

delta = maxdate - mindate

date_list = [mindate + datetime.timedelta(days=x)
        for x in range(0, delta.days + 1)]

#make four lists for y values

# associate deltas with the relevant username
# sum deltas with the same username and date
namecount = defaultdict(lambda: defaultdict(lambda: 0))
old_words = 0
for name, dt, count in sdata:
    delta = count - old_words
    old_words = count
    namecount[name][dt.date()] += delta


nameadd = {}
colors = deque(["b", "g", "r", "c", "m", "y"])
labels = []
bars = []
barsum = np.zeros(len(date_list))

for name, course_date_count in namecount.items():
    amounts = np.zeros(len(date_list))
    running_total = np.zeros(len(date_list))

    for i, date in enumerate(date_list):
        amounts[i] = course_date_count.get(date, 0)

    total = 0
    for i, count in enumerate(amounts):
        total += count
        running_total[i] = total

    nameadd[name] = running_total

    labels.append(name)
    bars.append(plt.bar(
            date_list,
            nameadd[name],
            bottom=barsum,
            color=colors[0]
        )[0]
    )
    colors.rotate(-1)
    barsum += running_total

print date_list
print nameadd

plt.xticks(rotation='vertical')
plt.ylabel('Words')
plt.title('Report Word Count Breakdown')

plt.legend(bars, labels, loc="upper left")

plt.subplots_adjust(bottom=.2)
plt.show()
