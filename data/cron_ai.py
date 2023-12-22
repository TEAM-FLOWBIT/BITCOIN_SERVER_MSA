import sys
import os

sys.path.append(os.path.realpath(__file__)[0:-18]+"..")
#print(os.path.realpath(__file__)[0:-18]+"..")
from machine.bithumb_machine import BithumbMachine
from AI.lstm_machine import LstmMachine
from machine.chart_machine import ChartMachine
from db.mysql.mysql_handler import MySqlHandler
import ast
import datetime
from AI.flowbit_machine import FlowbitMachine
from machine.chatGPT_machine import ChatMachine

import datetime

def pre_data(data):
    result = []
    for entry in data:
        values = [entry[key] for key in entry.keys() if key != 'timestamp']
        result.append(values)
    return result

def save_one_day_data():
    bithumbMachine = BithumbMachine()
    flowbitMachine = FlowbitMachine()
    mySqlHandler = MySqlHandler(mode="remote", db_name="cdb_dbname")

    data = bithumbMachine.get_last_data()
    mySqlHandler.insert_item_to_actual_data(data=data)

    past_data = mySqlHandler.find_close_price_from_actual_data(limit=15)
    #print(past_data)
    data = data.tolist()
    #data = pre_data(past_data)
    print(data)
    data.reverse()

    data = flowbitMachine.data_processing(data)
    result = flowbitMachine.get_predict_value(data)

    one_day_data = {}
    one_day_data["timestamp"] = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    one_day_data["predicted_price"] = result + 0.0
    mySqlHandler.insert_item_to_perdicted_data(data=one_day_data)

    chart_machine = ChartMachine()
    chat_machine = ChatMachine()

    actual_data_str, predicted_data_str = chart_machine.get_analysis_chart()
    res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)

    analysis_data = {"gpt_response":res, "timestamp":datetime.date.today().strftime("%Y-%m-%d")}

    mySqlHandler.insert_item_to_analysis_data(data=analysis_data)