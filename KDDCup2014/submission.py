from sklearn.externals import joblib
from sklearn.feature_extraction import DictVectorizer

import pandas
import numpy
import os,sys

import build_features as bf

probe_file = 'data/test.csv'
target = 'is_exciting'

print 'Loading data'
probe = pandas.read_csv(probe_file, quotechar='"')

print 'Building features'
probe_features = bf.extract_features(probe)
num_probe_features = probe_features[bf.features_numeric].as_matrix()
cat_probe_features = probe_features.drop(bf.features_numeric, axis=1)
d_probe_features = cat_probe_features.T.to_dict().values()

vectorizer = joblib.load(os.path.join('data/AA/model/', 'dict_vectorizer.pkl'))
vec_probe_features = vectorizer.transform(d_probe_features)
X_probe = numpy.hstack((vec_probe_features, num_probe_features))

print 'Loading Model'
filename = "".join(['mdl_', target, '.pkl'])
rf = joblib.load(os.path.join('data/AA/model/', filename))

print 'Predictions'
probe_probs = rf.predict_proba(X_probe)

df_pred = pandas.DataFrame(index=probe.index)
df_probs = pandas.Series(data=probe_probs[:,1], index=df_pred.index, name='is_exciting')
df_pred = df_pred.join(probe.projectid)
df_pred = df_pred.join(df_probs)
df_pred.to_csv('data/submissions/submissions_5.csv',index=False) 
