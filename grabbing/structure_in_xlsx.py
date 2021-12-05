import os
import json
from openpyxl import load_workbook

wb = load_workbook(r'123.xlsx')
for i in wb:
    sheet = wb[str(i)[12:-2]]

city = {}

with open('city_tr/cityapi.txt', 'r', encoding = 'utf-8') as file:
    for i in json.loads(file.read())['response']:
        if i['cityCode'] not in city:
            city[i['cityCode']] = [i['cityName']]
        else:
            city[i['cityCode']].append(i['cityName'])

codes = os.listdir('city_tr')

cur = 2

for i in codes:
    if i not in ['cityapi.txt', 'error.txt']:
        with open('city_tr/'+i, 'r', encoding = 'utf-8') as file:
            js = json.loads(file.read())

        names = city[i.replace('.txt', '')]
        towns = []
        try:
            for i in js['response']:
                towns.append(i['streetName'])
        except:
            towns = ['error']

        for i in range(len(names)):
            sheet['A'+ str(cur + i)].value = names[i]

        for i in range(len(towns)):
            sheet['B'+ str(cur + i)].value = towns[i]

        cur += max(len(towns), len(names)) + 1

wb.save('123.xlsx')