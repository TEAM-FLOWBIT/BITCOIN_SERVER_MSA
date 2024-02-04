import sys
import os
sys.path.append(os.path.realpath(__file__)[0:-18]+"..")
from machine.bithumb_machine import BithumbMachine
from machine.chart_machine import ChartMachine
from db.mongodb.mongodb_handler import MongoDBHandler
import datetime
from AI.machine.flowbit_machine import FlowbitMachine
from machine.chatGPT_machine import ChatMachine
import datetime

def data_processing(data):
    ret = []
    for i in data:
        ret.append(list(i.values())[2:])
    return ret

def save_one_day_data():
    print("start cron method")
    bithumbMachine = BithumbMachine()
    flowbitMachine = FlowbitMachine()
    mongodbMachine = MongoDBHandler(db_name="AI", collection_name="actual_data")

    print("insert last actual data to database")
    data = bithumbMachine.get_last_data()
    mongodbMachine.insert_item(data=data, db_name="AI", collection_name="actual_data")
    
    print("start price prediction")
    past_data = mongodbMachine.find_items_for_db(db_name="AI", collection_name="actual_data")
    data = data_processing(past_data)
    data.reverse()

    data = flowbitMachine.data_processing(data)
    result = flowbitMachine.get_predict_value(data)

    one_day_data = {}
    one_day_data["timestamp"] = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    one_day_data["predicted_price"] = result + 0.0
    print("end price prediction")

    print("insert predicted data to database")
    mongodbMachine.insert_item(data=one_day_data, db_name="AI", collection_name="predicted_data")

    print("start price analysis")
    chart_machine = ChartMachine()
    chat_machine = ChatMachine()

    actual_data_str, predicted_data_str = chart_machine.get_analysis_chart()
    res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)
    print("end price analysis")

    analysis_data = {"gpt_response":res, "timestamp":datetime.date.today().strftime("%Y-%m-%d")}

    print("insert analysis data to database")
    mongodbMachine.insert_item(data = analysis_data, db_name="AI", collection_name="analysis_data")