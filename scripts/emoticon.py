#! /usr/bin/python 
 
import sys, time
import webbrowser 
import pymongo
import os
from pymongo import Connection  
from bson import BSON
from bson.json_util import dumps
from bson import Code
from bson.son import SON
import json
import cPickle as pickle
import simplejson
from operator import itemgetter
import operator, time, string
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
from datetime import datetime
import random



#mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweefreakDB']

hashtag_key = '#%s' %' '.join(sys.argv[1:])

#group by hashtag from mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
hashtag_data = db.tweets.group(key={"hashtag": hashtag_key , "tweet":1}, condition={}, 
	                                 initial={"count": 0}, reduce=reducer)

tweets_text = [] 
tweets_location = []

fname = hashtag_key
fn = "%s_%s.txt"%fname
f = open(fn,"wb")
pickle.dump(hashtag_data,f)
f.close()

f = file(fname, "r")
lines = f.readlines()
for line in lines:
        try:
                tweet = simplejson.loads(line)
               
                # Ignore retweets!
                if tweet.has_key("retweeted_status") or not tweet.has_key("text"):
                        continue
               
                # Fetch text from tweet
                text = tweet["text"].lower()
               
                # Ignore 'manual' retweets, i.e. messages starting with RT             
                if text.find("rt ") > -1:
                        continue
               
                tweets_text.append( text )
                tweets_location.append( tweet['user']['location'] )
 
        except ValueError:
                pass

print tweets_text
print tweets_location







