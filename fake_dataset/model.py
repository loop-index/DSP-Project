import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, f1_score

# Load datasets
data = pd.read_csv("./fake_dataset/fake_dataset.csv")

# Get dummy variables for the categories
categories = data['ad_category'].str.get_dummies(sep=',')
data = data.join(categories).drop(['ad_category'], axis=1)

# Encode the data
data['location'] = data['location'].astype('category').cat.codes
data['age'] = data['age'].astype('category').cat.codes
# print(data.head())

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data.drop(['clicked'], axis=1), data['clicked'], test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions
print("Accuracy:", model.score(X_test, y_test))