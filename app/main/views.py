#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask.ext.login import login_required, current_user
from ..decorators import admin_required, permission_required
'''
from flask.ext.sqlalchemy import get_debug_queries
'''
from . import main
from .forms import EventApplyForm
from ..core import common

'''
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
    CommentForm
from .. import db
from ..models import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required
'''
from ..models import EventApply, Event, collection

# from ..models import Post


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/baoming/<int:eid>', methods=['GET', 'POST'])
def baoming(eid=0):

    if request.method == 'POST':
        form = EventApplyForm()

        if form.submit() and eid > 0:
            item = EventApply()
            item.event_id = eid
            item.id = collection.get_next_id('topics')
            item.name = form.name.data
            item.phone = form.phone.data
            item.company = form.company.data
            item.job = form.job.data
            item.remark = form.remark.data
            item.save()
            # print str(item.id) + '_' + item.name + '_' + item.phone + '_' +
            # item.company + '_' + item.job + '_' + item.remark
            return '{"info":"seccess","status":"y"}'
        else:
            return '{"info":"error","status":"n"}'
    else:
        '''
        item = Event()
        item.event_id = eid
        item.id = collection.get_next_id('events')
        item.title ='西城区新街口北大街74号剧空间剧场(近北京科学'
        item.address = '北京市西城区新街口北大街74号剧空间剧场(近北京科学教育电影制片厂院内)'
        item.content = '北京市西城区新街口北大街74号剧空间剧场(近北京科学教育电影制片厂院内)北京市西城区新街口北大街74号剧空间剧场(近北京科学教育电影制片厂院内)北京市西城区新街口北大街74号剧空间剧场(近北京科学教育电影制片厂院内)'
        item.save()
        '''
        event = Event.getinfo(eid)
        return render_template('baoming.html', event=event)
