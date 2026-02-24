import os
from celery import Celery
from celery.schedules import crontab

from . import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.update(CELERY_TIMEZONE=settings.TIME_ZONE,
                CELERYD_POOL='solo')   # с этим параметром запускаем селери без флага --pool=solo,
                                        # команда как на линксе: celery -A NewsPaper worker -l INFO

app.conf.beat_schedule = {
    'sending_publications_for_the_previous_week_on_mondays': {
        'task': 'news.tasks.sending_out_posts_for_the_previous_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),

    },
}

# CELERY_TIMEZONE='UTS' выдает ошибку  WARNING/MainProcess] zoneinfo._common.ZoneInfoNotFoundError: 'No time zone found with key UTS'
