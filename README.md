# Personal COVID-19 data processing
## To-Do
### Countries.py
- fix missing data for a country per day
- transcribe dates to day since number X confirmed to move the curve closer together
### General
data fixing script
	- Korea, South
	- Mailand China

### Deaths based model
Transcribe data to:
```
{
	'country': 'name'
	'deaths': [
		int,
		int,
		int,
		...
	]
}
```
- transcribe data
	- Pandas & Numpy?
	- design structure
	- transcribe daily data into summary.json?
		- keep the data in some other data format?
	
- Count daily change ratio
- create median prediction ration
- plot a graph

- what regions
	- how to collect data for EU only

## Design
				Country
		Confirmed | Recovered | Dead
DATE
## Resources
[Mathdroid API](https://github.com/mathdroid/covid-19-api)

## Requirements
```
python3
numpy
pandas
matplotlib
requests
```