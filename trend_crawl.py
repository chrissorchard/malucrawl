import tweepy
import requests
import re
import lxml.html
import cssselect
from urlparse import urlparse, parse_qs, urlunparse
from urllib import urlencode


from celery import Celery, group

celery = Celery('tasks', backend='redis://:Km7icdOpKvb6JIzN40iG@kanga-cso1g09c', broker='amqp://guest:mkP5b9mholFmthIixyNx@kanga-cso1g09c//')

consumer_key = "8MJXt6b7JO4D9CQuDdzNLg"
consumer_secret = "pJuG88umFd61hVmqgcv4S1A26B9FROwr1w2nPLBjMHk"

access_token = "877860914-fwOaxBigey11rhzETtE5fh5djzvzxFmIDWFVifAi"
access_token_secret = "Pv9j7PhpSktS7OFokWiV84T3GeYJeSSrZsJKrj1O4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def to_unicode(obj, encoding='utf-8'):
    # http://farmdev.com/talks/unicode/
    if isinstance(obj,basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj,encoding)
    return obj

def camelCaseToSentenceCase(string):
    # http://stackoverflow.com/a/9283563
    return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', string)

@celery.task
def twitter_trend():
    
    trend_list = api.trends_location('1')[0]['trends']
    
    def hash_tag_handle(name):
        if name.startswith('#'):
            name = camelCaseToSentenceCase(name[1:])
        return name

    return group((search.s(hash_tag_handle(to_unicode(item["name"]))) for item in trend_list)).apply_async().get()

@celery.task	
def search(keyword):
    base_url = urlunparse(("http","www.dogpile.co.uk","/search/web","",urlencode({"q":keyword.encode("utf-8")}),""))
    return group(
        (
            malware_scan.s(url) for url in map(
                lambda link: parse_qs(urlparse(link.get('href')).query)["du"][0],
                lxml.html.fromstring(
                    requests.get(base_url).text,
                    base_url = base_url
                ).cssselect(".webResult .resultDisplayUrl")
            )
        )
    ).apply_async().get()

@celery.task
def malware_scan(url):
    e_title = lxml.html.fromstring(
        requests.get(url).text,
        base_url = url
    ).cssselect("title")
    if e_title:
        return e_title[0].text
