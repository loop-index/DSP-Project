import pandas as pd
import numpy as np

# Define the range of age values and categories of advertisements
age_ranges = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
categories = [
    'Apparel & Accessories',
    'Automotive',
    'Beauty & Personal Care',
    'Books & Magazines',
    'Computers & Electronics',
    'Entertainment & Media',
    'Financial Services',
    'Food & Beverage',
    'Games & Toys',
    'Health & Wellness',
    'Home & Garden',
    'Industrial & Scientific',
    'Jewelry & Watches',
    'Movies & TV Shows',
    'Music & Audio',
    'Office Supplies',
    'Outdoor & Sporting Goods',
    'Pet Supplies',
    'Phones & Accessories',
    'Real Estate',
    'Restaurants & Dining',
    'Shoes',
    'Software',
    'Sports & Fitness',
    'Tools & Home Improvement',
    'Toys & Hobbies',
    'Travel & Tourism',
    'Video Games',
    'Business Services',
    'Education & Training',
    'Events & Conferences',
    'Gifts & Flowers',
    'Government & Politics',
    'Hobbies & Interests',
    'Luggage & Bags',
    'Medical Supplies & Equipment',
    'Office & School Supplies',
    'Photography & Video',
    'Religious & Ceremonial',
    'Science & Nature',
    'Vehicles & Parts'
]

# Define the number of rows in the dataset
num_rows = 1000000

# Create a pandas dataframe with random values for each column
df = pd.DataFrame({
    'age': np.random.choice(age_ranges, num_rows),
    'gender': np.random.choice([1, 0], num_rows), # 1 for male, 0 for female
    'location': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Philadelphia', 'Phoenix', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'San Francisco', 'Indianapolis', 'Charlotte', 'Seattle', 'Denver', 'Boston'], num_rows),
    # 'Category of Advertisement': [np.random.choice(categories, np.random.randint(1, 4), replace=False) for i in range(num_rows)],
    'ad_category': np.random.choice(categories, num_rows),
    'clicked': np.random.choice([1, 0], num_rows),
    'bid_price': np.round(np.random.uniform(0.1, 2.0, num_rows), 2)
})

# Display the first few rows of the generated dataframe
print(df.head())
df.to_csv('fake_dataset/fake_dataset.csv', index=False)