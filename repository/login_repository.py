from flask import render_template, redirect, url_for, Blueprint
from db_api.db_select import select

SQL_GET_USER_BY_USRNAME = ''' SELECT * FROM login WHERE username = '{username}' '''


def get_user_by_username():
    pass