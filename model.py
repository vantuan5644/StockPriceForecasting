import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

class LSTM():
    """A class for an building and inferencing an lstm model"""
    
    def __init__(self, input_shape, loss='mean_squared_error', optimizer='adam'):
        self.model = Sequential()
        
        self.model.add(LSTM(units = 50, return_sequences = True, input_shape = input_shape))
        self.model.add(Dropout(0.2))

        self.model.add(LSTM(units = 50, return_sequences = True))
        self.model.add(Dropout(0.2))

        self.model.add(LSTM(units = 50, return_sequences = True))
        self.model.add(Dropout(0.2))

        self.model.add(LSTM(units = 50))
        self.model.add(Dropout(0.2))

        self.model.add(Dense(units = 1))

        self.model.compile(optimizer = optimizer, loss = loss)

    def load_model_weights(self, filepath):
        print('[Model] Loading model from file %s' % filepath)
        self.model.load_weights(filepath)
    
    def predict(self,data):
        #Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
        print('[Model] Predicting...')
        predicted = self.model.predict(data)
        predicted = np.reshape(predicted, (predicted.size,))
        return predicted

