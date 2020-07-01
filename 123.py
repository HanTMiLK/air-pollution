import os
import sys
import json
import requests
r = requests.get(
    "https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=9be7b239-557b-4c10-9775-78cadfc555e9&format=json")
data = r.json()
datajs = data['records']
aqijs=json.dumps(datajs, ensure_ascii=False, sort_keys=True,indent=4)
with open('yooy.js','w', encoding='utf8') as f:
    f.write(aqijs)

#r=os.popen(os.path.join(r'python C:/Users/qzecw/Desktop/python_web','test.py'))
#print(r.read()) 