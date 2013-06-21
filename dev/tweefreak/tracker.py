#! /usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import sys
from sys import argv
import credentials
import json
import jsonpickle
import re

#credentials for Twitter OAuth 
CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET


class StdOutListener(StreamListener):
  
    #tweets 
    def on_status(self, status):  
      print status.text
      #simplified and readable date for the tweets
      date = status.created_at.date().strftime("20%y/%m/%d")      
      #jsonpickle defines complex Python model objects and turns the objects into JSON 
      data = json.loads(jsonpickle.encode(status))

  
     
if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    print >> sys.stderr, 'Retrieving data for #%s....' %' '.join(sys.argv[1:])
    stream = Stream(auth, listener)    
    hashtag = "#%s" %' '.join(sys.argv[1:])
    stream.filter(follow=None, track=[hashtag])