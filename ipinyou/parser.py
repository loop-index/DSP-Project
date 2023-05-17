import pandas as pd
import numpy as np
import dicts
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, f1_score
from sklearn.multioutput import MultiOutputClassifier, MultiOutputRegressor
import time, joblib

# Load datasets
try:
    prompt = input('Do you want to retrain the model? (y/N): ')
    if prompt == 'y':
        raise Exception('Retrain model')
    
    bidder = joblib.load('ipinyou/models/bidder.pkl')
    model = joblib.load('ipinyou/models/model.pkl')
    user_columns = pd.read_csv('ipinyou/models/user_columns.csv').columns

except:
    imps = pd.read_csv("ipinyou/data/imp.20130612.txt", sep='\t', header=None, usecols=[0, 17, 19, 20, 22, 23], nrows=1000000)
    imps = imps.dropna()
    imps.columns = ['BidID', 'FloorPrice', 'Bid', 'Paid', 'AdvertiserID', 'UserTags']

    clicks = pd.read_csv("ipinyou/data/clk.20130612.txt", sep='\t', usecols=[0], header=None)
    clicks.columns = ['BidID']
    clicks['Clicked'] = 1

    conv = pd.read_csv("ipinyou/data/conv.20130612.txt", sep='\t', usecols=[0], header=None)
    conv.columns = ['BidID']
    conv['Converted'] = 1

    data = pd.merge(imps, clicks, on='BidID', how='left')
    data['Clicked'] = data['Clicked'].fillna(0)
    data = pd.merge(data, conv, on='BidID', how='left')
    data['Converted'] = data['Converted'].fillna(0)
    data = data.drop(['BidID'], axis=1)

    print(data.head())

    user_tags = data['UserTags'].str.get_dummies(sep=',')
    user_columns = user_tags.columns
    data = data.join(user_tags)

    data = data.drop(['UserTags', 'Paid'], axis=1)
    data = data.drop(['Bid', 'Clicked', 'Converted'], axis=1).join(data[['Bid', 'Clicked', 'Converted']])

    clicked = data[data['Clicked'] == 1]
    print('Number of clicks:', len(clicked))

    converted = data[data['Converted'] == 1]
    print('Number of conversions:', len(converted))

    bidder = RandomForestRegressor()
    X_train, X_test, y_train, y_test = train_test_split(data.drop(['Bid', 'Converted'], axis=1), data['Bid'], test_size=0.2, random_state=42)
    bidder.fit(X_train, y_train)

    print("Accuracy:", bidder.score(X_test, y_test))

    model = RandomForestClassifier()
    X_train, X_test, y_train, y_test = train_test_split(data.drop(['Clicked', 'Converted'], axis=1), data['Clicked'], test_size=0.2, random_state=42)
    model.fit(X_train, y_train)

    print("Accuracy:", model.score(X_test, y_test))

    # Save the model
    joblib.dump(bidder, 'ipinyou/models/bidder.pkl')
    joblib.dump(model, 'ipinyou/models/model.pkl')
    pd.DataFrame(columns=user_columns).to_csv('ipinyou/models/user_columns.csv', index=False)

###################################################

advertisers = {1458: 'Chinese vertical e-commerce', 3358: 'Software', 3386: 'International e-commerce', 3427: 'Oil', 3476: 'Tire', 2259: 'Milk powder', 
               2261: 'Telecom', 2821: 'Footwear', 2997: 'Mobile e-commerce app install'}

while True:
    user = input("User Tags: ").split(',')
    floor_price = int(input("Floor Price: "))

    # Create a dataframe with the input data
    input_data = pd.DataFrame({'FloorPrice': floor_price, 'AdvertiserID': 0}, index=[0], dtype='int64')
    input_data = input_data.join(pd.DataFrame(columns=user_columns, data=np.zeros((1, len(user_columns)))))

    # Set the user tags to 1
    for tag in user:
        if tag in user_columns:
            input_data[tag] = 1

    # Set the advertiser ID
    start = time.time()
    for advertiser in advertisers:
        input_data['AdvertiserID'] = advertiser
        if 'Bid' in input_data.columns:
            input_data = input_data.drop(['Bid'], axis=1)
        input_data['Clicked'] = 1
        print("Advertiser:", advertisers[advertiser])

        # Make predictions
        bid_pred = bidder.predict(input_data)[0]
        print("\tPredicted bid:", bid_pred)

        # Predict if the user will click
        input_data['Bid'] = bid_pred
        if 'Clicked' in input_data.columns:
            input_data = input_data.drop(['Clicked'], axis=1)
        click_pred = model.predict(input_data)[0]
        print("\tPredicted click:", click_pred)

    print("Time taken:", (time.time() - start) * 1000, "ms")


