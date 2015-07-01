#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from app import create_app, db
#from app.models import User, Follow, Role, Permission, Post, Comment
from app.models import collection
# from flask.ext.migrate import Migrate, MigrateCommand  # 迁移跟踪
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    app.run()  # 192.168.199.239
