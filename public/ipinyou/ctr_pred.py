import pandas as pd
import numpy as np
import dicts
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, f1_score
from sklearn.multioutput import MultiOutputClassifier, MultiOutputRegressor
import time
import joblib

# Load datasets
try:
    prompt = input('Do you want to retrain the model? (y/N): ')
    if prompt == 'y':
        raise Exception('Retrain model')

    model = joblib.load('ipinyou/models/ctr_model.pkl')
    user_columns = pd.read_csv('ipinyou/models/ctr_columns.csv').columns

except:
    imps = pd.read_csv("ipinyou/data/imp.20130612.txt", sep='\t',
                       header=None, usecols=[0, 17, 19, 20, 22, 23], nrows=1000000)
    imps = imps.dropna()
    imps.columns = ['BidID', 'FloorPrice', 'Bid',
                    'Paid', 'AdvertiserID', 'UserTags']

    clicks = pd.read_csv("ipinyou/data/clk.20130612.txt",
                         sep='\t', usecols=[0], header=None)
    clicks.columns = ['BidID']
    clicks['Clicked'] = 1

    data = pd.merge(imps, clicks, on='BidID', how='left')
    data['Clicked'] = data['Clicked'].fillna(0)
    data = data.drop(['BidID'], axis=1)
    data = data.drop(['Bid', 'Clicked'], axis=1).join(data[['Bid', 'Clicked']])

    data = data.groupby(['AdvertiserID', 'UserTags'])
    clicks = data['Clicked'].sum()
    impressions = data['Clicked'].size()
    ctr = clicks / impressions
    # print(data.head())
    # print(ctr)

    ctr_pos = ctr.to_frame().reset_index()
    ctr_pos.columns = ['AdvertiserID', 'UserTags', 'CTR']

    user_tags = ctr_pos['UserTags'].str.get_dummies(sep=',')
    user_columns = user_tags.columns
    ctr_pos = ctr_pos.join(user_tags)

    ctr_pos = ctr_pos.drop(['UserTags'], axis=1)
    print(ctr_pos)

    X = ctr_pos.drop(['CTR'], axis=1)
    y = ctr_pos['CTR']
    model = RandomForestRegressor()

    model.fit(X, y)
    print("Accuracy:", model.score(X, y))

    joblib.dump(model, 'ipinyou/models/ctr_model.pkl')
    pd.DataFrame(columns=user_columns).to_csv(
        'ipinyou/models/ctr_columns.csv', index=False)

###################################################

advertisers = {1458: 'Chinese vertical e-commerce', 3358: 'Software', 3386: 'International e-commerce', 3427: 'Oil', 3476: 'Tire', 2259: 'Milk powder',
               2261: 'Telecom', 2821: 'Footwear', 2997: 'Mobile e-commerce app install'}

while True:
    user = input("User Tags: ").split(',')

    # Create a dataframe with the input data
    input_data = pd.DataFrame({'AdvertiserID': 0}, index=[0], dtype='int64')
    input_data = input_data.join(pd.DataFrame(
        columns=user_columns, data=np.zeros((1, len(user_columns)))))

    # Set the user tags to 1
    for tag in user:
        if tag in user_columns:
            input_data[tag] = 1

    # Set the advertiser ID
    start = time.time()
    max_ctr = 0
    max_advertiser = "Random"

    for advertiser in advertisers:
        input_data['AdvertiserID'] = advertiser
        pred = model.predict(input_data)[0]
        if pred > max_ctr:
            max_ctr = pred
            max_advertiser = advertisers[advertiser]

    print("Max CTR:", max_advertiser + ':', '{:.2%}'.format(max_ctr))

    print("Time taken:", '{:.2f}ms'.format((time.time() - start) * 1000))
