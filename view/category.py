from flask import render_template, redirect, url_for, Blueprint
from db_api.db_select import select


def view():
    data = {
    "categories" : select("SELECT  name , url, pictures  FROM category"),
    "accessories" : select("SELECT name, url FROM accessories"),
    "messengers" : select("SELECT name, url FROM messengers")
    }
    return render_template("categories.html", ds = data)





