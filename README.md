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

3) Clone this repo and cd into it

4) Setup MariaDB
```
sudo apt install mariadb-server

sudo mysql_secure_installation

sudo mysql -u root -p

> CREATE DATABASE irrigation;
> CREATE USER 'irrigation'@localhost IDENTIFIED BY 'some-password';
> GRANT ALL PRIVILEGES ON irrigation.* TO 'irrigation'@localhost;
> FLUSH PRIVILEGES;
> exit;

cat << EOF > .db_user
username: irrigation
password: some-password
EOF
```

5) Setup service
/etc/systemd/system/water.service
```
[Unit]
Description=Measure Water
After=multi-user.target
 
[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/wksp/irrigation_controller/measure_water.py
Restart=on-abort
 
[Install]
WantedBy=multi-user.target
```
```
sudo chmod 644 /etc/systemd/system/water.service
chmod +x /home/pi/wksp/irrigation_controller/measure_water.py
sudo systemctl daemon-reload
sudo systemctl enable water
sudo systemctl start water
```
