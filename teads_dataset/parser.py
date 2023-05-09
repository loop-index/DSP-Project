import pandas as pd
from os import listdir
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Load datasets
dirs = listdir('bids_dataset/US-market')

main_df = pd.read_csv('bids_dataset/US-market/{}'.format(dirs[0]), encoding="utf-16", sep='\t')
main_df = main_df.drop(columns=['Campaign Name', 'Country', 'Geo Targeting', 'ID', 'Language', 'Budget', 'Ad Group', 'Max. CPC', 'Keyword Type'])
main_df = main_df.drop([0, 1, 2, 3])

categories = ['adult', 'advertising', 'alcohol and tobacco', 'blacklist', 'blogs and personal', 'business', 'chat and messaging', 'content server', 'dating and personals', 
              'deceptive', 'drugs', 'economy and finance', 'education', 'entertainment', 'food', 'food and recipes', 'gambling', 'games', 'health', 
              'humor', 'illegal content', 'information tech', 'job related', 'media sharing', 'message boards and forums', 'news and media', 'parked', 'personals', 
              'proxy and filter avoidance', 'real estate', 'religion', 'search engines and portals', 'shopping', 'social networking', 'sport', 'sports', 'streaming media', 
              'translation', 'translators', 'travel', 'uncategorized', 'vehicles', 'virtual reality', 'weapons']

w2v = KeyedVectors.load_word2vec_format('public/w2v.bin', binary=True, limit=50000)

def text_to_categories(text):
    words = [w for w in text.lower().split() if w not in stopwords.words('english')]
    if len(words) == 0:
        return 'uncategorized'
    
    ranks = {}

    for category in categories:
        sim = w2v.n_similarity(category.split(), words)
        ranks[category] = sim

    res = []
    for key in ranks:
        if ranks[key] > 0.25:
            res.append(key.replace(' ', ''))

    if len(res) == 0:
        # key = max(ranks, key=ranks.get).replace(' ', '')
        # res.append(key)
        res.append('uncategorized')

    return ','.join(res)

main_df['Keyword'] = main_df['Keyword'].apply(text_to_categories)
main_df['CTR'] = main_df['CTR'].apply(lambda x: float(x.replace('%', '')))

dummy_categories = main_df['Keyword'].str.get_dummies(sep=',')

model = RandomForestRegressor()
X_train, X_test, y_train, y_test = train_test_split(dummy_categories, main_df['CTR'], test_size=0.05, random_state=42)
model.fit(X_train, y_train)
print("Score:", model.score(X_test, y_test))