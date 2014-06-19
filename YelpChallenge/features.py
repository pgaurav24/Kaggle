import pandas
import numpy
import csv
import re
import os
import features
import extract_table as tt

categories = pandas.read_csv(os.path.join(tt.traindir, 'yelp_business_categories.csv'))

feature_names = [ 'user_review_count_ff',\
                  'user_average_stars_ff',\
                  'user_votes_useful_ff',\
                  'user_votes_funny_ff',\
                  'user_votes_cool_ff',\
                  'business_latitude',\
                  'business_longitude',\
                  'business_stars',\
                  'business_categories_features',\
                  'business_review_count',\
                  'business_open',\
                  'checkin_count_sun_ff',\
                  'checkin_count_mon_ff',\
                  'checkin_count_tue_ff',\
                  'checkin_count_wed_ff',\
                  'checkin_count_thu_ff',\
                  'checkin_count_fri_ff',\
                  'checkin_count_sat_ff',\
                  'review_stars',\
                  'review_text_len']

def user_review_count_ff(data):
    return data['user_review_count'].fillna(0)

def user_average_stars_ff(data):
    return data['user_average_stars'].fillna(0)

def user_votes_useful_ff(data):
    return data['user_votes_useful'].fillna(0)

def user_votes_funny_ff(data):
    return data['user_votes_funny'].fillna(0)

def user_votes_cool_ff(data):
    return data['user_votes_cool'].fillna(0)

def checkin_count_sun_ff(data):
    return data['checkin_count_sun'].fillna(0)

def checkin_count_mon_ff(data):
    return data['checkin_count_mon'].fillna(0)

def checkin_count_tue_ff(data):
    return data['checkin_count_tue'].fillna(0)

def checkin_count_wed_ff(data):
    return data['checkin_count_wed'].fillna(0)

def checkin_count_thu_ff(data):
    return data['checkin_count_thu'].fillna(0)

def checkin_count_fri_ff(data):
    return data['checkin_count_fri'].fillna(0)

def checkin_count_sat_ff(data):
    return data['checkin_count_sat'].fillna(0)

def review_text_len(data):
    out = data['review_text'].apply(lambda x: len(str(x)) )
    out.name = 'review_text_len'
    return out
    
def business_categories_features(data):
    out = pandas.DataFrame(index=data.index)
    for category in categories.category.tolist():
        ff = data.business_categories.apply(lambda cc: 0 if pandas.isnull(cc) else (category in cc.split('|'))*1 )
        ff.name = re.sub(r'[^a-zA-Z0-9\[\]]', "_", category).lower()
        out = out.join(ff) 
    return out

# TODO: add review text features

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
    data = pandas.read_csv('data/yelp_training_set/yelp_training_tryset.csv', quotechar='"')
    features = extract_features(data)
    features.to_csv('data/yelp_training_set/yelp_training_features.csv',index=False,quoting=csv.QUOTE_NONNUMERIC)
