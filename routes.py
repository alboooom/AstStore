from flask import Flask, render_template, redirect, url_for
from view import main, category
import psycopg2
app = Flask(__name__)
@app.route('/')
def home():
    return main.view()


@app.route('/categories.html')
def categories():
    return category.view()


@app.route('/index.html')
def back_home():
    return main.view()


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
