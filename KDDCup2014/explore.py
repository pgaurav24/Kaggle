import sys
import pandas
import numpy
import matplotlib.pyplot as plt
import eda_utilities as eda

def main(infile):
    train_data = pandas.read_csv(infile,quotechar='"')
    
    features_lla = ['schoolid','school_ncesid','school_city','school_state','school_district','school_county']

    features_cat = ['school_metro','school_charter','school_magnet', 'school_year_round','school_nlns','school_kipp', 'school_charter_ready_promise',\
                'teacher_prefix','teacher_teach_for_america','teacher_ny_teaching_fellow',\
                'primary_focus_subject','primary_focus_area','secondary_focus_subject','secondary_focus_area',\
                'resource_type','poverty_level','grade_level']

    features_con = ['fulfillment_labor_materials','total_price_excluding_optional_support','total_price_including_optional_support',\
                'students_reached', 'eligible_double_your_impact_match', 'eligible_almost_home_match', 'total_amount']

    train_data['is_exciting_b'] = 1.0*(train_data['is_exciting'] == 't')   
    
    #n_col = 4
    #n_row = len(features_cat)/n_col + 1*(len(features_cat)%n_col > 0)
    #plt.subplot(n_row, n_col, i+1)
    #x.plot(kind='bar')
    #plt.show()

    print('# Categorical Features = %d'% (len(features_cat)))
    for i, feature_name in enumerate(features_cat):
        x = train_data.groupby(feature_name)['is_exciting_b'].mean()
        print(x)
        print('NaN - %d of %d'% (sum(pandas.isnull(train_data[feature_name])),len(train_data[feature_name])))
        print("------------------------------------------------")
    
    print('# Numeric Features = %d'% (len(features_con)))
    for i, feature_name in enumerate(features_con):
        print(train_data[feature_name].describe())
        print('NaN - %d of %d'% (sum(pandas.isnull(train_data[feature_name])),len(train_data[feature_name])))
        print("------------------------------------------------")

if __name__ == "__main__":
    infile = sys.argv[1]
    main(infile)
