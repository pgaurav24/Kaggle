rm(list=ls())

library(plyr)
library(ggplot2)
library(reshape)

train.dir <- '/Users/prashant/workspace/Kaggle/YelpRecSys2013/data/yelp_training_set/'
yelp.data <- read.csv(file=paste(train.dir, 'yelp_training_set.csv', sep=""), quote='\"', header=TRUE)

features.user <- c('user_review_count', 
                   'user_average_stars',
                   'user_votes_useful',
                   'user_votes_funny',
                   'user_votes_cool')

features.business <- c('latitude',
                       'longitude',
                       'business_stars',
                       'business_review_count',
                       'business_open')

features.checkin <- c('checkin_count_sun',
                      'checkin_count_mon',
                      'checkin_count_tue',
                      'checkin_count_wed',
                      'checkin_count_thu',
                      'checkin_count_fri',
                      'checkin_count_sat')

summary(subset(yelp.data, select=c('review_stars','review_date',
                                   features.user,
                                   features.business,
                                   features.checkin)))
                                                               
ggplot(data=yelp.data, aes(x=review_stars)) + 
  geom_histogram(aes(y=..density..), binwidth=1.0, colour="black", fill="white")
summary(yelp.data$review_stars)

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
  c.list[[uu]] <- cor(x=yelp.data$review_stars, y=yelp.data[[uu]], use="pairwise.complete.obs", method="pearson")
}

uu <- melt(as.data.frame(c.list))
ggplot(data=uu, aes(x=factor(variable), y=value)) + geom_bar(stat="identity") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

#table(yelp.data$business_open, yelp.data$review_stars)

per.business <-  ddply(yelp.data, .(business_id), summarize, nr=length(business_id), mr=mean(review_stars))
ggplot(data=per.business, aes(x=mr)) + 
  geom_histogram(binwidth=0.1, colour="black", fill="white")
ggplot(data=per.business, aes(x=nr)) + 
  geom_histogram(binwidth=10, colour="black", fill="white") + scale_x_continuous(limits=c(0, 250))


