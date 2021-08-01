from app import app
from flask_script import Manager, Server
from app import models


def custom_call():
#     populate_schedule()
#     
#     celery.conf.beat_schedule["test_task"] = {
#                 'task': 'tasks.my_scheduled_task',
#                 'schedule': 30,
#                 'args': (7, "test", 1, 1)
#                 }
#    
#    print(celery.conf.beat_schedule)
    pass


class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        custom_call()
        return Server.__call__(self, app, *args, **kwargs)

manager = Manager(app)

# Remeber to add the command to your Manager instance
manager.add_command('runserver', CustomServer())


if __name__ == "__main__":    
    #for zone in Zone.query.all():
    #    if not zone.disabled:
    #        schedule.every(zone.interval_days).day.at(zone.scheduled_time.strftime("%H:%M")).do(run_water, zone.number, zone.alias, zone.duration_minutes)

    #app.run(debug=True, host='0.0.0.0', port=8888)
    manager.run()