#! /usr/bin/python

import pandas as pd 
import numpy  as np
import matplotlib.pyplot as plt

from pandas import Series
from pandas import DataFrame

def fdist(x):
    return x/x.sum()

def entropy(x):
    prob_i = x/x.sum()
    prob_i[prob_i==0] = 1
    return -1.0*np.sum(prob_i.values*numpy.log2(prob_i.values))

def conditional_entropy(X):
    e = X.apply(entropy, 1)
    row_sum = X.apply(np.sum, 1)
    prob_xi =  row_sum/row_sum.sum()
    return np.sum(prob_xi.values*e.values)

def mutual_information(X):
    col_sum = X.apply(np.sum, 0) 
    ey = entropy(col_sum)
    ey_x = conditional_entropy(X)
    return ey-ey_x

