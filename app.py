from flask import Flask, render_template, request
from add_product import registrar_producto 
app = Flask(__name__)
@app.route('/',methods=['GET', 'POST'])
def index () :
    if request.method == 'POST':
        url_product = request.form['url']
        price_product = float(request.form['price'])
        email_costumer = request.form['email']
        phone_costumer = request.form['phone']
        registrar_producto(url_product, price_product, email_costumer, phone_costumer)
    return render_template("index.html")
    

if __name__ == '__main__':
    app.run(debug=True)