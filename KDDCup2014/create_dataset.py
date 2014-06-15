import hashlib
import pandas
import csv
import sys

target_vars = ['is_exciting',\
               'fully_funded',\
               'at_least_1_teacher_referred_donor',\
               'great_chat',\
               'at_least_1_green_donation',\
               'three_or_more_non_teacher_referred_donors',\
               'one_non_teacher_referred_donor_giving_100_plus',\
               'donation_from_thoughtful_donor']

def hbucket(s):
    m = hashlib.md5()
    m.update(s)
    return int(m.hexdigest(),16)%1000

cutoff='2014-01-01'

projects = pandas.read_csv('data/dataset/projects.csv')
outcomes = pandas.read_csv('data/dataset/outcomes.csv')
resources = pandas.read_csv('data/dataset/resources.csv')
essay = pandas.read_csv('data/dataset/essays.csv',quotechar='"')

resources['total_amount'] = resources['item_unit_price']*resources['item_quantity']
resources_grp = resources.groupby('projectid')['total_amount'].sum().reset_index()

outcomes_new = pandas.DataFrame(index=outcomes.index)
outcomes_new = outcomes_new.join(outcomes['projectid'])

for target in target_vars:
    ff = (outcomes[target].fillna('f') == 't')
    outcomes_new = outcomes_new.join(ff)

proj_outc = projects.merge(outcomes_new, on='projectid', how='left') 
proj_outc_reso = proj_outc.merge(resources_grp, on='projectid', how='left') 
dataset = proj_outc_reso.merge(essay, on=['projectid','teacher_acctid'], how='inner') 

for target in target_vars:
    dataset[target].fillna(False, inplace=True)

dataset['atleast_one_cond'] = dataset['three_or_more_non_teacher_referred_donors'] | \
                              dataset['one_non_teacher_referred_donor_giving_100_plus'] | \
                              dataset['donation_from_thoughtful_donor']

dataset['atleast_one_feature'] = dataset['fully_funded'] | \
                                 dataset['at_least_1_teacher_referred_donor'] | \
                                 dataset['great_chat'] | \
                                 dataset['at_least_1_green_donation'] | \
                                 dataset['atleast_one_cond']

print outcomes.shape, projects.shape, dataset.shape
    
dataset[dataset.date_posted <  cutoff].to_csv('data/train.csv',index=False,quoting=csv.QUOTE_ALL) 
dataset[dataset.date_posted >= cutoff].to_csv('data/test.csv',index=False,quoting=csv.QUOTE_ALL) 
