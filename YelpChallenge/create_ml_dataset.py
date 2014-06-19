import pandas
import numpy
import random
import os
import csv
import re
import extract_table as tt
import features as ff

dataset_in = pandas.read_csv(os.path.join(tt.traindir, 'yelp_training_set.csv'))
dataset_out = ff.extract_features(dataset_in)
dataset_out = dataset_out.join(dataset_in['review_votes_useful'])

rows = random.sample(dataset_out.index, int(0.7*dataset_out.shape[0]))
yelp_training_set = dataset_out.ix[rows]
yelp_validation_set = dataset_out.drop(rows)

training_filepath = os.path.join(tt.traindir, 'yelp_training_set_A.csv')
print 'writing training dataset to '+ training_filepath
yelp_training_set.to_csv(training_filepath,index=False,quoting=csv.QUOTE_NONNUMERIC)

validation_filepath = os.path.join(tt.traindir, 'yelp_training_set_B.csv')
print 'writing validation dataset to '+ validation_filepath
yelp_validation_set.to_csv(validation_filepath,index=False,quoting=csv.QUOTE_NONNUMERIC)
