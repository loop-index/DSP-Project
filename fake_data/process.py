import nltk
from nltk.corpus import stopwords
from gensim.models import KeyedVectors
import pandas as pd

ad_categories = ['fashion', 'vehicle', 'beauty', 'electronic', 'education', 'entertainment', 
                 'finance', 'food', 'health', 'house', 'industrial', 'technology', 'government', 
                 'estate', 'retail', 'service', 'sport', 'music', 'travel', 'miscellaneous', 'pets']

w2v = KeyedVectors.load_word2vec_format('public/w2v.bin', binary=True, limit=50000)


def extract_keywords(text):
    # Tokenize the text into words
    text = text.replace('-', ' ')
    words = nltk.word_tokenize(text.lower())
    
    # Remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    
    # Extract keywords using part-of-speech tagging
    pos_tags = nltk.pos_tag(filtered_words)
    keywords = [word for word, tag in pos_tags if tag.startswith('N')]

    if len(keywords) == 0:
        return keywords, 'miscellaneous'

    try:
        max_sim = 0
        res = 'miscellaneous'
        for cat in ad_categories:
            sim = w2v.n_similarity([cat], keywords)
            if sim > max_sim:
                max_sim = sim
                res = cat
        return keywords, res
    
    except:
        print(keywords)
        return keywords, 'miscellaneous'
        

data = pd.read_csv("fake_data/advertising.csv")
data['Ad Topic Line'] = data['Ad Topic Line'].apply(lambda x: extract_keywords(x)[1])

print(data.head())

# data = data[['Age', 'Male', 'Ad Topic Line', 'Area Income', 'Daily Internet Usage', 'Clicked on Ad']]
data.to_csv('fake_data/advertising_processed.csv', index=False)