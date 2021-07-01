from flask import Flask
from app.config import Config
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from celery import Celery

#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

#celery.conf.update(app.config)

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)

from app import routes
