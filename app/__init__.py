__author__ = 'analytic'

import logging
from logging.handlers import RotatingFileHandler
import sys
from mail import mail
from conf import BaseConfig

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


def configure_extensions(app):
    # mongo.init_app(app)
    mail.init_app(app)


def configure_logger(app):
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # 4MB max upload size
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
    app.secret_key = 'z\xcbu\xe5#\xf2U\xe5\xc4,\x0cz\xf9\xcboA\xd2Z\xf7Y\x15"|\xe4'

    log = logging.getLogger('werkzeug')
    if 'LOGGING_FILE' in app.config:
        handler = RotatingFileHandler(app.config['LOGGING_FILE'],
                                      maxBytes=10000000,
                                      backupCount=5)
    else:
        handler = logging.StreamHandler(sys.stdout)

    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    log.addHandler(handler)


app = Flask(__name__, static_folder="./upload")
app.name = "artFlask"
app.config.from_object(BaseConfig)
configure_logger(app)
configure_extensions(app)
db = SQLAlchemy(app)

import views
