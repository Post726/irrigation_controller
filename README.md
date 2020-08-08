# irrigation_controller
Based on the irrigation controller hat from BC Robotics
[tutorial](https://bc-robotics.com/tutorials/raspberry-pi-irrigation-control-part-1-2/)

Setting up the OS

1) Enable the I2C and 1-Wire interfaces

2) Run the following commands in a terminal
```
sudo apt-get update

sudo apt-get install python3-w1thermsensor

sudo apt-get install gnome-schedule

sudo pip3 install --upgrade setuptools

pip3 install RPI.GPIO

pip3 install adafruit-blinka

sudo pip3 install adafruit-circuitpython-ads1x15

sudo modprobe w1-gpio

sudo modprobe w1-therm

ls /sys/bus/w1/devices
# Take note of the DS18B20 sensor's address e.g. 28-0316853d8fff
```

3) Clone this repo
