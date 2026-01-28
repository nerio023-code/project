# this file will be the the frontend on my app. 
# This program will request the data in order to save it in the database.

import sqlite3 #import my toolbox
conn = sqlite3.connect('deals.db')
cur = conn.cursor()
#manually prompt the information 
url = input('Please enter URL: ')
price = float(input('Please write the price: '))
email = input('please enter write your email: ')

cur.execute('INSERT INTO products (url, target_price, user_email) VALUES (?,?,?)', (url, price, email))

conn.commit()
conn.close()

