from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'clothing_store_secret'

def init_db():
    conn = sqlite3.connect('bill.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        items TEXT,
        total REAL
    )''')
    conn.commit()
    conn.close()

# ---------- Welcome Page ----------
@app.route('/')
def welcome():
    return render_template('welcome.html')

# ---------- Catalog Page ----------
@app.route('/catalog')
def catalog():
    catalog = [
        {"id": 1, "name": "T-Shirt", "price": 500},
        {"id": 2, "name": "Jeans", "price": 1200},
        {"id": 3, "name": "Jacket", "price": 2000},
        {"id": 4, "name": "Dress", "price": 1500},
        {"id": 5, "name": "Sweater", "price": 1000},
        {"id": 6, "name": "Long dress", "price": 2000}
    ]
    return render_template('index.html', catalog=catalog)

# ---------- Add to Cart ----------
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = {
        "id": request.form['item_id'],
        "name": request.form['item_name'],
        "price": float(request.form['item_price'])
    }
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(item)
    session.modified = True
    return redirect('/catalog')

# ---------- View Cart ----------
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

# ---------- Checkout ----------
@app.route('/checkout', methods=['POST'])
def checkout():
    customer_name = request.form['customer_name']
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    items_str = ', '.join(item['name'] for item in cart_items)

    conn = sqlite3.connect('bill.db')
    c = conn.cursor()
    c.execute("INSERT INTO bills (customer_name, items, total) VALUES (?, ?, ?)",
              (customer_name, items_str, total))
    conn.commit()
    conn.close()

    session.pop('cart', None)
    return render_template('thankyou.html', customer=customer_name, items=items_str, total=total)

# ---------- Run App ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
