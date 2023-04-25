import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score, mean_squared_error, f1_score
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
import joblib
import csv, json, time, matplotlib

# Load datasets
data = pd.read_csv("data/ad_info.csv")

# Plot data
# data.plot(kind='scatter', x='publishedAt', y='retention')
# matplotlib.pyplot.show()

# print(input_data)

model = LinearRegression()
while True:
    category = int(input("Category: "))

    filtered = data[data['categoryId'] == category].sort_values(by=['publishedAt'])
    print(filtered)
    input_data = filtered[['publishedAt']]
    output_data = filtered['viewCount']

    # filtered.plot(kind='scatter', x='publishedAt', y='viewCount')
    # matplotlib.pyplot.show()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.1, random_state=42)

    # Train model
    model.fit(X_train, y_train)
    print("Score:", model.score(X_test, y_test))



