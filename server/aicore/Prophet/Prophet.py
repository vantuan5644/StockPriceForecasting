import json
import os
import pickle


class Prophet:
    def __init__(self):  # thêm mã chứng khoán
        # load model from pickel file
        with open(os.getcwd() + r"\aicore\Prophet\ProphetModel.txt", "rb") as f:
            self.prophet_model = pickle.load(f)

    def predict(self, periods=30):  # thêm mã chứng khoán
        future_need_predict = self.prophet_model.make_future_dataframe(periods=periods, include_history=False)
        df_predict = self.prophet_model.predict(future_need_predict)
        predict_dict = []
        for i in range(len(df_predict)):
            predict_dict.append(
                {"price": df_predict.loc[i, "yhat"], "time": df_predict.loc[i, "ds"].strftime("%d/%m/%Y %H:%M:%S")})
        return json.dumps(predict_dict)

    @staticmethod
    def re_train_model():
        # code re-train here
        return
