# this is my python project, is a web app that track deals of different
#  products on amazon (or other e comerce platforms) and send you an email 
# when this product drop his price
#----------------------------------------------------------------------------------------------
# Starting importing my toolbox
import sqlite3
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def verificar_precios():
    print('--- Verificando precios ---')
    
    # 1. Abrimos la base de datos
    conn = sqlite3.connect('deals.db')
    cur = conn.cursor()

    # Leemos de la tabla correcta
    cur.execute('SELECT * FROM products_v2')
    items = cur.fetchall()

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    email = 'nerio023@gmail.com'
    password = 'fwkl pydl dppr kzzg'

    for item in items:   # Analizando cada producto
        url = item[1]
        target_price = item[2]
        client_email = item[3]
        user_phone = item[4]

        # Usamos try para que si un producto falla, el programa NO se detenga y siga con el siguiente
        try:
            # HTML parsing
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_element = soup.find('span', id='productTitle')
            price_element = soup.find('span', class_='a-offscreen')
            
            if title_element and price_element:
                title = title_element.get_text().strip()
                price_text = price_element.get_text().strip()
                
                # Limpiamos el precio ($25.99 -> 25.99)
                price_clean = price_text.replace(',', '').replace('$', '')
                my_price = float(price_clean) 
                
                print(f"Revisando: {title[:15]}... | Precio: {my_price} | Meta: {target_price}")

                # LOGICA DE PRECIO
                if my_price < target_price:
                    print('¡ALERTA! El precio ha bajado.')
                    
                    if client_email and '@' in client_email:
                        message = MIMEMultipart()
                        message["Subject"] = f"🔥 Price Drop: {title[:30]}..."
                        message["From"] = email
                        message["To"] = client_email

                        html = f"""
                        <html>
                        <body style="font-family: Arial; border: 1px solid #eee; padding: 20px;">
                            <h2 style="color: #232f3e;">Price Alert!</h2>
                            <p>Your item <strong>{title}</strong> is now at <strong>${my_price}</strong></p>
                            <a href="{url}" style="background-color: #ff9900; color: white; padding: 10px; text-decoration: none;">Buy on Amazon</a>
                        </body>
                        </html>
                        """
                        
                        message.attach(MIMEText(html, "html"))
                        
                        connection = smtplib.SMTP("smtp.gmail.com", 587)
                        connection.starttls()
                        connection.login(user=email, password=password)
                        connection.sendmail(
                            from_addr=email,
                            to_addrs=client_email,
                            msg=message.as_string()
                        )
                        connection.close() # Cerramos el servidor de correo
                        
                        # Actualizamos la base de datos para no enviar el mismo correo mil veces
                        # Actualizamos el target_price al nuevo precio bajo encontrado
                        cur.execute('''UPDATE products_v2 SET target_price = ? WHERE url = ?''', (my_price, url))
                        conn.commit()
                        print("Email enviado exitosamente.")

                    if user_phone:
                        print("Aquí iría la lógica para enviar SMS.")
        
        except Exception as e:
            # Si hay un error con UN producto, lo imprimimos y seguimos con el siguiente
            print(f"Error revisando {url}: {e}")

    # Cerramos la base de datos AL FINAL de todo
    conn.close()
    print('--- Revisión finalizada ---')










   
   









