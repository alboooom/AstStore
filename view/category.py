from flask import render_template, redirect, url_for, Blueprint
from logic.db_select import select

def view():
    categories = select('SELECT  Name, url, pictures  FROM category')
    accessories = select('SELECT name, url FROM accessories')

    return render_template('categories.html', categories = categories, accessories = accessories)