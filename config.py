#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    '''
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    '''
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # mongodb://user1:password1@localhost/test
    MONGODB_SETTINGS = {
        'db': 'event',
        'host': 'mongodb://localhost:27017/'
    }
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    '''
    '''
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging  # 日志系统

        logging.basicConfig(level=logging.DEBUG,
                            format='%(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename='log/error.log',
                            filemode='w')

        DEBUG = logging.StreamHandler()
        DEBUG.setLevel(logging.DEBUG)
        ERROR = logging.StreamHandler()
        ERROR.setLevel(logging.ERROR)  #

        logging.debug('This is debug message')
        logging.info('This is info message')
        logging.warning('This is warning message')
        ###########
        ''''''
        formatter = logging.Formatter(
            '%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        ''''''
        ###########
        app.logger.addHandler(DEBUG)
        app.logger.addHandler(ERROR)
    '''

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
