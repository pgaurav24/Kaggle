import json
import csv
import os
from sets import Set

import preprocess_data


def get_categories(jsonfilename):
    jsonfilepath = os.path.join(preprocess_data.traindir,jsonfilename)
    categories = Set([])
    
    print 'reading '+ jsonfilepath
    reader = open(jsonfilepath, 'r')
    lines = reader.readlines()

    for line in lines:
        jrec = json.loads(line)
        cat = [ss.encode('utf-8') for ss in jrec.get('categories')]
        categories.update(cat)

    return categories

categories = get_categories('yelp_training_set_business.json')
print categories
print len(categories)
