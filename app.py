from flask import Flask, request, render_template
from machine.chart_machine import ChartMachine
import py_eureka_client.eureka_client as eureka_client
from db.mysql.mysql_handler import MySqlHandler
import socket
import AI.base_lstm as init
import data.save_one_day_ai as save_one_day_ai
from apscheduler.schedulers.background import BackgroundScheduler
import os
import requests
import json


# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind(('localhost', 0))
# port = sock.getsockname()[1]
# sock.close()
# rest_port = int(os.environ.get('PORT', 5000))

rest_port=port = int(os.getenv("PORT", 8080))
print(rest_port)
print(type(rest_port))
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

# @app.route("/get_predict_value")
# def get_predict_value():
#     mySqlHandler = MySqlHandler(mode="remote", db_name="cdb_dbname")
#     data = mySqlHandler.find_all_items_from_predicted_data(limit=1)[0]

#     #data = db.find_last_item(db_name="AI", collection_name="predicted_data")
#     #data['_id'] = str(data['_id'])

#     return data

@app.route("/get_predict_value")
def get_predict_value():

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    ret = {}
    url = 'https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD'
    exchange_rate =requests.get(url, headers=headers).json()[0]['basePrice']
    mySqlHandler = MySqlHandler(mode="remote", db_name="cdb_dbname")
    data = mySqlHandler.find_all_items_from_predicted_data(limit=1)[0]
    data["predicted_usd"] = data.get("predicted_price") / exchange_rate
    data["predicted_krw"] = data["predicted_price"]
    del data["predicted_price"]
    #data["usd"] = exchange[0]['basePrice']
    ret["predicted_data"] = data
    data = mySqlHandler.find_all_items_from_actual_data(limit=1)[0]
    ret["actual_data"] = data

    return ret

@app.route("/get_basic_chart")
def get_basic_chart():
    chart_machine = ChartMachine()

    return chart_machine.get_basic_chart()

@app.route("/get_all_chart")
def get_all_chart():
    chart_machine = ChartMachine()

    return chart_machine.get_all_chart()

@app.route("/get_chart_analysis")
def get_chart_analysis():
    mySqlHandler = MySqlHandler(mode="remote", db_name="cdb_dbname")
    #db = MongoDBHandler(db_name="AI", collection_name="analysis_data")
    data = mySqlHandler.find_all_items_from_analysis_data(limit=1)[0]
    #data = db.find_last_item(db_name="AI", collection_name="analysis_data")
    #data['_id'] = str(data['_id'])

    return data

sched = BackgroundScheduler(daemon=True)
sched.add_job(save_one_day_ai.save_one_day_data, 'cron', hour=0, minute=1)
sched.start()

if __name__ == "__main__":
    init.init_code()
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)