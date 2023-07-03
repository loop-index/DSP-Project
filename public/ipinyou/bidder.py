import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import time
import joblib
import math

# Load datasets


def load_models():
    try:
        bidder = joblib.load('public/ipinyou/models/bidder.pkl')
        user_columns = pd.read_csv(
            'public/ipinyou/models/ctr_columns.csv').columns

    except:
        print("Retraining model... Ctrl+C to cancel")

        imps = pd.read_csv("public/ipinyou/data/imp.20130612.txt",
                           sep='\t', header=None, usecols=[0, 1, 17, 19, 20, 22, 23])
        imps = imps.dropna()
        imps.columns = ['BidID', 'Timestamp', 'FloorPrice',
                        'Bid', 'Paid', 'AdvertiserID', 'UserTags']
        imps['Timestamp'] = pd.to_datetime(
            imps['Timestamp'], format='%y%m%d%H%M%S%f')
        imps['Weekday'] = imps['Timestamp'].dt.weekday
        imps['Hour'] = imps['Timestamp'].dt.hour
        imps = imps.drop(['Timestamp'], axis=1)

        clicks = pd.read_csv(
            "public/ipinyou/data/clk.20130612.txt", sep='\t', usecols=[0], header=None)
        clicks.columns = ['BidID']
        clicks['Clicked'] = 1

        data = pd.merge(imps, clicks, on='BidID', how='left')
        data['Clicked'] = data['Clicked'].fillna(0)
        data = data.drop(['BidID'], axis=1)

        user_tags = data['UserTags'].str.get_dummies(sep=',')
        user_columns = user_tags.columns
        data = data.join(user_tags)

        data = data.drop(['UserTags', 'Paid'], axis=1)
        data = data.drop(['Bid', 'Clicked'], axis=1).join(
            data[['Bid', 'Clicked']])

        print(data.head())

        clicked = data[data['Clicked'] == 1]
        print('Number of clicks:', len(clicked))

        bidder = RandomForestRegressor()
        X_train, X_test, y_train, y_test = train_test_split(
            data.drop(['Bid'], axis=1), data['Bid'], test_size=0.2, random_state=42)
        bidder.fit(X_train, y_train)

        print("Accuracy:", bidder.score(X_test, y_test))

        # Save the model
        joblib.dump(bidder, 'public/ipinyou/models/bidder.pkl')
        pd.DataFrame(columns=user_columns).to_csv(
            'public/ipinyou/models/ctr_columns.csv', index=False)

    return bidder, user_columns

###################################################


advertisers = {1458: 'Chinese vertical e-commerce', 3358: 'Software', 3386: 'International e-commerce', 3427: 'Oil', 3476: 'Tire', 2259: 'Milk powder',
               2261: 'Telecom', 2821: 'Footwear', 2997: 'Mobile e-commerce app install'}

bidder, user_columns = load_models()


def get_bid(user_tags, floor_price, advertiserID, ctr):
    # Create a dataframe with the input data
    input_data = pd.DataFrame(
        {'FloorPrice': floor_price, 'AdvertiserID': advertiserID}, index=[0], dtype='int64')

    # Set the weekday and hour
    now = pd.Timestamp.now()
    input_data['Weekday'] = now.weekday()
    input_data['Hour'] = now.hour

    # Set the user tags to 1
    input_data = input_data.join(pd.DataFrame(
        columns=user_columns, data=np.zeros((1, len(user_columns)))))
    for tag in user_tags:
        if tag in user_columns:
            input_data[tag] = 1

    input_data['Clicked'] = round(ctr)

    # Predict the bid
    bid = bidder.predict(input_data)[0]

    return {
        'bid': bid,
    }
