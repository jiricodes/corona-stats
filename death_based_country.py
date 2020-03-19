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

# Incubation time avg 5.1 days, meadian time to die 15 days
# returns calculated value of potentially infected 20 days earlier
# based on given mortality rate (0-100%)
def infected_based_deaths(deaths, ratio):
	return (100/ratio) * deaths


def get_death_change(data, current):
	i = 0
	for day in data['deaths']:
		if day > current:
			return i
		i += 1
	return None

def create_estimate(data, tod, mort_rat):
	new = [0] * len(data.index)
	start = get_death_change(data, 0)
	if not start or start < 20:
		return None
	new[start - 20] = int(infected_based_deaths(data['deaths'][start], mort_rat))
	i = start - 20
	k = 1
	while i + k < len(new):
		new[i + k] = int((k * new[i] / tod) + new[i])
		if k == tod:
			i = i + k
			k = 1
		else:
			k += 1
	return new


if __name__ == "__main__":
	all_days = list()
	for file in os.listdir('daily-stats/'):
		if fnmatch.fnmatch(file, '*.json'):
			all_days.append(load_daydata(f"daily-stats/{file}"))
	
	all_data = pd.concat(all_days).groupby(['countryRegion', 'date']).sum()
	countries_interest = ['Belgium']
	data_sets = list()
	for country in countries_interest:
		new = all_data.loc[country]
		est = create_estimate(new, 7, 1)
		new['estimate'] = est
		data_sets.append(new)
		# print(new)
	
	# Plottings
	fig, ax = pl.subplots()
	i = 0
	while i < len(countries_interest):
		ax.plot(data_sets[i].index, data_sets[i]['confirmed'], label=f'{countries_interest[i]} Confirmed')
		# ax.plot(data_sets[i].index, data_sets[i]['recovered'], label=f'{countries_interest[i]} Recovered')
		# ax.plot(data_sets[i].index, data_sets[i]['deaths'], label=f'{countries_interest[i]} Deaths')
		ax.plot(data_sets[i].index, data_sets[i]['estimate'], label=f'{countries_interest[i]} Estimated Infected')
		i += 1
	fig.legend(bbox_to_anchor=(-0.15, 0.25, 0.5, 0.5))
	fig.suptitle('Countries of interest timeline')
	pl.show()