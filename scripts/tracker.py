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

#group by tweet_text_emoticon from mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
hashtag_data = db.tweets.group(key={"hashtag": hashtag_key , "time":1}, condition={}, 
                                     initial={"count": 0}, reduce=reducer)

time = [','.join([str(json.dumps(tweet["time"])) 
                             for tweet in hashtag_data])]


#saving time to csv file to be used in graphs outside of tweeefreak
if not os.path.isdir('data/hashtag_data'):
        os.makedirs('data/hashtag_data')

fname = "%s" %' '.join(sys.argv[1:])
time_data = ' , '.join([str(json.dumps(tweet["time"])) 
                             for tweet in hashtag_data])

fn = "%s.csv" %fname
f = open(os.path.join(os.getcwd(), 'data', 'hashtag_data', fn), 'w')
f.write(time_data)
f.close()


#plotting the basic spike train
x = [time]
y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

plt.plot(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()


#print time