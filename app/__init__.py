import os
from flask import Flask
from flask_login import LoginManager
from flask_openid import OpenID
from flask_sqlalchemy import SQLAlchemy

from config import Config, basedir

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

lm.login_view = 'login'

from app import views, models
