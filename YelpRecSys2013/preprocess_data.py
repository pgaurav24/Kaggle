import json
import os
import csv
import numpy
import preprocess_data

traindir = '/Users/prashant/workspace/Kaggle/YelpRecSys2013/data/yelp_training_set'
testdir  = '/Users/prashant/workspace/Kaggle/YelpRecSys2013/data/yelp_test_set'

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

checkin_header = [ 'type',\
                   'business_id',\
                   'checkin_count_sun',\
                   'checkin_count_mon',\
                   'checkin_count_tue',\
                   'checkin_count_wed',\
                   'checkin_count_thu',\
                   'checkin_count_fri',\
                   'checkin_count_sat']


def yelp_user(jrec):
    record = [  jrec.get('type'),\
                jrec.get('user_id'),\
                jrec.get('review_count'),\
                jrec.get('average_stars'),\
                jrec.get('votes').get('useful'),\
                jrec.get('votes').get('funny'),\
                jrec.get('votes').get('cool') ]
    
    return record

def yelp_business(jrec):
    record = [  jrec.get('type'),\
                jrec.get('business_id'),\
                jrec.get('name').encode('utf-8').replace('\n', ' '),\
                jrec.get('neighborhoods'),\
                jrec.get('full_address').encode('utf-8').replace('\n', ' '),\
                jrec.get('city'),\
                jrec.get('state'),\
                jrec.get('latitude'),\
                jrec.get('longitude'),\
                jrec.get('stars'),\
                jrec.get('review_count'),\
                jrec.get('categories'),\
                jrec.get('open')]
    
    return record

def yelp_review(jrec):
    record = [  jrec.get('type'),\
                jrec.get('business_id'),\
                jrec.get('user_id'),\
                jrec.get('stars'),\
                jrec.get('text').encode('utf-8').replace('\n', ' ').replace('\r',' '),\
                jrec.get('date'),\
                jrec.get('votes').get('useful'),\
                jrec.get('votes').get('funny'),\
                jrec.get('votes').get('cool') ]
    
    return record

def yelp_checkin(jrec):
   checkin_info = jrec.get('checkin_info')
   checkin_count = numpy.zeros(7, dtype=numpy.int)

   for hh_dd, checkin in checkin_info.iteritems():
        dayofweek = int(hh_dd.split('-')[1])
        assert(dayofweek >= 0 and dayofweek <=6),"dayofweek out of range"
        checkin_count[dayofweek] = checkin_count[dayofweek] + checkin          

   record = [  jrec.get('type'), jrec.get('business_id')]
   record.extend(checkin_count.tolist())
    
   return record 

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
        jrec = json.loads(line)
        record  = getattr(preprocess_data, entity)(jrec)
        try:
            writer.writerow(record)
        except UnicodeEncodeError:
            print 'Error reading : '+ jrec
            raise

def main():
    convert_json_to_csv('yelp_training_set_user.json', 'yelp_user', user_header)
    convert_json_to_csv('yelp_training_set_business.json', 'yelp_business', business_header)
    convert_json_to_csv('yelp_training_set_review.json', 'yelp_review', review_header)
    convert_json_to_csv('yelp_training_set_checkin.json', 'yelp_checkin', checkin_header)
   
if __name__ == "__main__":
    main()
