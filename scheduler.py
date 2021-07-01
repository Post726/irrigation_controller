from celery.schedules import crontab
from models import Zone, Water


def populate_schedule(celery):
    for zone in Zone.query.all():
        task_name = f'zone_{zone.number}_schedule'
        if zone.disabled:
            if task_name in celery.conf.beat_schedule:
                del celery.conf.beat_schedule[task_name]
        else:
            celery.conf.beat_schedule[task_name] = {
                'task': 'tasks.my_scheduled_task',
                'schedule': crontab(hour=zone.scheduled_time.strftime("%H"), minute=zone.scheduled_time.strftime("%M")),
                'args': (zone.number, zone.alias, zone.interval_days, zone.duration_minutes)
                }


@celery.task(name='tasks.my_scheduled_task')
def my_scheduled_task(zone, alias, days, duration):
    os.system(f'touch /home/pi/wksp/irrigation_controller/zone_{zone}.start')
    time.sleep(duration*60)
    os.system(f'touch /home/pi/wksp/irrigation_controller/zone_{zone}.end')
