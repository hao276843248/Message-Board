from flask import Blueprint,render_template
#创建蓝图，第一个参数指定了蓝图的名字。
users = Blueprint('user',__name__)