#!/bin/bash

sleep 1
[ -f /home/pi/SensorArray_Without_Sigfox/sensor.py ] && {
    /usr/bin/git -C /home/pi/SensorArray_Without_Sigfox fetch origin
    /usr/bin/git -C /home/pi/SensorArray_Without_Sigfox reset --hard origin/master
    nohup python -u /home/pi/SensorArray_Without_Sigfox/sensor.py &
} || {
    /usr/bin/git clone https://github.com/zihengh1/SensorArray_Without_Sigfox/ /home/pi/SensorArray_Without_Sigfox
    nohup python -u /home/pi/SensorArray_Without_Sigfox/sensor.py &
}

