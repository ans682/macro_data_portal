import json
from urllib.request import urlopen
# import requests
from time import *
from random import randint

base_url_1 = "https://taldau.stat.gov.kz/ru/Api/GetIndexData/704449?period=7&dics=67"
base_url_2 = "https://taldau.stat.gov.kz/ru/Api/GetIndexData/703088?period=5&dics=67,3030"
base_url_3 = "https://taldau.stat.gov.kz/ru/Api/GetIndexData/703089?period=5&dics=68,481,1336,2493"
base_url_4 = "https://taldau.stat.gov.kz/ru/Api/GetIndexData/703090?period=5&dics=68,524,2819"
base_url_5 = "https://taldau.stat.gov.kz/ru/Api/GetIndexData/703094?period=4&dics=68,2513,2853"


urls_list = [base_url_1, base_url_2, base_url_3, base_url_4, base_url_5]

indicator_name_1 = "индекс реальных денежных доходов"
indicator_name_2 = "Цены производителей на продукцию сельского хозяйства"
indicator_name_3 = "Цены на продукцию лесного хозяйства"
indicator_name_4 = "Цены на продукцию рыболовства и рыбоводства"
indicator_name_5 = "Цены предприятий-производителей на промышленную продукцию"

indicator_names_list = [indicator_name_1, indicator_name_2,indicator_name_3,indicator_name_4,indicator_name_5]

############## CODE TO LOAD JSON FROM TALDAU #################
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
    for item in data:
        print(item["termNames"])

    print(" -------------------------------------------------------- ")

    ## Use the code below to save json into a file
    file_name = indicator_name + ".json"
    with open(file_name, 'w') as json_file:
        json.dump(data, json_file)
    

###############################################################