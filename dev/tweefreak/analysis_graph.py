#! /usr/bin/python

import sys, time
import webbrowser 
import pymongo
from pymongo import Connection  
from bson import BSON
from bson.json_util import dumps
from bson import Code
from bson.son import SON
import json
import cPickle as pickle
import simplejson
from string import punctuation
from operator import itemgetter
import operator, time, string
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import numpy as np
from datetime import datetime



#mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweefreakDB']

#hashtag_key = '#%s' %' '.join(sys.argv[1:])

#group by tweet_text_emoticon from mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
hashtag_data = db.tweets.group(key={"hashtag":1, "time":1}, condition={}, initial={"count": 0}, reduce=reducer)

time = ','.join([str(json.dumps(tweet["time"])) 
                             for tweet in hashtag_data])

print time

