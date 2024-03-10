from machine.bithumb_machine import BithumbMachine
from machine.chatGPT_machine import ChatMachine
from machine.chart_machine import ChartMachine
from AI.machine.flowbit_machine import FlowbitMachine
from db.mongodb.mongodb_handler import MongoDBHandler
from AI.machine.model_controller import ModelController
import datetime
from pytz import timezone

server_timezone = timezone('Asia/Seoul')

def pre_data(data):
    result = []
    for entry in data:
        values = [entry[key] for key in entry.keys() if key != 'timestamp' and key != "_id"]
        result.append(values)
    return result

def init_code():
    print("start initializing")
    print("start prev data")
    chart_machine = ChartMachine()
    chat_machine = ChatMachine()
    bithumbMachine = BithumbMachine()
    modelController = ModelController()
    for model_data in modelController.get_model_list():

        #flowbitMachine = FlowbitMachine()
        if model_data.get("model_type") != "prev":
            continue

        print(model_data.get("model_type"))
        print(model_data.get("coin_currency"))

        continue

        flowbitMachine = model_data.get("model_class")
        database_name = model_data.get("coin_currency")
        mongodbMachine = MongoDBHandler(mode="local", db_name=database_name, collection_name="actual_data")

        print("start reset database")
        mongodbMachine.delete_items(condition="ALL", db=database_name, collection="actual_data")
        mongodbMachine.delete_items(condition="ALL", db=database_name, collection="predicted_data")
        mongodbMachine.delete_items(condition="ALL", db=database_name, collection="analysis_data")
        print("end reset database")

        print("insert all actual data to database")
        datas = bithumbMachine.get_all_data(coin_currency=database_name)[:-1]
        mongodbMachine.insert_items(datas=datas, database_name=database_name, collection_name="actual_data")
    
        print("start price prediction")
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
            mongodbMachine.insert_item(data=one_day_data, database_name=database_name, collection_name="predicted_data")
        
        print("end price prediction")

        print("start price analysis")
        actual_data_str, predicted_data_str = chart_machine.get_analysis_chart(database_name=database_name)
        res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)
        analysis_data = {"gpt_response":res, "timestamp":datetime.date.today().strftime("%Y-%m-%d")}
        print("end price analysis")
    
        print("insert analysis data to database")
        mongodbMachine.insert_item(data = analysis_data, database_name=database_name, collection_name="analysis_data")
    
    for model_data in modelController.get_model_list():

        #flowbitMachine = FlowbitMachine()
        if model_data.get("model_type") != "pridict":
            continue

        print(model_data.get("model_type"))
        print(model_data.get("coin_currency"))

        flowbitMachine = model_data.get("model_class")
        database_name = model_data.get("coin_currency")
        mongodbMachine = MongoDBHandler(mode="local", db_name=database_name, collection_name="actual_data")

        #print("start reset database")
        #mongodbMachine.delete_items(condition="ALL", db=database_name, collection="actual_data")
        #mongodbMachine.delete_items(condition="ALL", db=database_name, collection="predicted_data")
        #mongodbMachine.delete_items(condition="ALL", db=database_name, collection="analysis_data")
        #print("end reset database")

        #print("insert all actual data to database")
        #datas = bithumbMachine.get_all_data(coin_currency=database_name)[:-1]
        #mongodbMachine.insert_items(datas=datas, database_name=database_name, collection_name="actual_data")

        datas = bithumbMachine.get_all_data(coin_currency=database_name)[:-1]
        time_step = 60

        data = datas[-time_step:]
        
        print("start price prediction")

        
        date_string = data[-1]["timestamp"]
        data = pre_data(data)
        data = flowbitMachine.data_processing(data)
        result = flowbitMachine.get_predict_value_for_list(data)
        result_data_size = len(result)

        one_day_data = {}
        
        date_format = "%Y-%m-%d"

        server_date = server_timezone.localize(datetime.datetime.strptime(date_string, date_format))
        one_day_later = (server_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        result = result.tolist()
        result.append(123455)
        print(result)
        one_day_data["timestamp"] = one_day_later
        one_day_data["predicted_price"] = result
        mongodbMachine.insert_item(data=one_day_data, database_name=database_name, collection_name="multiple_predicted_data")
            
        
        print("end price prediction")

        print("start price analysis")
        actual_data_str, predicted_data_str = chart_machine.get_analysis_chart(database_name=database_name)
        res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)
        analysis_data = {"gpt_response":res, "timestamp":datetime.date.today().strftime("%Y-%m-%d")}
        print("end price analysis")
    
        print("insert analysis data to database")
        mongodbMachine.insert_item(data = analysis_data, database_name=database_name, collection_name="analysis_data")

    