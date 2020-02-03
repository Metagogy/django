


from __future__ import absolute_import
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import shared_task
import time

@periodic_task(run_every=(crontab(minute="*")), name="per", ignore_result=True)
def return_5():
	time.sleep(5)
	return 5

@shared_task  # Use this decorator to make this a asyncronous function
def longtime_add(x, y):
    print 'long time task begins'
    # sleep 5 seconds
    time.sleep(5)
    print 'long time task finished'
    return x + y