import requests
import json
import time

# Basic information
# Total cases
basic_all = "https://corona.lmao.ninja/all"
# Per country basic
basic_country = "https://corona.lmao.ninja/countries"
# Confirmed
confirmed_details = "https://covid19.mathdro.id/api/confirmed"
# Recovered
recovered_details = "https://covid19.mathdro.id/api/recovered"
# Deaths
deaths_details = "https://covid19.mathdro.id/api/deaths"
# Daily summary
# Specific -> "https://covid19.mathdro.id/api/daily/[dateString]","example":"https://covid19.mathdro.id/api/daily/2-14-2020"
daily = "https://covid19.mathdro.id/api/daily/1-22-2020"
# Countries details
countries_details = "https://covid19.mathdro.id/api/countries"
# Specific country
country_details = "https://covid19.mathdro.id/api/countries/Finland/confirmed"


ret = requests.get(daily)

print(ret.text)
with open('sample.json', 'w') as f:
	my_daydata = dict()
	my_daydata['timestamp'] = time.time()
	my_daydata['data'] = ret.json()
	json.dump(my_daydata, f, indent=4)