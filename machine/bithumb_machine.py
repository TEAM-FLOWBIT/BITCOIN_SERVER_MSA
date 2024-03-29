from machine.base_machine import Machine
from pip._vendor import requests
import json
import datetime


class BithumbMachine:

    def get_ticker_details(self, order_currency, payment_currency):

        url = "https://api.bithumb.com/public/ticker/" + order_currency + "_" + payment_currency
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

    def save_data_for_db(self):

        url = "https://api.bithumb.com/public/candlestick/BTC_KRW/24h"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        res = json.loads(response.text)
        res["data"]

    def get_all_data(self, coin_currency):
        url = "https://api.bithumb.com/public/candlestick/" + coin_currency + "_KRW/24h"

        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        res = json.loads(response.text)
        data_list = res["data"]
        processed_data = []

        for entry in data_list:
            tmp = {}
            time_tmp = datetime.datetime.fromtimestamp(entry[0] / 1000)
            year = time_tmp.year
            month = time_tmp.month
            day = time_tmp.day
            tmp["timestamp"] = f"{year}-{month:02d}-{day:02d}"
            tmp["open_price"] = eval(entry[1])
            tmp["close_price"] = eval(entry[2])
            tmp["high_price"] = eval(entry[3])
            tmp["low_price"] = eval(entry[4])
            tmp["volume"] = eval(entry[5])
            processed_data.append(tmp)

        #print(processed_data[-1])
        # 결과 확인
        return processed_data
    
    def get_local_data(self):
        url = "https://api.bithumb.com/public/candlestick/BTC_KRW/24h"

        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        res = json.loads(response.text)

        return [[eval(sublist[2]) + 0.0] for sublist in res["data"][-15:]]

    def get_last_data(self):
        url = "https://api.bithumb.com/public/candlestick/BTC_KRW/24h"

        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)
        res = json.loads(response.text)
        data_list = res["data"]
        processed_data = []

        for entry in data_list:
            tmp = {}
            time_tmp = datetime.datetime.fromtimestamp(entry[0] / 1000)
            year = time_tmp.year
            month = time_tmp.month
            day = time_tmp.day
            tmp["timestamp"] = f"{year}-{month:02d}-{day:02d}"
            tmp["open_price"] = eval(entry[1])
            tmp["close_price"] = eval(entry[2])
            tmp["high_price"] = eval(entry[3])
            tmp["low_price"] = eval(entry[4])
            tmp["volume"] = eval(entry[5])
            processed_data.append(tmp)

        return processed_data[-1]