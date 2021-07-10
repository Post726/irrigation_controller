from flask import Flask, _app_ctx_stack
from app.config import Config
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from celery import Celery
from app.board import Board
from sqlalchemy.orm import scoped_session
from .database import SessionLocal, engine


app = Flask(__name__)
app.config.from_object(Config)

app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

csrf = CSRFProtect(app)
bootstrap = Bootstrap(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

board = Board()

from app import routes
