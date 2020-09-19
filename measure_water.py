import logging
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

# Flow Sensor Pin
fs = 24

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


# Returns amount of water through flow sensor in gallons
# If reset is set to False the ticks will continue incrementing
def read_water_flow(reset = True):
    global water_tick
    water_consumed = water_tick * water_ticks_to_ml / 1000 * l_to_gal
    
    if reset:
        water_tick = 0
    
    return water_consumed


def c_to_f(celcius):
    return celcius * 9 / 5 + 32


def do_logging(therm_sens):
    temperature = c_to_f(therm_sens.get_temperature())
    water_used = read_water_flow(False)
    
    logging.info(f'{water_used}, {temperature}')

if __name__ == "__main__":
    logging.basicConfig(filename='/home/pi/water.log', format='%(asctime)s, %(message)s', level=logging.DEBUG)
    
    setup_pins()
    
    # Create the I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    
    # Thermal Sensor
    therm_sens = W1ThermSensor()
    
    do_logging(therm_sens)
    
    GPIO.output(s1, GPIO.HIGH)
    
    while(True):
        time.sleep(60) # 1 Minute
        
        do_logging(therm_sens)
        