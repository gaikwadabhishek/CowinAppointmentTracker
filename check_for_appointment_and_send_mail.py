import requests
import json
from playsound import playsound
import time
from variables import *
import datetime
import smtplib, ssl
import datetime
 
currentDT = datetime.datetime.now()

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "sender_email@gmail.com"  # Enter your address
receiver_email = "receiver_email@gmail.com"  # Enter receiver address
password = "password_goes_here"
context = ssl.create_default_context()



URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(CITY, DATE)
if(isinstance(PINCODES, int)):
    pins = []
    pins.append(PINCODES)
else:
    pins = PINCODES
while(1):
    map = {}
    response = requests.get(URL)
    if (response.ok) and ('centers' in json.loads(response.text)):
        resp_json = json.loads(response.text)['centers']
    
    for i in resp_json:
        if(i['pincode'] in pins):
            for j in i['sessions']:
                if (j['min_age_limit'] == AGE_LIMIT and j['available_capacity']>0):
                    list = []
                    #list.append(i['name'])
                    list.append(i['pincode'])
                    list.append(j['date'])
                    list.append(j['available_capacity'])
                    map[i['name']] = list
    if map:
        print(datetime.datetime.now(), "APPOINTMENT AVAILABLE")
        print(map)

        print("Message Sent - ",map)
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, map)


        playsound('alarm.wav')
        print(datetime.datetime.now(), "SLEEPING FOR HALF HOUR")
        time.sleep(1800)
    else:
        print(datetime.datetime.now(), "appointment not available")
    time.sleep(30)


