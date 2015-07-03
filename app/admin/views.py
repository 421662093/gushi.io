#!/usr/bin/env python
#-*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask.ext.login import login_required, current_user, logout_user
from . import admin
from .decorators import permission_required
from .forms import EditEventForm
from ..models import Permission, EventApply, Event
from ..core import common


@admin.route('/eventapplylist', defaults={'eid': 0},)
@admin.route('/eventapplylist/<int:eid>', methods=['GET', 'POST'])
#@permission_required(Permission.LIST_USER)
#@login_required
#@admin_required
#@permission_required(Permission.USER)
def eventapply_list(eid):

    if request.method == 'POST':
        page = request.args.get('page', 1, type=int)
        show_followed = False

        print 'post'
    else:

        '''
        col1 = models.Test()
        col1.id = models.collection.get_next_id('test333')
        col1.body = 'discovery2222'
        col1.body_html = '222'
        col1.save()

        col1 = models.User()
        col1.id = models.collection.get_next_id('user')
        col1.email = '1@qq.com'
        col1.username = 'clr'
        col1.password = '123456'
        col1.save()
        '''
        ea_list = EventApply.getlist(eid=eid)
        func = {'stamp2time': common.stamp2time}

        # orig.get(body='Ross19').update({'$rename': {'body_html': 'body_w'}})
        return render_template('admin/eventapply_list.html', list=ea_list, common=func)


@admin.route('/eventlist')
def event_list():

    e_list = Event.getlist()
    func = {'stamp2time': common.stamp2time}

    return render_template('admin/event_list.html', list=e_list, common=func)


@admin.route('/eventedit', defaults={'id': 0}, methods=['GET', 'POST'])
@admin.route('/eventedit/<int:id>', methods=['GET', 'POST'])
#@permission_required(Permission.LIST_USER)
def event_edit(id):
    form = EditEventForm()

    if request.method == 'POST' and form.validate_on_submit():
        event = Event()
        event._id = id
        event.title = form.title.data
        event.start = form.start.data
        event.end = form.end.data
        event.address = form.address.data
        event.content = common.htmlescape(form.content.data)
        print str(form.validate_on_submit()) + '_' + event.title + '_' + str(event.start) + '_' + str(event.end) + '_' + event.address + '_' + event.content + '_'
        event.editinfo()
        return redirect(url_for('.event_list'))
    else:

        '''
        col1 = models.Test()
        col1.id = models.collection.get_next_id('test333')
        col1.body = 'discovery2222'
        col1.body_html = '222'
        col1.save()

        col1 = models.User()
        col1.id = models.collection.get_next_id('user')
        col1.email = '1@qq.com'
        col1.username = 'clr'
        col1.password = '123456'
        col1.save()
        '''
        isevent = False
        if id > 0:
            event = Event.getinfo(id)
            if id > 0 and event:
                isevent = True
        else:
            event = []
        func = {'stamp2time': common.stamp2time,
                'unescape': common.htmlunescape}
        return render_template('admin/event_edit.html', event=event, isevent=isevent, form=form, func=func)


@admin.route('/logout')
def logout():
    logout_user()
    return jsonify(msg='用户已登出')
