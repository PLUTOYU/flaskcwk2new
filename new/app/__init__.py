import logging
import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .flask_cerlery import make_celery
from flask_moment import Moment


#app and database's init
app = Flask(__name__)
moment = Moment(app)

app.config.from_object('config')
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)
#

#celery and redis's init
migrate = Migrate(app, db)

mail = Mail()

mail.init_app(app)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)


#auth blueprint's init
from app.auth import auth as auth_bp

app.register_blueprint(auth_bp, url_prefix='/')

#test_unit


from app import views, models
