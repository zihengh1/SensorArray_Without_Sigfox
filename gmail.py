# Python code to illustrate Sending mail with attachments 
# from your Gmail account 

# libraries to be imported 
import os
import time
from datetime import datetime
from datetime import timedelta

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def getMAC(interface='wlan0'):
    try:
        str = open('/sys/class/net/%s/address' %interface).read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]

macString = getMAC('wlan0')
device_id = macString[9:11]+macString[12:14]+macString[15:17]
device_id = device_id.upper()

now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S").split(" ")

# email start
fromaddr = "iisnrlpim25@gmail.com"
toaddr = "kexwoo@gmail.com"

# instance of MIMEMultipart 
msg = MIMEMultipart() 

# storing the senders email address 
msg['From'] = fromaddr 

# storing the receivers email address 
msg['To'] = toaddr 

# storing the subject 
msg['Subject'] = "ITRI Sensor log"

# string to store the body of the mail 
body = device_id + " , " +  str(now_time[0])

# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 

# open the file to be sent 
filename = device_id + "_" + str(now_time[0]) + ".csv"
attachment = open("/home/pi/Data/" + str(now_time[0]) + ".csv", "rb") 

# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 

# To change the payload into encoded form 
p.set_payload((attachment).read()) 

# encode into base64 
encoders.encode_base64(p) 

p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

# attach the instance 'p' to instance 'msg' 
msg.attach(p) 

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 

# start TLS for security 
s.starttls() 

# Authentication 
s.login(fromaddr, "PiM25PiM25") 

# Converts the Multipart msg into a string 
text = msg.as_string() 

# sending the mail 
s.sendmail(fromaddr, toaddr, text) 

# terminating the session 
s.quit() 


# create next day log file
now_time = (datetime.now()+timedelta(days = 1)).strftime("%Y-%m-%d %H:%M:%S").split(" ")
path = "/home/pi/Data/"

with open(path + str(now_time[0]) + ".csv", "a") as f:
        try: 
            f.write( "s0,s1,s2,s3,s4,datetime,device_id\r\n")
        except:
            print "Error: writing to SD"
