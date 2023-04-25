import pandas as pd
import numpy as np
from gensim.models import KeyedVectors
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import json, datetime

categories = ['adult', 'advertising', 'alcohol and tobacco', 'blacklist', 'blogs and personal', 'business', 'chat and messaging', 'content server', 'dating and personals', 
              'deceptive', 'drugs', 'economy and finance', 'education', 'entertainment', 'food', 'food and recipes', 'gambling', 'games', 'health', 
              'humor', 'illegal content', 'information tech', 'job related', 'media sharing', 'message boards and forums', 'news and media', 'parked', 'personals', 
              'proxy and filter avoidance', 'real estate', 'religion', 'search engines and portals', 'shopping', 'social networking', 'sport', 'sports', 'streaming media', 
              'translation', 'translators', 'travel', 'uncategorized', 'vehicles', 'virtual reality', 'weapons']

# Load datasets
ad_csv = pd.read_csv("data/advertising.csv")
ad_csv = ad_csv.drop(columns=['City', 'Timestamp', 'Area Income', 'Country', 'Daily Time Spent on Site'])

w2v = KeyedVectors.load_word2vec_format('public/w2v.bin', binary=True, limit=50000)

def text_to_categories(text):
    words = text.lower().split()
    ranks = {}

    for category in categories:
        sim = w2v.n_similarity(category.split(), words)
        ranks[category] = sim

    res = []
    for key in ranks:
        if ranks[key] > 0.22:
            res.append(key.replace(' ', ''))

    if len(res) == 0:
        key = max(ranks, key=ranks.get).replace(' ', '')
        res.append(key)

    return ','.join(res)

def age_coding(age_recode): 
    # Age ranges:
    # [18-24] = 0
    # (24-34] = 1
    # (34-44] = 2
    # (44-54] = 3
    # (54-64] = 4
    # (64-80] = 5

    # Convert age to age_recode
    if age_recode <= 24:
        return 0
    elif age_recode <= 34:
        return 1
    elif age_recode <= 44:
        return 2
    elif age_recode <= 54:
        return 3
    elif age_recode <= 64:
        return 4
    else:
        return 5

ad_csv['Ad Topic Line'] = ad_csv['Ad Topic Line'].apply(text_to_categories)
ad_csv['Age'] = ad_csv['Age'].apply(age_coding)

seen_categories = ad_csv['Ad Topic Line'].str.get_dummies(sep=',')
ad_csv = ad_csv.join(seen_categories)
output = ad_csv['Clicked on Ad']
ad_csv = ad_csv.drop(columns=['Ad Topic Line', 'Clicked on Ad', 'Daily Internet Usage'])

model = RandomForestClassifier(n_estimators=1000, max_depth=5, min_samples_split=10, min_samples_leaf=4)
X_train, X_test, y_train, y_test = train_test_split(ad_csv, output, test_size=0.05, random_state=42)
model.fit(X_train, y_train)
print("Score:", model.score(X_test, y_test))

# {'max_depth': 5, 'max_features': 'auto', 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 500}

while True:
    while True:
        try:
            gender = int(input("Enter 0 for female, 1 for male: "))
            break
        except ValueError:
            print("Invalid input, please try again...")

    while True:
        try:
            age_recode = int(input("Enter age: "))
            age_recode = age_coding(age_recode)
            break
        except ValueError:
            print("Invalid input, please try again...")
    
    cat = input("Enter comma-separated categories: ").lower().replace(' ', '').split(',')
    if cat == ['']:
        break

    # Create input dataframe, in order: gender, age_recode, categories
    x_input = pd.DataFrame({'Age': age_recode, 'Male': gender}, index=[0], dtype='int64')
    x_input = x_input.join(pd.DataFrame(columns=seen_categories.columns, data=np.zeros((1, len(seen_categories.columns)))))

    for c in cat:
        if c in x_input.columns:
            x_input[c] = 1

        else:
            print(f"Category '{c}' not found, skipping...")

    if x_input.sum().sum() == 0:
        print("No valid categories found, skipping...")
        continue

    # Predict
    y_pred = model.predict(x_input)
    print(f"Prediction: User would {'not ' if y_pred[0] == 0 else ''}click on the ad.")



