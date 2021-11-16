# -*-coding:utf-8-*-
import datetime


class Config():
    # 动态跟踪修改
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置SQLalchemy数据库信息
    # 开发
    # SQLALCHEMY_DATABASE_URI = 'postgresql://dsti:fdAlks&8@10.12.7.226/dwdev01'
    # session 类型
    SESSION_TYPE = "memcached"
    # 设置秘钥
    SECRET_KEY = "QEWRQWERASDFVZXCVWREWQER111"
    SESSION_FILE_THRESHOLD = 500  # 存储session的个数如果大于这个值时，就要开始进行删除了
    SESSION_PERMANENT = True  # 如果设置为True，则关闭浏览器session就失效。
    # 过期时间 1小时
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=60 * 60)
    # 设置数据库显示查询语句
    # SQLALCHEMY_ECHO = False
    # 设置数据库自动提交
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class developmentConfig(Config):
    DEBUG = True


class productionConfig(Config):
    DEBUG = False


config = {'development': developmentConfig,
          'production': productionConfig}
