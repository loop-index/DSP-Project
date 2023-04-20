import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier
from sklearn.multioutput import MultiOutputRegressor, MultiOutputClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import joblib
import csv, json, time

# Load datasets
# users = pd.read_csv("./raw/users.csv", nrows=500)
# browsing = pd.read_csv("./raw/browsing.csv", nrows=500)
# domains = pd.read_csv("./raw/domain_categories.csv", nrows=500)

# Try to load the model
try:
    retrain = input('Do you want to retrain the model? (y/N): ')
    if retrain == 'y':
        raise Exception('Retrain model')

    starting_time = time.time()
    clf = joblib.load('model.pkl')
    categories = pd.read_csv('columns.csv')
    gender_enc = joblib.load('gender_enc.pkl')
    age_enc = joblib.load('age_enc.pkl')
    print("Loaded model after", time.time() - starting_time, "seconds")

except:
    starting_time = time.time()
    users = pd.read_csv("./raw/users.csv")
    browsing = pd.read_csv("./raw/browsing.csv", usecols=['panelist_id', 'domain', 'active_seconds'])
    domains = pd.read_csv("./raw/domain_categories.csv").sample(frac=0.1)
    all_categories = pd.read_csv("./raw/categories.csv")

    print("Loaded datasets after", time.time() - starting_time, "seconds")
    starting_time = time.time()

    # Join datasets
    merged_data = pd.merge(browsing, users, on="panelist_id")
    browsing = None
    users = None
    merged_data = pd.merge(merged_data, domains, on="domain")
    domains = None
    merged_data = merged_data[["gender", "age_recode", "category", "active_seconds"]]

    # Drop rows with missing values
    merged_data = merged_data.dropna()

    # Split categories string into dummies
    # categories = merged_data['category'].str.get_dummies(sep=',')
    # merged_data = pd.concat([merged_data.drop(['category']), categories], axis=1)
    merged_data = merged_data.join(merged_data['category'].str.get_dummies(sep=','))

    # merged_data = pd.concat([merged_data, categories], axis=1)
    active_seconds = merged_data['active_seconds']
    merged_data = merged_data.drop(['active_seconds', 'category'], axis=1)

    # Encode the data
    gender_enc = LabelEncoder()
    age_enc = LabelEncoder()

    merged_data['gender'] = gender_enc.fit_transform(merged_data['gender'])
    merged_data['age_recode'] = age_enc.fit_transform(merged_data['age_recode'])

    print("Prepared datasets after", time.time() - starting_time, "seconds")

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(merged_data, active_seconds, test_size=0.01, random_state=42)

    # DecisionTreeClassifier is good for gender (60% accuracy)
    # LogisticRegression is good for age_recode (42% accuracy)
    # Current best is MultiOutputClassifier(DecisionTreeClassifier()) (38-39% accuracy)

    # Define the parameter grid to search
    param_grid = {
        'max_depth': [2, 4, 6, 8, 10],
        'min_samples_split': [2, 5, 10, 15, 20],
        'min_samples_leaf': [1, 2, 4, 8, 16],
        'max_features': ['auto', 'sqrt', 'log2']
    }

    # Choose a machine learning algorithm
    # clf = MultiOutputClassifier(DecisionTreeClassifier(criterion='gini', max_depth=10, min_samples_leaf=1, min_samples_split=2))
    clf = LogisticRegression()
    # clf = DecisionTreeClassifier(criterion='gini', max_depth=10, min_samples_leaf=1, min_samples_split=2)
    # clf = DecisionTreeRegressor(criterion='poisson', max_depth=10, min_samples_leaf=1, min_samples_split=2)

    # # Create a GridSearchCV object
    # grid_search = GridSearchCV(clf, param_grid, cv=5)
    # grid_search.fit(X_train, y_train)

    # # Print the best parameters and best score
    # print("Best parameters: ", grid_search.best_params_)
    # print("Best score: ", grid_search.best_score_)

    # DecisionTreeClassifier for age_recode
    # Best parameters:  {'criterion': 'gini', 'max_depth': 10, 'min_samples_leaf': 1, 'min_samples_split': 2}
    # Best score:  0.348659761951588

    # LogisticRegression for age 
    # Best parameters:  {'C': 1, 'penalty': 'l2', 'solver': 'saga'}
    # Best score:  0.3618551300281496

    # Train the model
    starting_time = time.time()
    clf.fit(X_train, y_train)
    print("Trained model after", time.time() - starting_time, "seconds")

    # Calculate the accuracy
    print("Accuracy: ", clf.score(X_test, y_test))

    # # Save the model
    # starting_time = time.time()
    # joblib.dump(clf, 'model.pkl')
    # categories.to_csv('columns.csv', index=False)
    # joblib.dump(gender_enc, 'gender_enc.pkl')
    # joblib.dump(age_enc, 'age_enc.pkl')
    # print("Saved model after", time.time() - starting_time, "seconds")


# while True:
#     cat = input("Enter comma-separated categories: ").lower().replace(' ', '').split(',')
#     if cat == ['']:
#         break

#     x_input = pd.DataFrame(columns=categories.columns, data=np.zeros((1, len(categories.columns))))
#     for c in cat:
#         if c in x_input.columns:
#             x_input[c] = 1

#         else:
#             print(f"Category '{c}' not found, skipping...")

#     if x_input.sum().sum() == 0:
#         print("No valid categories found, skipping...")
#         continue

#     # Predict
#     y_pred = clf.predict(x_input)
#     print(f"Prediction: {gender_enc.inverse_transform([int(y_pred[0][0])])[0]}, {age_enc.inverse_transform([int(y_pred[0][1])])[0]}")


# Change approach: Group data by users (panelist id) and input the gender, age, and categories. From there predict if that user will like a category or not.



