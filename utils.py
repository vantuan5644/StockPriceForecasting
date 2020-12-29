from typing import List, Union

import numpy as np
import pandas as pd
import vnquant.DataLoader as web


def MAPE(y_true, y_pred):
    error = np.abs(y_true - y_pred) / y_true
    error.replace([np.inf, -np.inf], np.nan, inplace=True)
    error = error[~np.isnan(error)]

    return np.mean(error) * 100


def get_data_splits(df, train_size, test_size, validation_size=0):
    train_len = 0
    if isinstance(train_size, float) and train_size < 1:
        train_len = int(df.shape[0] * train_size)
    if isinstance(train_size, int) and train_size >= 1:
        train_len = train_size

    train_data = df.iloc[: train_len]

    test_len = 0
    if isinstance(test_size, float) and test_size < 1:
        test_len = int(df.shape[0] * test_size)
    if isinstance(test_size, int) and test_size >= 1:
        test_len = test_size
    test_data = df.iloc[-test_len:]

    if validation_size != 0:
        val_data = df.iloc[train_len:-test_len]
        return train_data, val_data, test_data
    else:
        return train_data, test_data


def get_stock_price_history(name: Union[str, List[str]], start_date: str, end_date: str):
    loader = web.DataLoader(name, start=start_date, end=end_date)
    data = loader.download()
    return data
