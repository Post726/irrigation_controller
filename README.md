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

sudo apt-get install libatlas-base-dev

sudo apt-get install redis-server

sudo pip3 install --upgrade setuptools
```

3) Clone this repo and cd into it
```
pip3 install -r requirements.txt

sudo modprobe w1-gpio

sudo modprobe w1-therm

ls /sys/bus/w1/devices
# Take note of the DS18B20 sensor's address e.g. 28-0316853d8fff
```

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

5) Setup services
```
sudo chmod 644 setup/systemd/system/*
sudo cp setup/systemd/system/* /etc/systemd/system/
sudo cp setup/conf.d/* /etc/conf.d/
sudo systemctl daemon-reload
sudo systemctl enable irrigation
sudo systemctl enable celery
sudo systemctl enable uwsgi
sudo systemctl start irrigation
sudo systemctl start celery
sudo systemctl start uwsgi
```
