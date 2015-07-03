#!/usr/bin/env python
#-*- coding: utf-8 -*-
from datetime import datetime
from flask.ext.mongoengine.wtf import model_form
from mongoengine import EmbeddedDocument, EmbeddedDocumentField

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import hashlib

from app.exceptions import ValidationError
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from core import common


class Permission:
    USER = 0x01
    LIST_USER = 0x11
    EDIT_USER = 0x12
    DISCOVERY = 0x02
    INDEX_DISCOVERY = 0x21
    ADMINISTER = 0x80


class Event(db.Document):
    __tablename__ = 'event'
    meta = {
        'collection': __tablename__,
    }
    _id = db.IntField(primary_key=True)
    title = db.StringField(
        default='', max_length=32, db_field='t')  # 用户id，0为官方话题
    start = db.IntField(default=common.getstamp(), db_field='s')
    end = db.IntField(default=common.getstamp(), db_field='e')
    address = db.StringField(default='', db_field='a')
    content = db.StringField(default='', db_field='c')

    @staticmethod
    def getlist(count=10):
        #.exclude('password_hash') 不包含字段
        return Event.objects().order_by("-date").limit(count)

    @staticmethod
    def getinfo(eid):
        #.exclude('password_hash') 不包含字段
        return Event.objects.get(_id=eid)

    def editinfo(self):
        if self._id > 0:
            update = {}
            # update.append({'set__email': self.email})

            if len(self.title) > 0:
                update['set__title'] = self.title
                update['set__start'] = self.start
                update['set__end'] = self.end
            if len(self.address) > 0:
                update['set__address'] = self.address
            if len(self.content) > 0:
                update['set__content'] = self.content

            Event.objects(_id=self._id).update_one(**update)
            return 1
        else:
            self._id = collection.get_next_id(self.__tablename__)
            self.save()
            return self._id


class EventApply(db.Document):
    __tablename__ = 'eventapply'
    meta = {
        'collection': __tablename__,
    }
    _id = db.IntField(primary_key=True)
    name = db.StringField(
        default='', max_length=32, db_field='n')  # 用户id，0为官方话题
    phone = db.StringField(default='', max_length=20,  db_field='p')
    company = db.StringField(default='', max_length=64, db_field='c')
    job = db.StringField(default='', max_length=64, db_field='j')
    remark = db.StringField(default='', db_field='r')
    event_id = db.IntField(default=0, db_field='ei')
    date = db.IntField(default=common.getstamp(), db_field='d')

    @staticmethod
    def getlist(eid=0, count=10):
        if eid == 0:
            return EventApply.objects().order_by("-date").limit(count)
        else:
            return EventApply.objects(event_id=eid).order_by("-date").limit(count)

    @staticmethod
    def isphone(eid, phone):
        #.exclude('password_hash') 不包含字段
        return EventApply.objects(event_id=eid, phone=phone)


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id)


class collection(db.Document):
    meta = {
        'collection': 'collection',
    }
    name = db.StringField(max_length=30, required=True)
    index = db.IntField(required=True)

    @staticmethod
    def get_next_id(tablename):
        doc = collection.objects(name=tablename).modify(inc__index=1)
        if doc:
            return doc.index + 1
        else:
            collection(name=tablename, index=1).save()
            return 1
