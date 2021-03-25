import os
import sys
import threading

import flask
from flask import Flask, request, render_template, jsonify, current_app
import time

app = Flask(__name__)

tokens = {}
session = {"session":time.time()}


class FileUtil():
    file_path = sys.path[0] + "/"
    file_name = "msg.db"

    def __init__(self):
        if not sys.path.extend(self.file_path + self.file_name):
            open(self.file_path + self.file_name, "w+")

    def write(self, msg):
        if msg:
            with threading.Lock():
                with open(self.file_path + self.file_name, "a+") as f:
                    f.write(msg + "\n")

    def read(self):
        data = []
        with threading.Lock():
            with open(self.file_path + self.file_name, "r") as f:
                data = f.readlines()
        return data

    def delete(self, index):
        with threading.Lock():
            with open(self.file_path + self.file_name, "r") as f:
                msg = f.readlines()
            msg.pop(index)
            with open(self.file_path + self.file_name, "w") as f:
                f.write("".join(msg))


FILE_UTIL = FileUtil()


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/get_data')
def get_data():
    errno = 1
    key = str(time.time())
    tokens["key"] = key
    if request.cookies.get("session") == session.get("session"):
        errno = 0
    mkres = flask.make_response(jsonify({"data": FILE_UTIL.read(), "errno": errno}))
    mkres.set_cookie('token', key)  # 设置token 签名
    return mkres


@app.route('/input', methods=["POST"])
def msg_input():
    if request.cookies.get("token") == tokens.get("key"):
        # 1. 获取到传入参数
        data_dict = request.json
        msg = data_dict.get("msg")
        FILE_UTIL.write(msg)
    else:
        return jsonify(errno=0, msg="风控异常")
    return jsonify(errno=0, msg="写入成功")


@app.route('/favicon.ico')
def favicon():
    # 静态路径访问的模拟默认实现，send_static_file
    return current_app.send_static_file('news/lyb.png')


@app.route('/login', methods=["GET", "POST"])
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


@app.route('/logout', methods=["GET", "POST"])
def admin_logout():
    mkres = flask.make_response(render_template("index.html"))
    mkres.delete_cookie('session')  # cookies只有在响应返回的时候才能设置
    return mkres


@app.route('/delete/<int:index>', methods=["POST"])
def delete(index):
    if request.cookies.get("session") == session.get("session"):
        FILE_UTIL.delete(index)
    return jsonify(errno=0)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
