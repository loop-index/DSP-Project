import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as rq
from random import choice
import spacy, math, time
from collections import Counter
import newspaper
from newspaper import Article, Config
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from translate import Translator
import re

nlp = spacy.load("en_core_web_sm")
w2v = KeyedVectors.load_word2vec_format('public/w2v.bin', binary=True, limit=50000)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    # Add more user agents as desired
]

categories = ['adult', 'advertising', 'alcohol and tobacco', 'blacklist', 'blogs and personal', 'business', 'chat and messaging', 'content server', 'dating and personals', 
              'deceptive', 'drugs', 'economy and finance', 'education', 'entertainment', 'food', 'food and recipes', 'gambling', 'games', 'health', 
              'humor', 'illegal content', 'information tech', 'job related', 'media sharing', 'message boards and forums', 'news and media', 'parked', 'personals', 
              'proxy and filter avoidance', 'real estate', 'religion', 'search engines and portals', 'shopping', 'social networking', 'sport', 'sports', 'streaming media', 
              'translation', 'translators', 'travel', 'uncategorized', 'vehicles', 'virtual reality', 'weapons']

def processing():
    data = pd.read_csv('teads_dataset/dataset.csv')
    data = data.drop(columns=['auction_id' , 'timestamp', 'creative_id', 'campaign_id', 'advertiser_id', 'placement_id', 'placement_language', 
                     'website_id', 'ua_os', 'ua_browser_version', 'ua_device', 'user_average_seconds_played'])
    print(data.head())
    data.to_csv('teads_dataset/dataset_processed.csv', index=False)

    data['retention'] = data['seconds_played'] / data['creative_duration']
    data['retention'] = data['retention'].apply(lambda x: '{:.2f}'.format(x))

    data.to_csv('teads_dataset/dataset_processed.csv', index=False)

    data['referer_deep_three'] = data['referer_deep_three'].apply(lambda x: get_domain_text(x))
    data.to_csv('teads_dataset/dataset_processed.csv', index=False)
    
def get_news_description(link):
    config = Config()
    config.browser_user_agent = choice(user_agents)
    url = 'https://' + link.split('/')[0]
    try:
        news = newspaper.build(url, config=config)
        # If the link is a category, return news description, else return None as it's an article
        if link not in [u.split('//')[1] for u in news.category_urls()]:
            return None

        if news.description != '':
            return news.description
        else:
            return None
    except:
        return None
    
def get_article_keywords(link):
    config = Config()
    config.browser_user_agent = choice(user_agents)
    url = 'https://' + link
    try:
        article = Article(url, config=config)
        article.download()
        article.parse()
        article.nlp()
        return article.keywords, article.summary
    except:
        return None


def get_domain_text(link):
    news = get_news_description(link)
    if news:
        words = [word for word in news.split() if word not in stopwords.words('english')]
        source_type = 'news'

    else:
        words, news = get_article_keywords(link)
        source_type = 'article'

    if not words:
        return None
    else:
        ranks = {}
        for category in categories:
            sim = w2v.n_similarity(category.split(), words)
            ranks[category.replace(' ', '')] = sim

        res = []
        for key in ranks:
            if ranks[key] > 0.25:
                res.append(key)

        if len(res) == 0:
            # key = max(ranks, key=ranks.get).replace(' ', '')
            # res.append(key)
            res.append('uncategorized')

        return (source_type, words, ','.join(sorted(res, key=lambda x: ranks[x])[:5]))

def translate(text):
    try:
        ts = Translator(to_lang='en')
        return ts.translate(text)
    except:
        return None
 
def get_article(link):
    config = Config()
    config.browser_user_agent = choice(user_agents)
    url = 'https://' + link
    try:
        a = Article(url, config=config)
        a.download()
        a.parse()
        meta_description = a.meta_description.split()
        if (len(meta_description) > 0 or (len(a.meta_keywords) > 0 and a.meta_keywords[0] != '')):
            return a.title, meta_description, a.meta_keywords
        else:
            try:
                a.nlp()
                return a.title, a.summary.split(), a.keywords
            except:
                return None
    except:
        return None
    
def get_source(link):
    config = Config()
    config.browser_user_agent = choice(user_agents)
    url = 'https://' + link.split('/')[0]
    try:
        n = newspaper.build(url, config=config)
        return n.brand, translate(n.description).split(), []
    except:
        return None

def get_keywords(link):
    tup = get_article(link)
    # return tup
    if tup:
        words = [re.sub(r'[^\w\s]', '', word.lower()) for word in tup[1]]
        words = [word for word in words if word not in stopwords.words('english')] + [word.lower() for word in tup[2] if word.lower() not in stopwords.words('english')]
        return tup[0], text_to_categories(words)
    else:
        return None
    
def text_to_categories(text):
    words = text
    if len(words) == 0:
        return 'uncategorized'
    
    ranks = {}

    for category in categories:
        sim = w2v.n_similarity(category.split(), words)
        ranks[category] = sim

    res = []
    for key in ranks:
        if ranks[key] > 0.305:
            res.append(key.replace(' ', ''))

    if len(res) == 0:
        key = max(ranks, key=ranks.get).replace(' ', '')
        res.append(key)
        # res.append('uncategorized')

    # res = sorted(res, key=lambda x: ranks[x], reverse=True)
    # count = math.ceil(len(res) / 5)
    # res = res[:count]

    return ','.join(res)

data = pd.read_csv('teads_dataset/dataset_processed.csv', nrows=10)
# print(data[data['ua_country'] != 'us'])
# print(data.groupby('referer_deep_three')['retention'].mean().sort_values(ascending=False))
# data = data.loc[[1]]
# print(data)
data['referer_deep_three'] = data['referer_deep_three'].apply(lambda x: print(get_keywords(x)))
