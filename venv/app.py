import logging
import os
from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import json

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config['DATABASE'] = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    db = get_db()
    products = db.execute('SELECT * FROM products').fetchall()
    return render_template('index.html', products=products)

@app.route('/admin')
def admin_page():
    conn = sqlite3.connect('/app/database.db')  # Sesuaikan lokasi database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")  # Ambil semua data di tabel orders
    orders = cursor.fetchall()
    conn.close()

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        user_id = request.form['user_id']
        server_id = request.form['server_id']
        nickname = request.form['nickname']
        email = request.form['email']
        whatsapp = request.form['whatsapp']
        cart_data = request.form['cart_data']
        
        cart = json.loads(cart_data)
        produk = ", ".join([item['name'] for item in cart])
        jumlah_produk = sum(item['quantity'] for item in cart)
        total_harga = sum(float(item['price']) * item['quantity'] for item in cart) + 1000  # Adding admin fee
        
        db = get_db()
        db.execute('INSERT INTO orders (user_id, server_id, nickname, email, whatsapp, produk, jumlah_produk, total_harga) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (user_id, server_id, nickname, email, whatsapp, produk, jumlah_produk, total_harga))
        db.commit()

        return redirect(url_for('paymentsuccess'))

    return render_template('checkout.html')

@app.route('/payment_success')
def paymentsuccess():
    return render_template('payment_success.html')

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/wdp')
def wdp():
    return render_template('wdp.html')

@app.route('/sl')
def sl():
    return render_template('sl.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
