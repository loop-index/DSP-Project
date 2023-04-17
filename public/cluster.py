# # import pandas as pd
# from sklearn.cluster import KMeans
# from sklearn.metrics import pairwise_distances_argmin_min
# from sklearn.metrics.pairwise import cosine_similarity
# from gensim.models import Word2Vec
# import gensim
# from gensim import corpora

# import db_main

# # dataframe = pd.read_sql('SELECT * FROM users;', con=db_main.get_connection())
# interests = db_main.get_interests()
# interest_set = set()

# for set in interests:
#     for interest in set[0].strip("[]").split(','):
#         interest_set.add(interest.strip().strip('\"').lower())

# words = list(interest_set)

# model = Word2Vec([words], min_count=1)
# embeddings = [model.wv[word] for word in words]

# kmeans = KMeans(n_clusters=10, n_init='auto', random_state=0).fit(embeddings)

# closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, embeddings)

# # for i in range(len(kmeans.cluster_centers_)):
# #     cluster_words = [words[j] for j in range(len(words)) if kmeans.labels_[j] == i]
# #     print(f'Cluster {words[closest[i]]}: {cluster_words}')

# # Interpret the clusters
# for i in range(len(closest)):
#     # Find the closest words to the centroid of each cluster
#     centroid = kmeans.cluster_centers_[i]
#     distances = cosine_similarity([centroid], embeddings)
#     closest_idx = distances.argsort()[0][::-1]
#     closest_words = [words[idx] for idx in closest_idx[:5]]
    
#     print(f'Cluster {i+1}: {closest_words}')


# # ---------------------------------------------
# # interest_mat = dataframe['interests'].apply(pd.Series)
# # interest_mat = interest_mat.fillna(0)

# # print(interest_mat)

# # kmeans = KMeans(n_clusters=5, random_state=0)
# # kmeans.fit(interest_mat)

# # dataframe['cluster'] = kmeans.labels_

# # def get_cluster(id):
# #     return dataframe.loc[dataframe['user_id'] == id]['cluster'].values[0]
