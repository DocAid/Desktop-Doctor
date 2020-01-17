import requests
import json
params = {"name":"raghav","age":"12"}
r = requests.get('https://localhost:5000',params=params)
print(r.json())