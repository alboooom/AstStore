from flask import render_template, redirect, url_for, Blueprint
from logic.db_select import select

def view():
    data = {
    "categories" : select("SELECT  name , url  FROM category"),
    "accessories" : select("SELECT name, url FROM accessories"),
    "sliders" : select("SELECT name, image, description,  url FROM sliders")
    }
    return render_template("index.html", ds = data)





