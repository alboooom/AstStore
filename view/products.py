from flask import render_template, redirect, url_for, Blueprint, request
from db_api.db_select import select
from repository.product_repository import select_product


def allview():

    data = {
        "categories" : select("SELECT  name , url  FROM category"),
        "products" : select("SELECT  name , url, price, image, product_id  FROM products"),
        "accessories" : select("SELECT name, url FROM accessories"),
        "sliders" : select("SELECT name, image, description,  url, button FROM sliders"),
        "messengers" : select("SELECT name, url FROM messengers")
    }
    return render_template("products.html", ds=data)


def oneview():

    data_id = (request.values.to_dict())["id"]
    data = select_product(data_id)
    return render_template('product.html', ds=data)





