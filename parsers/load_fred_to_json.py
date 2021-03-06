import json
from urllib.request import urlopen
# import requests
from time import *
from random import randint

from django.template import base

base_url_1 = "https://api.stlouisfed.org/fred/series/observations?series_id=DDOE01KZA086NWDB&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_2 = "https://api.stlouisfed.org/fred/series/observations?series_id=CPIFABSL&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_3 = "https://api.stlouisfed.org/fred/series/observations?series_id=PCAGDPKZA646NWDB&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_4 = "https://api.stlouisfed.org/fred/series/observations?series_id=MKTGDPKZA646NWDB&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_5 = "https://api.stlouisfed.org/fred/series/observations?series_id=KAZNGDPDUSD&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_6 = "https://api.stlouisfed.org/fred/series/observations?series_id=KAZNGDPRPCHPT&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_7 = "https://api.stlouisfed.org/fred/series/observations?series_id=USACPIALLMINMEI&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_8 = "https://api.stlouisfed.org/fred/series/observations?series_id=FPCPITOTLZGUSA&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_9 = "https://api.stlouisfed.org/fred/series/observations?series_id=FPCPITOTLZGKAZ&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"
base_url_10 = "https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key=7d1fa8e45a6f8b1fa966454d53fb91dd&file_type=json"

urls_list = [base_url_1, base_url_2, base_url_3, base_url_4, base_url_5, 
    base_url_6, base_url_7, base_url_8, base_url_9, base_url_10]

indicator_name_1 = "CPI|Kazakhstan"
indicator_name_2 = "CPI FABSL|United States"
indicator_name_3 = "GDP per capita|Kazakhstan"
indicator_name_4 = "GDP|Kazakhstan"
indicator_name_5 = "GDP in current prices|Kazakhstan"
indicator_name_6 = "GDP in constant prices|Kazakhstan"
indicator_name_7 = "CPI for all items|United States"
indicator_name_8 = "Inflation Consumer Prices|United States"
indicator_name_9 = "Inflation Consumer Prices|Kazakhstan"
indicator_name_10 = "GDP|United States"



indicator_names_list = [indicator_name_1, indicator_name_2, indicator_name_3, indicator_name_4, indicator_name_5, 
    indicator_name_6, indicator_name_7, indicator_name_8, indicator_name_9, indicator_name_10]

############## CODE TO LOAD JSON FROM FRED #################
for i in range(len(urls_list)):
    indicator_name = indicator_names_list[i]
    print("Indicator: ", indicator_name)

    # Set up a random timer to wait before parsing a new page
    x = randint(2,5)
    print(x)
    sleep(x)
    print(f'I waited {x} seconds')

    with urlopen(urls_list[i]) as response:
        source = response.read()
    

    data = json.loads(source)
    # print(json.dumps(data, indent = 2, ensure_ascii=False)) # ascii is False in order to print Russian chars
    

    ## Use the code below to save json into a file
    file_name = indicator_name + ".json"
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file)
    

###############################################################