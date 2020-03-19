import json
import os
import fnmatch
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as pl
import statistics

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

if __name__ == "__main__":
	all_days = list()
	for file in os.listdir('daily-stats/'):
		if fnmatch.fnmatch(file, '*.json'):
			all_days.append(load_daydata(f"daily-stats/{file}"))
	
	all_data = pd.concat(all_days).groupby(['date']).sum()
	# Prediction data filler
	i = len(all_data['confirmed']) - 7
	rats_conf = list()
	rats_rec = list()
	rats_dead = list()
	while i < len(all_data['confirmed']):
		rats_conf.append(all_data['confirmed'][i]/all_data['confirmed'][i - 1])
		rats_rec.append(all_data['recovered'][i]/all_data['recovered'][i - 1])
		rats_dead.append(all_data['deaths'][i - 1]/all_data['confirmed'][i - 1])
		i += 1
	med_conf = statistics.median(rats_conf)
	med_rec = statistics.median(rats_rec)
	med_dead = statistics.median(rats_dead) + 1
	print(f"Confirmed {med_conf} | Recovered {med_rec} | Deaths {med_dead}")
	start_date = all_data.index[-1]
	end_date = dt.datetime.strptime("04/30/2020", "%m/%d/%Y")
	current = dict()
	tmp_date = start_date
	predict = list()
	tmp_conf = all_data['confirmed'][-1]
	tmp_rec = all_data['recovered'][-1]
	tmp_dead = all_data['deaths'][-1]
	while tmp_date < end_date:
		tmp_date += dt.timedelta(days=1)
		current = dict()
		current['date'] = tmp_date
		current['confirmed'] = tmp_conf * med_conf
		current['deaths'] = tmp_dead * med_dead
		current['recovered'] = tmp_rec * med_rec
		predict.append(current)
		tmp_conf = current['confirmed']
		tmp_dead = current['deaths']
		tmp_rec = current['recovered']
	fut = pd.DataFrame(predict)
	fut = fut.set_index('date')
	all_data = pd.concat([all_data, fut])
	# Plottings
	fig, ax = pl.subplots()
	ax.step(all_data.index, all_data['confirmed'], where='mid', label='Confirmed')
	ax.plot(all_data.index, all_data['confirmed'], color='grey', alpha=0.3)
	ax.step(all_data.index, all_data['deaths'], where='mid', label='Deaths', color='red')
	ax.plot(all_data.index, all_data['deaths'], color='grey', alpha=0.3)
	ax.step(all_data.index, all_data['recovered'], where='mid', label='Recovered')
	ax.plot(all_data.index, all_data['recovered'], color='grey', alpha=0.3)
	fig.legend(bbox_to_anchor=(-0.15, 0.25, 0.5, 0.5))
	fig.suptitle('Confirmed cases World')
	pl.show()