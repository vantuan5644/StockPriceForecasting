from flask import render_template
import pandas as pd 
import numpy as np
import os
import json
from aicore.Prophet.Prophet import ProphetModel
from util.setup import APP_NAME, ARIMA, PROPHET, LSTM, ENSEMBLE_LEARNING, STOCK_CODES, COMPANY_NAME
from util.datetimeUtil import get_datetime_value_from_df, get_timestamp_from_filename_model

def dashboard():
    indexes = np.arange(1,len(STOCK_CODES)+1)
    lasttime_turned_model = []
    for code in STOCK_CODES:
        filename_models = os.listdir(os.getcwd() + "\\aicore\Prophet\model\\")
        for filename in filename_models:
            if (code in filename):
                lasttime_turned_model.append(get_timestamp_from_filename_model(filename))

    return render_template("dashboard.html", companies=zip(indexes,STOCK_CODES,COMPANY_NAME, lasttime_turned_model))

def predict_stock_price(stockCode, method):
    results = None
    if (method == ARIMA):
        pass
    elif (method == LSTM):
        pass
    elif (method == ENSEMBLE_LEARNING):
        pass
    else:
        model = ProphetModel(stockCode)
        results = model.predict(365)
    
    return results

def get_price_to_today(stockCode):
    path = os.getcwd() + r"\dataset\\" + stockCode + ".csv"
    if (os.path.isfile(path)):
        df = pd.read_csv(path)
        time_prices = get_datetime_value_from_df(df)
        return json.dumps(time_prices)
    else:
        return "Fail to query old data!"

    
