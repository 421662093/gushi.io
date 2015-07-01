#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import Flask
from flask.ext.mongoengine import MongoEngine
# from flask.ext.bootstrap import Bootstrap
# from flask.ext.mail import Mail
# from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
db = MongoEngine()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # app.config.from_pyfile('the-config.cfg')

    config[config_name].init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .core import core as core_blueprint
    app.register_blueprint(core_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
