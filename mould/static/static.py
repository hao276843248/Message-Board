from flask import Blueprint, render_template, current_app

# 创建蓝图，第一个参数指定了蓝图的名字。
static = Blueprint('static', __name__)


@static.route('/')
def hello_world():
    return render_template("index.html")


@static.route('/favicon.ico')
def favicon():
    # 静态路径访问的模拟默认实现，send_static_file
    return current_app.send_static_file('news/lyb.png')
