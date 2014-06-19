rm(list=ls())

library(plyr)
library(ggplot2)
library(reshape)

train.dir <- '/Users/prashant/workspace/Kaggle/YelpChallenge/data/yelp_training_set/'
yelp.data <- read.csv(file=paste(train.dir, 'yelp_training_set.csv', sep=""), quote='\"', header=TRUE)

features.user <- c('user_review_count', 'user_average_stars', 'user_votes_useful', 'user_votes_funny', 'user_votes_cool')
features.business <- c('business_latitude', 'business_longitude', 'business_stars', 'business_review_count', 'business_open') 
features.checkin <- c('checkin_count_sun', 'checkin_count_mon', 'checkin_count_tue', 'checkin_count_wed', 'checkin_count_thu', 'checkin_count_fri', 'checkin_count_sat')

summary(subset(yelp.data, select=c('review_stars','review_date','review_votes_useful', features.user, features.business, features.checkin)))
                                                               
ggplot(data=yelp.data, aes(x=log(1+review_votes_useful))) + 
  geom_histogram(binwidth=0.1, colour="black", fill="white")
summary(yelp.data$review_votes_useful)
summary(log(1+yelp.data$review_votes_useful))

ggplot(data=yelp.data, aes(x=user_votes_funny,y=review_votes_useful)) + geom_point(shape=1) + geom_smooth(method=lm) 

ggplot(data=yelp.data, aes(x=review_votes_useful)) + 
  geom_histogram(binwidth=1.0, colour="black", fill="white") + facet_grid(review_stars ~ .)

yelp.data$review_date <- as.Date(yelp.data$review_date)
ggplot(data=yelp.data, aes(x=review_date)) + 
  geom_histogram(binwidth=90, colour="black", fill="white")

checkin <- subset(yelp.data, select=features.checkin) 
colnames(checkin) <- c('sun','mon','tue','wed','thu','fri','sat')
m.checkin <- melt(checkin)
mm <- ddply(m.checkin, .(variable), summarise, avg.checkin=mean(value, na.rm=T)) 
ggplot(data=mm, aes(x=factor(variable), y=avg.checkin)) + geom_bar(stat="identity")

features <- c(features.user, features.business, features.checkin)
c.list <- list()
for (uu in features) {
  if (uu == 'business_open')
    next
  c.list[[uu]] <- cor(x=yelp.data$review_votes_useful, y=yelp.data[[uu]], use="pairwise.complete.obs", method="pearson")
}

uu <- melt(as.data.frame(c.list))
ggplot(data=uu, aes(x=factor(variable), y=value)) + geom_bar(stat="identity") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

#table(yelp.data$business_open, yelp.data$review_stars)

per.business <-  ddply(yelp.data, .(business_id), summarize, num_rec=length(business_id), mean_votes=mean(review_votes_useful))
ggplot(data=per.business, aes(x=mean_votes)) + 
  geom_histogram(binwidth=0.1, colour="black", fill="white")


