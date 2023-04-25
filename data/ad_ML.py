import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, f1_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import joblib
import csv, json, time

# Load datasets
data = pd.read_csv("data\\ad_info.csv")

# Split data
input_data = data[['publishedAt', 'categoryId']]
output_data = data[['viewCount']]

print(input_data.head())
print(output_data.head())

X_train, X_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor()
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))



