from flask import Flask, request, render_template
from machine.chart_machine import ChartMachine
import py_eureka_client.eureka_client as eureka_client
from db.mysql.mysql_handler import MySqlHandler
import AI.init_coin_data as init
import data.cron_ai as soda
from apscheduler.schedulers.background import BackgroundScheduler
import os

rest_port=port = int(os.getenv("PORT", 8080))
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
    ret = {}
    mySqlHandler = MySqlHandler(mode="remote", db_name="cdb_dbname")
    data = mySqlHandler.find_all_items_from_predicted_data(limit=1)[0]
    data["predicted_krw"] = data["predicted_price"]
    del data["predicted_price"]
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
    data = mySqlHandler.find_all_items_from_analysis_data(limit=1)[0]

    return data

if __name__ == "__main__":
    init.init_code()
    port = int(os.getenv("PORT", 8080))
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(soda.save_one_day_data, 'cron', hour=0, minute=1)
    sched. remove_all_jobs()
    sched.start()
    app.run(host='0.0.0.0', port=port, debug=True)