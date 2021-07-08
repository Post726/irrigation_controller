from app import app, celery, board
from app.models import db, Zone, Water, Temperature
from app.board import pins, Board
import os
import time
from datetime import datetime


# setting up the context for SQLAlchemy
app.app_context().push()


# This is not working. Only seem able to setup schedule at app start
# Need to move to django or restart flask app to pickup schedule updates
# def populate_schedule():
#     for zone in Zone.query.all():
#         task_name = f'zone_{zone.number}_schedule'
#         if zone.disabled:
#             if task_name in celery.conf.beat_schedule:
#                 del celery.conf.beat_schedule[task_name]
#         else:
#             celery.conf.beat_schedule[task_name] = {
#                 'task': 'tasks.my_scheduled_task',
#                 'schedule': crontab(hour=zone.scheduled_time.strftime("%H"), minute=zone.scheduled_time.strftime("%M")),
#                 'args': (zone.number, zone.alias, zone.interval_days, zone.duration_minutes)
#                 }
#     
#     
#     os.system('sudo systemctl restart celerybeat')


@celery.task
def run_water(zone, alias, minutes):
    start_time = datetime.now()
    b = Board() # init a new board since tasks dont seem to have GPIO setup...
    b.register_flow()
    
    temperature = b.get_temp()
    db.session.add(Temperature(temperature))
    db.session.commit()
    
#     moisture0 = board.read_analog_sensor(analog0)
#     moisture1 = board.read_analog_sensor(analog1)
#     moisture2 = board.read_analog_sensor(analog2)
#     moisture3 = board.read_analog_sensor(analog3)
#     sql_helper.insert_moistures(moisture0, moisture1, moisture2, moisture3)
    
    b.set_high(pins[zone])
    time.sleep(minutes*60) # sleep for our duration with the solenoid open 
    b.set_low(pins[zone])
    
    water_used = b.read_water_flow()
    db.session.add(Water(zone, alias, start_time, water_used))
    db.session.commit()
    
    b.deregister_flow()