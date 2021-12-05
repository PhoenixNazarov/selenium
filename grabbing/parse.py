import requests
import time
import random
import os

token = 'eyJ0eXAiOiJKV1QiLCJwaWQiOiJRa3hlOGJYeGpnZnFnVW9PQkJtcTNwR0c4ZWJlNkgrQ3hjUXRIUElVTnUwUmt5MlZCTWNoZmc9PSIsImFsZyI6IkhTMjU2In0.eyJEZXBhcnRtZW50Q29kZSI6IjExMzEzIiwicm9sZSI6MSwiU3ViRGVwYXJ0bWVudENvZGUiOiI3NzU5IiwiRmlyc3ROYW1lIjoi16jXldeg15nXqiIsImhvdF93aXpfdXplciI6IjBIWiIsImlzcyI6Im15LmhvdG1vYmlsZS5jby5pbCIsIk51bWJlck9mU3Vic2NyaWJlcnMiOiIxMiIsIlRlYW1OYW1lIjoi16rXmdenINeq16cg157Xm9eZ16jXldeqINeY15zXpNeV16DXmdeV16oiLCJBY2NvdW50Q2F0ZWdvcnkiOiIyIiwiTWFya2V0Q29kZSI6IjciLCJodF93aXpfbWFya2V0X2NvZGUiOiIiLCJVc2VyTXNpc2RuIjoiMDU1OTU0MDMxMyIsIk1vZHVsZXNTY3JlZW4iOiIxMiwxNCwxNSwxNywxOCIsIlRlYW1Db2RlIjoiNTA4NiIsIlVzZXJJRCI6IjIwOTAyOTgwMCIsIkRlcGFydG1lbnROYW1lIjoiUmVzZWxsZXJzL0Rpc3RyaWJ1dG9ycyIsIkxhc3ROYW1lIjoi15LXldec157XnyIsIlJlcXVlc3RvciI6IjIwOTAyOTgwMC0xMjgzZDU0ZC0xMDQ2LTQwNDEtYTljYS0wYzYyY2YxNDM5YjEiLCJleHAiOjE2MzI4OTU1NjQsIlN1YkRlcGFydG1lbnROYW1lIjoi16rXmdenINeq16ciLCJpYXQiOjE2MzI4NTIzNjR9.yT49QGWTVDlUHossFrxHxAzjRSL83UcYnjyNre7gj9c'
def get_cities():
    headers = {
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept': 'application/json, text/plain, */*',
        'SPFActionToken': 'null',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'RetailerToken': token,
        'Content-Type': 'application/json',
        'Origin': 'https://retailsys.hotnet.net.il',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://retailsys.hotnet.net.il/',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # https://api.hotmobile.co.il:200/api/HMAddress/GetCities
    # https://api.hotmobile.co.il:200/api/HMAddress/GetCities


    data = '{"IsMapa":true}'
    response = requests.post('https://api.hotmobile.co.il:200/api/HMAddress/GetCities', headers=headers, data=data)

    return response


def get_streets(city_id):
    headers = {
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept': 'application/json, text/plain, */*',
        'SPFActionToken': 'null',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'RetailerToken': token,
        'Content-Type': 'application/json',
        'Origin': 'https://retailsys.hotnet.net.il',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://retailsys.hotnet.net.il/',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    # https://api.hotmobile.co.il:200/api/HMAddress/GetCities
    # https://api.hotmobile.co.il:200/api/HMAddress/GetCities


    data = '{CityId: "'+city_id+'", IsMapa: true}'
    response = requests.post('https://api.hotmobile.co.il:200/api/HMAddress/GetStreets', headers=headers, data=data)

    return response


cities = get_cities()

with open('city_tr/cityapi.txt', 'w', encoding = 'utf-8') as file:
    file.write(cities.text)

parsing = os.listdir('city_tr')
for i in range(len(parsing)):
    parsing[i] = parsing[i].replace('.txt', '')

cnt = 0
ln = len(cities.json()['response'])


print('success start')
for i in cities.json()['response']:
    cnt += 1
    if i['cityCode'] in parsing:
        continue


    try:
        streets = get_streets(i['cityCode'])
        while streets.json()['errorFound'] != False:
            time.sleep(10)
    except:
        print('error')
        with open('city_tr/error.txt','a', encoding = 'utf-8') as file:
            file.write(str(i)+'\n')
        continue

    print(streets.text)

    with open(f'city_tr/{i["cityCode"]}.txt', 'w', encoding = 'utf-8') as file:
        file.write(streets.text)

    time.sleep(random.randint(3,5))

    print(cnt, '/', ln, i)
    parsing.append(i['cityCode'])



# Cities
# import requests
#
# headers = {
#     'Accept': 'application/json, text/plain, */*',
#     'SPFActionToken': 'null',
#     'sec-ch-ua-mobile': '?0',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
#     'RetailerToken': 'eyJ0eXAiOiJKV1QiLCJwaWQiOiJRa3hlOGJYeGpnZnFnVW9PQkJtcTNwR0c4ZWJlNkgrQ3hjUXRIUElVTnUwUmt5MlZCTWNoZmc9PSIsImFsZyI6IkhTMjU2In0.eyJEZXBhcnRtZW50Q29kZSI6IjExMzEzIiwicm9sZSI6MSwiU3ViRGVwYXJ0bWVudENvZGUiOiI3NzU5IiwiRmlyc3ROYW1lIjoi16fXqNeV15wiLCJpc3MiOiJteS5ob3Rtb2JpbGUuY28uaWwiLCJUZWFtTmFtZSI6Iteq15nXpyDXqtenIFdCIiwiVXNlck1zaXNkbiI6IjA1NTk3OTMxODkiLCJNb2R1bGVzU2NyZWVuIjoiMTIsMTQsMTUiLCJUZWFtQ29kZSI6IjgxMjAiLCJVc2VySUQiOiIzMTY5NzQwNTQiLCJEZXBhcnRtZW50TmFtZSI6IlJlc2VsbGVycy9EaXN0cmlidXRvcnMiLCJMYXN0TmFtZSI6Iteg15nXp9eZ15jXlCIsIlJlcXVlc3RvciI6IjMxNjk3NDA1NC00NDE4ZDZlYy01ZGVhLTQwNzctOGM4Mi0yZGEyMWQyMWU2MDUiLCJleHAiOjE2MjgzNDkzODEsIlN1YkRlcGFydG1lbnROYW1lIjoi16rXmdenINeq16ciLCJpYXQiOjE2MjgzMDYxODF9.sJwHYz81zEBDMXeTnes-hjHO7BG4-iBgyuvTcBYNPw8',
#     'Content-Type': 'application/json',
#     'Origin': 'https://retailsys.hotnet.net.il',
#     'Sec-Fetch-Site': 'cross-site',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Dest': 'empty',
#     'Referer': 'https://retailsys.hotnet.net.il/',
#     'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
# }
#
# data = '^{^\\^IsDrop^\\^:false,^\\^IsMapa^\\^:false,^\\^IsScheduled^\\^:false^}'
#
# response = requests.post('https://api.hotmobile.co.il:200/api/HMAddress/GetCities', data=data)
# print(response.text)