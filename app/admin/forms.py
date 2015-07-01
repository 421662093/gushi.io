#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask.ext.wtf import Form

from wtforms import IntegerField, StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError, validators
from flask.ext.pagedown.fields import PageDownField
#from ..models import User


class EditEventForm(Form):

    title = StringField('title', validators=[Length(0, 64)])
    start = IntegerField('start')
    end = IntegerField('end')
    address = StringField('address', validators=[Length(0, 128)])
    content = StringField('content')
