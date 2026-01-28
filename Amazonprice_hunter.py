# this is my python project, is a web app that track deals of different
#  products on amazon (or other e comerce platforms) and send you an email 
# when this product drop his price
#----------------------------------------------------------------------------------------------
# Star importing my toolbox
from bs4 import BeautifulSoup #read HTML
import requests   # It is the browser that travels through the web page 
import smtplib    #toolbox that send emails
from email.mime.text import MIMEText      #for the email content
from email.mime.multipart import MIMEMultipart 
import sqlite3   
import time   # my timer 

while True :      # infinte loop that keep looking for the price deals
    
    conn = sqlite3.connect('deals.db')   #open my database and read
    cur = conn.cursor()

    cur.execute('SELECT * FROM products')
    items = cur.fetchall()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
        }
    email = 'nerio023@gmail.com'
    password = 'fwkl pydl dppr kzzg'

    for item in items :   # analyzing each product 
        url = item[1]
        target_price = item[2]
        client_email = item[3]
        user_phone = item[4]

        # HTML parsing, looking the information on the website 
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        title_element = soup.find('span', id='productTitle')
        price_element = soup.find('span', class_='a-offscreen')
        if title_element and price_element :
            title = title_element.get_text().strip()   # clean the item name 
            price = price_element.get_text().strip()    # clean the item price 
            price_clean = price.replace(',', '').replace('$','')
            my_price = float(price_clean) 
                
            # create the logic for the target price  
            if target_price > my_price :
                print('Alert your product drop his price')
                
                if client_email and '@' in client_email:
                        # 1. Preparamos el "contenedor" del correo
                        message = MIMEMultipart()
                        message["Subject"] = f"🔥 Price Drop: {title[:40]}..."
                        message["From"] = email
                        message["To"] = client_email

                        # 2. create the HTML desing for the email
                        html = f"""
                        <html>
                        <body style="font-family: Arial; border: 1px solid #eee; padding: 20px;">
                            <h2 style="color: #232f3e;">Price Alert!</h2>
                            <p>Your item <strong>{title}</strong> is now at <strong>${my_price}</strong></p>
                            <a href="{url}" style="background-color: #ff9900; color: white; padding: 10px; text-decoration: none;">Buy on Amazon</a>
                        </body>
                        </html>
                        """
                        # 3. Metemos el HTML dentro del contenedor
                        message.attach(MIMEText(html, "html"))
                        connection = smtplib.SMTP("smtp.gmail.com", 587)
                        connection.starttls()
                        connection.login(user=email, password=password)
                        connection.sendmail(
                        from_addr=email,
                        to_addrs= client_email,
                        msg=message.as_string()
                        )
                        connection.close()
                        cur.execute('''UPDATE products SET target_price = ? WHERE url = ?''', (my_price, url))
                        conn.commit()
                        print("we'll sent you an email!")
                if user_phone :
                        print("we'll sent you a text message")
    conn.close()
    time.sleep(60 * 60 * 6)










   
   









