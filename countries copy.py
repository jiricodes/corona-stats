import json
import os
import fnmatch
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as pl
import statistics
from srcs.load_dailydata import load_daydata

def dataframe_tojson(country, data):
	data.to_json(f'{country}.json')
	with open(f'{country}.json', 'r') as f:
		stuff = json.load(f)
	with open(f'{country}.json', 'w') as f:
		json.dump(stuff, f, indent=4)

if __name__ == "__main__":
	all_days = list()
	for file in os.listdir('daily-stats/'):
		if fnmatch.fnmatch(file, '*.json'):
			all_days.append(load_daydata(f"daily-stats/{file}"))
	
	all_data = pd.concat(all_days).groupby(['countryRegion', 'date']).sum()
	countries_list = sorted(set(list(zip(*all_data.index))[0]))
	
	# countries_interest = ['Finland', 'Italy', 'Iran', 'US', 'Japan', 'South Korea']
	# countries_interest = ['Finland', 'France', 'UK', 'Germany', 'Belgium']
	countries_interest = ['South Korea']
	# data_sets = list()
	for country in countries_interest:
		new = all_data.loc[country]
		l = len(new.index)
		i = range(l)
		new['index'] = i
		new = new.set_index(['index'])
		print(new)
	# 	ratios = list()
	# 	ratios.append(1)
	# 	k = 1
	# 	while k < len(new.index):
	# 		r = new['confirmed'][k]/new['confirmed'][k - 1]
	# 		ratios.append(r)
	# 		k += 1
		# Prediction data filler
		# i = len(new['confirmed']) - 7
		# rats_conf = list()
		# rats_rec = list()
		# rats_dead = list()
		# while i < len(new['confirmed']):
		# 	rats_conf.append(new['confirmed'][i]/new['confirmed'][i - 1])
		# 	rats_rec.append(new['recovered'][i]/new['recovered'][i - 1])
		# 	rats_dead.append(new['deaths'][i - 1]/new['confirmed'][i - 1])
		# 	i += 1
		# med_conf = statistics.median(rats_conf)
		# med_rec = statistics.median(rats_rec)
		# med_dead = statistics.median(rats_dead) + 1
		# print(f"{country}:\nConfirmed {med_conf} | Recovered {med_rec} | Deaths {med_dead}")
		# start_date = new.index[-1]
		# end_date = dt.datetime.strptime("04/30/2020", "%m/%d/%Y")
		# current = dict()
		# tmp_date = start_date
		# predict = list()
		# tmp_conf = new['confirmed'][-1]
		# tmp_rec = new['recovered'][-1]
		# tmp_dead = new['deaths'][-1]
		# while tmp_date < end_date:
		# 	tmp_date += dt.timedelta(days=1)
		# 	current = dict()
		# 	current['date'] = tmp_date
		# 	current['confirmed'] = tmp_conf * med_conf
		# 	current['deaths'] = tmp_dead * med_dead
		# 	current['recovered'] = tmp_rec * med_rec
		# 	predict.append(current)
		# 	tmp_conf = current['confirmed']
		# 	tmp_dead = current['deaths']
		# 	tmp_rec = current['recovered']
		# fut = pd.DataFrame(predict)
		# fut = fut.set_index('date')
		# new = pd.concat([new, fut])
		# dataframe_tojson(country, new)
		# print(new_rats)
		# new['ratio'] = ratios
		# data_sets.append(new)
	
	# Plottings
	# fig, ax = pl.subplots()
	# i = 0
	# while i < len(countries_interest):
	# 	ax.step(data_sets[i].index, data_sets[i]['confirmed'], where='mid', label=f'{countries_interest[i]} Confirmed')
	# 	ax.plot(data_sets[i].index, data_sets[i]['confirmed'], color='grey', alpha=0.3)
	# 	ax.step(data_sets[i].index, data_sets[i]['recovered'], where='mid', label=f'{countries_interest[i]} Recovered')
	# 	ax.plot(data_sets[i].index, data_sets[i]['recovered'], color='grey', alpha=0.3)
	# 	ax.step(data_sets[i].index, data_sets[i]['deaths'], where='mid', label=f'{countries_interest[i]} Deaths')
	# 	ax.plot(data_sets[i].index, data_sets[i]['deaths'], color='grey', alpha=0.3)
	# 	i += 1
	# fig.legend(bbox_to_anchor=(-0.15, 0.25, 0.5, 0.5))
	# fig.suptitle('Countries of interest timeline')
	# ax.set_xlabel('Dates')
	# pl.show()