#!/usr/bin/python3
import time
import datetime
import requests
import json


def unify_countries(data):
	for entry in data:
		if entry["countryRegion"] == "Bahamas, The" or entry["countryRegion"] == "The Bahamas":
			entry["countryRegion"] == "Bahamas"
		elif entry["countryRegion"] == "Czech Republic":
			entry["countryRegion"] == "Czechia"
		elif entry["countryRegion"] == "Iran (Islamic Republic of)":
			entry["countryRegion"] == "Iran"
		elif entry["countryRegion"] == "Korea, South" or entry["countryRegion"] == "Republic of Korea":
			entry["countryRegion"] == "South Korea"
		elif entry["countryRegion"] == "Others":
			entry["countryRegion"] == "Diamond Princess"
		elif entry["countryRegion"] == "Viet Nam":
			entry["countryRegion"] == "Vietnam"
		elif entry["countryRegion"] == "occupied Palestinian territory":
			entry["countryRegion"] == "Palestine"
		elif entry["countryRegion"] == "Republic of Moldova":
			entry["countryRegion"] == "Moldova"
		elif entry["countryRegion"] == "Russia":
			entry["countryRegion"] == "Russian Federation"
		elif entry["countryRegion"] == "Taiwan*":
			entry["countryRegion"] == "Taiwan"
		elif entry["countryRegion"] == "The Gambia" or entry["countryRegion"] == "Gambia, The":
			entry["countryRegion"] == "Gambia"
		elif entry["countryRegion"] == "United Kingdom":
			entry["countryRegion"] == "UK"
		if "\ufeffprovinceState" in entry.keys():
			entry['provinceState'] = entry['\ufeffprovinceState']
			del entry['\ufeffprovinceState']
	return data

# Start date
start_datestr = "03/13/2020"
start_date = datetime.datetime.strptime(start_datestr, "%m/%d/%Y")
# End date
end_datestr = "03/14/2020"
end_date =datetime.datetime.strptime(end_datestr, "%m/%d/%Y")
# end_date = datetime.datetime.fromtimestamp(time.time())
# Base url
url = "https://covid19.mathdro.id/api/daily/"

# Data fetching loop to end -1 day, since today's data have different endpoint (laste request == error)
print(f"Fetching data for all days between {start_date} and {end_date}")
current = start_date
while current < end_date:
	date_str = f"{current.month}-{current.day}-{current.year}"
	print(date_str, end="\t")
	ret = requests.get(f"{url}{date_str}")
	if ret.status_code == 200:
		daydata = dict()
		daydata['timestamp'] = current.timestamp()
		daydata['data'] = unify_countries(ret.json())
		with open(f"{current.year}{current.month:02d}{current.day:02d}.json", 'w') as f:
			json.dump(daydata, f, indent=4)
		print("Success")
	else:
		print("Error")
	current += datetime.timedelta(days=1)

# Adding today's data manully
# date_str = f"{end_date.month}-{end_date.day}-{end_date.year}"
# print(f"Fetching latest data {date_str}")
# ret = requests.get(f"{url}")
# if ret.status_code == 200:
# 	with open(f"daily_round_{end_date.year}{end_date.month:02d}{end_date.day:02d}.json", 'w') as f:
# 		json.dump(ret.json(), f, indent=4)
# 	print("Success")
# else:
# 	print("Error")


	