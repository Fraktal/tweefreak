#! /usr/bin/python

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
from pymongo import Connection 
import sys
import credentials
import json
import jsonpickle
import logging
import re

#credentials for Twitter OAuth 
CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET

#hashtag being tracked
hashtag_key = '#%s' %' '.join(sys.argv[1:])

#Mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweetDB']


class StdOutListener(StreamListener):
  
    #tweets and Mongo
    def on_status(self, status):  
      print status.text
      try:

         #simplified and readable date for the tweets
         date = status.created_at.date().strftime("20%y/%m/%d")  
         time = status.created_at.time().strftime("%H:%M:%S")#GMT time stored in Mongo    

         #jsonpickle defines complex Python model objects and turns the objects into JSON 
         data = json.loads(jsonpickle.encode(status))
          
         #storing tweet data in Mongo  
         db.tweets.save({"hashtag": hashtag_key, "date": date, "time": time, "text": status.text, "tweet": data})
            
      except ConnectionFailure, error:
          sys.stderr.write("could not connect to MongoDB: %s" % error)
          sys.exit(1)     
                
    #error handling
    def on_error(self, error):
        print error 


#count the number of tweets in Mongo and print it
total_count = db.tweets.count()


if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    print >> sys.stderr,"retrieving data for %s....." %hashtag_key
    stream = Stream(auth, listener)    
    stream.filter(follow = None, track=[hashtag_key])