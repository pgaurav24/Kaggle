import hashlib
import pandas
import csv
import sys

def hbucket(s):
    m = hashlib.md5()
    m.update(s)
    return int(m.hexdigest(),16)%1000

def main(cutoff='2014-01-01'):
    projects = pandas.read_csv('data/dataset/projects.csv')
    outcomes = pandas.read_csv('data/dataset/outcomes.csv')
    resources = pandas.read_csv('data/dataset/resources.csv')
    essay = pandas.read_csv('data/dataset/essays.csv',quotechar='"')
    
    resources['total_amount'] = resources['item_unit_price']*resources['item_quantity']
    
    resources_col = resources.groupby('projectid')['total_amount'].sum().reset_index()
    #resources_f2 = resources.groupby('projectid')['project_resource_type'].apply(lambda x: x.unique().tolist())

    proj_outc = projects.merge(outcomes, on='projectid', how='left') 
    proj_outc_reso = proj_outc.merge(resources_col, on='projectid', how='left') 
    dataset = proj_outc_reso.merge(essay, on=['projectid','teacher_acctid'], how='inner') 
    
    print outcomes.shape, projects.shape, dataset.shape
    
    dataset[dataset.date_posted <  cutoff].to_csv('data/train.csv',index=False,quoting=csv.QUOTE_ALL) 
    dataset[dataset.date_posted >= cutoff].to_csv('data/test.csv',index=False,quoting=csv.QUOTE_ALL) 

if __name__ == "__main__":
    main()
