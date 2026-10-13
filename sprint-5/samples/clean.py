import os
import sqlite3

def get_user(username):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    connection.close()
    return result

password = os.environ.get("APP_PASSWORD")
