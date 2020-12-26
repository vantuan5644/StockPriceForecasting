import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

class lstm():
    """A class for an building and inferencing an lstm model"""
    
    def __init__(self, input_shape, output_shape, optimizer='adam', loss = 'mean_squared_error'):
        self.model = Sequential()
        self.model.add(LSTM(n_neurons, batch_input_shape=(n_batch, input_shape.shape[1], input_shape.shape[2]), stateful=True))
        self.model.add(Dense(output_shape.shape[1]))
        self.model.compile(optimizer = optimizer, loss = loss)

    def load_model_weights(self, filepath):
        self.model.load_weights(filepath)
        print('[Model] Loaded model from file %s' % filepath)

    def forecast_lstm(X, n_batch):
        # reshape input pattern to [samples, timesteps, features]
        X = X.reshape(1, 1, len(X))
        # make forecast
        forecast = self.model.predict(X, batch_size=n_batch)
        # convert to array
        return [x for x in forecast[0, :]]

    def predict(self, n_batch, train, test, n_lag, n_seq):
        forecasts = list()
        for i in range(len(test)):
          X, y = test[i, 0:n_lag], test[i, n_lag:]
          # make forecast
          forecast = forecast_lstm(X, n_batch)
          # store the forecast
          forecasts.append(forecast)
        return forecasts

    def difference(dataset, interval=1):
        diff = list()
        for i in range(interval, len(dataset)):
          value = dataset[i] - dataset[i - interval]
          diff.append(value)
        return pd.Series(diff)

    def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
        n_vars = 1 if type(data) is list else data.shape[1]
        df = pd.DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
          cols.append(df.shift(i))
          names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
          cols.append(df.shift(-i))
          if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
          else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
        # put it all together
        agg = pd.concat(cols, axis=1)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
          agg.dropna(inplace=True)
        return agg
      
    def preprocess_data(self, series, n_test, n_lag, n_seq):
      '''
      n_test: so luong test
      n_lag: so luong ngay input
      n_seq: so luong ngay can predict
      '''
        raw_values = series.values
        # transform data to be stationary
        diff_series = difference(raw_values, 1)
        diff_values = diff_series.values
        diff_values = diff_values.reshape(len(diff_values), 1)
        # rescale values to -1, 1
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled_values = scaler.fit_transform(diff_values)
        scaled_values = scaled_values.reshape(len(scaled_values), 1)
        # transform into supervised learning problem X, y
        supervised = series_to_supervised(scaled_values, n_lag, n_seq)
        supervised_values = supervised.values
        # split into train and test sets
        train, test = supervised_values[0:-n_test], supervised_values[-n_test:]
        return scaler, train, test


    def inverse_difference(last_ob, forecast):
        # invert first forecast
        inverted = list()
        inverted.append(forecast[0] + last_ob)
        # propagate difference forecast using inverted first value
        for i in range(1, len(forecast)):
          inverted.append(forecast[i] + inverted[i-1])
        return inverted

    def inverse_transform(self,series, forecasts, scaler, n_test):
        inverted = list()
        for i in range(len(forecasts)):
          # create array from forecast
          forecast = np.array(forecasts[i])
          forecast = forecast.reshape(1, len(forecast))
          # invert scaling
          inv_scale = scaler.inverse_transform(forecast)
          inv_scale = inv_scale[0, :]
          # invert differencing
          index = len(series) - n_test + i - 1
          last_ob = series.values[index]
          inv_diff = inverse_difference(last_ob, inv_scale)
          # store
          inverted.append(inv_diff)
        return inverted

    def evaluate_forecasts(self,test, forecasts, n_lag, n_seq):
        total_error = []
        for i in range(n_seq):
          actual = np.asarray([row[i] for row in test])
          predicted = np.asarray([forecast[i] for forecast in forecasts])
      # 		print(actual[:30],predicted[:30])
          error = np.abs(actual - predicted)/actual
      # 		error.replace([np.inf, -np.inf], np.nan, inplace=True)
          error = error[~np.isnan(error)].mean()*100
          total_error.append(error)
          print('t+%d MAPE: %f' % ((i+1), error))
        print('Total:',np.array(total_error).mean())