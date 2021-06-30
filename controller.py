from irrigation import board, sql_helper
from irrigation.board import s1 , s2 , s3, s4, s5, s6
from irrigation.board import a0 as analog0, a1 as analog1, a2 as analog2, a3 as analog3
from datetime import datetime
import time
import schedule
import sys

from flask import Flask, current_app
import app
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

from models import Zone

pins = {
    1: s1,
    2: s2,
    3: s3,
    4: s4,
    5: s5,
    6: s6,
}

def run_water(zone, alias, minutes):
    start_time = datetime.now()
    print()
    
    temperature = board.get_temp()
    sql_helper.insert_temperature(temperature)
    print(f"Temperature: {temperature} F")
    
    moisture0 = board.read_analog_sensor(analog0)
    moisture1 = board.read_analog_sensor(analog1)
    moisture2 = board.read_analog_sensor(analog2)
    moisture3 = board.read_analog_sensor(analog3)
    sql_helper.insert_moistures(moisture0, moisture1, moisture2, moisture3)
    print(f"Moisture0: {moisture0}")
    print(f"Moisture1: {moisture1}")
    print(f"Moisture2: {moisture2}")
    print(f"Moisture3: {moisture3}")
    
    board.set_high(pins[zone])
    time.sleep(minutes*60) # sleep for our duration with the solenoid open 
    board.set_low(pins[zone])
    
    water_used = board.read_water_flow()    
    sql_helper.Water().insert(zone, alias, start_time, water_used)
    
    print(f"Water (Gallons): {water_used}")


if __name__ == "__main__":
    board.setup_pins()
    board.shut_off_all_pins()
    
    with app.app_context():
        for zone in Zone.query.all():
            if not zone.disabled:
                print(zone.alias)
                sys.stdout.flush()
                schedule.every(zone.interval_days).day.at(zone.scheduled_time.strftime("%H:%M")).do(run_water, zone.number, zone.alias, zone.duration_minutes)
    
    # Testing
    # schedule.run_all()
    # exit()
    
    # Loop so that the scheduling task
    # keeps on running all time.
    while True:
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        
        time.sleep(5)
