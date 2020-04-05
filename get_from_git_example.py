## 
# Example code for importing the data from a GIT repository.
# Modify this to work in your client app!

from xarray import DataArray, Dataset
import json
import numpy as np
import pandas

import base64
import requests

url = 'https://api.github.com/repos/David-Rayner-GVC/pet_data/contents/json/Gothenburg.json'
req = requests.get(url)
if req.status_code == requests.codes.ok:
    req = req.json()  # the response is a JSON
    # req is now a dict with keys: name, encoding, url, size ...
    # and content. But it is encoded with base64.
    content = base64.b64decode(req['content'])
else:
    print('Content was not found.')

dict_loaded = json.loads(content)  

for key, value in dict_loaded['data_vars'].items():
 dict_loaded['data_vars'][key]['data'] = [np.nan if isinstance(x,str) else x for x in value['data'] ]

# re-create xarray Dataset
x_loaded = Dataset.from_dict(dict_loaded)

# Convert time from string to datetime64 if you want. 
x_loaded['time'].values = pandas.to_datetime(x_loaded['time'].values)

#########################################
## Now example from icon_git
# RetrieveForecast has options for conversion to xarray or datetime64

import icon_git
x_loaded = icon_git.RetrieveForecast('Gothenburg')

