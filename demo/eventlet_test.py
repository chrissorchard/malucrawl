urls = (
    "https://www.google.com/intl/en_ALL/images/logo.gif",
    "http://python.org/images/python-logo.gif",
    "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif",
    "http://listen.technobase.fm/tunein-aacplus-pls"
)

import eventlet
requests = eventlet.import_patched('requests')
from datetime import timedelta
from six import binary_type

MAX_SIZE = 1000 * 1024
CHUNK = 1024


def fetch(url):
    print "opening", url
    body = binary_type()
    timeout = eventlet.Timeout(timedelta(minutes=0.1).seconds)
    try:
        r = requests.get(url, stream=True)
        data = r.raw.read(1024)
        body += data
        while data and (len(body) <= MAX_SIZE):
            data = r.raw.read(1024)
            body += data
        expected_length = int(r.headers.get("Content-Length", 0))

        # If len(data) < CHUNK we're at the end of the file.
        # If it's the expected length, that's great we got the whole file,
        # even if len(data) == CHUNK.
        # Otherwise because we've read a full chunk of an unknown total
        # length we're not at the end of the file.
        if not len(body) == expected_length and not (len(data) < CHUNK):
            print "file too big", url
    except eventlet.Timeout as t:
        if t is not timeout:
            raise  # not my timeout
        else:
            print "took too long", url
    finally:
        timeout.cancel()

    print "done with", url
    return url, body

pool = eventlet.GreenPool(200)
for url, body in pool.imap(fetch, urls):
    print "got body from", url, "of length", len(body)
