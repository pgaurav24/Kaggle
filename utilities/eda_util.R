rm(list=ls());
library(gmodels);
library(plyr);

`%ni%` <- Negate(`%in%`);

fdist <- function(x)
{
    t <- table(x, exclude=NULL);
    t1 <- cbind(t);
    n <- length(x);
    t_per <- round(t1/n * 100,2);
    res <- cbind(t1, t_per);
    colnames(res) <- c("Count", "Percentage");
    return(res);
}

rmse <- function(x,y)
{
    sse <- sum((x-y)*(x-y));
    mse <- sse/length(x);
    rmse <- sqrt(mse);
    return(rmse);
}

mad <- function(x,y)
{
    mad <- sum(abs(x-y))/length(x);
    return(mad);
}

aggregate_stats <- function(x,y,lab)
{
    l<-aggregate(x~y,FUN=length);
    m<-aggregate(x~y,FUN=mean);
    s<-aggregate(x~y,FUN=sd);
    R<-cbind(l,m,s);
    Q<-R[,c(1,2,4,6)];
    # names(Q)<-c(names(Q)[1],"count","mean","std");
    names(Q)<-c(lab,"count","mean","std");
    Q.subset <- subset(Q,Q$count>=50);
    Q.sort <- Q.subset[order(-Q.subset$count,na.last=TRUE), ]
    return(Q.sort);
}

frequency_distribution <- function(x)
{
    x.freq = table(x);
    total <- sum(x.freq);
    x.rel_freq <- 100.0* x.freq/total;
    R = cbind(x.freq, x.rel_freq);
    return(R);
}


entropy <- function(x)
{
    row_sum <- sum(x);
    prob_i <- x/row_sum;
    prob_i[prob_i==0] = 1;
    return(sum(-1.0 * prob_i * log(prob_i)));
}

conditional_entropy <- function(X)
{
    e <- apply(X,1,entropy);
    num_elements <- margin.table(X);
    row_totals <- margin.table(X,1);
    return(sum(row_totals * e)/num_elements);
}

information_gain <- function(x,y)
{
    Xtab <- table(x,y,exclude=NULL);
    col_totals <- margin.table(Xtab,2);
    ey <- entropy(col_totals);
    ey_x <- conditional_entropy(Xtab);
    ig <- ey -ey_x;
    return(ig);
}

information_gain_ratio <- function(x,y)
{
    Xtab <- table(x,y);
    col_totals <- margin.table(Xtab,2);
    ey <- entropy(col_totals);
    ey_x <- conditional_entropy(Xtab);
    ig <- ey -ey_x;
    row_totals <- margin.table(Xtab,1);
    iv <- entropy(row_totals);
    igr <- ig/iv;
    return(igr);
}
