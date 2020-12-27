from flask import Flask
import pandas as pd 
import numpy as np
from flask import render_template
from controller.dashboard import dashboard, predict_stock_price, get_price_to_today
from aicore.Prophet.Prophet import Prophet
from util.setup import APP_NAME, ARIMA, PROPHET, LSTM, ENSEMBLE_LEARNING, STOCK_CODES
import datetime

app = Flask(APP_NAME, template_folder="templates", static_folder="static", static_url_path="/static")

@app.route("/", methods=["GET"])
@app.route("/dashboard", methods=["GET"])
def home():
     return dashboard()



@app.route("/getPredict/<stockCode>/<method>", methods=["GET"])
def predict(stockCode, method):
    return predict_stock_price(stockCode, method)


@app.route("/getOldPrices/<stockCode>", methods=["GET"])
def get_old_price(stockCode):
        query = get_price_to_today(stockCode)
        return query

if __name__ == "__main__":
    app.run(debug=True, port=3000)