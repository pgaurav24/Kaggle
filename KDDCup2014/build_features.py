import sys, csv
import pandas
import numpy
import build_features

def school_metro_b(data):
    return data['school_metro'].fillna('#NA')

def primary_focus_subject_b(data):
    return data['primary_focus_subject'].fillna('#NA')
 
def primary_focus_area_b(data):
    return data['primary_focus_area'].fillna('#NA')

def secondary_focus_subject_b(data):
    return data['secondary_focus_subject'].fillna('#NA')
 
def secondary_focus_area_b(data):
    return data['secondary_focus_area'].fillna('#NA')

def resource_type_b(data):
    return data['resource_type'].fillna('#NA')

def grade_level_b(data):
    return data['grade_level'].fillna('#NA')

def fulfillment_labor_materials_b(data):
    df = pandas.Series(pandas.cut(data.fulfillment_labor_materials, 3), index=data.index, name='fulfillment_labor_materials_b') 
    return df.fillna('#NA')
 
def students_reached_b(data):
    df = pandas.Series(pandas.qcut(data.students_reached, 5), index=data.index, name='students_reached_b') 
    return df.fillna('#NA')

def total_amount_b(data):
    df = pandas.Series(pandas.qcut(data.total_amount, 5), index=data.index, name='total_amount_b') 
    return df.fillna('#NA')
    
def extract_features(feature_names, data):
    feat = pandas.DataFrame(index=data.index)
    for fname in feature_names:
            if fname in data:
                feat = feat.join(data[fname])
            else:
                d = getattr(build_features, fname)(data)
                d.name = fname
                feat = feat.join(d)
    return feat

if __name__ == "__main__":
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
 
    data = pandas.read_csv('data/test.csv', quotechar='"')
    features = extract_features(feature_names, data)
    features.to_csv('data/features.csv',index=False,quoting=csv.QUOTE_ALL) 
