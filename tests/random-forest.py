import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, f1_score
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier
from sklearn.multioutput import MultiOutputRegressor, MultiOutputClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
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
    clf = joblib.load('tests\\save\\model.pkl') # Fix this path
    categories = pd.read_csv('tests\\save\\columns.csv')
    gender_enc = joblib.load('tests\\save\\gender_enc.pkl')
    age_enc = joblib.load('tests\\save\\age_enc.pkl')
    total_all_categories = pd.read_csv('tests\\save\\total_all_categories.csv')
    print("Loaded model after", time.time() - starting_time, "seconds")

except:
    starting_time = time.time()
    users = pd.read_csv("./raw/users.csv")
    browsing = pd.read_csv("./raw/browsing.csv", usecols=['panelist_id', 'domain', 'active_seconds'])
    domains = pd.read_csv("./raw/domain_categories.csv").sample(frac=1, random_state=42)
    all_categories = pd.read_csv("./raw/categories.csv")

    print("Loaded datasets after", time.time() - starting_time, "seconds")
    starting_time = time.time()

    # Join datasets
    merged_data = pd.merge(browsing, users, on="panelist_id")
    browsing = None
    users = None
    merged_data = pd.merge(merged_data, domains[['domain', 'category']], on="domain")
    domains = None
    merged_data = merged_data[["gender", "age_recode", "category", "active_seconds"]]

    # Sum the seconds of each group of categories
    merged_data = merged_data.groupby(['gender', 'age_recode', 'category'])['active_seconds'].sum().reset_index()
    total_all_categories = merged_data.groupby(['gender', 'age_recode'])['active_seconds'].sum().reset_index()
    merged_data = merged_data.dropna()
    categories = merged_data['category'].str.get_dummies(sep=',')
    merged_data = merged_data.join(categories)

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

    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
                'max_features': max_features,
                'max_depth': max_depth,
                'min_samples_split': min_samples_split,
                'min_samples_leaf': min_samples_leaf,
                'bootstrap': bootstrap}

    # Define the parameter grid to search
    param_grid = {
        'n_estimators': n_estimators,
        'max_depth': max_depth,
        'min_samples_split': min_samples_split,
        'min_samples_leaf': min_samples_leaf,
        'bootstrap': bootstrap,
    }

    # clf = RandomForestRegressor(n_estimators=100, min_samples_split=10, min_samples_leaf=1, max_features='sqrt', max_depth=80, bootstrap=False)
    clf = RandomForestRegressor()
    # clf = MLPRegressor(hidden_layer_sizes=(100, 100, 100), max_iter=500, activation='relu', solver='adam', random_state=42)

    # rf_random = RandomizedSearchCV(estimator = clf, param_distributions = random_grid, n_iter = 100, cv = 3, verbose=2, random_state=42, n_jobs = -1)
    # # Fit the random search model
    # rf_random.fit(X_train, y_train)
    # print(rf_random.best_params_)

    # # Create a GridSearchCV object
    # grid_search = GridSearchCV(clf, param_grid, cv=5, scoring='neg_mean_squared_error', verbose=1)
    # grid_search.fit(X_train, y_train)

    # # Print the best parameters and best score
    # print("Best parameters: ", grid_search.best_params_)
    # print("Best score: ", grid_search.best_score_)

    # Train the model
    starting_time = time.time()
    clf.fit(X_train, y_train)
    print("Trained model after", time.time() - starting_time, "seconds")

    # Calculate the accuracy
    print("Training accuracy: ", clf.score(X_train, y_train))
    print("Test accuracy: ", clf.score(X_test, y_test))

    # Save the model
    starting_time = time.time()
    joblib.dump(clf, 'tests\\save\\model.pkl')
    total_all_categories.to_csv('tests\\save\\total_all_categories.csv', index=False)
    categories.to_csv('tests\\save\\columns.csv', index=False)
    joblib.dump(gender_enc, 'tests\\save\\gender_enc.pkl')
    joblib.dump(age_enc, 'tests\\save\\age_enc.pkl')
    print("Saved model after", time.time() - starting_time, "seconds")


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
    x_input = pd.DataFrame({'gender': gender, 'age_recode': age_recode}, index=[0], dtype='int64')
    x_input = x_input.join(pd.DataFrame(columns=categories.columns, data=np.zeros((1, len(categories.columns)))))

    for c in cat:
        if c in x_input.columns:
            x_input[c] = 1

        else:
            print(f"Category '{c}' not found, skipping...")

    if x_input.sum().sum() == 0:
        print("No valid categories found, skipping...")
        continue

    # Predict
    y_pred = clf.predict(x_input)
    percentage = y_pred[0] / (total_all_categories.loc[(total_all_categories['gender'] == gender_enc.inverse_transform([gender])[0])
                                   & (total_all_categories['age_recode'] == age_enc.inverse_transform([age_recode])[0])]['active_seconds'].values[0]) * 100
    print(f"Prediction: User would spend {percentage:.2f}% on the category.")
    # print(f"Prediction: User would spend {y_pred[0]:.2f} seconds on the category.")


# Change approach: Group data by users (panelist id) and input the gender, age, and categories. From there predict if that user will like a category or not.



