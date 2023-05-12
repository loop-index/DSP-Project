import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, f1_score

# Load datasets
data = pd.read_csv("./fake_data/advertising_processed.csv")

# Get dummy variables for the categories
categories = data['Ad Topic Line'].str.get_dummies(sep=',')
data = data.join(categories).drop(['Ad Topic Line'], axis=1)

# # Encode the data
# data['location'] = data['location'].astype('category').cat.codes
# data['age'] = data['age'].astype('category').cat.codes
data['City'] = data['City'].astype('category').cat.codes
data['Country'] = data['Country'].astype('category').cat.codes
data = data.drop(['Timestamp'], axis=1)
print(data.head())

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data.drop(['Clicked on Ad'], axis=1), data['Clicked on Ad'], test_size=0.1, random_state=42)

# Train the model
# model = RandomForestClassifier()
model = RandomForestRegressor(max_depth=10, min_samples_leaf=2, min_samples_split=2, n_estimators=100)

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# # Create a GridSearchCV object and fit it to the data
# grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)
# grid_search.fit(data.drop(['Clicked on Ad'], axis=1), data['Clicked on Ad'])

# # Print the best hyperparameters and the corresponding score
# print("Best parameters:", grid_search.best_params_)
# print("Best score:", grid_search.best_score_)

# Best parameters: {'max_depth': 10, 'min_samples_leaf': 2, 'min_samples_split': 2, 'n_estimators': 100}
# Best score: 0.8719021510310379

model.fit(X_train, y_train)

# Make predictions
print("Accuracy:", model.score(X_test, y_test))