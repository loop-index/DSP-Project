from gensim.models import KeyedVectors
import db_main, json

model = KeyedVectors.load_word2vec_format('public/w2v.bin', binary=True, limit=50000)

# interest_set = set()
# categories = {}

def insert_category(interest):
    max_sim = 0
    max_category = None

    categories = db_main.get_interest_groups()

    for category in categories:
        data = category[1].split(',')
        if interest in data:
            return category[0], 0 # Already in category

        sim = model.n_similarity([interest], data)
        if sim > max_sim:
            max_sim = sim
            max_category = category[0]

    if max_sim > 0.5:
        return max_category, 1 # Added to category

    else:
        return interest, 2 # New category

def get_categories():
    return db_main.get_interest_groups()

def add_user_to_group(user_id, interest):
    main_key, action = insert_category(interest)
    if action == 0:
        group_users = db_main.get_query('SELECT users FROM interest_groups WHERE main_key = \'{}\';'.format(main_key))[0][0].split(',')
        if user_id not in group_users:
            query = 'UPDATE interest_groups SET users = CONCAT(users, \',{}\') WHERE main_key = \'{}\';'.format(user_id, main_key)
            db_main.post_query(query)
            print(query)

    elif action == 1:
        group_users = db_main.get_query('SELECT users FROM interest_groups WHERE main_key = \'{}\';'.format(main_key))[0][0].split(',')
        if user_id in group_users:
            query = 'UPDATE interest_groups SET interests = CONCAT(interests, \',{}\') WHERE main_key = \'{}\';'.format(interest, main_key)
        else:
            query = 'UPDATE interest_groups SET users = CONCAT(users, \',{}\'), interests = CONCAT(interests, \',{}\') WHERE main_key = \'{}\';'.format(user_id, interest, main_key)
        db_main.post_query(query)
        print(query)

    elif action == 2:
        query = 'INSERT INTO interest_groups (main_key, interests, users) VALUES (\'{}\', \'{}\', \'{}\');'.format(main_key, interest, user_id)
        db_main.post_query(query)
        print(query)

    return main_key

# users = db_main.get_query('SELECT user_id, interests FROM users;')
# for user in users:
#     user_id = user[0]
#     interests = json.loads(user[1])
#     for interest in interests:
#         add_user_to_group(str(user_id), interest.lower())

