import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import csv, json

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

# Calculate average active seconds per category per user
# category_user_average_seconds = merged_data.groupby(["category", "gender", "age_recode"])["active_seconds"].apply(lambda x: x.mean())

# Calculate top categories per user

# Get user with most active seconds for each category
# top_users = category_user_active_seconds.reset_index().groupby("category").apply(lambda x: x.nlargest(3, "active_seconds"))
top_users = category_user_active_seconds.reset_index().groupby(["age_recode", "gender"]).apply(lambda x: x.sort_values("active_seconds", ascending=False))

# print(top_users)

# Prepare the data
X = top_users[['category']]
y = top_users[['gender', 'age_recode']]
X_encoded = pd.get_dummies(X, columns=['category'])
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.3, random_state=42)

# Choose a machine learning algorithm
clf = DecisionTreeClassifier()

# Train the model
clf.fit(X_train, y_train)

# Evaluate the model
# y_pred = clf.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {accuracy:.2f}')

# Predict the demographic
categories = ['entertainment', 'business']
X_new = pd.DataFrame({'category': categories})
X_new_encoded = pd.get_dummies(X_new, columns=['category'])
X_new_encoded = X_new_encoded.reindex(columns=X_encoded.columns, fill_value=0)
y_new = clf.predict(X_new_encoded)
print(f'Predicted demographic: {y_new}')


# Print results
# categories = csv.reader(open("./raw/categories.csv", "r"))
# next(categories, None)  # skip the headers

# results = {}

# for category in categories:
#     try:
#         category = category[0]
#         for i, row in top_users.loc[top_users['category'] == category].iterrows():
#             if category not in results:
#                 results[category] = []
#             results[category].append((row['gender'], row['age_recode'], row['active_seconds']))
    
#     except KeyError:
#         print(f"There is no data for category {category}.")

# print(json.dumps(results, indent=4))