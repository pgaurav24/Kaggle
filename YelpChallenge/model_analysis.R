rm(list=ls())

library(plyr)
library(ggplot2)
library(reshape)

train.dir <- '/Users/prashant/workspace/Kaggle/YelpChallenge/data/yelp_training_set/'
yelp.pred <- read.csv(file=paste(train.dir, 'yelp_predictions_set_B1.csv', sep=""), quote='\"', header=TRUE)
yelp.pred$predicted_adj <- exp(yelp.pred$predicted)-1

ggplot(data=yelp.pred, aes(x=actual,y=predicted_adj)) + geom_point(shape=1) + geom_smooth(method=lm) 