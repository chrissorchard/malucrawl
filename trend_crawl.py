import tweepy
import requests
import re
import lxml.html
from urlparse import urlparse, parse_qs, urlunparse
from urllib import urlencode

consumer_key = "8MJXt6b7JO4D9CQuDdzNLg"
consumer_secret = "pJuG88umFd61hVmqgcv4S1A26B9FROwr1w2nPLBjMHk"

access_token = "877860914-fwOaxBigey11rhzETtE5fh5djzvzxFmIDWFVifAi"
access_token_secret = "Pv9j7PhpSktS7OFokWiV84T3GeYJeSSrZsJKrj1O4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def camelCaseSentenceToCase(string):
    # http://stackoverflow.com/a/9283563
    return re.sub(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))', r' \1', string)


def twitter_trend():
    trend_list = api.trends_location('1')[0]['trends']

    for name in (dct["name"] for dct in trend_list):
        if name.startswith('#'):
            name = camelCaseSentenceToCase(name[1:])
        print name
	
def search(keyword):
    return map(
        lambda link: parse_qs(urlparse(link.get('href')).query)["du"][0],
        lxml.html.fromstring(
            requests.get(urlunparse(
                ("http","www.dogpile.co.uk","/search/web",'',urlencode({"q":keyword}),'')
            )).text
        ).cssselect(".webResult .resultDisplayUrl")
    )
