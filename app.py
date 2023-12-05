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
eureka_client.init(eureka_server="https://minwoomaven.apps.sys.paas-ta-dev10.kr/eureka",
                   app_name="bitcoin-service",
                   instance_port=rest_port)

app = Flask(__name__)

@app.route("/")
def home():
    html = """
    <html>
        <head><meta charset="utf-8"></head>
        <body>
            <h1>MAIN PAGE</h1>
        </body>
    </html>
    """
    return html

@app.route("/get_predict_value")
def get_predict_value():
    db = MongoDBHandler(db_name="AI", collection_name="predicted_data")

    data = db.find_last_item(db_name="AI", collection_name="predicted_data")
    data['_id'] = str(data['_id'])

    return data

@app.route("/get_basic_chart")
def get_basic_chart():
    chart_machine = ChartMachine()

    return chart_machine.get_basic_chart()

@app.route("/get_chart_analysis")
def get_chart_analysis():
    # chart_machine = ChartMachine()
    # chat_machine = ChatMachine()

    # actual_data_str, predicted_data_str = chart_machine.get_analysis_chart()
    # res = chat_machine.get_analysis_result(actual_data_str, predicted_data_str)

    db = MongoDBHandler(db_name="AI", collection_name="analysis_data")
    data = db.find_last_item(db_name="AI", collection_name="analysis_data")
    data['_id'] = str(data['_id'])
    
    return data

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=rest_port, use_reloader=False)