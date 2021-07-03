from flask import Flask
from app.config import Config
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from celery import Celery
from app.board import Board


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

board = Board()

from app import routes
