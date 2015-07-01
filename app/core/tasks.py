# coding:utf-8
from datetime import datetime
from .. import scheduler

'''
@scheduler.scheduled_job('cron', id='my_job_id', second='*/3', hour='*')
def tick():
    print('Tick! The time is: %s' % datetime.now())
'''
