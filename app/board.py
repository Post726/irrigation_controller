import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
import RPi.GPIO as GPIO
from adafruit_ads1x15.analog_in import AnalogIn
from w1thermsensor import W1ThermSensor

# Solenoid pins
s1 = 13
s2 = 16
s3 = 19
s4 = 20
s5 = 26
s6 = 21

pins = {
    1: s1,
    2: s2,
    3: s3,
    4: s4,
    5: s5,
    6: s6,
}

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

water_ticks_to_ml = 2.25 # 2.25 ml/revolution
l_to_gal = 0.264172
    
# TODO move this to non-global?
# Used to count the number of times the flow input is triggered
water_tick = 0
    
    
class Board:
    def __init__(self):
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Analog to Digital Converter
        self.ads = ADS.ADS1015(self.i2c)
        self.ads.gain = 1 # +/- 4.096

        # Thermal Sensor
        self.therm_sens = W1ThermSensor()
        
        self.setup_pins()
        

    def setup_pins(self):
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
        
        
    def cleanup(self):
        GPIO.cleanup()
        
        
    def register_flow(self):
        def flow_trig(channel):
            global water_tick
            water_tick += 1
        
        GPIO.add_event_detect(fs, GPIO.FALLING, callback=flow_trig) # Event to detect flow (1 tick per revolution)
    
    
    def deregister_flow(self):
        GPIO.remove_event_detect(fs)
        
        
    def set_low(self, pin):
        GPIO.output(pin, GPIO.LOW)


    def set_high(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        

    def get_state(self, pin):
        return GPIO.input(pin)


    def shut_off_all_pins(self):
        self.set_low(s1)
        self.set_low(s2)
        self.set_low(s3)
        self.set_low(s4)
        self.set_low(s5)
        self.set_low(s6)
        self.set_low(a0_p)
        self.set_low(a1_p)
        self.set_low(a2_p)
        self.set_low(a3_p)
        

    def read_analog_sensor(self, sensor_pin, delay = 0.5):
        # Power on the sensor
        self.set_high(power_pin[sensor_pin])
        
        # Read the senso after a delay
        time.sleep(delay)
        # Create single-ended input on the channel
        chan = AnalogIn(self.ads, sensor_pin)
        value = chan.value
        
        # Turn power back off to the sensor
        self.set_low(power_pin[sensor_pin])
        
        return value


    # Returns amount of water through flow sensor in gallons
    # If reset is set to False the ticks will continue incrementing
    def read_water_flow(self, reset = True):
        global water_tick
        water_consumed = water_tick * water_ticks_to_ml / 1000 * l_to_gal
        
        if reset:
            water_tick = 0
        
        return water_consumed


    def get_temp(self):
        return c_to_f(self.therm_sens.get_temperature())


def c_to_f(celcius):
    return celcius * 9 / 5 + 32
