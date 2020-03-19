import requests
import json

ret =  requests.get("https://w3qa5ydb4l.execute-api.eu-west-1.amazonaws.com/prod/finnishCoronaData")
with open("fin_corona_stats.json", "w") as f:
	json.dump(ret.json(), f, indent=4)
