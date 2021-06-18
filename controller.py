from irrigation import pin_controller, sql_helper
from irrigation.pin_controller import s1 as zone1, s2 as zone2, s3 as zone3, s4 as zone4, s5 as zone5, s6 as zone6
from irrigation.pin_controller import a0 as analog0, a1 as analog1, a2 as analog2, a3 as analog3
from datetime import datetime
import time
import schedule


def run_water(zone, minutes):
    start_time = datetime.now()
    
    temperature = pin_controller.get_temp()
    sql_helper.insert_temperature(temperature)
    print(f"Temperature: {temperature} F")
    
    moisture0 = pin_controller.read_analog_sensor(analog0)
    moisture1 = pin_controller.read_analog_sensor(analog1)
    moisture2 = pin_controller.read_analog_sensor(analog2)
    moisture3 = pin_controller.read_analog_sensor(analog3)
    sql_helper.insert_moistures(moisture0 ,moisture1, moisture2, moisture3)
    print(f"Moisture0: {moisture0}")
    print(f"Moisture1: {moisture1}")
    print(f"Moisture2: {moisture2}")
    print(f"Moisture3: {moisture3}")
    
    pin_controller.set_high(zone)
    time.sleep(minutes*60) # sleep for our duration with the solenoid open 
    pin_controller.set_low(zone)
    
    water_used = pin_controller.read_water_flow()    
    sql_helper.insert_water(start_time, water_used)
    
    print(f"Water (Gallons): {water_used}")


if __name__ == "__main__":
    pin_controller.setup_pins()
    
    schedule.every(1).day.at("22:00").do(run_water, zone1, 60)
    schedule.every(1).day.at("00:00").do(run_water, zone2, 60)
    schedule.every(1).day.at("02:00").do(run_water, zone3, 60)
    #schedule.every(1).day.at("04:00").do(run_water, zone4, 60)
    #schedule.every(1).day.at("06:00").do(run_water, zone5, 60)
    #schedule.every(1).day.at("20:00").do(run_water, zone6, 60)
    
    # Testing
    # schedule.run_all()
    # exit()
    
    # Loop so that the scheduling task
    # keeps on running all time.
    while True:
        # Checks whether a scheduled task 
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)
