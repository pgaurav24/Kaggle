import os,sys,csv
import pandas
import numpy

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import roc_auc_score
from sklearn.externals import joblib

import build_features as bf

target_vars = ['is_exciting']

#target_vars = ['is_exciting',\
#               'fully_funded',\
#               'at_least_1_teacher_referred_donor',\
#               'great_chat',\
#               'at_least_1_green_donation',\
#               'three_or_more_non_teacher_referred_donors',\
#               'one_non_teacher_referred_donor_giving_100_plus',\
#               'donation_from_thoughtful_donor',\
#               'atleast_one_cond',\
#               'atleast_one_feature']

full_train_file = 'data/train.csv'
train_file = 'data/train-A.csv'
test_file  = 'data/train-B.csv'

print 'Loading data'
train = pandas.read_csv(train_file, quotechar='"')
test  = pandas.read_csv(test_file, quotechar='"')

print 'Building features'
train_features = bf.extract_features(train)
test_features  = bf.extract_features(test)

num_train_features = train_features[bf.features_numeric].as_matrix()
num_test_features  = test_features[bf.features_numeric].as_matrix()

cat_train_features = train_features.drop(bf.features_numeric, axis=1)
cat_test_features  = test_features.drop(bf.features_numeric, axis=1)

d_train_features = cat_train_features.T.to_dict().values()
d_test_features  = cat_test_features.T.to_dict().values()

vectorizer = DictVectorizer(sparse=False)
vec_train_features = vectorizer.fit_transform(d_train_features)
joblib.dump(vectorizer, os.path.join('data/AA/model/', 'dict_vectorizer.pkl'))

X_train = numpy.hstack((vec_train_features, num_train_features))

vec_test_features = vectorizer.transform(d_test_features)
X_test = numpy.hstack((vec_test_features, num_test_features))

rf_features = vectorizer.get_feature_names()
rf_features.extend(bf.features_numeric)
print(len(rf_features))

predictions = pandas.DataFrame(index=test.index)
predictions = predictions.join( pandas.Series(data=test['is_exciting'], name='label', index=test.index) )

for target in target_vars:
    print 'Training RF Model - %s' % target
    rf = RandomForestClassifier(n_estimators=50, max_features=20,\
            max_depth=10, min_samples_leaf=5, n_jobs=-1)

    y_train = train[target]
    tpr = y_train.mean() 
    y_weight = train[target].apply(lambda x: tpr if x==False else 1-tpr) 
    y_weight = y_weight.apply(lambda x:round(x, 2))
    rf.fit(X_train, y_train, y_weight.values)

    rf_feature_imp = pandas.Series(rf.feature_importances_, index=rf_features, name='Importance')
    rf_feature_imp.sort(ascending=False)
    print rf_feature_imp.ix[:5]

    print 'Predictions'
    y_test = test[target]

    probs = rf.predict_proba(X_test)
    print roc_auc_score(y_test, probs[:,1])
    
    s_pred = pandas.Series(data=probs[:,1], name=target, index=test.index)
    predictions = predictions.join(s_pred)
    
    filename = "".join(['mdl_', target, '.pkl'])
    print 'Saving Model %s'%(os.path.join('data/AA/model/', filename))
    joblib.dump(rf, os.path.join('data/AA/model/', filename))

predictions.to_csv('data/AA/predictions.csv',index=False,quoting=csv.QUOTE_ALL) 
