import serial
import time
import os
from datetime import datetime
import encode as Enc

def getMAC(interface='wlan0'):
    try:
        str = open('/sys/class/net/%s/address' %interface).read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]

macString = getMAC('wlan0')
device_id = macString[9:11]+macString[12:14]+macString[15:17]
device_id = device_id.upper()
#print(device_id)

#device_id = "CCLLJJ"
sigfox_id = -1
path = "/home/pi/Data/"
Restful_URL = "https://data.lass-net.org/Upload/SigFox.php"

while True:
    data = ""
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(" ")
    for i in range(0, 5):
        if i is not sigfox_id:
            try:
                if(os.path.exists('/dev/ttyUSB' + str(i))):
                    print("dev/ttyUSB " + str(i) + "exists")
                    ser = serial.Serial(
                        port = '/dev/ttyUSB'+str(i),
                        baudrate = 9600,
                        parity = serial.PARITY_NONE,
                        stopbits = serial.STOPBITS_ONE, 
                        bytesize = serial.EIGHTBITS,
                  	)
                    data += '|s%d:%d' % (i, int(ser.read(32)[7].encode('hex'), 16))
                    ser.flushInput()
                    ser.close()
                    time.sleep(0.2)
                else:
                    print("dev/ttyUSB " + str(i) + "not exists")

            except Exception as e:
                ser.close()
                print "serial.port is closed"
                print(e)
    if len(data):
        data += '|%s_%s' % (str(now_time[0]), str(now_time[1]))
        data_dict = Enc.split_string(data)
        T3_binstr = Enc.dec_to_binstr(data_dict)
        T3_hexstr = Enc.bin_to_hex(T3_binstr)
        print "T3_hexstr : ", T3_hexstr
    
        try: 
            restful_str3 = "wget -O /tmp/last_upload.log \"" + Restful_URL + "?device_id=" + device_id + "&data=" + T3_hexstr + "\""
            os.system(restful_str3)
        except Exception as e:
            print(e)

        data += '|' + device_id
 	
        with open(path + str(now_time[0]) + ".txt", "a") as f:
            try: 
                f.write(data + "\n")
            except:
                print "Error: writing to SD"	
    
    time.sleep(282)
