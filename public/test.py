# import pandas as pd
# import numpy as np

# user_data = pd.read_csv('./raw/users.csv', nrows=1000, header=0)
# print(user_data)

# browsing_data = pd.read_csv('./raw/browsing.csv', nrows=1000, header=0)
# print(browsing_data)

# domain_data = pd.read_csv('./raw/domain_categories.csv', nrows=1000, header=0)
# print(domain_data)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import csv

# Load datasets
users = pd.read_csv("./raw/users.csv")
browsing = pd.read_csv("./raw/browsing.csv", nrows=500000)
domains = pd.read_csv("./raw/domain_categories.csv")

# Split categories column into separate rows
categories = domains['category'].str.strip('\"').str.split(',', expand=True).stack().str.strip().reset_index(level=1, drop=True)
categories.name = 'category'
domains = domains.drop('category', axis=1).join(categories)

# Join datasets
merged_data = pd.merge(browsing, users, on="panelist_id")
merged_data = pd.merge(merged_data, domains, on="domain")

# Preprocess data
merged_data.drop_duplicates(inplace=True)
merged_data.dropna(inplace=True)
merged_data = merged_data[["gender", "age_recode", "category", "active_seconds"]]

# Group data by category and user demographics and count active seconds
grouped_data = merged_data.groupby(["category", "gender", "age_recode"], as_index=False).agg({"active_seconds": "sum"})

# Find user who spends the most time on each category
max_time_users = grouped_data.loc[grouped_data.groupby(["category"])["active_seconds"].idxmax()]

# Print results
for category in max_time_users["category"].unique():
    category_users = max_time_users[max_time_users["category"] == category]
    print(f"The user who spends the most time on category '{category}' is {category_users.iloc[0]['gender']} and in the age range {category_users.iloc[0]['age_recode']}") 


# # Preprocess data
# merged_data.drop_duplicates(inplace=True)
# merged_data.dropna(inplace=True)
# merged_data = merged_data[["gender", "age_recode", "category", "active_seconds"]]

# # Calculate total active seconds per category per user
# category_user_active_seconds = merged_data.groupby(["category", "gender", "age_recode"])["active_seconds"].sum()

# # Get user with most active seconds for each category
# top_users = category_user_active_seconds.reset_index().groupby("category").apply(lambda x: x.nlargest(1, "active_seconds"))

# # Print results
# categories = csv.reader(open("./raw/categories.csv", "r"))
# next(categories, None)  # skip the headers

# for category in categories:
#     try:
#         category = category[0]
#         top_user = top_users.loc[category]
#         gender = top_user["gender"].values[0]
#         age_range = top_user["age_recode"].values[0]
#         print(f"The user who spends the most time on {category} is {gender} and in the {age_range} age range.")
#     except KeyError:
#         print(f"There is no data for category {category}.")

# ----------------------------

# # Split data
# X = merged_data.drop("category", axis=1)
# y = merged_data["category"]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train model
# clf = DecisionTreeClassifier()
# clf.fit(X_train, y_train)

# # Evaluate model
# accuracy = clf.score(X_test, y_test)
# print("Accuracy:", accuracy)