# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'service_center_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель данных для ремонтных услуг
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()
    if Product.query.count() == 0:
        items = [
            Product(name="Диагностика ПК и выявление неисправностей", price=0, image="diagnostic.jpg", category="Ремонт компьютеров"),
            Product(name="Сложный ремонт материнской платы ПК", price=2500, image="motherboard.jpg", category="Ремонт компьютеров"),
            Product(name="Замена термопасты и чистка системы охлаждения", price=1200, image="cleaning.jpg", category="Ремонт компьютеров"),
            Product(name="Восстановление и перепайка цепей питания", price=3200, image="power.jpg", category="Ремонт компьютеров"),
            Product(name="Сборка персонального компьютера под ключ", price=4000, image="assembly.jpg", category="Ремонт компьютеров"),
            Product(name="Ремонт и обслуживание лазерных принтеров / МФУ", price=1800, image="printer_fix.jpg", category="Периферия"),
            Product(name="Заправка и восстановление картриджей", price=600, image="toner.jpg", category="Периферия"),
            Product(name="Ремонт ЖК-мониторов (замена ламп, плат инвертора)", price=2000, image="lcd.jpg", category="Периферия"),
            Product(name="Ремонт блоков питания периферийных устройств", price=1100, image="psu.jpg", category="Периферия"),
            Product(name="Восстановление кабелей и разъемов (USB, VGA, HDMI)", price=800, image="cables.jpg", category="Периферия")
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

# СТРАНИЦА КОРЗИНЫ С ПОДЧЕТОМ СТОИМОСТИ
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
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total
            })
            
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# ОЧИСТКА КОРЗИНЫ
@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)