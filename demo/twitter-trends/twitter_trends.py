import tweepy
import json
import pprint

consumer_key="8MJXt6b7JO4D9CQuDdzNLg"
consumer_secret="pJuG88umFd61hVmqgcv4S1A26B9FROwr1w2nPLBjMHk"

access_token="877860914-fwOaxBigey11rhzETtE5fh5djzvzxFmIDWFVifAi"
access_token_secret="Pv9j7PhpSktS7OFokWiV84T3GeYJeSSrZsJKrj1O4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

trend_list = api.trends_location('1')[0]['trends']

for dct in trend_list:
	name = dct['name'].encode('gb18030','ignore')
	if(name.startswith('#')):
		name = name.replace('#','',1)
		tempList = list(name)
		for i, c in enumerate(tempList):
			if(i == 0): continue
			if c.isupper():
				if(tempList[i+1].isupper() and tempList[i-1].isupper()):
					continue
				else:
					tempList[i] = ' '+tempList[i]
		name = ''.join(tempList)
	print name
	
