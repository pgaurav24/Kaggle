import pandas
import numpy
import os
import csv
import preprocess_data as ppd

user = pandas.read_csv(os.path.join(ppd.traindir, 'yelp_training_set_user.csv'))
business = pandas.read_csv(os.path.join(ppd.traindir, 'yelp_training_set_business.csv'))
checkin = pandas.read_csv(os.path.join(ppd.traindir, 'yelp_training_set_checkin.csv'))
review =  pandas.read_csv(os.path.join(ppd.traindir, 'yelp_training_set_review.csv'))

# business.neighborhoods.apply(lambda l: len(json.loads(l))).describe()
categories = set()
for cc in business.categories:
    if pandas.isnull(cc) == False:
        categories.update(g for g in cc.split('|'))

categories = sorted(categories)
print len(categories)

business_categories = pandas.DataFrame(index=business.index)
business_categories = business_categories.join(business['business_id'])

for category in categories:
    ff = business.categories.apply(lambda cc: False if pandas.isnull(cc) else (category in cc.split('|')) )
    ff.name=category
    business_categories = business_categories.join(ff) 

review = review[['business_id', 'user_id',  'review_stars', 'review_date']]

df1 = review.merge(user, on='user_id', how='left') 
df2 = df1.merge(business, on='business_id', how='left') 
dataset = df2.merge(checkin, on='business_id', how='left')


categories_filepath = os.path.join(ppd.traindir, 'yelp_training_set_category.csv')
print 'writing categories dataset to '+ categories_filepath
business_categories.to_csv(categories_filepath,index=False,quoting=csv.QUOTE_NONNUMERIC)


training_filepath = os.path.join(ppd.traindir, 'yelp_training_set.csv')
print 'writing training dataset to '+ training_filepath
dataset.to_csv(training_filepath,index=False,quoting=csv.QUOTE_NONNUMERIC)
