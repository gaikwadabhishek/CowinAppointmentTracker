import requests
import json
from playsound import playsound
import time
from variables import *
import datetime

# dynamically get tomorrows date
#DATE = int(datetime.datetime.now().strftime("%d")) + 1
URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(CITY, DATE)
print(URL)
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
        print("PRESS CTR + C to close")
        playsound('alarm.wav')
        print(datetime.datetime.now(), "SLEEPING FOR HALF HOUR")
        time.sleep(1800)
    else:
        print(datetime.datetime.now(), "appointment not available")
    time.sleep(CHECK_AFTER_SECONDS)


