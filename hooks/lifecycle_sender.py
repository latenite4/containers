#!/usr/bin/python
# Python script to to send container lifecycle hook messages
#
# usage: ./life_cycle.py destIP destPort
#
# R. Melton
# July 3, 2015
#
import requests
import json,sys


cont_name = sys.argv[1]
listener_address = sys.argv[2]
listener_port = sys.argv[3]
listener_address+":"+listener_port

# you must go to http://www.wunderground.com/ and create a free account and get a free API 
# key. copy your API key here.
api_key = ""
api_url = 'http://'+listener_address

headers = {'Content-type': 'application/json', 'Accept': 'application/json','X-Requested-With': 'XMLHttpRequest','User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'}


r = requests.post(api_url, data = {'name':'contname'})
sys.exit(0)

# query the weather underground server
r = requests.get(api_url,headers=headers)

# grab JSON response struct
json_struct = json.loads(r.text)
#print r.text

# pull out varius parts of the response JSON struct
weather = json_struct["current_observation"]
location = weather["display_location"]
country = location["country"]
city = location["full"]
temperature = weather["temperature_string"]
wind = weather["wind_string"]
weather_conditions = weather["weather"]

print '\n\n'+'HTTP status: '+str(r.status_code)+'\n'

print 'Weather Report:'
print '  City: '+city+"  "+country 
print '  Temp: '+temperature
print '  Wind: '+wind
print '  Cond: '+weather_conditions
print '\n\n'


# get 10 day forcast and print
forecast_api_url = "http://api.wunderground.com/api/"+weather_ug_api_key+"/forecast10day/q/tx/"+weather_zip+".json"

# query the weather underground server
r = requests.get(forecast_api_url,headers=headers)

# grab JSON response struct
json_struct = json.loads(r.text)
forecast = json_struct["forecast"]["simpleforecast"]["forecastday"]
#print forecast

print '10 Day Forecast for City: '+city+"  "+country 
print 'Date\thigh\tlow\tconditions'
for day in forecast:
   #print day
   high_temp = day["high"]["fahrenheit"]
   low_temp = day["low"]["fahrenheit"]
   conds = day["conditions"]
   day_num = day["date"]["day"]
   print day_num, "\t",high_temp,"\t",low_temp, "\t",conds

    








