import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, f1_score
import json

# Load datasets
data = pd.read_csv("./factori_browsing/factori.csv", nrows=10)
# data = data[['userAgent', 'url_metadata_canonical_url', 'refDomain', 'mappedEvent', 'channel', 'keywords', 'categories', 'country']]
data = data[['userAgent', 'mappedEvent', 'channel', 'categories', 'country']]

def parse_keywords(keywords):
    return json.loads(keywords)['Text']

def parse_categories(categories):
    cat_list = json.loads(categories)['Text']
    categories = set()
    [categories.add(cat.split('/')[1]) for cat in cat_list]
    return ','.join(categories)

# data['keywords'].apply(lambda x: print(parse_keywords(x)))
data['categories'] = data['categories'].apply(lambda x: parse_categories(x))
print(data.head())
