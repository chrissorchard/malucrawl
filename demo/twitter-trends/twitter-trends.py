import tweepy

consumer_key="8MJXt6b7JO4D9CQuDdzNLg"
consumer_secret="pJuG88umFd61hVmqgcv4S1A26B9FROwr1w2nPLBjMHk"

access_token="877860914-fwOaxBigey11rhzETtE5fh5djzvzxFmIDWFVifAi"
access_token_secret="Pv9j7PhpSktS7OFokWiV84T3GeYJeSSrZsJKrj1O4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#print api.me().name

print api.trends_location('1')
