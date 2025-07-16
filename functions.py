''' function to handle missing data and delete ID column '''

def basic_preprocessing_baseline(df):
    
    # fill NaN total_male/total_female with 0
    df['total_male'] = df['total_male'].fillna(0)
    df['total_female'] = df['total_female'].fillna(0)
    
    # fill NaN travel_with with missing
    df['travel_with'] = df['travel_with'].fillna('missing')
    
    # fill NaN most_impressing with "No comments"
    df['most_impressing'] = df['most_impressing'].fillna('No comments')
   
    # drop id column
    df = df.drop(['ID'], axis =1)
    
    return df

''' more complete function to handle missing data and to make some adjustments in the data set '''

def adjustments_full(df):
    
    # fill NaN total_male/total_female with 0
    df['total_male'] = df['total_male'].fillna(0)
    df['total_female'] = df['total_female'].fillna(0)
    
    # add a column group_size based on total_male/total_female
    df['group_size'] = df['total_female'] + df['total_male']
    
    # fill NaN travel_with with "Alone" if group_size is one
    df.loc[df.group_size == 1, 'travel_with'] = 'Alone'
    
    # fill remaining NaN travel_with with missing
    df['travel_with'] = df['travel_with'].fillna('missing')

    # handle group_size equals zero: either replace by 1 if alone traveller or median group size of the train data
    df.loc[(df.group_size == 0) & (df.travel_with == 'Alone'), 'group_size'] = 1
    df.loc[df.group_size == 0, 'group_size'] = train['group_size'].median()

    # add column group_size_binned
    bins_gs = [0,1,2,5,10,15,100]
    labels_gs = ['1 traveller','2 travellers', '3-5 travellers', '6-10 travellers', '11-15 travellers', 'more than 15 travellers']
    df['group_size_binned'] = pd.cut(df['group_size'], bins=bins_gs, labels=labels_gs)
    df['group_size_binned'] = df['group_size_binned'].astype('object')

    # drop total_male, total_female and group_size 
    df = df.drop(['total_male'], axis =1)
    df = df.drop(['total_female'], axis =1)
    df = df.drop(['group_size'], axis =1)
    
    # drop most_impressing
    df = df.drop(['most_impressing'], axis =1)

    # drop id column
    df = df.drop(['ID'], axis =1)
    
    # drop purpose column
    df = df.drop(['purpose'], axis =1)

    # drop info_source column
    df = df.drop(['info_source'], axis =1)

    # drop tour_arrangement column
    df = df.drop(['tour_arrangement'], axis =1)

    # drop payment_mode column
    df = df.drop(['payment_mode'], axis =1)

    # drop first_trip_tz column
    df = df.drop(['first_trip_tz'], axis=1)

    # add subregions just as in the EDA
    df['country'] = df['country'].str.lower()
    df = df.replace({'country' : {'united states of america': 'united States', 'swaziland' : 'eswatini', 'cape verde' : 'cabo verde', 'swizerland' : 'switzerland', 'ukrain' : 'ukraine','malt' : 'malta', 'burgaria' : 'bulgaria', 'korea' : 'south korea', 'comoro' : 'comoros', 'scotland' : 'united kingdom', 'russia' : 'russia', 'srilanka': 'sri lanka'}})
    df = df.replace({'country' : {'ivory coast': "côte d'ivoire", 'drc' : 'congo', 'uae' : 'united arab emirates', 'trinidad tobacco' : 'trinidad and tobago', 'costarica' : 'costa rica', 'philipines' : 'philippines', 'djibout' : 'djibouti', 'morroco' : 'morocco'}})
    df['country'] = df['country'].str.capitalize()
    df = pd.merge(df, subregions, how ='left')

    # drop country column
    df = df.drop(['country'], axis =1)

     # bin night_mainland and night_zanzibar columns
    bins = [-1,0,7,14,21,28,56,1000]
    labels = ['none','up to 1 week', '1-2 weeks', '2-3 weeks', '3-4 weeks', '4-8 weeks', 'more than 8 weeks']
    df['nights_zanzibar_binned'] = pd.cut(df['night_zanzibar'], bins=bins, labels=labels)
    df['nights_mainland_binned'] = pd.cut(df['night_mainland'], bins=bins, labels=labels)

    # delete night_mainland and night_zanzibar columns
    df = df.drop(['night_mainland'], axis =1)
    df = df.drop(['night_zanzibar'], axis =1)

    df['nights_zanzibar_binned'] = df['nights_zanzibar_binned'].astype('object')
    df['nights_mainland_binned'] = df['nights_mainland_binned'].astype('object')
    
    return df