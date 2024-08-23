from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "flash message"

app.config.from_object('config')

mysql = MySQL(app)

from app.controllers import auth_controller, product_controller, user_controller
