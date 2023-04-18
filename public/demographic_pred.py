import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib
import csv, json

# Try to load the model
try:
    retrain = input('Do you want to retrain the model? (y/N): ')
    if retrain == 'y':
        raise Exception('Retrain model')

    clf = joblib.load('./models/model.pkl')
    X_encoded = pd.read_csv('./models/columns.csv')
    gender_enc = joblib.load('./models/gender_enc.pkl')
    age_enc = joblib.load('./models/age_enc.pkl')

except:
    # Load datasets
    users = pd.read_csv("./raw/users.csv")
    browsing = pd.read_csv("./raw/browsing.csv")
    browsing = browsing.sample(frac=0.1, random_state=42)
    domains = pd.read_csv("./raw/domain_categories.csv")

    # Split categories string into list
    domains['category'] = domains['category'].apply(lambda x: x.split(','))
    domains = domains.explode('category')

    # Join datasets
    merged_data = pd.merge(browsing, users, on="panelist_id")
    merged_data = pd.merge(merged_data, domains, on="domain")
    merged_data = merged_data[["gender", "age_recode", "category", "active_seconds"]]

    # print(merged_data)

    # Calculate total active seconds per category per user
    category_user_active_seconds = merged_data.groupby(["gender", "age_recode", "category"])["active_seconds"].sum()

    # Calculate top categories per user
    top_users = category_user_active_seconds.reset_index().groupby(["age_recode", "gender"]).apply(lambda x: x.sort_values("active_seconds", ascending=False))

    # Prepare the data
    X = top_users[['category']]
    y = top_users[['gender', 'age_recode', 'active_seconds']]

    # Encode the data
    gender_enc = LabelEncoder()
    age_enc = LabelEncoder()

    y['gender'] = gender_enc.fit_transform(y['gender'])
    y['age_recode'] = age_enc.fit_transform(y['age_recode'])
    X_encoded = pd.get_dummies(X, columns=['category'])
    # X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.3, random_state=42)

    # Choose a machine learning algorithm
    clf = DecisionTreeRegressor()

    # Train the model
    # clf.fit(X_train, y_train)
    clf.fit(X_encoded, y)

    # Save the model
    joblib.dump(clf, './models/model.pkl')
    X_encoded.to_csv('./models/columns.csv', index=False)
    joblib.dump(gender_enc, './models/gender_enc.pkl')
    joblib.dump(age_enc, './models/age_enc.pkl')

# Load all categories
categories_set = csv.reader(open("./raw/categories.csv", "r"))
next(categories_set, None)  # skip the headers
categories_set = [row[0] for row in categories_set]

# Predict the demographic
while True:
    categories = input('Enter categories (separated by comma): ').lower().replace(' ', '').split(',')
    if categories == ['']:
        print('Bye!')
        break

    # Check if all categories are valid
    if not all(category in categories_set for category in categories):
        print('Invalid category!')
        continue

    # X_new = pd.DataFrame({'category': categories})
    # print(X_new)
    # X_new_encoded = pd.get_dummies(X_new, columns=['category'])
    # X_new_encoded = X_new_encoded.reindex(columns=X_encoded.columns, fill_value=0)
    categories = [f'category_{category}' for category in categories]
    # Create a new dataframe with the same columns as the training data, fill it with 0s
    X_new_encoded = pd.DataFrame(columns=X_encoded.columns, data=np.zeros((1, len(X_encoded.columns))))
    X_new_encoded[categories] = 1.0
    y_new = clf.predict(X_new_encoded)

    # # Print the result and confidence
    # print(f'Predicted demographic: {y_new[0][0]} {y_new[0][1]} {y_new[0][2]} (confidence: {clf.predict_proba(X_new_encoded)[0][0]})')

    predicted_gender = gender_enc.inverse_transform([int(y_new[0][0])])[0]
    predicted_age_recode = age_enc.inverse_transform([int(y_new[0][1])])[0]
    predicted_active_seconds = y_new[0][2]
    print(f'Predicted demographic: gender={predicted_gender}, age_recode={predicted_age_recode}, active_seconds={predicted_active_seconds:.2f}')

