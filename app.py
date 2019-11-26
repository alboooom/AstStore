from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main():
    return render_template('index.html')
@app.route('/categories.html')
def categories():
    return render_template('categories.html')
@app.route('/index.html')
def back_home():
    return redirect(url_for('main'))
@app.route('/cart.html')
def cart():
    return render_template('cart.html')
@app.route('/product.html')
def product():
    return render_template('product.html')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')
@app.route('/checkout.html')
def checkout():
    return render_template('checkout.html')
