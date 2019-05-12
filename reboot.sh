#!/bin/bash

sleep 10
[ -f /home/pi/SensorArray_Without_Sigfox/sensor.py ] && {
    /usr/bin/sudo git -C /home/pi/SensorArray_Without_Sigfox remote update
    /usr/bin/sudo git -C /home/pi/SensorArray_Without_Sigfox fetch origin
    /usr/bin/sudo git -C /home/pi/SensorArray_Without_Sigfox reset --hard origin/master
    #/usr/bin/sudo nohup python -u /home/pi/SensorArray_Without_Sigfox/sensor.py &
} || {
    /usr/bin/sudo git clone https://github.com/zihengh1/SensorArray_Without_Sigfox/ /home/pi/SensorArray_Without_Sigfox
    #/usr/bin/sudo nohup python -u /home/pi/SensorArray_Without_Sigfox/sensor.py &
}

sleep 10
#set timezone to UTC
sudo timedatectl set-timezone UTC
