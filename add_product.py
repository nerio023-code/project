# this file will be the the frontend on my app. 
# This program will request the data in order to save it in the database.
import sqlite3

def registrar_producto(url, price, email, phone):
    conn = sqlite3.connect('deals.db')
    cur = conn.cursor()

    # 1. Crear la tabla NUEVA (versión 2) con espacio para el teléfono
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products_v2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            target_price REAL,
            user_email TEXT,
            user_phone TEXT
        )
    ''')
    
    # 2. Guardar los 4 datos en la tabla NUEVA (products_v2)
    # Fíjate que aquí dice 'INSERT INTO products_v2' y agregamos 'user_phone'
    cur.execute('''INSERT INTO products_v2 (url, target_price, user_email, user_phone) VALUES (?,?,?,?)''', (url, price, email, phone))
    
    conn.commit()
    conn.close()

