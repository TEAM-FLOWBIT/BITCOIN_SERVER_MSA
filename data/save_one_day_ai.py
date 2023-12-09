import sys
import os

sys.path.append(os.path.realpath(__file__)[0:-18]+"..")
#print(os.path.realpath(__file__)[0:-18]+"..")
from machine.bithumb_machine import BithumbMachine
from db.mongodb.mongodb_handler import MongoDBHandler
from AI.lstm_machine import LstmMachine
from machine.chart_machine import ChartMachine
from db.mysql.mysql_handler import MySqlHandler
import ast
import datetime
from machine.chatGPT_machine import ChatMachine

import datetime

def extract_close_prices(data):
    #print(str(data))
    #close_prices = [float(entry['close_price']) for entry in data]
    return close_prices

def get_last_price_mysql(data):
    data = ast.literal_eval(str(data))
    list_data = [int(item[0]) for item in data]
    return list_data

def save_one_day_data():
    bithumbMachine = BithumbMachine()
    lstmMachine = LstmMachine()
    mongodbMachine = MongoDBHandler(mode="local", db_name="AI", collection_name="actual_data")
    mySqlHandler = MySqlHandler(mode="local", db_name="flowbit")

    #하루치 데이터 저장
    data = bithumbMachine.get_last_data()
    mySqlHandler.insert_item_to_actual_data(data=data)
    #recv = mongodbMachine.insert_item(data=data, db_name="AI", collection_name="actual_data")

    #model 예측 과정

    past_data = mySqlHandler.find_close_price_from_actual_data(limit=15)
    #print(past_data)
    data = get_last_price_mysql(past_data)
    #past_data = mongodbMachine.find_items_for_db(db_name="AI", collection_name="actual_data")
    #print(past_data)
    #data = extract_close_prices(past_data)
    data.reverse()
    #print(data)
    data = lstmMachine.data_processing(data)
    result = lstmMachine.get_predict_value(data)

    #예측된 값 저장
    one_day_data = {}
    one_day_data["timestamp"] = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    one_day_data["predicted_price"] = result + 0.0
    #mongodbMachine.insert_item(data=one_day_data, db_name="AI", collection_name="predicted_data")
    mySqlHandler.insert_item_to_predicted_data(data=one_day_data)

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
    #print(analysis_data)

    #mongodbMachine.insert_item(data = analysis_data, db_name="AI", collection_name="analysis_data")