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
import re
import time

#credentials for Twitter OAuth 
CONSUMER_KEY = credentials.CONSUMER_KEY
CONSUMER_SECRET = credentials.CONSUMER_SECRET
ACCESS_TOKEN = credentials.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = credentials.ACCESS_TOKEN_SECRET

#Mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweefreakDB']


class StdOutListener(StreamListener):
  
    #tweets and Mongo
    def on_status(self, status):  
      #print status.text
      try:

         #tracking variables
         date = status.created_at.date().strftime("20%y/%m/%d")  
         time = status.created_at.time().strftime("%H:%M:%S") #GMT for hour
         hashtag_tracked = '#%s' %' '.join(sys.argv[1:])
         #print time   

         #jsonpickle defines complex Python model objects and turns the objects into JSON 
         data = json.loads(jsonpickle.encode(status))
       
         #store the whole tweet 
         db.tweets.save({"hashtag": hashtag_tracked, "time": time, "date": date, "tweet": data})

      except ConnectionFailure, e:
          sys.stderr.write("connection error: %s" % e)
          sys.exit(1)     
                

    #error handling
    def on_error(self, error):
        print error 


#count the number of tweets in mongo and print it
total_count = db.tweets.count()
print "   Total tweets: ", total_count  
     
if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET )
    print >> sys.stderr, 'Retrieving data for #%s....' %' '.join(sys.argv[1:])
    stream = Stream(auth, listener)    
    hashtag = "#%s" %' '.join(sys.argv[1:])
    stream.filter(follow=None, track=[hashtag])
