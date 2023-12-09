#init code

import sys
import os

sys.path.append(os.path.realpath(__file__)[0:-12] + "..")

#print(os.path.realpath(__file__)[0:-12] + "..")

from machine.bithumb_machine import BithumbMachine
from db.mongodb.mongodb_handler import MongoDBHandler
from AI.lstm_machine import LstmMachine
from db.mysql.mysql_handler import MySqlHandler
from machine.chatGPT_machine import ChatMachine
from machine.chart_machine import ChartMachine

import datetime

def extract_close_prices(data):
    close_prices = [float(entry['close_price']) for entry in data]
    return close_prices

def init_code():
    bithumbMachine = BithumbMachine()
    lstmMachine = LstmMachine()
    mySqlHandler = MySqlHandler(mode="local", db_name="flowbit")
    #mongodbMachine = MongoDBHandler(db_name="AI", collection_name="actual_data")

    #bithubm에서 모든 데이터 가지고 와서 바로 저장
    datas = bithumbMachine.get_all_data()
    #print(type(datas))
    mySqlHandler.insert_items_to_actual_data(datas)
    #mongodbMachine.insert_items(datas=datas,db_name="AI", collection_name="actual_data")

    #저장된 데이터 불러오기
    #data = mongodbMachine.find_items(db_name="AI", collection_name="actual_data")
    #data = list(data)

    #data = mySqlHandler.find_items_

    #학습 형식으로 데이터 생성
    result = []
    for i in range(0, len(datas) - 14):
        chunk = datas[i:i+15]
        result.insert(0, chunk)
    result.reverse()

    #가격 예측 후 순서대로 저장
    for i in result:
        data = extract_close_prices(i)
        data = lstmMachine.data_processing(data)
        result = lstmMachine.get_predict_value(data)
        one_day_data = {}
        date_string = i[-1]["timestamp"]  # 예시로 사용할 날짜 문자열
        date_format = "%Y-%m-%d"  # 날짜 형식을 지정합니다. 여기서는 "년-월-일" 형식입니다.
        one_day_data["timestamp"] = ( datetime.datetime.strptime(date_string, date_format) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        one_day_data["predicted_price"] = result + 0.0
        #print(one_day_data)
        mySqlHandler.insert_item_to_predicted_data(data=one_day_data)
        #mongodbMachine.insert_item(data=one_day_data, db_name="AI", collection_name="predicted_data")

    chart_machine = ChartMachine()
    chat_machine = ChatMachine()

    actual_data_str, predicted_data_str = chart_machine.get_analysis_chart()
    #print(actual_data_str)
    #print()
    #print(predicted_data_str)
    res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)

    analysis_data = {"gpt_response":res, "timestamp":datetime.date.today().strftime("%Y-%m-%d")}
    #print(analysis_data)

    mySqlHandler.insert_item_to_analysis_data(data=analysis_data)