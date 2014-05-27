import sys,csv
import pandas
import numpy

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.feature_extraction import DictVectorizer

import build_features

feature_names = [ 'school_metro_b',\
                  'school_charter',\
                  'school_magnet',\
                  'school_year_round',\
                  'school_nlns',\
                  'school_kipp',\
                  'school_charter_ready_promise',\
                  'teacher_prefix',\
                  'teacher_teach_for_america',\
                  'teacher_ny_teaching_fellow',\
                  'primary_focus_subject_b',\
                  'primary_focus_area_b',\
                  'secondary_focus_subject_b',\
                  'secondary_focus_area_b',\
                  'poverty_level',
                  'resource_type_b',\
                  'fulfillment_labor_materials_b',\
                  'total_price_excluding_optional_support',\
                  'total_price_including_optional_support',\
                  'eligible_double_your_impact_match',\
                  'eligible_almost_home_match',\
                  'students_reached_b',\
                  'total_amount_b']
 
features_numeric = ['total_price_excluding_optional_support', 'total_price_including_optional_support'] 


full_train_file = 'data/train.csv'
train_file = 'data/train-A.csv'
test_file  = 'data/train-B.csv'
probe_file = 'data/test.csv'

print 'Loading data'
train = pandas.read_csv(train_file, quotechar='"')
test  = pandas.read_csv(test_file, quotechar='"')
probe = pandas.read_csv(probe_file, quotechar='"')

print 'Building features'
train_features = build_features.extract_features(feature_names, train)
test_features = build_features.extract_features(feature_names, test)
probe_features = build_features.extract_features(feature_names, probe)

num_train_features = train_features[features_numeric].as_matrix()
num_test_features  = test_features[features_numeric].as_matrix()
num_probe_features = probe_features[features_numeric].as_matrix()

cat_train_features = train_features.drop(features_numeric, axis=1)
cat_test_features  = test_features.drop(features_numeric, axis=1)
cat_probe_features = probe_features.drop(features_numeric, axis=1)

d_train_features = cat_train_features.T.to_dict().values()
d_test_features  = cat_test_features.T.to_dict().values()
d_probe_features = cat_probe_features.T.to_dict().values()

vectorizer = DictVectorizer(sparse=False)
vec_train_features = vectorizer.fit_transform(d_train_features)
X_train = numpy.hstack((vec_train_features, num_train_features))
y_train = (train['is_exciting'] == 't')*1

print 'Training RF Model'
rf = RandomForestClassifier(n_estimators=50, max_features=10, max_depth=10, min_samples_leaf=5, n_jobs=-1, compute_importances=True)
rf.fit(X_train, y_train)

rf_features = vectorizer.get_feature_names()
rf_features.extend(features_numeric)
rf_feature_imp = pandas.Series(rf.feature_importances_,index=rf_features,name='Importance')
rf_feature_imp.sort(ascending=False)

print rf_feature_imp.ix[:10]

print 'Predictions'
vec_test_features = vectorizer.transform(d_test_features)
X_test = numpy.hstack((vec_test_features, num_test_features))
y_test = (test['is_exciting'] == 't')*1.0

probs = rf.predict_proba(X_test)
print roc_auc_score(y_test, probs[:,1])

vec_probe_features = vectorizer.transform(d_probe_features)
X_probe = numpy.hstack((vec_probe_features, num_probe_features))
probe_probs = rf.predict_proba(X_probe)

df_pred = pandas.DataFrame(index=probe.index)
df_probs = pandas.Series(data=probe_probs[:,1], index=df_pred.index, name='is_exciting')
df_pred = df_pred.join(probe.projectid)
df_pred = df_pred.join(df_probs)
df_pred.to_csv('data/submissions_2.csv',index=False) 

