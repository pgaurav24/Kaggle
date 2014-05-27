import hashlib
import pandas
import csv
import sys

def hbucket(s):
    m = hashlib.md5()
    m.update(s)
    return int(m.hexdigest(),16)%1000

def main(infile='train.csv',cutoff=700):
    train_data = pandas.read_csv(infile,quotechar='"')
    train_data['bucketid'] = train_data['projectid'].apply(hbucket) 
    train_data.sort_index(by='bucketid')

    train = train_data[(train_data.bucketid < cutoff)]
    train.to_csv('data/train-A.csv',index=False,quoting=csv.QUOTE_ALL) 
    
    validate = train_data[(train_data.bucketid >= cutoff)]
    validate.to_csv('data/train-B.csv',index=False,quoting=csv.QUOTE_ALL) 

if __name__ == "__main__":
    infile = sys.argv[1]
    main(infile)
