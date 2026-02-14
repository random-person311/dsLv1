import mysql.connector
import pprint

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "dslevel1_fp"
)
cursor = db.cursor(dictionary=True)




def auth(username, password):
    cursor.execute("SELECT role FROM users WHERE username =%s AND password =%s", (username, password))
    status = cursor.fetchone()
    if status == None:
        return None
    else:
        return int(status['role'])
    
def add_user(username, password, role):
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
    db.commit()

def get_user_by_name(username):
    cursor.execute("SELECT * FROM users WHERE username =%s", (username,))
    return cursor.fetchone()