from flask import render_template, redirect, url_for, Blueprint
from db_api.db_select import select

SQL_SELECT_ONE_Product = ''' SELECT name, price, image, about, (select array(select image FROM product_image
                             WHERE product_id = '{param_id}')) as images, (select image FROM product_image
                             WHERE product_id = '{param_id}' and main = True) as main_img  
                             FROM products WHERE product_id = '{param_id}' '''


def select_product(prod_id):
    return select(SQL_SELECT_ONE_Product.format(param_id=prod_id))
