# this file will be the the frontend on my app. 
# This program will request the data in order to save it in the database.
import sqlite3

def registrar_producto (url, price, email) :
    conn = sqlite3.connect('deals.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO products (url, target_price, user_email) VALUES (?,?,?)''',(url, price, email))
    conn.commit()
    conn.close()

