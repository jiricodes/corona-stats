import json
import os
import fnmatch
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as pl
import statistics
from srcs.load_dailydata import load_daydata
import seaborn as sns
import cufflinks as cf
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

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

def create_estimate(data, tod, mort_rat, s_death):
	new = [0] * len(data.index)
	start = get_death_change(data, s_death)
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
	i = start - 20
	k = 1
	while i - k >= 0:
		value = int(new[i] - (k * new[i] / 2 / tod))
		if value < 0:
			break
		else:
			new[i - k] = value
		if k == tod:
			i = i - k
			k = 1
		else:
			k += 1
	return new

def get_median_estimate(data):
	est = list()
	i = 0
	while i < len(data[0]):
		tmp = list()
		for line in data:
			tmp.append(line[i])
		m = statistics.median_grouped(tmp)
		est.append(m)
		i += 1
	return est 
if __name__ == "__main__":
	cf.go_offline()
	all_days = list()
	for file in os.listdir('daily-stats/'):
		if fnmatch.fnmatch(file, '*.json'):
			all_days.append(load_daydata(f"daily-stats/{file}"))
	
	all_data = pd.concat(all_days).groupby(['countryRegion', 'date']).sum()
	ch = all_data.loc['China']
	ch.iplot()
	# all_data = pd.concat(all_days).groupby(['countryRegion']).sum()
	# print(all_data)
	# countries_interest = ['Belgium', 'US', 'Italy', 'Iran']
	# data_sets = list()
	# for country in countries_interest:
		# new = all_data.loc[country]
		# all_estimates = list()
		# d = 0
		# while d < new['deaths'][-1]:
		# 	est = create_estimate(new, 7, 1, d)
		# 	all_estimates.append(est)
		# 	d = new['deaths'][get_death_change(new, d)]
		# med_est = get_median_estimate(all_estimates)
		# new['estimate'] = med_est
		# data_sets.append(new)
		# print(new)
	# tmat = all_data.pivot_table(index='countryRegion', columns='date', values='deaths').fillna(value=0)
	# print(tmat)
	# sns.heatmap(tmat, cmap='coolwarm')
	# sns.jointplot(x='deaths',y='confirmed',data=all_data,kind='kde')
	# # Plottings
	# rows = int(len(data_sets)/3) + 1
	# fig, ax = pl.subplots(ncols=3, nrows=2)
	# i = 0
	# while i < len(countries_interest):
	# 	ax[int(i/3)][int(i%3)].plot(data_sets[i].index, data_sets[i]['confirmed'], label=f'{countries_interest[i]} Confirmed')
	# 	# ax.plot(data_sets[i].index, data_sets[i]['recovered'], label=f'{countries_interest[i]} Recovered')
	# 	# ax.plot(data_sets[i].index, data_sets[i]['deaths'], label=f'{countries_interest[i]} Deaths')
	# 	# ax[i].plot(data_sets[i].index, data_sets[i][f'estimate'], label=f'{countries_interest[i]} Estimated Infected')
	# 	ax[int(i/3)][int(i%3)].set_title(f'{countries_interest[i]}')
	# 	i += 1
	# pl.tight_layout()
	# # fig.legend(bbox_to_anchor=(-0.15, 0.25, 0.5, 0.5))
	pl.show()