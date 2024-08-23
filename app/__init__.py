from flask import Flask
from flask_mysqldb import MySQL
from config import app_config

app = Flask(__name__)
app.config.from_object(app_config)

mysql = MySQL(app)

from app.controllers import auth_controller, product_controller, user_controller
