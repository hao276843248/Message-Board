import time

import flask
from flask import Blueprint
from flask import request, jsonify

from mould.session import tokens, session
from mould.util import FILE_UTIL, message_filter

# 创建蓝图，第一个参数指定了蓝图的名字。
action = Blueprint('action', __name__)


@action.route('/get_data')
def get_data():
    index = int(request.args.get("index",1))
    errno = 1
    key = str(time.time())
    tokens["key"] = key
    if request.cookies.get("session") == session.get("session"):
        errno = 0
    make_res = flask.make_response(jsonify({"data": FILE_UTIL.read_page(index), "errno": errno}))
    make_res.set_cookie('token', key)  # 设置token 签名
    return make_res


@action.route('/input', methods=["POST"])
def msg_input():
    if request.cookies.get("token") == tokens.get("key"):
        # 1. 获取到传入参数
        data_dict = request.json
        msg = data_dict.get("msg")
        msg_filter = message_filter(msg)
        FILE_UTIL.write(msg_filter)
    else:
        return jsonify(errno=0, msg="风控异常")
    return jsonify(errno=0, msg="写入成功")


@action.route('/delete/<int:index>', methods=["POST"])
def delete(index):
    if request.cookies.get("session") == session.get("session"):
        FILE_UTIL.delete(index)
    return jsonify(errno=0)
