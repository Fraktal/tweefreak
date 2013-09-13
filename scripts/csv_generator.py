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
import sys
import csv

#hashtag being tracked
hashtag_key = '#%s.csv' %' '.join(sys.argv[1:])

# open a CSV file to write geo data
csv_file = hashtag_key
out_csv = csv.writer(open(csv_file, 'wb'), delimiter=',') 
out_csv.writerow([ 'date','time'])

#list keys
date_val = {}
time_val = {}

#Mongo connection
conn = pymongo.Connection('localhost', 27017)
db = conn['tweefreakDB']


for r in db.tweets.find(fields=['date', 'time']): #not saving data due to unicode!!
        date = date_val[r['date']].encode('utf-8')
     	time = time_val[r['time']].encode('utf-8')


#saving time to csv file to be used in graphs outside of tweefreak
if not os.path.isdir('data/hashtag_csv'):
        os.makedirs('data/hashtag_csv')


#write data to CSV file
out_csv.writerow([ date, time]) 

