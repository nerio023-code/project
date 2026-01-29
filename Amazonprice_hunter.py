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
    
    conn = sqlite3.connect('deals.db')
    cur = conn.cursor()

    # Leemos de la tabla correcta
    cur.execute('SELECT * FROM products_v2')
    items = cur.fetchall()

    # Usamos headers más completos para que Amazon no nos oculte info
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    email = 'nerio023@gmail.com'
    password = 'fwkl pydl dppr kzzg'

    for item in items:
        url = item[1]
        target_price = item[2]
        client_email = item[3]
        user_phone = item[4]

        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscamos el título
            title_element = soup.find('span', id='productTitle')
            
            # --- MEJORA EN LA BUSQUEDA DE PRECIO ---
            # Primero intentamos la clase estándar
            price_element = soup.find('span', class_='a-offscreen')
            
            # Si no funciona, intentamos con 'a-price-whole' (otra forma que usa Amazon)
            if not price_element:
                price_element = soup.find('span', class_='a-price-whole')

            if title_element and price_element:
                title = title_element.get_text().strip()
                price_text = price_element.get_text().strip()
                
                # --- CORRECCIÓN PARA ROPA Y RANGOS ---
                # Si Amazon devuelve algo como "$20.00 - $50.00", nos quedamos solo con la primera parte
                if "-" in price_text:
                    price_text = price_text.split("-")[0].strip()

                # Limpiamos el precio ($25.99 -> 25.99)
                price_clean = price_text.replace(',', '').replace('$', '')
                
                # Verificamos que NO esté vacío antes de convertir
                if price_clean:
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
                            connection.sendmail(from_addr=email, to_addrs=client_email, msg=message.as_string())
                            connection.close()
                            
                            cur.execute('''UPDATE products_v2 SET target_price = ? WHERE url = ?''', (my_price, url))
                            conn.commit()
                            print("Email enviado.")
                else:
                    print(f"⚠️ No se pudo leer el precio numérico para: {title[:15]}...")

            else:
                print(f"⚠️ No se encontró elemento de precio para el link: {url[:30]}...")
        
        except Exception as e:
            print(f"Error revisando {url}: {e}")

    conn.close()
    print('--- Revisión finalizada ---')









   
   









