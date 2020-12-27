import pickle
import os
import json
import pandas as pd 
import numpy as np
from datetime import datetime
from fbprophet import Prophet
from util.setup import STOCK_CODES

class ProphetModel:
    def __init__(self, stock_code): # thêm mã chứng khoán
        stock_code_ = stock_code
        filepath_model = None

        if (stock_code not in STOCK_CODES): 
            stock_code_ = "FPT"
        # load model from pickel file
        filename_models = os.listdir(os.getcwd() + "\\aicore\Prophet\model\\")
        for filename in filename_models:
            if (stock_code_ in filename):
                filename_model = filename
                break

        with open(os.getcwd() + r"\aicore\Prophet\model\\" + filename_model, "rb") as f:
            self.prophet_model = pickle.load(f)

    def predict(self, periods=30): # thêm mã chứng khoán
        future = self.prophet_model.make_future_dataframe(periods=periods, include_history=False)
        future_need_predict = pd.DataFrame({"ds": []})
        for i in range(len(future)):
            res = len(pd.bdate_range(future.loc[i,"ds"], future.loc[i,"ds"]))
            if res > 0:
                if len(future_need_predict) > 0:
                    future_need_predict = future_need_predict.append(pd.DataFrame({"ds": [future.loc[i,"ds"]]}), ignore_index=True, )
                else:
                    future_need_predict = pd.DataFrame({"ds": [future.loc[i,"ds"]]})

        print(future_need_predict)
        df_predict = self.prophet_model.predict(future_need_predict)
        predict_dict = []
        for i in range(len(df_predict)):
            predict_dict.append({"price": df_predict.loc[i, "yhat"], "time": df_predict.loc[i, "ds"].strftime("%d/%m/%Y %H:%M:%S")})
        return json.dumps(predict_dict)

    @staticmethod
    def re_train_model():
        # code re-train here
        stock_list = os.listdir(os.getcwd() + r"\dataset")
        for stock_file in stock_list:
            filepath = os.getcwd() + f"\dataset\\{stock_file}"
            stock_code = stock_file.replace(".csv","")
            df = pd.read_csv(filepath)
            df = df[["date", "close"]]
            df["date"] = pd.to_datetime(df["date"], format="%Y%m%d", errors="coerce")
            df.rename(columns={"date":"ds","close":"y"}, inplace=True)
            print(df)
            # divide data to train, validation and test set
            x_train = df.copy()
            # grid Search to turn hyperparameters
            # code only for demo
            best_params = {
                'changepoint_range': 0.99, 
                'changepoint_prior_scale': 0.19999999999999998, 
                'seasonality_prior_scale': 10.0
                }
            model = Prophet(**best_params).fit(x_train) 
           
            filepath_model =  os.getcwd() + r"\aicore\Prophet\model\\" + stock_code + datetime.now().strftime("-%dm%mm%Y-%Hm%Mm%S") + ".csv"
            with open(filepath_model, "wb") as f:
                filename_models = os.listdir(os.getcwd() + "\\aicore\Prophet\model\\")
                for filename in filename_models:
                    if (stock_code in filename and filename != (filepath_model.split(r"\\"))[1]):
                        os.remove(os.getcwd() + r"\\aicore\Prophet\model\\" + filename)
                pickle.dump(model, f)
        
        return True


        
