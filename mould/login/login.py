import time

import flask
from flask import request, jsonify, render_template, Blueprint

# 创建蓝图，第一个参数指定了蓝图的名字。
from mould.session import session

login = Blueprint('login', __name__)


@login.route('/login', methods=["GET", "POST"])
def admin_login():
    # 取到登录的参数
    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)
    if not all([username, password]):
        return jsonify(errno=1, errmsg="请输入用户名密码")

    if username == str(1) and password == str(1):
        key = str(time.time())
        session["session"] = key
        makers = flask.make_response(jsonify({"errno": 0}))
        makers.set_cookie('session', key)  # cookies只有在响应返回的时候才能设置
        return makers
    else:
        return jsonify(errno=1, errmsg="密码错误", )


@login.route('/logout', methods=["GET", "POST"])
def admin_logout():
    make_res = flask.make_response(render_template("index.html"))
    make_res.delete_cookie('session')  # cookies只有在响应返回的时候才能设置
    return make_res
