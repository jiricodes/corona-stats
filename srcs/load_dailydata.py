import numpy as np
import pandas as pd
import datetime as dt
import json

def load_daydata(filename):
	def transcribe_counts(daily_data):
		for item in daily_data['data']:
			if item['confirmed'] == "":
				item['confirmed'] = 0
			else:
				item['confirmed'] = int(item['confirmed'])
			if item['deaths'] == "":
				item['deaths'] = 0
			else:
				item['deaths'] = int(item['deaths'])
			if item['recovered'] == "":
				item['recovered'] = 0
			else:
				item['recovered'] = int(item['recovered'])
		return daily_data

	with open(filename, 'r') as f:
		daily_data = json.load(f)

	daily_data = transcribe_counts(daily_data)
	ddata = pd.DataFrame(daily_data['data'])
	tmp = ddata.drop(['provinceState', 'lastUpdate'], axis=1)
	countries_daily = tmp.groupby('countryRegion').sum()
	date_stamp = dt.datetime.fromtimestamp(daily_data['timestamp'])
	countries_daily['date'] = date_stamp
	return countries_daily