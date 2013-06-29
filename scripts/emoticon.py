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
hashtag_data = db.tweets.group(key={"hashtag": hashtag_key , "text":1}, condition={}, 
	                                 initial={"count": 0}, reduce=reducer)

text = [','.join([str(json.dumps(tweet["text"])) 
                             for tweet in hashtag_data])]
 
print text






