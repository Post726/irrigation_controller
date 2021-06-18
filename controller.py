from irrigation import pin_controller, sql_helper
from irrigation.pin_controller import s1, s2, s4, s5, s6, a0, a1, a2, a3
from datetime import datetime
import time
import schedule

def run_water(zone, minutes):
    start_time = datetime.now()
    
    temperature = pin_controller.get_temp()
    sql_helper.insert_temperature(temperature)
    print(f"Temperature: {temperature} F")
    
    moisture0 = pin_controller.read_analog_sensor(a0)
    moisture1 = pin_controller.read_analog_sensor(a1)
    moisture2 = pin_controller.read_analog_sensor(a2)
    moisture3 = pin_controller.read_analog_sensor(a3)
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
    sql_helper.setup() # sql_helper.setup(replace=True)
    
    run_water(s1, 1)