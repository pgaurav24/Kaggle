import pandas
import numpy
import random
import os
import csv
import re
import extract_table as tt

from sklearn.ensemble  import RandomForestRegressor
from sklearn.metrics   import mean_squared_error
from sklearn.externals import joblib

trainfile = 'yelp_training_set_A.csv'
validatefile = 'yelp_training_set_B.csv'
target = 'review_votes_useful'


train = pandas.read_csv(os.path.join(tt.traindir, 'yelp_training_set_A.csv'), quotechar='"')
test  = pandas.read_csv(os.path.join(tt.traindir, 'yelp_training_set_B.csv'), quotechar='"')

print train.shape
print test.shape

predictions = pandas.DataFrame(index=test.index) 
predictions = predictions.join( pandas.Series(data=test[target], name='actual', index=test.index) )

rf = RandomForestRegressor(n_estimators=100, max_features=20,\
                    max_depth=10, min_samples_leaf=5, n_jobs=-1)

print 'Training RF Model - %s' % target
y_train = train[target]
y_train = y_train.apply(lambda x: numpy.log(x+1.))
X_train = train.drop(target,1)

rf.fit(X_train, y_train)

rf_feature_imp = pandas.Series(rf.feature_importances_, index=X_train.columns.values, name='Importance')
rf_feature_imp.sort(ascending=False)
print rf_feature_imp.ix[:20]

print 'Predictions'
y_test = test[target]
y_test = y_test.apply(lambda x: numpy.log(x+1.))
X_test = test.drop(target,1)

y_pred = rf.predict(X_test)
print mean_squared_error(y_test, y_pred)

yy1 = pandas.Series(data=y_test, name='scaled', index=test.index)
yy2 = pandas.Series(data=y_pred, name='predicted', index=test.index)
predictions = predictions.join(yy1)
predictions = predictions.join(yy2)

filename = "".join(['mdl_', target, '.pkl'])
filepath = os.path.join(tt.traindir,'model' ,filename)
print 'Saving Model %s'%(filepath)
#joblib.dump(rf, filepath)
predictions.to_csv(os.path.join(tt.traindir, 'yelp_predictions_set_B1.csv'),index=False,quoting=csv.QUOTE_ALL) 
