# -*- coding: utf-8 -*-

import requests
from pprint import pprint
import mysql_terminals
import pandas as pd
import datetime
import time

day = 10

def unix_time(a, b, c, d, e):
  t_time = datetime.datetime(a, b, c, d, e)
  return int(time.mktime(t_time.timetuple()))

def times():
  time_begin = unix_time(2022, 4, day, 2, 0) * 1000  # время начала
  time_unix = [time_begin, time_begin + 86400000]  # сутки
  return time_unix


atz = {"137" : 7761, "276" : 7728, "302" : 8063, "786" : 8064, "212" : 8044, "728" : 8044, "305" : 8046, 'all' : 0}

#-------------------------------------GEOTEK-----------------------------------------------------

myurl_geo = "https://s4.geotek.online/api"

def post_head():
  headers = {
    'Content-type': 'application/json',
    'Accept': 'application/json'
  }

  params = {
  "userName": "nova",
  "password": "nova2021"}

  response = requests.post("https://s4.geotek.online/api/Token", json=params, headers=headers).json()
  jwt = response["accessToken"]
  head = {'Authorization': f'Bearer {jwt}'}
  return head


def post_atz(x): #7728 #TODO изменить метод на суммирование заправок
  params = {
  "from": times()[0],
  "till": times()[1],
  "objectID": x
}
  method = "/ObjectsHistory/Transactions"
  response = requests.post(url=myurl_geo + method, headers=post_head(), json=params).json()
  itog = {}
  for i in response:
      if itog.get(i['keyName'], 0) != 0:
          itog[i['keyName']] += i['value']
      else:
          itog[i['keyName']] = i['value']
  return itog


#----------------------------------------OMNICOMM-------------------------------------------------------------


myurl = 'https://online.omnicomm.ru'

def times_omni():
    time_begin = unix_time(2022, 4, day, 2, 0)  # время начала
    time_unix = [time_begin, time_begin + 86400]  # сутки
    return time_unix


def post_head_omni():
  params = {
    "login": "nova_monitoring",
    "password": "hHat4YFN"
  }
  response = requests.post("https://online.omnicomm.ru/auth/login?jwt=1", data=params).json()
  jwt = response["jwt"]
  head = {'Authorization' : f'JWT {jwt}'}
  return head

#прибавлять по 86400 на каждые сутки
def iter_zapros():
    new_data = {}
    x = 0
    y = x + 382
    time_1 = times_omni()[0]
    time_2 = times_omni()[1]
    for i in range(4):
        spisok = '%2C'.join(mysql_terminals.bd[x:y])
        zapravki = f"/ls/api/v1/reports/statistics?timeBegin={time_1}&timeEnd={time_2}&dataGroups=%5Bfuel%5D&vehicles=%5B{spisok}%5D&"
        data = requests.get(url=myurl + zapravki, headers=post_head_omni()).json()
        data = data['data']["vehicleDataList"]
        x += 382
        y += 382
        for i in data:
            new_data[i['name']] = i['fuel']['refuelling']/10
    return new_data


def proverka(): #TODO разделить проверку на циклы на основе бинарного поиска по 4 запроса
    new_data = {}
    ban_id = []
    for auto in mysql_terminals.bd[:100]:
        try:
            zapravki = f"/ls/api/v1/reports/statistics?timeBegin={times_omni()[0]}&timeEnd={times_omni()[1]}&dataGroups=%5Bfuel%5D&vehicles=%5B{auto}%5D&"
            data = requests.get(url=myurl + zapravki, headers=post_head_omni()).json()
            data = data['data']["vehicleDataList"]
            for i in data:
                new_data[i['name']] = i['fuel']['refuelling']
        except:
            ban_id.append(auto)
    return ban_id


def proverka_new():
    ban_id = []
    x = 0
    y = x + 382
    time_1 = times_omni()[0]
    time_2 = times_omni()[1]
    for i in range(4):
        spisok = '%2C'.join(mysql_terminals.bd[x:y])
        zapravki = f"/ls/api/v1/reports/statistics?timeBegin={time_1}&timeEnd={time_2}&dataGroups=%5Bfuel%5D&vehicles=%5B{spisok}%5D&"
        data = requests.get(url=myurl + zapravki, headers=post_head_omni()).json()
        # data = data['data']["vehicleDataList"]
        if data['code'] == 1:
            for auto in mysql_terminals.bd[x:y]: # TODO переделать под бинарный поиск
                zapravki = f"/ls/api/v1/reports/statistics?timeBegin={times_omni()[0]}&timeEnd={times_omni()[1]}&dataGroups=%5Bfuel%5D&vehicles=%5B{auto}%5D&"
                data = requests.get(url=myurl + zapravki, headers=post_head_omni()).json()
                if data['code'] == 1:
                    ban_id.append(auto)

        x += 382
        y += 382
    return ban_id



def data_frame(s1, s2): #TODO переделать алгоритм через словарь
    new = {}
    for i in s1:
        new[i] = [s1[i]]
    for val in s2:
        if val in s1:
            new[val].append(s2[val])

    colNames = [2, 3]
    return pd.DataFrame.from_dict(new, orient='index', columns=colNames)

# pprint(data_frame(post_atz(atz['all']), iter_zapros()).to_excel('bigdata.xlsx'))
# pprint(post_atz(atz['137']))




