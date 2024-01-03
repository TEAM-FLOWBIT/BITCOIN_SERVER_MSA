from machine.bithumb_machine import BithumbMachine
from AI.lstm_machine import LstmMachine
from db.mysql.mysql_handler import MySqlHandler
from machine.chatGPT_machine import ChatMachine
from machine.chart_machine import ChartMachine
from AI.flowbit_machine import FlowbitMachine
from db.mysql.mysql_handler import MySqlHandler
import datetime
from pytz import timezone

server_timezone = timezone('Asia/Seoul')

def pre_data(data):
    result = []
    for entry in data:
        values = [entry[key] for key in entry.keys() if key != 'timestamp']
        result.append(values)

    return result

def init_code():
    bithumbMachine = BithumbMachine()
    flowbitMachine = FlowbitMachine()
    mySqlHandler = MySqlHandler(mode="remote")
    mySqlHandler.set_table()

    datas = bithumbMachine.get_all_data()[:-1]
    mySqlHandler.insert_items_to_actual_data(datas)
    
    results = []
    for i in range(0, len(datas) - 14):
        chunk = datas[i:i+15]
        results.insert(0, chunk)
    results.reverse()
    
    for i in results:
        data = pre_data(i)
        data = flowbitMachine.data_processing(data)
        result = flowbitMachine.get_predict_value(data)
        one_day_data = {}
        date_string = i[-1]["timestamp"]
        date_format = "%Y-%m-%d"

        server_date = server_timezone.localize(datetime.datetime.strptime(date_string, date_format))
        one_day_later = (server_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        one_day_data["timestamp"] = one_day_later
        one_day_data["predicted_price"] = result + 0.0
        print(one_day_data)
        mySqlHandler.insert_item_to_predicted_data(data=one_day_data)

    print(datas[-1])
    print(results[-1])


    chart_machine = ChartMachine()
    chat_machine = ChatMachine()

    actual_data_str, predicted_data_str = chart_machine.get_analysis_chart()
    res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)
    analysis_data = {"gpt_response":res, "timestamp":datetime.date.today().strftime("%Y-%m-%d")}

    mySqlHandler.insert_item_to_analysis_data(data=analysis_data)