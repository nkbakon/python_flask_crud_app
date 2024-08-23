import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'flash message'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'flaskcrud'

app_config = Config()