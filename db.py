from unicodedata import name

import mysql.connector
import pprint

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "dslv1_fp"
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

def get_users():#get_aa_users()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

def get_user(id):
    cursor.execute("SELECT * FROM users WHERE id =%s", (id,))
    return cursor.fetchone()

def delete_user(id):
    cursor.execute("DELETE FROM users WHERE id =%s", (id,))
    db.commit()

def update_user(id, dict):
    cursor.execute("UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s"
                   , (dict['username'], dict['password'], dict['role'], id))
    db.commit()

def get_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()

def get_all_products():
    cursor.execute("SELECT * FROM products ORDER BY name")
    return cursor.fetchall()

def update_product(id, dict):
    cursor.execute("UPDATE products SET name = %s, desc = %s, category = %s, price = %s, stock = %s WHERE id = %s",
                     (dict['name'], dict['desc'], dict['category'], dict['price'], dict['stock'], id))
    db.commit()

def add_product(dict): 
    cursor.execute('INSERT INTO products (name, `desc`, category, price, stock) VALUES (%s, %s, %s, %s, %s)',
                   (dict['name'], dict['desc'], dict['category'], dict['price'], dict['stock']))
    db.commit()

def delete_product(id):
    cursor.execute('DELETE FROM products WHERE id = %s', (id,))
    db.commit()

def get_product_stock(id):
    cursor.execute('SELECT stock FROM products WHERE id = %s', (id,))
    record = cursor.fetchone()
    if record != None:
        return int(record['stock'])
    else:
        return None

def add_purchase(username, product_id, quantity):
    cursor.execute("""
    INSERT INTO purchases (user_id, product_id, quantity, total_amount)
    VALUES (
    (SELECT id FROM users WHERE username=%(username)s),
    %(product_id)s,
    %(quantity)s,
    %(quantity)s * (SELECT price FROM products WHERE id=%(product_id)s)
    );
    """, {
    'username': username,
    'product_id': product_id,
    'quantity': quantity
    })
    cursor.execute('UPDATE products SET stock=%s WHERE id=%s', (get_product_stock(product_id) - quantity, product_id))
    db.commit()

def get_user_purchases(username):
    cursor.execute("""
    SELECT purchases.id, products.name, purchases.quantity, purchases.total_amount, purchases.date FROM purchases
    INNER JOIN products ON purchases.product_id = products.id
    WHERE user_id = (
    SELECT id FROM users WHERE username=%s
    );
    """, (username,))
    return cursor.fetchall()