rm(list=ls())
setwd('/Users/prashant/workspace/ExData')

library(plyr)
library(ggplot2)
library(gridExtra)

names <- c('imdbID', 'title', 'year', 'score', 'votes', 'runtime', 'genres')

imdb <- read.csv(file='imdb_top_10000.txt', sep='\t', header=FALSE)
colnames(imdb) <- names

imdb$runtime <- lapply(strsplit(as.character(imdb$runtime)," ", fixed=TRUE), function(v) (v[1])) 
imdb$runtime <- as.integer(imdb$runtime)
imdb$title <- lapply(strsplit(as.character(imdb$title),"(", fixed=TRUE), function(v) v[1]) 

list.genres <- strsplit(as.character(imdb$genres), '|', fixed=TRUE)
all.genres <- list()
for (g in list.genres) {
  all.genres <- union(all.genres, g)
}
all.genres <- paste(all.genres)

for (gg in all.genres) {
  ll <- lapply(list.genres, function(v) return((gg %in%  v)))
  imdb[, gg] <- unlist(ll) 
} 

summary(subset(imdb,select=c('score','runtime','year','votes')))

nrow(subset(imdb, runtime == 0))
imdb$runtime[imdb$runtime == 0] <- NA
summary(imdb$runtime)

qplot(year, data=imdb, xlim = c(1950, 2012), binwidth=1, xlab='Release Year')
qplot(score, data=imdb, binwidth=0.2, xlab='IMDB Rating')
qplot(runtime, data=imdb, binwidth=10, xlab='RunTime Distribution')

qplot(year, score,  data=imdb, xlab='Release Year', ylab='IMDB Rating')
qplot(log(votes), score,  data=imdb, xlab='Number of Votes', ylab='IMDB Rating')

min.score <- imdb$score[which.min(imdb$score)]
subset(imdb, score == min.score, select=c('title', 'score', 'year','votes'))

max.score <- imdb$score[which.max(imdb$score)]
subset(imdb, score == max.score, select=c('title', 'score', 'year','votes'))

genre.count <- colSums(subset(imdb, select=all.genres))
sort(genre.count, decreasing=TRUE)

genre.count <- rowSums(subset(imdb, select=all.genres))
summary(genre.count)

imdb$decade <- floor(imdb$year/10)*10
decade.mean <- ddply(imdb, .(decade), summarize, mean_score = mean(score))

ggplot(data=imdb, aes(year, score)) + geom_point(shape=1) + 
  geom_line(data=decade.mean, aes(decade, mean_score, colour='Red', size=0.1)) + 
  scale_x_continuous(breaks=seq(1940,2020, by=10)) + 
  scale_y_continuous(breaks=seq(0,10, by=1))

plots <- list()
i <- 1
for (gg in all.genres) {
  imdb.subset <- subset(imdb, imdb[[gg]] == TRUE, select=c('year'))  
  
  plots[[i]]  <- ggplot(data=imdb, aes(x=year)) + 
  geom_density(data=imdb.subset, fill='red', alpha = 0.2, binwidth=10) +
  geom_density(data=imdb, fill='gray', alpha = 0.2, binwidth=10) +
  ggtitle(gg)
  
  i <- i+1
}
do.call(grid.arrange, plots)