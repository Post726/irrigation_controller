from app import board, tasks
import time
import schedule
import sys

from flask import Flask, current_app
from app import app
from app.config import Config
from app.database import SessionLocal, engine

import logging

# logging.basicConfig()
# schedule_logger = logging.getLogger('schedule')
# schedule_logger.setLevel(level=logging.DEBUG)

import app.models as models

def run_water(zone, alias, minutes):
    print(f"watering Zone {zone} ({alias}) for {minutes} minutes")
    sys.stdout.flush() # helps with logging in systemctl
    tasks.run_water(zone, alias, minutes)

if __name__ == "__main__":
    # board.cleanup()    
    board.shut_off_all_pins()
    board.register_flow()
    
    # tasks.run_water(1, "tomatoes", 10)
    
    with SessionLocal() as db:
        #models.Base.metadata.create_all(bind=engine)
        #models.init_zones(db)
        #models.init_schedules(db)
        
        for sched in db.query(models.Schedule).all():
            if not sched.disabled:
                zone = db.query(models.Zone).get(sched.zone)
                print(zone.alias)
                schedule.every(sched.interval_days).days.at(sched.scheduled_time.strftime("%H:%M")).do(run_water, sched.zone, zone.alias, sched.duration_minutes)
    
    sys.stdout.flush() # helps with logging in systemctl
    
    # Testing
    # schedule.run_all()
    # exit()
    
    # Loop so that the scheduling task
    # keeps on running all time.
    while True:
        # Checks whether a scheduled task 
        # is pending to run or not
        try:
            schedule.run_pending()
        
            time.sleep(5)
        finally:
            board.cleanup()
