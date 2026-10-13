import sqlite3
import pickle

password = "admin123"

def get_user(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)

    result = cursor.fetchone()
    connection.close()
    return result

def load_data(data):
    return pickle.loads(data)
