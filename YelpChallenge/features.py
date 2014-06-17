import pandas
import numpy
import csv
import re
import os
import features
import extract_table as tt

categories = pandas.read_csv(os.path.join(tt.traindir, 'yelp_business_categories.csv'))

feature_names = [ 'user_review_count',\
                  'user_average_stars',\
                  'user_votes_useful',\
                  'user_votes_funny',\
                  'user_votes_cool',\
                  'business_latitude',\
                  'business_longitude',\
                  'business_stars',\
                  'business_review_count',\
                  'business_categories_features',\
                  'business_open',\
                  'checkin_count_sun',\
                  'checkin_count_mon',\
                  'checkin_count_tue',\
                  'checkin_count_wed',\
                  'checkin_count_thu',\
                  'checkin_count_fri',\
                  'checkin_count_sat',\
                  'review_stars',\
                  'review_text_len']

def review_text_len(data):
    df = data['review_text'].apply(lambda x: len(str(x)) )
    df.name = 'review_text_len'

    return df
    
def business_categories_features(data):
    out = pandas.DataFrame(index=data.index)
    for category in categories.category.tolist():
        ff = data.business_categories.apply(lambda cc: False if pandas.isnull(cc) else (category in cc.split('|')) )
        ff.name = re.sub(r'[^a-zA-Z0-9\[\]]', "_", category).lower()
        out = out.join(ff) 
    
    return out

# TODO
# add review text features

def extract_features(data):
    feat = pandas.DataFrame(index=data.index)
    for fname in feature_names:
            print fname
            if fname in data:
                feat = feat.join(data[fname])
            else:
                d = getattr(features, fname)(data)
                feat = feat.join(d)
    return feat

if __name__ == "__main__":
    data = pandas.read_csv('data/yelp_training_set/yelp_training_set.csv', quotechar='"')
    features = extract_features(data)
    features.to_csv('data/yelp_training_set/yelp_training_features.csv',index=False,quoting=csv.QUOTE_NONNUMERIC)
