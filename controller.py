from irrigation import pin_controller, sql_helper
from irrigation.pin_controller import s1, s2, s4, s5, s6, a0, a1, a2, a3

def run_water(zone, minutes):
    pin_controller.set_high(zone)
    time.sleep(minutes*60) # sleep for our duration with the solenoid open 
    pin_controller.set_low(zone)
    
    return pin_controller.read_water_flow()


if __name__ == "__main__":
    pin_controller.setup_pins()
    
    # Readings
    moisture1 = pin_controller.read_analog_sensor(a1)
    temperature = pin_controller.get_temp()
    
    # water_used = run_water(s1, 1)
    sql_helper.setup(replace=True)
    sql_helper.insert_water('2020-01-01 00:00:00', 5)
    sql_helper.insert_temperature(56)
    print(sql_helper.get_temperatures())
    print(sql_helper.get_water())
    
    print(f"Moisture: {moisture1}")
    print(f"Temperature: {temperature}")
    # print(f"Water (Gallons): {water_used}")