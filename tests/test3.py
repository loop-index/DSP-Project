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
import joblib
import csv, json, time

# Load datasets
# users = pd.read_csv("./raw/users.csv", nrows=500)
# browsing = pd.read_csv("./raw/browsing.csv", nrows=500)
# domains = pd.read_csv("./raw/domain_categories.csv", nrows=500)

users = pd.read_csv("./raw/users.csv")
browsing = pd.read_csv("./raw/browsing.csv", usecols=['panelist_id', 'domain', 'active_seconds'])
domains = pd.read_csv("./raw/domain_categories.csv").sample(frac=0.5)
all_categories = pd.read_csv("./raw/categories.csv")

print("Loaded datasets...")

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
categories = merged_data['category'].str.get_dummies(sep=',')
# merged_data = pd.concat([merged_data, categories], axis=1)
merged_data = merged_data.drop(columns=['category'])
print("Joined datasets...")

# Encode the data
gender_enc = LabelEncoder()
age_enc = LabelEncoder()

merged_data['gender'] = gender_enc.fit_transform(merged_data['gender'])
merged_data['age_recode'] = age_enc.fit_transform(merged_data['age_recode'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(categories, merged_data[['gender']], test_size=0.2, random_state=42)

# DecisionTreeClassifier is good for gender (60% accuracy)
# LogisticRegression is good for age_recode (42% accuracy)

# Choose a machine learning algorithm
# clf = MultiOutputClassifier(DecisionTreeClassifier())
clf = DecisionTreeClassifier()

# Train the model
clf.fit(X_train, y_train)

# Calculate the accuracy
print("Accuracy: ", clf.score(X_test, y_test))