import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import time, joblib, db_main, random

# Load datasets
def load_models():
    try:
        model = joblib.load('public/ipinyou/models/ctr_model.pkl')
        user_columns = pd.read_csv('public/ipinyou/models/ctr_columns.csv').columns

    except:
        print("Retraining model... Ctrl+C to cancel")
        imps = pd.read_csv("public/ipinyou/data/imp.20130612.txt", sep='\t', header=None, usecols=[0, 17, 19, 20, 22, 23])
        imps = imps.dropna()
        imps.columns = ['BidID', 'FloorPrice', 'Bid', 'Paid', 'AdvertiserID', 'UserTags']

        clicks = pd.read_csv("public/ipinyou/data/clk.20130612.txt", sep='\t', usecols=[0], header=None)
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

        ctr_pos = ctr.to_frame().reset_index()
        ctr_pos.columns = ['AdvertiserID', 'UserTags', 'CTR']

        user_tags = ctr_pos['UserTags'].str.get_dummies(sep=',')
        user_columns = user_tags.columns
        ctr_pos = ctr_pos.join(user_tags)

        ctr_pos = ctr_pos.drop(['UserTags'], axis=1)

        X = ctr_pos.drop(['CTR'], axis=1)
        y = ctr_pos['CTR']
        model = RandomForestRegressor()

        model.fit(X, y)
        print("CTR accuracy:", model.score(X, y))

        joblib.dump(model, 'public/ipinyou/models/ctr_model.pkl')
        pd.DataFrame(columns=user_columns).to_csv('public/ipinyou/models/ctr_columns.csv', index=False)

    return model, user_columns

###################################################

model, user_columns = load_models()

def get_advertiser_for(user_tags, floor_price):
    # Create a dataframe with the input data
    input_data = pd.DataFrame({'AdvertiserID': 0}, index=[0], dtype='int64')
    input_data = input_data.join(pd.DataFrame(columns=user_columns, data=np.zeros((1, len(user_columns)))))

    # Set the user tags to 1
    for tag in user_tags:
        if tag in user_columns:
            input_data[tag] = 1

    # Set the advertiser ID
    # max_ctr = 0
    # max_advertiser = "Random"

    advertisers = [a[0] for a in db_main.get_advertisers_with_active_campaigns()]
    ctr_list = {}

    for advertiser in advertisers:
        input_data['AdvertiserID'] = advertiser
        pred = model.predict(input_data)[0]
        ctr_list.setdefault(advertiser, pred)

    top_3 = sorted(ctr_list, key=ctr_list.get, reverse=True)[:3]
    top_advertiser = random.choice(top_3)

    campaigns = db_main.get_campaign_from_advertiser(top_advertiser)
    top_campaign = random.choice(campaigns)

    return {
        'advertiserID': top_advertiser,
        'ctr': ctr_list[top_advertiser],
        'campaignID': top_campaign[0],
        'campaign': top_campaign[1],
        'advertiser': db_main.get_advertiser_name(top_advertiser),
    }


