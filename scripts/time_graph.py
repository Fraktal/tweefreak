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


#hashtag being tracked
hashtag_key = '#%s' %' '.join(sys.argv[1:])

#Mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweefreakDB']

#group by hashtag from Mongo
reducer = Code("""
                   function(obj, prev){
                     prev.count++;
                   }
                   """)
hashtag_data = db.tweets.group(key={"hashtag": hashtag_key , "time":1}, condition={}, 
	                                 initial={"count": 0}, reduce=reducer)


#Pulling out time data from hashtag queried 
time = ' '.join([str(json.dumps(tweet["time"])) 
                             for tweet in hashtag_data])


#saving time to csv file to be used in graphs outside of tweeefreak
if not os.path.isdir('data/hashtag_csv'):
        os.makedirs('data/hashtag_csv')

fn = "%s.csv" %hashtag_key
f = open(os.path.join(os.getcwd(), 'data', 'hashtag_csv', fn), 'w')
f.write(time)
f.close()

print time

"""
#plotting the basic spike train
x = [time]
y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

plt.plot(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()


#print time
"""