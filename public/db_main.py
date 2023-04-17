import mysql.connector

connection = mysql.connector.connect(
    user='root', password='1234',
    host='localhost', database='test')

cursor = connection.cursor()

def get_all_users():
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

def get_by_id(id):
    cursor.execute('SELECT * FROM users WHERE user_id = %s', (id,))
    return cursor.fetchone()

def get_interest_groups():
    cursor.execute('SELECT main_key, interests FROM interest_groups')
    return cursor.fetchall()

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