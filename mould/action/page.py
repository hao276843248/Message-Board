import time

import flask
from flask import Blueprint
from flask import request, jsonify

from mould.session import tokens, session
from mould.util import FILE_UTIL, message_filter

# 创建蓝图，第一个参数指定了蓝图的名字。
page = Blueprint('page', __name__)


@page.route('/total')
def total():
    return jsonify(errno=0, msg="", data=FILE_UTIL.total())
