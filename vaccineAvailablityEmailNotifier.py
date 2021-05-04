# importing the library
import requests
import datetime
import json
import time
import yagmail



# Set the district Id (97 for Patna, 638 for Basti, 670 for Lucknow)
DISTRICT_ID_I_CARE = {"97": "Patna", "670": "Lucknow"}

yag = yagmail.SMTP(user='your email id@gmail.com', password='your password')

receiver = ["add comma seperated list of email"]
body = "Covid vaccine is available"
subject = "{} Vaccine available in {} distric at {} location on {} for age {}"
html = '<a href="https://www.cowin.gov.in/home">Click me!</a>'


# Age so that its between 18 and 45
age = 20

# for infinite loop
starttime = time.time()

# Print details flag
print_flag = 'Y'

# Number of days in future
daysInfuture = 20

# Generating range of dates to plug in api
base = datetime.datetime.today()
date_list = [base + datetime.timedelta(days=x) for x in range(daysInfuture)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

# Getting loopy with sleepy
while True:
	for DISTRICT_ID, NAME in DISTRICT_ID_I_CARE.items():
		print("\n")
		print("District Name :",  NAME)
		for INP_DATE in date_str:
		    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(DISTRICT_ID, INP_DATE)
		    response = requests.get(URL)
		    if response.ok:
		        resp_json = response.json()
		        # for debugging only
		        # print(json.dumps(resp_json, indent = 1))
		        flag = False
		        if resp_json["sessions"]:
		            print("Available on: {}".format(INP_DATE))
		            if(print_flag=='y' or print_flag=='Y'):
		                for session in resp_json["sessions"]:
		                        if session["min_age_limit"] <= age:
		                            print("\t", session["name"])
		                            print("\t", session["block_name"])
		                            print("\t Price: ", session["fee_type"])
		                            print("\t Available Capacity: ", session["available_capacity"])
		                            if(session["available_capacity"] > 1):
		                            	yag.send(to=receiver, subject=subject.format(session["available_capacity"], NAME ,session["name"], session["date"], session["min_age_limit"]) , contents=[body, html])
		                            if(session["vaccine"] != ''):
		                                print("\t Vaccine: ", session["vaccine"])
		                            print("\n\n")
		                            
		            
		        # Not available :(         
		        else:
		            print("No available slots on {}".format(INP_DATE))
	time.sleep(60.0 - ((time.time() - starttime) % 60.0))
	            
