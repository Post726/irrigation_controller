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

from app.models import Zone

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
        for zone in db.query(Zone).all():
            if not zone.disabled:
                print(zone.alias)
                schedule.every(zone.interval_days).days.at(zone.scheduled_time.strftime("%H:%M")).do(run_water, zone.number, zone.alias, zone.duration_minutes)
    
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
