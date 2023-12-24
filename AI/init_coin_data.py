import sys
import os
from machine.bithumb_machine import BithumbMachine
from AI.lstm_machine import LstmMachine
from db.mysql.mysql_handler import MySqlHandler
from machine.chatGPT_machine import ChatMachine
from machine.chart_machine import ChartMachine
from AI.flowbit_machine import FlowbitMachine
from db.mysql.mysql_handler import MySqlHandler
import datetime

def pre_data(data):
    result = []
    for entry in data:
        values = [entry[key] for key in entry.keys() if key != 'timestamp']
        result.append(values)

    return result

def init_code():
    bithumbMachine = BithumbMachine()
    lstmMachine = LstmMachine()
    flowbitMachine = FlowbitMachine()
    mySqlHandler = MySqlHandler(mode="remote")
    mySqlHandler.set_table()

    datas = bithumbMachine.get_all_data()[-50:]
    mySqlHandler.insert_items_to_actual_data(datas)

    result = []
    for i in range(0, len(datas) - 14):
        chunk = datas[i:i+15]
        #print(chunk)
        result.insert(0, chunk)
    result.reverse()


    #가격 예측 후 순서대로 저장
    for i in result:
        data = pre_data(i)
        data = flowbitMachine.data_processing(data)
        result = flowbitMachine.get_predict_value(data)
        one_day_data = {}
        date_string = i[-1]["timestamp"]  # 예시로 사용할 날짜 문자열
        date_format = "%Y-%m-%d"  # 날짜 형식을 지정합니다. 여기서는 "년-월-일" 형식입니다.
        one_day_data["timestamp"] = ( datetime.datetime.strptime(date_string, date_format) + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        one_day_data["predicted_price"] = result + 0.0
        print(one_day_data)
        mySqlHandler.insert_item_to_predicted_data(data=one_day_data)

    chart_machine = ChartMachine()
    chat_machine = ChatMachine()

    actual_data_str, predicted_data_str = chart_machine.get_analysis_chart()
    res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)
    analysis_data = {"gpt_response":res, "timestamp":datetime.date.today().strftime("%Y-%m-%d")}


    mySqlHandler.insert_item_to_analysis_data(data=analysis_data)