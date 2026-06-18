# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'service_center_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(300), nullable=False) # Увеличили длину под ссылки
    category = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()
    if Product.query.count() == 0:
        items = [
            Product(name="Диагностика ПК и выявление неисправностей", price=0, image="https://images.pexels.com/photos/2582937/pexels-photo-2582937.jpeg?auto=compress&cs=tinysrgb&w=400", category="Ремонт компьютеров"),
            Product(name="Сложный ремонт материнской платы ПК", price=2500, image="https://images.pexels.com/photos/343481/pexels-photo-343481.jpeg?auto=compress&cs=tinysrgb&w=400", category="Ремонт компьютеров"),
            Product(name="Замена термопасты и чистка системы охлаждения", price=1200, image="https://images.pexels.com/photos/2280549/pexels-photo-2280549.jpeg?auto=compress&cs=tinysrgb&w=400", category="Ремонт компьютеров"),
            Product(name="Восстановление и перепайка цепей питания", price=3200, image="https://images.pexels.com/photos/1435312/pexels-photo-1435312.jpeg?auto=compress&cs=tinysrgb&w=400", category="Ремонт компьютеров"),
            Product(name="Сборка персонального компьютера под ключ", price=4000, image="https://images.pexels.com/photos/45112/pexels-photo-45112.jpeg?auto=compress&cs=tinysrgb&w=400", category="Ремонт компьютеров"),
            
            Product(name="Ремонт и обслуживание лазерных принтеров / МФУ", price=1800, image="https://images.pexels.com/photos/459793/pexels-photo-459793.jpeg?auto=compress&cs=tinysrgb&w=400", category="Периферия"),
            Product(name="Заправка и восстановление картриджей", price=600, image="https://images.pexels.com/photos/3933221/pexels-photo-3933221.jpeg?auto=compress&cs=tinysrgb&w=400", category="Периферия"),
            Product(name="Ремонт ЖК-мониторов (замена ламп, плат инвертора)", price=2000, image="https://images.pexels.com/photos/1038916/pexels-photo-1038916.jpeg?auto=compress&cs=tinysrgb&w=400", category="Периферия"),
            Product(name="Ремонт блоков питания периферийных устройств", price=1100, image="https://images.pexels.com/photos/8533217/pexels-photo-8533217.jpeg?auto=compress&cs=tinysrgb&w=400", category="Периферия"),
            Product(name="Восстановление кабелей и разъемов (USB, VGA, HDMI)", price=800, image="https://images.pexels.com/photos/421927/pexels-photo-421927.jpeg?auto=compress&cs=tinysrgb&w=400", category="Периферия")
        ]
        db.session.add_all(items)
        db.session.commit()

@app.route('/')
@app.route('/catalog')
def catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']
    pid_str = str(product_id)
    if pid_str in cart:
        cart[pid_str] += 1
    else:
        cart[pid_str] = 1
    session['cart'] = cart
    return redirect(url_for('catalog'))

@app.route('/cart')
def cart():
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', cart_items=[], total_price=0)
    cart_items = []
    total_price = 0
    for product_id, quantity in session['cart'].items():
        product = Product.query.get(int(product_id))
        if product:
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)