import os

WTF_CSRF_ENABLED = True
SECRET_KEY = '2Dhe5dGyttvDqAQv'


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True




# Flask-Mail configuration
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
# MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_USERNAME = '763444204@qq.com'
MAIL_PASSWORD = 'hbdqlqfbtlzkbeec'
MAIL_DEFAULT_SENDER = '763444204@qq.com'

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
