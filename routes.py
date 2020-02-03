from flask import Flask, render_template, redirect, url_for, request, sessions

from login import LogMain
from view import main, category, products
import psycopg2
app = Flask(__name__)
l = LogMain()


@app.route('/login', methods=['GET', 'POST'])
def loginwindow():
    return l.loginwindow()


@app.route('/')
def Cmain():
    return main.view()


@app.route('/categories')
def Ccategory():
    return category.view()


# @app.route('/cart.html')
# def Ccart():
#     return render_template('cart.html')


@app.route('/products')
def Cproducts():
    return products.allview()


@app.route('/products/product')
def Cproduct():
    return products.oneview()


@app.route('/contact.html')
def Ccontact():
    return render_template('product.html')


@app.route('/checkout.html')
def Ccheckout():
    return render_template('checkout.html')
