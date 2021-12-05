import os
import json
from openpyxl import load_workbook


city = {}

with open('city_tr/cityapi.txt', 'r', encoding = 'utf-8') as file:
    for i in json.loads(file.read())['response']:
        if i['cityCode'] not in city:
            city[i['cityCode']] = [i['cityName']]
        else:
            city[i['cityCode']].append(i['cityName'])

codes = os.listdir('city_tr')

for i in codes:
    if i not in ['cityapi.txt', 'error.txt']:
        with open('city_tr/'+i, 'r', encoding = 'utf-8') as file:
            js = json.loads(file.read())

        with open('city_tr_struct/'+i, 'w', encoding = 'utf-8') as file:
            try:
                file.write(' | '.join(city[i.replace('.txt', '')])+ '\n\n')
                for i in js['response']:
                    file.write(i['streetName'] + '\n')
            except:
                file.write('\n')
