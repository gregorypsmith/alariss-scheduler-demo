# we need to add some more dependencies
# flask-sqlalchemy for the database
# flask-cas for CAS authentication

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_mail import Mail
from flask_login import LoginManager, UserMixin
from flask_bootstrap import Bootstrap


app = Flask(__name__, template_folder='../templates')
app.config.from_object("scheduler_app.config.DevelopmentConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# print(os.environ['APP_SETTINGS'])
basedir = os.path.abspath(os.path.dirname(__file__))
# database_uri_postgres = 'postgres://cvcpylyugwdnwt:8ee8510d9a25f68c30514e002dada5934d4bdbef06595f01e4b002fffc6b38da@ec2-54-204-39-43.compute-1.amazonaws.com:5432/d90r5mu72ko8a3'
database_uri = 'sqlite:///' + os.path.join(basedir, 'alariss.sqlite')

app.config.update(

	# # DB SETTINGS
	# SQLALCHEMY_TRACK_MODIFICATIONS = False,
    SQLALCHEMY_DATABASE_URI = database_uri,

	# EMAIL SETTINGS
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_TLS = False,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	
	)

db = SQLAlchemy(app)
admin = Admin(app)
mail = Mail(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from scheduler_app import routes