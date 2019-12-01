from flask import render_template, redirect, url_for, Blueprint
from logic.db_select import select

def view():
    categories = select('SELECT  Name, url  FROM category')
    accessories = select('SELECT name, url FROM Accessories')

    return render_template('index.html', categories = categories, accessories = accessories)





