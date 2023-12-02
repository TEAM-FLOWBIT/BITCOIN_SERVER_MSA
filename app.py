from flask import Flask, request, render_template
from bs4 import BeautifulSoup
import urllib
import urllib.request
from tensorflow.keras.models import load_model
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from system.AI.lstm_machine import LstmMachine
from db.mongodb.mongodb_handler import MongoDBHandler
from machine.bithumb_machine import BithumbMachine
from bson import json_util
from machine.chart_machine import ChartMachine
from machine.chatGPT_machine import ChatMachine
import py_eureka_client.eureka_client as eureka_client
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 0))
port = sock.getsockname()[1]
sock.close()

rest_port = port
#rest_port = 5000
eureka_client.init(eureka_server="http://localhost:8761/eureka",
                   app_name="bitcoin-service",
                   instance_port=rest_port)

app = Flask(__name__)

@app.route("/test_model")
def model():

    aiMachine = LstmMachine()
    machine = BithumbMachine()
    data = machine.get_local_data()

    data = aiMachine.data_processing(data)
    predicted_data = aiMachine.get_predict_value(data)
    print(predicted_data)
    return "예측값: " + str(predicted_data)
    #return "예측값: " + str(data["price"])  

@app.route("/test_bithumb")
def bithumb():
    machine = BithumbMachine()
    data = machine.get_local_data()

    return data


@app.route("/")
def home():
    html = """
    <html><head><meta charset="utf-8"></head>
  <body>
     날씨정보<br/>
    <form action = "/weather">
      <input type = "text" name = "city" />
      <input type = "submit"/>
    </form>
  </body>
</html>
"""
    return html


@app.route('/weather')
def weather():
    city = request.args.get("city", "")
    url = "https://search.naver.com/search.naver?&query="
    url = url + urllib.parse.quote_plus(city + "날씨")

    soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    temp = soup.select("div.weather_graphic > div.temperature_text > strong")
    desc = soup.select("div._today > div.temperature_info > p")
    summary = soup.select("div._today > div.temperature_info > dl")

    return render_template("weather.html", weather={"city": city, "temp": temp[0].text, "desc": desc[0].text, "summary": summary[0].text})

@app.route("/get_predict_value")
def get_predict_value():
    db = MongoDBHandler(db_name="AI", collection_name="predicted_data")

    data = db.find_last_item(db_name="AI", collection_name="predicted_data")
    data['_id'] = str(data['_id'])
    #print(data)

    return data

@app.route("/get_basic_chart")
def get_basic_chart():
    chart_machine = ChartMachine()
    return chart_machine.get_basic_chart()
    # db = MongoDBHandler(db_name="AI", collection_name="actual_data")
    # actual_data = db.find_items_for_chart( db_name="AI", collection_name="actual_data", limit=14)
    # predicted_data = db.find_items_for_chart(db_name="AI", collection_name="predicted_data", limit=15)

    # actual_data_list = []
    # predicted_data_list = []
    # lables = []

    # for i in actual_data:
    #     print(i)
    #     #i["_id"] = str(i["_id"])
    #     #del i["_id"]
    #     actual_data_list.append(i["close_price"])

    # for i in predicted_data:
    #     print(i)
    #     #i["_id"] = str(i["_id"])
    #     #del i["_id"]
    #     lables.append(i["timestamp"])
    #     predicted_data_list.append(i["predicted_price"])

    # chart_data = {}
    # actual_data_list.reverse()
    # predicted_data_list.reverse()
    # lables.reverse()

    # max_value = max(actual_data_list + predicted_data_list)
    # min_value = min(actual_data_list + predicted_data_list)

    # blank = (min_value + max_value) / 10
    # chart_data["max"] = max_value + blank
    # chart_data["min"] = min_value + blank
    # chart_data["label"] = lables
    # chart_data["datas"] = [
    #     {"label" : "actual_data", "datas" : actual_data_list}, 
    #     {"label" : "predicted_data", "datas" : predicted_data_list}]

    # return chart_data

@app.route("/get_chart_analysis")
def get_chart_analysis():
    chart_machine = ChartMachine()
    chat_machine = ChatMachine()
    actual_data_str, predicted_data_str = chart_machine.get_analysis_chart()
    res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)
    #print(res)
    #chart_data = chart_machine.get_analysis_chart()

    #print(chart_data.get("datas"))
    return res

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=rest_port, use_reloader=False)