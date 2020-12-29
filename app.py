import sys

import flask
from flask import Flask, request, render_template, jsonify, current_app

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/get_data')
def get_data():
    path = sys.path[0] + "\msg.db"
    with open(path) as f:
        msg = f.readlines()
    errno = 1
    if request.cookies.get("session") == "Trues":
        errno = 0
    return jsonify(data=msg, errno=errno)


@app.route('/input', methods=["POST"])
def msg_input():
    # 1. 获取到传入参数
    data_dict = request.json
    msg = data_dict.get("msg")
    path = sys.path[0] + "\msg.db"
    if msg:
        with open(path, "a") as f:
            f.write(msg + "\n")
    return jsonify(errno=0)


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
        mkres = flask.make_response(jsonify({"errno": 0}))
        mkres.set_cookie('session', "Trues")  # cookies只有在响应返回的时候才能设置
        return mkres
    else:
        return jsonify(errno=1, errmsg="密码错误", )


@app.route('/logout', methods=["GET", "POST"])
def admin_logout():
    mkres = flask.make_response(render_template("index.html"))
    mkres.delete_cookie('session')  # cookies只有在响应返回的时候才能设置
    return mkres


@app.route('/delete/<int:index>', methods=["POST"])
def delete(index):
    if request.cookies.get("session") == "Trues":
        path = sys.path[0] + "\msg.db"
        with open(path) as f:
            msg = f.readlines()
        msg.pop(index)
        with open(path, "w") as f:
            f.write("".join(msg))
    return jsonify(errno=0)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
