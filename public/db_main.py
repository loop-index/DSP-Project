import mysql.connector

connection = mysql.connector.connect(
    user='root', password='1234',
    host='localhost', database='test')

cursor = connection.cursor()

# Generic functions

def get_query(query):
    cursor.execute(query)
    return cursor.fetchall()

def post_query(query):
    cursor.execute(query)
    connection.commit()

def get_connection():
    return connection

def shutdown():
    cursor.close()
    connection.close()

# Specific functions

def get_all_users():
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

def get_by_id(id):
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (id,))
    return cursor.fetchone()

def get_interest_groups():
    cursor.execute('SELECT main_key, interests FROM interest_groups')
    return cursor.fetchall()

def get_advertiser_name(id):
    cursor.execute('SELECT name FROM advertiser WHERE advertiser_id = %s', (id,))
    return cursor.fetchone()[0]

def get_advertisers_with_active_campaigns():
    cursor.execute('SELECT advertiser_id FROM campaign WHERE start_date <= CURDATE() AND end_date >= CURDATE() AND status = \'Active\'')
    return cursor.fetchall()

def get_campaign_from_advertiser(advertiser_id):
    cursor.execute('SELECT campaign_id, name FROM campaign WHERE advertiser_id = %s AND start_date <= CURDATE() AND end_date >= CURDATE() AND status = \'Active\'', (advertiser_id,))
    return cursor.fetchall()
