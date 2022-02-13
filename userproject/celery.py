
from django.conf import settings

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','userproject.settings')
app=Celery('userproject')
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'request:{self.request!r}')