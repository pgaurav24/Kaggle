import pandas
import numpy
import random
import os
import csv
import re
import extract_table as tt

user = pandas.read_csv(os.path.join(tt.traindir, 'yelp_training_set_user.csv'))
business = pandas.read_csv(os.path.join(tt.traindir, 'yelp_training_set_business.csv'))
checkin = pandas.read_csv(os.path.join(tt.traindir, 'yelp_training_set_checkin.csv'))
review =  pandas.read_csv(os.path.join(tt.traindir, 'yelp_training_set_review.csv'))

df1 = review.merge(user, on='user_id', how='left') 
df2 = df1.merge(business, on='business_id', how='left') 
dataset = df2.merge(checkin, on='business_id', how='left')

categories = set()
for cc in business.business_categories:
    if pandas.isnull(cc) == False:
        categories.update(g for g in cc.split('|'))

categories = sorted(categories)
print len(categories)

categories_filepath = os.path.join(tt.traindir, 'yelp_business_categories.csv')
categories = pandas.DataFrame(categories, columns=['category'])
categories.to_csv(categories_filepath,index=False)

training_filepath = os.path.join(tt.traindir, 'yelp_training_set.csv')
print 'writing training dataset to '+ training_filepath
dataset.to_csv(training_filepath,index=False,quoting=csv.QUOTE_NONNUMERIC)
