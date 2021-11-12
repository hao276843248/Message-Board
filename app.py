from flask import Flask

from mould.action.action import action
from mould.action.page import page
from mould.login.login import login
from mould.static.static import static

app = Flask(__name__)

# 注册蓝图，第一个参数logins是蓝图对象，url_prefix参数默认值是根路由，如果指定，会在蓝图注册的路由url中添加前缀。
app.register_blueprint(action, url_prefix='')
app.register_blueprint(login, url_prefix='')
app.register_blueprint(static, url_prefix='')
app.register_blueprint(page, url_prefix='')

if __name__ == '__main__':
    print(app.url_map)
    app.run(host="0.0.0.0", port=4000)
