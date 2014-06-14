import json
import os
import csv
import preprocess_data

traindir = '/Users/prashant/workspace/Kaggle/YelpRecSys2013/data/yelp_training_set'
user_header = [ 'type',\
                'user_id',\
                'review_count',\
                'average_stars',\
                'votes_useful',\
                'votes_funny',\
                'votes_cool']

business_header = [ 'type',\
                    'business_id',\
                    'name',\
                    'neighborhoods',\
                    'full_address',\
                    'city',\
                    'state',\
                    'latitude',\
                    'longitude',\
                    'stars',\
                    'review_count',\
                    'categories',\
                    'open']

review_header = [   'type',\
                    'business_id',\
                    'user_id',\
                    'stars',\
                    'text',\
                    'date',\
                    'votes_useful',\
                    'votes_funny',\
                    'votes_cool']


def yelp_user(jrecord):
    record = [  jrecord.get('type'),\
                jrecord.get('user_id'),\
                jrecord.get('review_count'),\
                jrecord.get('average_stars'),\
                jrecord.get('votes').get('useful'),\
                jrecord.get('votes').get('funny'),\
                jrecord.get('votes').get('cool') ]
    
    return record

def yelp_business(jrecord):
    record = [  jrecord.get('type'),\
                jrecord.get('business_id'),\
                jrecord.get('name').encode('utf-8').replace('\n', ' '),\
                jrecord.get('neighborhoods'),\
                jrecord.get('full_address').encode('utf-8').replace('\n', ' '),\
                jrecord.get('city'),\
                jrecord.get('state'),\
                jrecord.get('latitude'),\
                jrecord.get('stars'),\
                jrecord.get('review_count'),\
                jrecord.get('categories'),\
                jrecord.get('open')]
    
    return record

def yelp_review(jrecord):
    record = [  jrecord.get('type'),\
                jrecord.get('business_id'),\
                jrecord.get('user_id'),\
                jrecord.get('stars'),\
                jrecord.get('text').encode('utf-8').replace('\n', ' '),\
                jrecord.get('date'),\
                jrecord.get('votes').get('useful'),\
                jrecord.get('votes').get('funny'),\
                jrecord.get('votes').get('cool') ]
    
    return record

def yelp_checkin(jrecord):
    record = [  jrecord.get('type'),\
                jrecord.get('business_id')]

def convert_json_to_csv(jsonfilename, entity, header):
    jsonfilepath = os.path.join(traindir,jsonfilename)
    
    print 'reading '+ jsonfilepath
    reader = open(jsonfilepath, 'r')
    lines = reader.readlines()
    
    csvfilename = os.path.splitext(jsonfilename)[0] +'.csv'
    csvfilepath = os.path.join(traindir, csvfilename)
    
    print 'writing '+ csvfilepath
    writer = csv.writer(open(csvfilepath ,'wb'), delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(header)

    for line in lines:
        jrecord = json.loads(line)
        record  = getattr(preprocess_data, entity)(jrecord)
        try:
            writer.writerow(record)
        except UnicodeEncodeError:
            print jrecord
            raise

def main():
    convert_json_to_csv('yelp_training_set_user.json', 'yelp_user', user_header)
    convert_json_to_csv('yelp_training_set_business.json', 'yelp_business', business_header)
    convert_json_to_csv('yelp_training_set_review.json', 'yelp_review', review_header)
   
if __name__ == "__main__":
    main()
