import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor
from adafruit_ads1x15.analog_in import AnalogIn

# Solenoid pins
s1 = 13
s2 = 16
s3 = 19
s4 = 20
s5 = 26
s6 = 21

# Moisture Sensor Pins
a0 = ADS.P0
a1 = ADS.P1
a2 = ADS.P2
a3 = ADS.P3

# Analog input GPIO power pins for moisture sensors
a0_p = 12
a1_p = 6
a2_p = 5
a3_p = 25

# Flow Sensor Pin
fs = 24

power_pin = {
    a0: a0_p,
    a1: a1_p,
    a2: a2_p,
    a3: a3_p,
}

# TODO move this to non-global?
# Used to count the number of times the flow input is triggered
water_tick = 0

water_ticks_to_ml = 2.25 # 2.25 ml/revolution
l_to_gal = 0.264172


def setup_pins():
    #Set GPIO pins to use BCM pin numbers
    GPIO.setmode(GPIO.BCM)

    # Setup solenoid pins
    GPIO.setup(s1, GPIO.OUT)
    GPIO.setup(s2, GPIO.OUT)
    GPIO.setup(s3, GPIO.OUT)
    GPIO.setup(s4, GPIO.OUT)
    GPIO.setup(s5, GPIO.OUT)
    GPIO.setup(s6, GPIO.OUT)
    
    # Setup analog sensor power pins
    GPIO.setup(a0_p, GPIO.OUT)
    GPIO.setup(a1_p, GPIO.OUT)
    GPIO.setup(a2_p, GPIO.OUT)
    GPIO.setup(a3_p, GPIO.OUT)
    
    # Setup the Flow Sensor pins
    GPIO.setup(fs, GPIO.IN)
    GPIO.add_event_detect(fs, GPIO.FALLING) # Event to detect flow (1 tick per revolution)
    
    def flow_trig(self):
        global water_tick
        water_tick += 1
 
    GPIO.add_event_callback(fs, flow_trig)


def shut_off_all_pins():
    GPIO.output(s1, GPIO.LOW)
    GPIO.output(s2, GPIO.LOW)
    GPIO.output(s3, GPIO.LOW)
    GPIO.output(s4, GPIO.LOW)
    GPIO.output(s5, GPIO.LOW)
    GPIO.output(s6, GPIO.LOW)
    GPIO.output(a0_p, GPIO.LOW)
    GPIO.output(a1_p, GPIO.LOW)
    GPIO.output(a2_p, GPIO.LOW)
    GPIO.output(a3_p, GPIO.LOW)

def read_analog_sensor(ads, sensor_pin, delay = 0.5):
    # Power on the sensor
    GPIO.output(power_pin[sensor_pin], GPIO.HIGH)
    
    # Read the senso after a delay
    time.sleep(delay)
    # Create single-ended input on the channel
    chan = AnalogIn(ads, sensor_pin)
    value = chan.value
    
    # Turn power back off to the sensor
    GPIO.output(power_pin[sensor_pin], GPIO.LOW)
    
    return value


# Returns amount of water through flow sensor in gallons
# If reset is set to False the ticks will continue incrementing
def read_water_flow(reset = True):
    global water_tick
    water_consumed = water_tick * water_ticks_to_ml / 1000 * l_to_gal
    
    if reset:
        water_tick = 0
    
    return water_consumed


def run_water(zone, minutes):
    GPIO.output(zone, GPIO.HIGH)
    time.sleep(minutes*60) # sleep for our duration with the solenoid open 
    GPIO.output(zone, GPIO.LOW)
    
    return read_water_flow()

def c_to_f(celcius):
    return celcius * 9 / 5 + 32


if __name__ == "__main__":
    setup_pins()
    
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    
    # Analog to Digital Converter
    ads = ADS.ADS1015(i2c)
    ads.gain = 1 # +/- 4.096

    # Thermal Sensor
    therm_sens = W1ThermSensor()
    
    # Readings
    moisture1 = read_analog_sensor(ads, a1)
    temperature = c_to_f(therm_sens.get_temperature())
    
    water_used = run_water(s1, 1)
    
    print(f"Moisture: {moisture1}")
    print(f"Temperature: {temperature}")
    print(f"Water (Gallons): {water_used}")